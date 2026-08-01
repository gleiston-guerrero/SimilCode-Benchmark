#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
panel_jueces.py — M4a: panel de jueces automaticos SIN autoevaluacion
=====================================================================

Cada justificacion es puntuada por los OTROS modelos, nunca por el que la
escribio. Con ello se elimina por diseno el sesgo de autopreferencia, que es
la objecion principal a usar modelos como evaluadores de modelos.

Lo que este panel SI mide: el acuerdo entre jueces automaticos y el orden
relativo que asignan a los cuatro sistemas.

Lo que este panel NO mide: validez. Cuatro modelos no son cuatro evaluadores
independientes — comparten datos de entrenamiento y patrones de preferencia
introducidos por el ajuste con retroalimentacion humana, entre ellos la
preferencia por respuestas largas. Un acuerdo alto entre ellos puede reflejar
sesgo compartido y no fiabilidad. La validez la aporta unicamente el anclaje
con evaluadores humanos sobre una submuestra (ver calidad_justificaciones.py).

Diseno:
  * CIEGO: el juez recibe los dos archivos de codigo y la justificacion, sin
    ninguna indicacion de que sistema la produjo.
  * SIN AUTOEVALUACION: para cada justificacion, jueces = todos menos el autor.
  * ORDEN ALEATORIO con semilla fija, para que ningun juez vea los items
    agrupados por autor.
  * El juez NO recibe la categoria esperada ni la banda: se le pide juzgar la
    ARGUMENTACION, no el veredicto.
  * Escala continua 0-100 en cuatro criterios (evita el efecto techo de Likert).

Subcomandos:
  panel     Ejecuta el panel contra las APIs.
  analizar  Severidad por juez, ICC por estrato de autor, comparacion entre
            modelos con puntuaciones tipificadas por juez, y diagnostico de
            sesgo de longitud.

Requiere benchmark_replicas.py en el mismo directorio (reutiliza sus funciones
de llamada a las cuatro APIs).
"""

import argparse
import csv
import json
import math
import os
import random
import re
import sys
import time
from collections import defaultdict

try:
    from benchmark_replicas import PROVIDER_CFG
except ImportError:
    sys.exit("No se pudo importar benchmark_replicas.py. Coloca este script "
             "en el mismo directorio que benchmark_replicas.py.")

CRITERIOS = ["correccion", "especificidad", "explicacion", "utilidad"]
CATS = ["identico", "funcional", "estructural", "diferente"]

PLANTILLA = """Eres un evaluador experto en didactica de la programacion. Vas a calificar la CALIDAD DE LA ARGUMENTACION de un texto que justifica una comparacion entre dos fragmentos de codigo.

No sabes quien escribio el texto y no debes intentar deducirlo.

=== ARCHIVO A ({nombre_a}) ===
{codigo_a}

=== ARCHIVO B ({nombre_b}) ===
{codigo_b}

=== TEXTO A EVALUAR ===
{justificacion}

=== INSTRUCCIONES ===
Lee los dos archivos y comprueba si lo que el texto afirma sobre ellos es cierto.

Califica el texto en cuatro criterios, cada uno con un ENTERO de 0 a 100:

1. correccion — Correccion tecnica: las afirmaciones sobre el codigo, son verdaderas? 0 = contiene afirmaciones falsas o inventadas; 100 = todo lo que afirma es verificable en los archivos.
2. especificidad — Se refiere a elementos concretos de ESTOS archivos, o es generico? 0 = serviria para cualquier par de codigos; 100 = solo tiene sentido para este par.
3. explicacion — Explica POR QUE, o solo enuncia QUE? 0 = puro enunciado sin razonamiento; 100 = razonamiento trazable de principio a fin.
4. utilidad — Le serviria a un estudiante para entender el veredicto? 0 = inutil; 100 = suficiente por si sola.

REGLAS IMPORTANTES:
- NO califiques si el veredicto de similitud te parece acertado. Aqui se juzga la ARGUMENTACION, no la conclusion. Un texto puede razonar impecablemente hacia un veredicto equivocado: debe puntuar alto en `explicacion`.
- NO premies la extension. Un texto breve y preciso puede puntuar 100; uno largo y vago debe puntuar bajo.
- Usa el rango completo, incluidos los extremos.

