#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
baselines.py — Comparacion metodologicamente equilibrada frente a Dolos y JPlag
===============================================================================

Problema que resuelve: Dolos y JPlag son herramientas de COHORTE. Sus puntajes
dependen del conjunto de entregas analizado (Dolos descuenta el codigo de
plantilla compartido; la similitud de JPlag es relativa al grupo). Ejecutarlas
sobre parejas aisladas de dos archivos desactiva ese mecanismo y no corresponde
a su uso institucional.

Por eso el protocolo ejecuta AMBOS modos y los reporta por separado:

  MODO COHORTE  (principal)  : todas las entregas del lenguaje en una sola
                               corrida; despues se extraen los 120 pares.
  MODO AISLADO  (secundario) : cada par por separado, como se hace habitualmente
                               en la literatura. La diferencia entre ambos modos
                               es en si misma un resultado reportable.

Los pares 'identico' comparan un archivo consigo mismo. Como ninguna herramienta
compara una entrega contra si misma, se materializa una copia con nombre distinto
(sufijo _COPY) para que la comparacion exista realmente y no se asuma un 100%.

Subcomandos:
  preparar  Construye los directorios de entregas para ambos modos.
  parsear   Unifica las salidas de las herramientas en un unico CSV.
  evaluar   Calcula coincidencia, sensibilidad, especificidad y desgloses,
            con banda SIMETRICA (la misma de los LLM) y tambien relajada.
