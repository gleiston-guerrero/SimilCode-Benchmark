#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calidad_justificaciones.py — M4: calidad de la retroalimentacion (ciega)
=======================================================================

Problema que resuelve: comparar la calidad de las justificaciones que produce
cada modelo sin que el evaluador sepa que modelo las escribio, y sin que el
orden de presentacion introduzca sesgo.

Diseno:
  * Muestreo ESTRATIFICADO por categoria y lenguaje, para que ningun modelo
    resulte favorecido por el reparto de casos.
  * Cada caso muestreado aporta las justificaciones de LOS CUATRO modelos, de
    modo que la comparacion es INTRASUJETO (mismo par de codigo) y admite
    pruebas pareadas.
  * Los items se barajan con semilla fija y se identifican por un codigo opaco.
    La clave modelo <-> item se guarda en un archivo APARTE que el evaluador
    no debe abrir hasta terminar.
  * Escala continua 0-100 en cuatro criterios, evitando el efecto techo que
    produjo la escala Likert 1-5 del instrumento de validacion.

Subcomandos:
  hojas     Genera la hoja de calificacion ciega y la clave.
  analizar  ICC(2,1), alfa de Cronbach, descriptivos por modelo y prueba
            pareada de Friedman con post-hoc de Wilcoxon y Bonferroni.

Sin dependencias externas (solo biblioteca estandar).
"""

import argparse
import csv
import math
import os
import random
import sys
from collections import defaultdict

CATS = ["identico", "funcional", "estructural", "diferente"]

CRITERIOS = [
    ("correccion", "Correccion tecnica: lo que afirma sobre el codigo, "
                   "es verdadero? (0 = falso o inventado, 100 = todo verificable)"),
    ("especificidad", "Especificidad: se refiere a elementos concretos del codigo "
                      "o es generico? (0 = valdria para cualquier par, 100 = "
                      "solo vale para este par)"),
    ("explicacion", "Poder explicativo: explica POR QUE, o solo describe QUE? "
                    "(0 = puro enunciado, 100 = razonamiento trazable)"),
    ("utilidad", "Utilidad docente: le serviria a un estudiante para entender "
                 "el veredicto? (0 = inutil, 100 = suficiente por si sola)"),
]


# ------------------------------------------------------------------ utilidades
def leer(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def validas(filas):
    return [x for x in filas
            if not str(x.get("error", "")).strip()
            and str(x.get("justification_global", "")).strip()]


# ---------------------------------------------------------------------- hojas
def _rutas_codigo(path_meta):
    """case_id -> (ruta_a, ruta_b) desde metadata.csv. El evaluador necesita
    leer los dos archivos para juzgar la correccion tecnica; sin esto el primer
    criterio no se puede aplicar."""
    if not path_meta or not os.path.exists(path_meta):
        return {}
    out = {}
    for r in leer(path_meta):
        k = {c.lower(): c for c in r}
        cid = next((r[k[c]] for c in ("case_id", "id", "caso") if c in k), None)
        a = next((r[k[c]] for c in ("code_a_path", "code_a", "archivo_a", "a")
                  if c in k), "")
        b = next((r[k[c]] for c in ("code_b_path", "code_b", "archivo_b", "b")
                  if c in k), "")
        if cid:
            out[str(cid).strip()] = (a, b)
    return out


def cmd_hojas(args):
    filas = validas(leer(args.resultados))
    if not filas:
        sys.exit("No hay filas validas con justificacion en " + args.resultados)
    rutas = _rutas_codigo(args.metadata)
    if not rutas:
        print("AVISO: no se pudieron leer rutas de codigo desde %r.\n"
              "       Las columnas codigo_a/codigo_b quedaran vacias y el criterio\n"
              "       de CORRECCION TECNICA no sera aplicable. Pasa --metadata con\n"
              "       el metadata.csv del corpus." % args.metadata)

    # Una justificacion por (caso, proveedor): la de la replica indicada.
    elegido = {}
    for x in filas:
        k = (x["case_id"], x["provider"])
        if k not in elegido or int(x["replica"]) < int(elegido[k]["replica"]):
            elegido[k] = x

    proveedores = sorted({p for _, p in elegido})
    casos = defaultdict(dict)
    for (c, p), x in elegido.items():
        casos[c][p] = x

    # Solo casos con los CUATRO modelos: la comparacion debe ser intrasujeto.
    completos = {c: d for c, d in casos.items() if len(d) == len(proveedores)}
    descartados = len(casos) - len(completos)

    # Estratificacion por (lenguaje, categoria)
    celdas = defaultdict(list)
    for c, d in completos.items():
        m = next(iter(d.values()))
        celdas[(m["language"], m["category"])].append(c)

    rng = random.Random(args.semilla)
    muestra = []
    faltantes = []
    for celda in sorted(celdas):
        ids = sorted(celdas[celda])
        rng.shuffle(ids)
        if len(ids) < args.por_celda:
            faltantes.append((celda, len(ids)))
        muestra.extend(ids[:args.por_celda])

    items = []
    for c in muestra:
        for p in proveedores:
            items.append(casos[c][p])
    rng.shuffle(items)

    ancho = max(3, len(str(len(items))))
    cabecera = ["item_id", "lenguaje", "categoria", "justificacion",
                "codigo_a", "codigo_b"] + [k for k, _ in CRITERIOS] + ["comentario"]
    clave = [["item_id", "case_id", "provider", "model", "replica"]]

    with open(args.hoja, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cabecera)
        for i, x in enumerate(items, 1):
            iid = "J%0*d" % (ancho, i)
            ra, rb = rutas.get(x["case_id"], (x.get("code_a_path", ""),
                                              x.get("code_b_path", "")))
            w.writerow([iid, x.get("language", ""), x.get("category", ""),
                        " ".join(str(x["justification_global"]).split()),
                        ra, rb, "", "", "", "", ""])
            clave.append([iid, x["case_id"], x["provider"],
                          x.get("model", ""), x.get("replica", "")])

    with open(args.clave, "w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows(clave)

    with open(args.instrucciones, "w", encoding="utf-8") as fh:
        fh.write(INSTRUCCIONES.format(
            n=len(items), casos=len(muestra), modelos=len(proveedores),
            hoja=os.path.basename(args.hoja),
            criterios="\n".join("  * %s — %s" % (k.upper(), d) for k, d in CRITERIOS)))

    print("Casos completos (los %d modelos): %d" % (len(proveedores), len(completos)))
    if descartados:
        print("Casos descartados por faltar algun modelo: %d" % descartados)
    for celda, n in faltantes:
        print("  AVISO: la celda %s solo tiene %d casos (pediste %d)"
              % (celda, n, args.por_celda))
    print("Muestra: %d casos x %d modelos = %d items"
          % (len(muestra), len(proveedores), len(items)))
    print("\nEscrito:", args.hoja)
    print("Escrito:", args.clave, " <- NO abrir hasta terminar de calificar")
    print("Escrito:", args.instrucciones)
    print("\nEntrega a cada evaluador una COPIA de la hoja, renombrada con su "
          "identificador (p.ej. hoja_E1.csv, hoja_E2.csv).")


INSTRUCCIONES = """INSTRUCCIONES PARA EL EVALUADOR — calidad de la retroalimentacion
================================================================