Responde EXCLUSIVAMENTE con un objeto JSON, sin texto adicional ni marcas de codigo:
{{"correccion": <0-100>, "especificidad": <0-100>, "explicacion": <0-100>, "utilidad": <0-100>, "comentario": "<una frase; si detectas una afirmacion falsa, cual>"}}
"""


# ------------------------------------------------------------------ utilidades
def leer(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def rutas_codigo(path_meta):
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


def leer_codigo(repo, rel, max_chars):
    p = os.path.join(repo, rel) if rel else ""
    if not rel or not os.path.isfile(p):
        return None
    with open(p, "r", encoding="utf-8", errors="replace") as fh:
        t = fh.read()
    if len(t) > max_chars:
        t = t[:max_chars] + "\n... [truncado a %d caracteres]" % max_chars
    return t


REINTENTABLES = {408, 409, 425, 429, 500, 502, 503, 504, 529}


def _codigo_http(e):
    """Extrae el codigo HTTP tanto de urllib.error.HTTPError (gemini, deepseek)
    como del RuntimeError('HTTP nnn: ...') que levantan las envolturas de
    anthropic y openai en benchmark_replicas.py."""
    c = getattr(e, "code", None)
    if isinstance(c, int):
        return c
    m = re.search(r"HTTP(?:\s+Error)?\s+(\d{3})", str(e))
    return int(m.group(1)) if m else None


def llamar_con_reintentos(fn, prompt, modelo, key, temperature, timeout,
                          intentos=5, base=5.0):
    """Un 503 o un 429 son cortes transitorios: rendirse ante ellos convierte
    una indisponibilidad momentanea en un hueco permanente en los datos."""
    for intento in range(1, intentos + 1):
        try:
            return fn(prompt, modelo, key, temperature, timeout)
        except Exception as e:  # noqa: BLE001
            cod = _codigo_http(e)
            transitorio = (cod in REINTENTABLES) or isinstance(
                e, (TimeoutError, ConnectionError))
            if not transitorio or intento == intentos:
                raise
            espera = base * (2 ** (intento - 1))
            print("      %s; reintento %d/%d en %.0f s"
                  % (("HTTP %d" % cod) if cod else str(e)[:50],
                     intento, intentos - 1, espera), flush=True)
            time.sleep(espera)


def extraer_json(texto):
    t = str(texto).strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.I | re.M).strip()
    m = re.search(r"\{.*\}", t, re.S)
    if not m:
        raise ValueError("sin objeto JSON en la respuesta")
    obj = json.loads(m.group(0))
    vals = {}
    for c in CRITERIOS:
        if c not in obj:
            raise ValueError("falta el criterio %r" % c)
        v = float(str(obj[c]).replace(",", "."))
        if not (0 <= v <= 100):
            raise ValueError("%s fuera de 0-100: %r" % (c, obj[c]))
        vals[c] = v
    vals["comentario"] = " ".join(str(obj.get("comentario", "")).split())[:300]
    return vals


# ---------------------------------------------------------------------- panel
def cmd_panel(args):
    filas = [x for x in leer(args.resultados)
             if not str(x.get("error", "")).strip()
             and str(x.get("justification_global", "")).strip()]
    if not filas:
        sys.exit("No hay justificaciones validas en " + args.resultados)

    rutas = rutas_codigo(args.metadata)
    if not rutas:
        sys.exit("No se pudieron leer rutas de codigo de %r. El criterio de "
                 "correccion tecnica exige que el juez lea los archivos."
                 % args.metadata)

    # Una justificacion por (caso, autor): la replica mas baja disponible.
    elegido = {}
    for x in filas:
        k = (x["case_id"], x["provider"])
        if k not in elegido or int(x["replica"]) < int(elegido[k]["replica"]):
            elegido[k] = x

    autores = sorted({p for _, p in elegido})
    casos = defaultdict(dict)
    for (c, p), x in elegido.items():
        casos[c][p] = x
    completos = {c: d for c, d in casos.items() if len(d) == len(autores)}

    rng = random.Random(args.semilla)
    if args.por_celda > 0:
        celdas = defaultdict(list)
        for c, d in completos.items():
            m = next(iter(d.values()))
            celdas[(m["language"], m["category"])].append(c)
        seleccion = []
        for celda in sorted(celdas):
            ids = sorted(celdas[celda])
            rng.shuffle(ids)
            if len(ids) < args.por_celda:
                print("  AVISO: la celda %s solo tiene %d casos (pediste %d)"
                      % (celda, len(ids), args.por_celda))
            seleccion.extend(ids[:args.por_celda])
    else:
        seleccion = sorted(completos)

    jueces = args.jueces or autores
    faltan = [p for p in jueces if not os.environ.get(PROVIDER_CFG[p]["env"])]
    if faltan:
        sys.exit("Faltan variables de entorno para: %s"
                 % ", ".join(PROVIDER_CFG[p]["env"] for p in faltan))
    modelos = {p: (getattr(args, p + "_model", None)
                   or PROVIDER_CFG[p]["default_model"]) for p in jueces}

    # Items: (caso, autor, juez) con juez != autor
    items = []
    for c in seleccion:
        for autor in autores:
            for juez in jueces:
                if juez == autor:
                    continue
                for rep in range(1, args.replicas + 1):
                    items.append((c, autor, juez, rep))
    rng.shuffle(items)

    cols = ["case_id", "language", "category", "author_provider", "judge_provider",
            "judge_model", "judge_snapshot", "replica", "timestamp_utc",
            "latency_s", "n_palabras_just"] + CRITERIOS + ["comentario", "error"]

    hechas = set()
    modo = "w"
    if args.resume and os.path.exists(args.out):
        for r in leer(args.out):
            if not str(r.get("error", "")).strip() and str(r.get("correccion", "")).strip():
                hechas.add((r["case_id"], r["author_provider"],
                            r["judge_provider"], str(r["replica"])))
        modo = "a"
        print("Reanudando: %d valoraciones validas ya presentes." % len(hechas))

    print("Casos: %d | autores: %d | jueces: %s | replicas: %d"
          % (len(seleccion), len(autores), ", ".join(jueces), args.replicas))
    print("Modelos juez: " + ", ".join("%s=%s" % (k, v) for k, v in sorted(modelos.items())))
    print("Valoraciones a producir: %d\n" % len(items))

    total, i, errores = len(items), 0, 0
    with open(args.out, modo, encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        if modo == "w":
            w.writeheader()
        for caso, autor, juez, rep in items:
            i += 1
            if (caso, autor, juez, str(rep)) in hechas:
                continue
            x = casos[caso][autor]
            ra, rb = rutas.get(caso, ("", ""))
            ca = leer_codigo(args.repo, ra, args.max_chars)
            cb = leer_codigo(args.repo, rb, args.max_chars)
            if ca is None or cb is None:
                print("[%d/%d] %s -> SIN CODIGO (%s | %s)" % (i, total, caso, ra, rb))
                continue
            just = " ".join(str(x["justification_global"]).split())
            prompt = PLANTILLA.format(
                nombre_a=os.path.basename(ra), codigo_a=ca,
                nombre_b=os.path.basename(rb), codigo_b=cb,
                justificacion=just)

            row = {k: "" for k in cols}
            row.update({"case_id": caso, "language": x.get("language", ""),
                        "category": x.get("category", ""),
                        "author_provider": autor, "judge_provider": juez,
                        "judge_model": modelos[juez], "replica": rep,
                        "n_palabras_just": len(just.split()),
                        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                       time.gmtime())})
            try:
                fn = PROVIDER_CFG[juez]["fn"]
                key = os.environ[PROVIDER_CFG[juez]["env"]]
                texto, lat, snap = llamar_con_reintentos(
                    fn, prompt, modelos[juez], key, args.temperature,
                    args.timeout, intentos=args.intentos)
                vals = extraer_json(texto)
                row.update(vals)
                row["latency_s"] = round(lat, 3)
                row["judge_snapshot"] = snap
                estado = "OK  " + " ".join("%s=%g" % (c[:4], vals[c]) for c in CRITERIOS)
            except Exception as e:  # noqa: BLE001
                row["error"] = str(e)[:200]
                estado = "ERROR " + str(e)[:100]
                errores += 1
            w.writerow(row)
            fh.flush()
            print("[%d/%d] %s %s->%s rep%d  %s"
                  % (i, total, caso, autor[:4], juez[:4], rep, estado), flush=True)
            if args.sleep > 0:
                time.sleep(args.sleep)

    print("\nListo. Valoraciones en: %s  (errores: %d)" % (args.out, errores))
    if errores:
        print("Relanza el mismo comando con --resume para completar los fallidos.")


# ------------------------------------------------------------------- analizar
def _media(v):
    return sum(v) / len(v)


def _var(v, ddof=1):
    if len(v) - ddof <= 0:
        return 0.0
    m = _media(v)
    return sum((x - m) ** 2 for x in v) / (len(v) - ddof)


def _de(v):
    return math.sqrt(_var(v))


def icc21(matriz):
    n, k = len(matriz), len(matriz[0])
    if n < 2 or k < 2:
        return float("nan")
    total = [x for f in matriz for x in f]
    gm = _media(total)
    ms_r = k * sum((_media(f) - gm) ** 2 for f in matriz) / (n - 1)
    cols = [[matriz[i][j] for i in range(n)] for j in range(k)]
    ms_c = n * sum((_media(c) - gm) ** 2 for c in cols) / (k - 1)
    ss_e = sum((matriz[i][j] - _media(matriz[i]) - _media(cols[j]) + gm) ** 2
               for i in range(n) for j in range(k))
    ms_e = ss_e / ((n - 1) * (k - 1))
    den = ms_r + (k - 1) * ms_e + k * (ms_c - ms_e) / n
    return (ms_r - ms_e) / den if den else float("nan")


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


def spearman(a, b):
    ra, rb = _rango(a), _rango(b)
    ma, mb = _media(ra), _media(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return num / den if den else float("nan")


def friedman(bloques):
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
    filas = [r for r in leer(args.infile) if not str(r.get("error", "")).strip()
             and str(r.get("correccion", "")).strip()]
    if not filas:
        sys.exit("Sin valoraciones validas en " + args.infile)
    for r in filas:
        r["_g"] = _media([float(r[c]) for c in CRITERIOS])

    jueces = sorted({r["judge_provider"] for r in filas})
    autores = sorted({r["author_provider"] for r in filas})
    print("Valoraciones validas: %d | jueces: %s | autores: %s"
          % (len(filas), ", ".join(jueces), ", ".join(autores)))

    print("\n== Severidad de cada juez (sobre todo lo que califico) ==")
    est = {}
    for j in jueces:
        v = [r["_g"] for r in filas if r["judge_provider"] == j]
        est[j] = (_media(v), _de(v) or 1.0)
        print("  %-10s media %5.1f  DT %4.1f  n=%d" % (j, est[j][0], _de(v), len(v)))
    print("  Rango de severidad entre jueces: %.1f puntos"
          % (max(m for m, _ in est.values()) - min(m for m, _ in est.values())))
    print("  Con exclusion de autoevaluacion, cada autor es juzgado por un\n"
          "  subconjunto distinto de jueces, asi que estas diferencias de\n"
          "  severidad sesgarian la comparacion. Por eso se tipifica por juez.")

    for r in filas:
        m, s = est[r["judge_provider"]]
        r["_z"] = (r["_g"] - m) / s

    print("\n== Acuerdo entre jueces, por estrato de autor ==")
    print("  (dentro de cada estrato el diseno SI es cruzado: mismos jueces)")
    for a in autores:
        sub = [r for r in filas if r["author_provider"] == a]
        js = sorted({r["judge_provider"] for r in sub})
        d = defaultdict(dict)
        for r in sub:
            d[r["case_id"]][r["judge_provider"]] = r["_g"]
        m = [[d[c][j] for j in js] for c in sorted(d) if len(d[c]) == len(js)]
        if len(m) >= 3:
            print("  autor %-10s jueces=%-28s n=%3d  ICC(2,1)=%.3f"
                  % (a, ",".join(x[:4] for x in js), len(m), icc21(m)))
        else:
            print("  autor %-10s datos insuficientes" % a)

    print("\n== Correlacion por pares de jueces (Spearman, items comunes) ==")
    for i, ja in enumerate(jueces):
        for jb in jueces[i + 1:]:
            da = {(r["case_id"], r["author_provider"]): r["_g"]
                  for r in filas if r["judge_provider"] == ja}
            db = {(r["case_id"], r["author_provider"]): r["_g"]
                  for r in filas if r["judge_provider"] == jb}
            com = sorted(set(da) & set(db))
            if len(com) >= 8:
                print("  %-10s vs %-10s  rho=%.3f  (n=%d)"
                      % (ja, jb, spearman([da[k] for k in com], [db[k] for k in com]),
                         len(com)))

    print("\n== Diagnostico de sesgo de longitud ==")
    for j in jueces:
        sub = [r for r in filas if r["judge_provider"] == j
               and str(r.get("n_palabras_just", "")).strip()]
        if len(sub) >= 10:
            rho = spearman([float(r["n_palabras_just"]) for r in sub],
                           [r["_g"] for r in sub])
            print("  %-10s rho(palabras, puntuacion) = %+.3f  (n=%d)" % (j, rho, len(sub)))
    todos = [r for r in filas if str(r.get("n_palabras_just", "")).strip()]
    if len(todos) >= 10:
        print("  PANEL      rho(palabras, puntuacion) = %+.3f"
              % spearman([float(r["n_palabras_just"]) for r in todos],
                         [r["_g"] for r in todos]))
    print("  Un rho positivo alto indicaria que el panel premia la extension y\n"
          "  no la calidad. Debe reportarse junto con cualquier ranking.")

    for etiqueta, campo in (("BRUTA", "_g"), ("TIPIFICADA POR JUEZ", "_z")):
        agr = defaultdict(list)
        for r in filas:
            agr[(r["case_id"], r["author_provider"])].append(r[campo])
        porcaso = defaultdict(dict)
        for (c, a), v in agr.items():
            porcaso[c][a] = _media(v)
        bloques = [[d[a] for a in autores] for d in porcaso.values()
                   if len(d) == len(autores)]
        if len(bloques) < 6:
            continue
        print("\n== Calidad por modelo — puntuacion %s ==" % etiqueta)
        for j, a in enumerate(autores):
            col = [b[j] for b in bloques]
            ic = 1.96 * _de(col) / math.sqrt(len(col))
            print("  %-10s %7.2f  (DT %5.2f, IC95 %6.2f a %6.2f, n=%d)"
                  % (a, _media(col), _de(col), _media(col) - ic, _media(col) + ic,
                     len(col)))
        chi, gl, rangos = friedman(bloques)
        print("  Friedman: chi2=%.2f, gl=%d | rango medio: %s"
              % (chi, gl, ", ".join("%s=%.2f" % (a, r) for a, r in zip(autores, rangos))))
        pares = [(a, b) for i, a in enumerate(autores) for b in autores[i + 1:]]
        print("  Post-hoc Wilcoxon (Bonferroni x%d):" % len(pares))
        for a, b in pares:
            ia, ib = autores.index(a), autores.index(b)
            z, p = wilcoxon([x[ia] for x in bloques], [x[ib] for x in bloques])
            pc = min(1.0, p * len(pares)) if p == p else float("nan")
            print("    %-10s vs %-10s z=%6.2f p=%.4f p_corr=%.4f%s"
                  % (a, b, z, p, pc, " *" if pc == pc and pc < 0.05 else ""))

    print("\nRECORDATORIO: estas cifras describen el ACUERDO del panel y el orden\n"
          "que asigna, no su VALIDEZ. Sin anclaje humano sobre una submuestra no\n"
          "puede afirmarse que midan calidad.")

    if args.out:
        agr = defaultdict(list)
        for r in filas:
            agr[(r["case_id"], r["author_provider"])].append(r)
        with open(args.out, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["case_id", "language", "category", "author_provider",
                        "n_jueces", "n_palabras_just", "global_bruto", "global_z"]
                       + CRITERIOS)
            for (c, a), rs in sorted(agr.items()):
                w.writerow([c, rs[0]["language"], rs[0]["category"], a, len(rs),
                            rs[0].get("n_palabras_just", ""),
                            round(_media([r["_g"] for r in rs]), 2),
                            round(_media([r["_z"] for r in rs]), 3)]
                           + [round(_media([float(r[k]) for r in rs]), 2)
                              for k in CRITERIOS])
        print("\nDetalle escrito en:", args.out)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)

    a = s.add_parser("panel", help="Ejecuta el panel de jueces contra las APIs.")
    a.add_argument("--resultados", default="resultados_replicas.csv")
    a.add_argument("--metadata", default="metadata.csv")
    a.add_argument("--repo", default=".", help="Raiz donde estan java/ y csharp/.")
    a.add_argument("--out", default="panel_jueces.csv")
    a.add_argument("--por-celda", type=int, default=3,
                   help="Casos por celda lenguaje x categoria. 0 = todos los casos.")
    a.add_argument("--jueces", nargs="+", choices=sorted(PROVIDER_CFG),
                   help="Por defecto, los cuatro.")
    a.add_argument("--replicas", type=int, default=1)
    a.add_argument("--semilla", type=int, default=20260801)
    a.add_argument("--temperature", type=float, default=0.0)
    a.add_argument("--sleep", type=float, default=1.0)
    a.add_argument("--timeout", type=float, default=180.0)
    a.add_argument("--max-chars", type=int, default=6000)
    a.add_argument("--intentos", type=int, default=5,
                   help="Intentos por llamada ante fallos transitorios (503, "
                        "429, 500...). Espera exponencial desde 5 s.")
    a.add_argument("--resume", action="store_true")
    for prov in sorted(PROVIDER_CFG):
        a.add_argument("--%s-model" % prov, dest="%s_model" % prov, default=None)
    a.set_defaults(func=cmd_panel)

    b = s.add_parser("analizar", help="Severidad, ICC por estrato, comparacion y sesgos.")
    b.add_argument("--in", dest="infile", default="panel_jueces.csv")
    b.add_argument("--out", default="panel_detalle.csv")
    b.set_defaults(func=cmd_analizar)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()