"""

import argparse
import csv
import json
import os
import shutil
import sys
import zipfile
from collections import Counter, defaultdict

# El files.csv de Dolos incrusta el contenido completo de cada archivo en una
# columna, muy por encima del limite por campo por defecto (131072).
def _subir_limite_csv():
    lim = sys.maxsize
    while True:
        try:
            csv.field_size_limit(lim)
            return
        except OverflowError:
            lim = int(lim / 10)


_subir_limite_csv()

CATS = ["identico", "funcional", "estructural", "diferente"]
ALIAS = {"identical": "identico", "functional": "funcional",
         "structural": "estructural", "different": "diferente",
         "identico": "identico", "funcional": "funcional",
         "estructural": "estructural", "diferente": "diferente"}


def _strip(s):
    t = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuaeiouu")
    return str(s).strip().lower().translate(t)


def load_meta(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for r in rows:
        cat = ALIAS.get(_strip(r.get("similarity_category") or r.get("category") or ""))
        if cat is None:
            sys.exit("Categoria desconocida en %s" % r.get("case_id"))
        out.append({
            "case_id": r["case_id"],
            "language": r.get("language", "").strip(),
            "category": cat,
            "a": (r.get("code_a_path") or "").replace("\\", "/"),
            "b": (r.get("code_b_path") or "").replace("\\", "/"),
            "lo": int(float(r.get("expected_similarity_min", 0))),
            "hi": int(float(r.get("expected_similarity_max", 100))),
        })
    return out


def lang_key(language):
    return "csharp" if "#" in language or _strip(language).startswith("cs") else "java"


# --------------------------------------------------------------------- preparar
def cmd_preparar(args):
    meta = load_meta(args.metadata)
    root = args.outdir
    if os.path.isdir(root):
        shutil.rmtree(root)

    # --- MODO COHORTE: una carpeta por lenguaje; una subcarpeta por "entrega"
    cohort_map = defaultdict(dict)   # lang -> {submission_name: src_path}
    pair_names = {}                  # case_id -> (subA, subB)
    for m in meta:
        lg = lang_key(m["language"])
        a_name = os.path.splitext(os.path.basename(m["a"]))[0]
        b_name = os.path.splitext(os.path.basename(m["b"]))[0]
        if m["a"] == m["b"]:
            b_name = a_name + "_COPY"      # materializa la copia para 'identico'
        cohort_map[lg][a_name] = m["a"]
        cohort_map[lg][b_name] = m["b"]
        pair_names[m["case_id"]] = (a_name, b_name)

    n_files = 0
    for lg, subs in cohort_map.items():
        for name, src in subs.items():
            d = os.path.join(root, "cohorte", lg, name)
            os.makedirs(d, exist_ok=True)
            s = os.path.join(args.repo, src)
            if not os.path.isfile(s):
                sys.exit("No se encuentra el archivo de codigo: " + s)
            shutil.copy(s, os.path.join(d, os.path.basename(src)))
            n_files += 1

    # --- MODO AISLADO: una carpeta por caso, con dos entregas dentro
    for m in meta:
        a_name, b_name = pair_names[m["case_id"]]
        base = os.path.join(root, "aislado", m["case_id"])
        for name, src in ((a_name, m["a"]), (b_name, m["b"])):
            d = os.path.join(base, name)
            os.makedirs(d, exist_ok=True)
            shutil.copy(os.path.join(args.repo, src), os.path.join(d, os.path.basename(src)))

    # mapa de pares para el parseo posterior
    with open(os.path.join(root, "pares.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["case_id", "language", "lang_key", "category",
                    "expected_low", "expected_high", "sub_a", "sub_b"])
        for m in meta:
            a_name, b_name = pair_names[m["case_id"]]
            w.writerow([m["case_id"], m["language"], lang_key(m["language"]),
                        m["category"], m["lo"], m["hi"], a_name, b_name])

    print("Preparado en:", root)
    for lg, subs in sorted(cohort_map.items()):
        print("  cohorte/%-7s %3d entregas" % (lg, len(subs)))
    print("  aislado/        %3d carpetas de par" % len(meta))
    print("  archivos copiados:", n_files + 2 * len(meta))
    print("\nMapa de pares: %s" % os.path.join(root, "pares.csv"))


# ---------------------------------------------------------------------- parsear
def _norm(p):
    q = str(p).replace("\\", "/").rstrip("/")
    base = os.path.basename(q)
    return os.path.splitext(base)[0]


_DIRS_NO_ENTREGA = {"cohorte", "aislado", "csharp", "java", "baselines_work", ""}


def _norm_sub(p):
    """Nombre de entrega a partir de una ruta de ARCHIVO.

    En el layout de `preparar`, cada entrega es una CARPETA que contiene un
    unico archivo: cohorte/<lenguaje>/<entrega>/<archivo>. La copia de los
    pares identicos vive en la carpeta `X_COPY` pero el archivo de dentro
    conserva el nombre original `X.<ext>`, asi que tomar el nombre del archivo
    haria colapsar la copia con su original. Moss y JPlag identifican la
    entrega por la carpeta; aqui se hace lo mismo para que las tres
    herramientas compartan el mismo espacio de nombres."""
    q = str(p).replace("\\", "/").rstrip("/")
    padre = os.path.basename(os.path.dirname(q))
    if padre and padre.lower() not in _DIRS_NO_ENTREGA:
        return padre
    return _norm(q)


def _dolos_mapa_archivos(carpeta):
    """Lee files.csv de Dolos -> {id: nombre_de_entrega}.
    Dolos identifica los archivos por numero en pairs.csv; el nombre real vive
    en files.csv, asi que hay que cruzar ambos."""
    ruta = os.path.join(carpeta, "files.csv")
    if not os.path.exists(ruta):
        return {}
    mapa = {}
    with open(ruta, "r", encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            keys = {k.lower(): k for k in r}
            kid = next((keys[k] for k in keys if k in ("id", "fileid", "file_id")), None)
            kpath = next((keys[k] for k in keys
                          if "path" in k or k in ("filename", "file", "name")), None)
            if kid and kpath:
                mapa[str(r[kid]).strip()] = _norm_sub(r[kpath])
    return mapa


def parse_dolos_csv(path):
    """Lee pairs.csv de Dolos -> {(subA,subB): similitud 0-100}.

    Acepta tanto un pairs.csv con rutas literales como el formato habitual de
    Dolos 2.x, donde las columnas leftFileId/rightFileId son numeros que se
    resuelven contra el files.csv de la misma carpeta."""
    out = {}
    mapa = _dolos_mapa_archivos(os.path.dirname(os.path.abspath(path)))
    sin_resolver = colapsados = n_filas = 0
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            keys = {k.lower(): k for k in r}
            lf = next((keys[k] for k in keys if "left" in k and "path" in k), None) or \
                 next((keys[k] for k in keys if "left" in k and "id" in k), None) or \
                 next((keys[k] for k in keys if "left" in k), None)
            rf = next((keys[k] for k in keys if "right" in k and "path" in k), None) or \
                 next((keys[k] for k in keys if "right" in k and "id" in k), None) or \
                 next((keys[k] for k in keys if "right" in k), None)
            sim = next((keys[k] for k in keys if k == "similarity"), None) or \
                  next((keys[k] for k in keys if "similarity" in k), None)
            if not (lf and rf and sim):
                continue
            try:
                v = float(r[sim])
            except (TypeError, ValueError):
                continue
            if v <= 1.0:
                v *= 100.0
            a, b = str(r[lf]).strip(), str(r[rf]).strip()
            if mapa and a in mapa and b in mapa:
                a, b = mapa[a], mapa[b]
            else:
                # No son identificadores del files.csv: deben ser rutas.
                if not ("/" in a or "\\" in a):
                    sin_resolver += 1
                a, b = _norm_sub(a), _norm_sub(b)
            if a == b:
                colapsados += 1
                continue
            out[frozenset((a, b))] = v
            n_filas += 1
    print("      [dolos] %d filas -> %d pares distintos; %d entregas en files.csv"
          % (n_filas, len(out), len(mapa)))
    if colapsados:
        print("      [dolos] AVISO: %d filas descartadas por nombre de entrega repetido "
              "(A == B). Revisa el layout de baselines_work." % colapsados)
    if sin_resolver:
        print("      [dolos] AVISO: %d filas con identificador no resuelto contra "
              "files.csv. Los nombres pueden ser incorrectos." % sin_resolver)
    if n_filas != len(out):
        print("      [dolos] AVISO: %d filas colapsaron sobre pares ya vistos; hay "
              "nombres de entrega duplicados." % (n_filas - len(out)))
    return out


def _jplag_pick_sim(d):
    """De un dict de similitudes de JPlag ({'AVG':..,'MAX':..}) toma AVG.
    JPlag emite dos metricas por par; AVG es la magnitud comparable con la
    'similarity' de Dolos y con la media de los dos porcentajes de Moss.
    Esta eleccion debe declararse en Metodos."""
    if not isinstance(d, dict):
        return d
    low = {k.lower(): v for k, v in d.items()}
    for k in ("avg", "average", "avg_similarity", "average_similarity"):
        if k in low:
            return low[k]
    return next(iter(d.values()), None)


def parse_jplag(path):
    """Lee resultados de JPlag: acepta CSV exportado o el .jplag (zip con JSON).

    JPlag 6 exporta un CSV cuya cabecera es del tipo
        submissionName1,submissionName2,AVG,MAX
    Se toma SIEMPRE la columna AVG (media de las dos similitudes direccionales)."""
    out = {}
    if path.lower().endswith(".csv"):
        with open(path, "r", encoding="utf-8-sig", newline="") as fh:
            rows = [r for r in csv.reader(fh) if r]
        if not rows:
            return out
        head = [c.strip().lower() for c in rows[0]]
        # ¿La primera fila es cabecera? Lo es si su tercera celda no es numerica.
        def _isnum(x):
            try:
                float(x); return True
            except (TypeError, ValueError):
                return False
        tiene_cabecera = len(rows[0]) > 2 and not _isnum(rows[0][2])
        if tiene_cabecera:
            cand = [i for i, c in enumerate(head)
                    if any(k in c for k in ("submission", "name", "file", "left", "right", "id"))]
            avg = [i for i, c in enumerate(head) if c in ("avg", "average")
                   or "avg" in c or "average" in c]
            sims = [i for i, c in enumerate(head) if "similarity" in c or "score" in c]
            ia, ib = (cand + [0, 1])[0], (cand + [0, 1])[1]
            isim = (avg or sims or [2])[0]
            body = rows[1:]
            print("      [jplag] columnas: A=%r B=%r similitud=%r"
                  % (rows[0][ia], rows[0][ib], rows[0][isim]))
        else:
            ia, ib, isim = 0, 1, 2      # formato posicional sub1, sub2, AVG
            body = rows
        for row in body:
            if len(row) <= max(ia, ib, isim):
                continue
            try:
                v = float(row[isim])
            except ValueError:
                continue
            if v <= 1.0:
                v *= 100.0
            out[frozenset((_norm(row[ia]), _norm(row[ib])))] = v
        return out

    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        target = next((n for n in names if n.endswith("overview.json")), None)
        if target is None:
            sys.exit("No se encontro overview.json dentro de %s" % path)
        data = json.loads(z.read(target).decode("utf-8", errors="replace"))

    # JPlag 6 sustituye los nombres por identificadores y guarda el mapa aparte.
    idmap = {}
    def find_map(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if "display_name" in k.lower() and isinstance(v, dict):
                    idmap.update({str(a): str(b) for a, b in v.items()})
                find_map(v)
        elif isinstance(node, list):
            for v in node:
                find_map(v)
    find_map(data)
    resolve = lambda x: idmap.get(str(x), x)

    def walk(node):
        if isinstance(node, dict):
            keys = {k.lower() for k in node}
            has_pair = {"first_submission", "second_submission"} <= keys or \
                       {"firstsubmission", "secondsubmission"} <= keys
            if has_pair:
                g = lambda *c: next((node[k] for k in node if k.lower() in c), None)
                a = g("first_submission", "firstsubmission")
                b = g("second_submission", "secondsubmission")
                s = g("similarities", "similarity", "avg_similarity", "maximum_similarity")
                s = _jplag_pick_sim(s)
                try:
                    v = float(s)
                    if v <= 1.0:
                        v *= 100.0
                    out[frozenset((_norm(resolve(a)), _norm(resolve(b))))] = v
                except (TypeError, ValueError):
                    pass
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(data)
    if not out:
        sys.exit("No se pudieron extraer similitudes de %s. Usa la exportacion CSV "
                 "de JPlag (--csv-export) y pasa ese archivo." % path)
    # overview.json puede estar truncado a los N pares mas similares.
    print("      [jplag] %d pares leidos del .jplag. Si esperabas mas, JPlag trunca "
          "overview.json (--max-comparisons -1 para desactivarlo)." % len(out))
    return out


def parse_moss_html(path):
    """Lee la pagina de resultados de Moss -> {(subA,subB): similitud 0-100}.
    Moss emite dos porcentajes por par (uno por entrega); se toma la MEDIA, que
    es la magnitud simetrica comparable con Dolos y JPlag. Debe documentarse."""
    import re
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        html = fh.read()
    out = {}
    anchor = re.compile(r'<a\s+href="[^"]*"[^>]*>\s*([^<(]+?)\s*\((\d+)%\)\s*</a>',
                        re.IGNORECASE)
    for row in re.split(r"<tr[^>]*>", html, flags=re.IGNORECASE)[1:]:
        m = anchor.findall(row)
        if len(m) >= 2:
            (pa, va), (pb, vb) = m[0], m[1]
            a, b = _norm(pa), _norm(pb)
            if a == b:
                continue
            out[frozenset((a, b))] = (float(va) + float(vb)) / 2.0
    if not out:
        sys.exit("No se pudieron extraer pares de %s. Guarda la pagina de "
                 "resultados de Moss como HTML y vuelve a intentarlo." % path)
    return out


PARSERS = {"dolos": parse_dolos_csv, "jplag": parse_jplag, "moss": parse_moss_html}


def cmd_parsear(args):
    with open(args.pares, "r", encoding="utf-8-sig", newline="") as fh:
        pares = list(csv.DictReader(fh))

    sims = {}   # (tool, mode) -> {frozenset: sim}
    for spec in args.entrada:
        try:
            tool, mode, path = spec.split(":", 2)
        except ValueError:
            sys.exit("Formato de --entrada: herramienta:modo:ruta  (p.ej. dolos:cohorte:out/pairs.csv)")
        tool, mode = tool.lower(), mode.lower()
        if not os.path.exists(path):
            sys.exit("No existe: " + path)
        if tool not in PARSERS:
            sys.exit("Herramienta no soportada: %s (validas: %s)"
                     % (tool, ", ".join(sorted(PARSERS))))
        d = PARSERS[tool](path)
        sims.setdefault((tool, mode), {}).update(d)
        print("  %-6s %-8s %4d comparaciones leidas de %s" % (tool, mode, len(d), os.path.basename(path)))

    rows, faltan = [], Counter()
    for p in pares:
        key = frozenset((p["sub_a"], p["sub_b"]))
        for (tool, mode), d in sims.items():
            v = d.get(key)
            if v is None:
                faltan[(tool, mode)] += 1
                if not args.faltantes_cero:
                    continue
                v = 0.0
            rows.append({"case_id": p["case_id"], "language": p["language"],
                         "category": p["category"], "expected_low": p["expected_low"],
                         "expected_high": p["expected_high"], "tool": tool,
                         "mode": mode, "similarity": round(v, 2)})

    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["case_id", "language", "category",
                                           "expected_low", "expected_high",
                                           "tool", "mode", "similarity"])
        w.writeheader()
        w.writerows(rows)
    print("\nEscrito:", args.out, "|", len(rows), "filas")
    for k, n in faltan.items():
        modo = "registrados como 0" if args.faltantes_cero else "OMITIDOS"
        print("  AVISO: %s/%s sin comparacion para %d pares (%s)" % (k[0], k[1], n, modo))


# ------------------------------------------------------------------------ antlr
def _leer_texto(path):
    """Lee un archivo de texto detectando la codificacion.
    Tee-Object de Windows PowerShell escribe UTF-16LE por defecto, no UTF-8."""
    with open(path, "rb") as fh:
        crudo = fh.read()
    if crudo.startswith(b"\xff\xfe"):
        return crudo.decode("utf-16-le", errors="replace"), "utf-16-le (BOM)"
    if crudo.startswith(b"\xfe\xff"):
        return crudo.decode("utf-16-be", errors="replace"), "utf-16-be (BOM)"
    if crudo.startswith(b"\xef\xbb\xbf"):
        return crudo[3:].decode("utf-8", errors="replace"), "utf-8 (BOM)"
    muestra = crudo[:4000]
    if muestra.count(b"\x00") > len(muestra) // 4:
        # Muchos bytes nulos: UTF-16 sin BOM. El lado del nulo indica el orden.
        pares = muestra[: (len(muestra) // 2) * 2]
        impares = sum(1 for i in range(1, len(pares), 2) if pares[i] == 0)
        if impares > len(pares) // 4:
            return crudo.decode("utf-16-le", errors="replace"), "utf-16-le"
        return crudo.decode("utf-16-be", errors="replace"), "utf-16-be"
    return crudo.decode("utf-8", errors="replace"), "utf-8"


def cmd_antlr(args):
    """Cuantifica los fallos de analisis sintactico (ANTLR) de JPlag a partir del
    log de la corrida, y los cruza con los 120 pares del estudio.

    Cuando la gramatica de JPlag no puede analizar un archivo, la herramienta
    continua pero lo tokeniza de forma incompleta: la similitud de esa entrega
    deja de ser fiable. La proporcion de entregas afectadas es un resultado
    reportable sobre la cobertura sintactica de la herramienta."""
    import re
    pat_sub = re.compile(r"CODE_[A-Z]+_(?:CS|JAVA)_\d+(?:_COPY)?", re.IGNORECASE)
    pat_err = re.compile(r"(line \d+:\d+|mismatched input|extraneous input|"
                         r"no viable alternative|missing '|token recognition error|"
                         r"rule stack|cannot find symbol|ParsingException)", re.IGNORECASE)

    afectadas, n_err, n_lineas = Counter(), 0, 0
    ultima = None
    texto, codif = _leer_texto(args.log)
    for linea in texto.splitlines():
        n_lineas += 1
        m = pat_sub.findall(linea)
        if m:
            ultima = m[-1].upper()
        if pat_err.search(linea):
            n_err += 1
            # El nombre puede venir en la misma linea o en la inmediatamente previa.
            objetivo = (m[-1].upper() if m else ultima)
            if objetivo:
                afectadas[objetivo] += 1

    print("Log: %s  [%s]  (%d lineas, %d con error de analisis)"
          % (args.log, codif, n_lineas, n_err))
    if not afectadas:
        print("No se detectaron entregas con fallo de analisis.")
        if n_lineas < 20:
            print("AVISO: el log tiene muy pocas lineas. Comprueba que capturaste "
                  "la salida completa con  2>&1 | Tee-Object -FilePath ...")
        return
    print("\nEntregas afectadas: %d" % len(afectadas))
    for k, v in sorted(afectadas.items(), key=lambda kv: (-kv[1], kv[0])):
        print("  %-24s %4d errores" % (k, v))

    if args.pares and os.path.exists(args.pares):
        with open(args.pares, "r", encoding="utf-8-sig", newline="") as fh:
            pares = list(csv.DictReader(fh))
        tocados, por_cat = [], Counter()
        total_cat = Counter()
        for p in pares:
            total_cat[p["category"]] += 1
            a, b = _norm(p["sub_a"]).upper(), _norm(p["sub_b"]).upper()
            if a in afectadas or b in afectadas:
                tocados.append(p)
                por_cat[p["category"]] += 1
        print("\nPares del estudio con al menos una entrega afectada: %d de %d (%.1f%%)"
              % (len(tocados), len(pares), 100.0 * len(tocados) / max(1, len(pares))))
        for c in CATS:
            if total_cat[c]:
                print("  %-12s %3d de %3d (%.1f%%)"
                      % (c, por_cat[c], total_cat[c], 100.0 * por_cat[c] / total_cat[c]))
        if args.out:
            with open(args.out, "w", encoding="utf-8", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(["submission", "n_errores"])
                for k, v in sorted(afectadas.items()):
                    w.writerow([k, v])
            print("\nEscrito:", args.out)


# ---------------------------------------------------------------------- evaluar
def cmd_evaluar(args):
    with open(args.infile, "r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        sys.exit("CSV vacio")

    combos = sorted({(r["tool"], r["mode"]) for r in rows})
    for banda, etiqueta in ((0, "SIMETRICA (misma que los LLM)"),
                            (10, "RELAJADA (+10 pts en 'diferente')")):
        print("\n" + "=" * 72)
        print("BANDA %s" % etiqueta)
        print("=" * 72)
        print("%-8s %-9s %11s %13s %13s" % ("tool", "modo", "coincid.%", "sensib.%", "especif.%"))
        for tool, mode in combos:
            sub = [r for r in rows if r["tool"] == tool and r["mode"] == mode]
            hit = tp = fn = tn = fp = 0
            for r in sub:
                lo, hi = int(r["expected_low"]), int(r["expected_high"])
                if r["category"] == "diferente":
                    hi += banda
                if r["category"] == "identico":
                    lo -= args.tol_identico
                s = float(r["similarity"])
                ok = lo <= s <= hi
                hit += ok
                if r["category"] == "diferente":
                    tn += ok
                    fp += (not ok)
                else:
                    tp += ok
                    fn += (not ok)
            n = len(sub)
            sens = 100.0 * tp / (tp + fn) if (tp + fn) else float("nan")
            spec = 100.0 * tn / (tn + fp) if (tn + fp) else float("nan")
            print("%-8s %-9s %10.1f %12.1f %12.1f   (n=%d)"
                  % (tool, mode, 100.0 * hit / n, sens, spec, n))

        print("\n  Desglose por categoria (%% dentro del rango):")
        print("  %-8s %-9s" % ("tool", "modo") + "".join("%13s" % c for c in CATS))
        for tool, mode in combos:
            vals = []
            for cat in CATS:
                sub = [r for r in rows if r["tool"] == tool and r["mode"] == mode
                       and r["category"] == cat]
                if not sub:
                    vals.append(float("nan")); continue
                h = 0
                for r in sub:
                    lo, hi = int(r["expected_low"]), int(r["expected_high"])
                    if cat == "diferente":
                        hi += banda
                    if cat == "identico":
                        lo -= args.tol_identico
                    h += lo <= float(r["similarity"]) <= hi
                vals.append(100.0 * h / len(sub))
            print("  %-8s %-9s" % (tool, mode) + "".join("%13.1f" % v for v in vals))

    print("\n" + "=" * 72)
    print("EFECTO DEL PROTOCOLO: similitud media por herramienta y modo")
    print("=" * 72)
    for tool in sorted({t for t, _ in combos}):
        for cat in CATS:
            line = "  %-7s %-12s" % (tool, cat)
            for mode in ("cohorte", "aislado"):
                sub = [float(r["similarity"]) for r in rows
                       if r["tool"] == tool and r["mode"] == mode and r["category"] == cat]
                line += "  %s=%6.1f" % (mode, sum(sub) / len(sub)) if sub else "  %s=  n/d" % mode
            print(line)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)

    a = s.add_parser("preparar", help="Construye los directorios de entregas.")
    a.add_argument("--metadata", default="metadata.csv")
    a.add_argument("--repo", default=".", help="Raiz del repositorio (donde estan java/ y csharp/).")
    a.add_argument("--outdir", default="baselines_work")
    a.set_defaults(func=cmd_preparar)

    b = s.add_parser("parsear", help="Unifica las salidas de las herramientas.")
    b.add_argument("--pares", default="baselines_work/pares.csv")
    b.add_argument("--entrada", nargs="+", required=True,
                   metavar="herramienta:modo:ruta",
                   help="p.ej. dolos:cohorte:out/csharp/pairs.csv jplag:cohorte:res.csv")
    b.add_argument("--out", default="baselines_raw.csv")
    b.add_argument("--faltantes-cero", action="store_true",
                   help="Los pares que la herramienta no reporta se registran como 0. "
                        "Necesario para Moss, que solo lista coincidencias por encima "
                        "de su umbral. Debe declararse en Metodos.")
    b.set_defaults(func=cmd_parsear)

    c = s.add_parser("evaluar", help="Metricas con banda simetrica y relajada.")
    c.add_argument("--in", dest="infile", default="baselines_raw.csv")
    c.add_argument("--tol-identico", type=int, default=0,
                   help="Tolerancia a la baja para la categoria 'identico' "
                        "(banda 100-100 es un punto exacto). Debe fijarse a priori "
                        "y aplicarse por igual a todas las herramientas. P.ej. 5.")
    c.set_defaults(func=cmd_evaluar)

    d = s.add_parser("antlr", help="Cuantifica los fallos de analisis sintactico de JPlag.")
    d.add_argument("--log", required=True, help="Log de la corrida (jplag_cs.log / jplag_java.log)")
    d.add_argument("--pares", default="baselines_work/pares.csv")
    d.add_argument("--out", default="", help="CSV opcional con las entregas afectadas.")
    d.set_defaults(func=cmd_antlr)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()