Vas a calificar {n} justificaciones producidas por {modelos} sistemas distintos
sobre {casos} pares de codigo. No sabes que sistema escribio cada una, y ese
desconocimiento es parte del diseno: no intentes deducirlo.

COMO CALIFICAR

Abre {hoja} en una hoja de calculo. Cada fila es una justificacion. Las columnas
`codigo_a` y `codigo_b` indican los dos archivos comparados: abrelos y leelos
antes de puntuar, porque el primer criterio exige comprobar si lo que la
justificacion afirma sobre el codigo es cierto.

Puntua cada fila en CUATRO criterios, con un numero entero de 0 a 100:

{criterios}

Usa el rango completo. Si todo te parece un 80, la escala no esta midiendo nada.
Reserva los extremos: 0 y 100 existen y deben usarse cuando corresponda.

La columna `comentario` es opcional; usala cuando una puntuacion necesite
explicacion, sobre todo si detectas una afirmacion falsa sobre el codigo.

QUE NO HACER

No califiques si el veredicto de similitud te parece acertado: eso ya se mide
aparte. Aqui se juzga la ARGUMENTACION, no la conclusion. Una justificacion
puede razonar impecablemente hacia un veredicto equivocado, y debe puntuar alto
en `explicacion` aunque el veredicto falle.

No compares filas entre si buscando coherencia. Cada fila se puntua sola.

No consultes con el otro evaluador mientras calificas. La concordancia entre
ambos es un resultado del estudio; si os poneis de acuerdo antes, se destruye.

AL TERMINAR

Guarda el archivo con tu identificador (hoja_E1.csv o hoja_E2.csv) y entregalo
sin abrir el archivo de clave.
"""


# ------------------------------------------------------------------- analizar
def _media(v):
    return sum(v) / len(v)


def _var(v, ddof=1):
    if len(v) - ddof <= 0:
        return 0.0
    m = _media(v)
    return sum((x - m) ** 2 for x in v) / (len(v) - ddof)


def icc21(matriz):
    """ICC(2,1): acuerdo absoluto, modelo de dos vias con efectos aleatorios,
    medidas individuales. matriz = lista de filas (sujetos), cada una con una
    puntuacion por evaluador."""
    n = len(matriz)
    k = len(matriz[0])
    total = [x for fila in matriz for x in fila]
    gm = _media(total)
    ms_r = k * sum((_media(f) - gm) ** 2 for f in matriz) / (n - 1)
    cols = [[matriz[i][j] for i in range(n)] for j in range(k)]
    ms_c = n * sum((_media(c) - gm) ** 2 for c in cols) / (k - 1)
    ss_e = sum((matriz[i][j] - _media(matriz[i]) - _media(cols[j]) + gm) ** 2
               for i in range(n) for j in range(k))
    ms_e = ss_e / ((n - 1) * (k - 1))
    den = ms_r + (k - 1) * ms_e + k * (ms_c - ms_e) / n
    return (ms_r - ms_e) / den if den else float("nan")


def alfa_cronbach(matriz):
    k = len(matriz[0])
    if k < 2:
        return float("nan")
    items = [[f[j] for f in matriz] for j in range(k)]
    sv = sum(_var(c) for c in items)
    tv = _var([sum(f) for f in matriz])
    return (k / (k - 1)) * (1 - sv / tv) if tv else float("nan")


def _rango(v):
    orden = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(orden):
        j = i
        while j + 1 < len(orden) and v[orden[j + 1]] == v[orden[i]]:
            j += 1
        med = (i + j) / 2.0 + 1.0
        for t in range(i, j + 1):
            r[orden[t]] = med
        i = j + 1
    return r


def friedman(bloques):
    """bloques: lista de listas, cada una con k medidas pareadas."""
    n, k = len(bloques), len(bloques[0])
    suma = [0.0] * k
    for b in bloques:
        for j, x in enumerate(_rango(b)):
            suma[j] += x
    chi = (12.0 / (n * k * (k + 1))) * sum(s ** 2 for s in suma) - 3 * n * (k + 1)
    return chi, k - 1, [s / n for s in suma]


def _phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def wilcoxon(a, b):
    """Prueba de rangos con signo; aproximacion normal con correccion de empates."""
    d = [x - y for x, y in zip(a, b) if x != y]
    n = len(d)
    if n < 6:
        return float("nan"), float("nan")
    r = _rango([abs(x) for x in d])
    wp = sum(r[i] for i in range(n) if d[i] > 0)
    wn = sum(r[i] for i in range(n) if d[i] < 0)
    w = min(wp, wn)
    mu = n * (n + 1) / 4.0
    sd = math.sqrt(n * (n + 1) * (2 * n + 1) / 24.0)
    z = (w - mu + 0.5) / sd if sd else float("nan")
    return z, 2 * _phi(-abs(z))


def cmd_analizar(args):
    clave = {r["item_id"]: r for r in leer(args.clave)}
    hojas = {}
    for spec in args.hojas:
        if ":" in spec:
            etiqueta, ruta = spec.split(":", 1)
        else:
            etiqueta, ruta = os.path.splitext(os.path.basename(spec))[0], spec
        hojas[etiqueta] = {r["item_id"]: r for r in leer(ruta)}
        print("  %-6s %4d items leidos de %s" % (etiqueta, len(hojas[etiqueta]), ruta))

    etiquetas = sorted(hojas)
    campos = [k for k, _ in CRITERIOS]

    # global por item y evaluador = media de los cuatro criterios
    glob = defaultdict(dict)
    subes = defaultdict(lambda: defaultdict(dict))
    incompletos = 0
    for iid in clave:
        for e in etiquetas:
            r = hojas[e].get(iid)
            if not r:
                continue
            try:
                v = [float(str(r[c]).replace(",", ".")) for c in campos]
            except (ValueError, KeyError):
                incompletos += 1
                continue
            if any(x < 0 or x > 100 for x in v):
                sys.exit("Puntuacion fuera de 0-100 en %s / %s" % (e, iid))
            glob[iid][e] = _media(v)
            for c, x in zip(campos, v):
                subes[c][iid][e] = x
    if incompletos:
        print("  AVISO: %d celdas sin puntuar o no numericas (omitidas)" % incompletos)

    comunes = sorted(i for i in glob if len(glob[i]) == len(etiquetas))
    if len(comunes) < 10:
        sys.exit("Solo %d items puntuados por todos los evaluadores; insuficiente."
                 % len(comunes))
    print("\nItems puntuados por los %d evaluadores: %d de %d"
          % (len(etiquetas), len(comunes), len(clave)))

    matriz = [[glob[i][e] for e in etiquetas] for i in comunes]
    print("\n== Fiabilidad interevaluador (puntuacion global) ==")
    print("  ICC(2,1) acuerdo absoluto: %.3f" % icc21(matriz))
    for j, e in enumerate(etiquetas):
        col = [f[j] for f in matriz]
        print("  %-6s media %.1f  DT %.1f  min %.0f  max %.0f"
              % (e, _media(col), math.sqrt(_var(col)), min(col), max(col)))

    print("\n  Por criterio:")
    for c in campos:
        m = [[subes[c][i][e] for e in etiquetas] for i in comunes
             if len(subes[c][i]) == len(etiquetas)]
        print("    %-14s ICC(2,1) = %.3f" % (c, icc21(m)))

    print("\n== Consistencia interna de los cuatro criterios ==")
    for e in etiquetas:
        m = [[subes[c][i][e] for c in campos] for i in comunes]
        print("  %-6s alfa de Cronbach = %.3f" % (e, alfa_cronbach(m)))

    # --- comparacion entre modelos, pareada por caso
    prom = {i: _media(list(glob[i].values())) for i in comunes}
    porcaso = defaultdict(dict)
    for i in comunes:
        k = clave[i]
        porcaso[k["case_id"]][k["provider"]] = prom[i]
    provs = sorted({clave[i]["provider"] for i in comunes})
    bloques = [[d[p] for p in provs] for d in porcaso.values()
               if len(d) == len(provs)]

    print("\n== Calidad por modelo (media de los evaluadores) ==")
    for j, p in enumerate(provs):
        col = [b[j] for b in bloques]
        sd = math.sqrt(_var(col))
        ic = 1.96 * sd / math.sqrt(len(col))
        print("  %-10s %5.1f  (DT %4.1f, IC95 %.1f-%.1f, n=%d)"
              % (p, _media(col), sd, _media(col) - ic, _media(col) + ic, len(col)))

    if len(bloques) >= 6 and len(provs) >= 3:
        chi, gl, rangos = friedman(bloques)
        print("\n== Friedman (bloques = %d casos pareados) ==" % len(bloques))
        print("  chi2 = %.2f, gl = %d" % (chi, gl))
        print("  rango medio: " + ", ".join("%s=%.2f" % (p, r)
                                            for p, r in zip(provs, rangos)))
        pares = [(a, b) for i, a in enumerate(provs) for b in provs[i + 1:]]
        corr = len(pares)
        print("\n  Post-hoc Wilcoxon (p corregido por Bonferroni, x%d):" % corr)
        for a, b in pares:
            ia, ib = provs.index(a), provs.index(b)
            z, p = wilcoxon([x[ia] for x in bloques], [x[ib] for x in bloques])
            pc = min(1.0, p * corr) if p == p else float("nan")
            marca = " *" if pc == pc and pc < 0.05 else ""
            print("    %-10s vs %-10s  z=%6.2f  p=%.4f  p_corr=%.4f%s"
                  % (a, b, z, p, pc, marca))

    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["item_id", "case_id", "provider", "language", "category"]
                       + ["%s_%s" % (c, e) for c in campos for e in etiquetas]
                       + ["global_%s" % e for e in etiquetas] + ["global_medio"])
            for i in comunes:
                k = clave[i]
                fila = [i, k["case_id"], k["provider"],
                        hojas[etiquetas[0]][i].get("lenguaje", ""),
                        hojas[etiquetas[0]][i].get("categoria", "")]
                fila += [subes[c][i].get(e, "") for c in campos for e in etiquetas]
                fila += [glob[i][e] for e in etiquetas] + [prom[i]]
                w.writerow(fila)
        print("\nDetalle escrito en:", args.out)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)

    a = s.add_parser("hojas", help="Genera la hoja de calificacion ciega y la clave.")
    a.add_argument("--resultados", default="resultados_replicas.csv")
    a.add_argument("--metadata", default="metadata.csv",
                   help="metadata.csv del corpus, para incluir las rutas de los "
                        "dos archivos de codigo de cada caso.")
    a.add_argument("--por-celda", type=int, default=3,
                   help="Casos por cada combinacion lenguaje x categoria (def. 3).")
    a.add_argument("--semilla", type=int, default=20260801)
    a.add_argument("--hoja", default="hoja_calificacion.csv")
    a.add_argument("--clave", default="CLAVE_NO_ABRIR.csv")
    a.add_argument("--instrucciones", default="INSTRUCCIONES_EVALUADOR.txt")
    a.set_defaults(func=cmd_hojas)

    b = s.add_parser("analizar", help="ICC(2,1), alfa, descriptivos y pruebas pareadas.")
    b.add_argument("--clave", default="CLAVE_NO_ABRIR.csv")
    b.add_argument("--hojas", nargs="+", required=True,
                   metavar="etiqueta:ruta",
                   help="p.ej. E1:hoja_E1.csv E2:hoja_E2.csv")
    b.add_argument("--out", default="calidad_detalle.csv")
    b.set_defaults(func=cmd_analizar)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()