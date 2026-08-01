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


def parse_dolos_csv(path):
    """Lee pairs.csv de Dolos -> {(subA,subB): similitud 0-100}"""
    out = {}
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            keys = {k.lower(): k for k in r}
            lf = next((keys[k] for k in keys if "left" in k and "path" in k), None)
            rf = next((keys[k] for k in keys if "right" in k and "path" in k), None)
            sim = next((keys[k] for k in keys if k == "similarity"), None)
            if not (lf and rf and sim):
                continue
            try:
                v = float(r[sim])
            except (TypeError, ValueError):
                continue
            if v <= 1.0:
                v *= 100.0
            a, b = _norm(r[lf]), _norm(r[rf])
            out[frozenset((a, b))] = v
    return out


def parse_jplag(path):
    """Lee resultados de JPlag: acepta CSV exportado o el .jplag (zip con JSON)."""
    out = {}
    if path.lower().endswith(".csv"):
        with open(path, "r", encoding="utf-8-sig", newline="") as fh:
            rd = csv.reader(fh)
            for row in rd:
                if len(row) < 3:
                    continue
                try:
                    v = float(row[2])
                except ValueError:
                    continue
                if v <= 1.0:
                    v *= 100.0
                out[frozenset((_norm(row[0]), _norm(row[1])))] = v
        return out

    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        target = next((n for n in names if n.endswith("overview.json")), None)
        if target is None:
            sys.exit("No se encontro overview.json dentro de %s" % path)
        data = json.loads(z.read(target).decode("utf-8", errors="replace"))

    def walk(node):
        if isinstance(node, dict):
            keys = {k.lower() for k in node}
            has_pair = {"first_submission", "second_submission"} <= keys or \
                       {"firstsubmission", "secondsubmission"} <= keys
            if has_pair:
                g = lambda *c: next((node[k] for k in node if k.lower() in c), None)
                a = g("first_submission", "firstsubmission")
                b = g("second_submission", "secondsubmission")
                s = g("similarity", "similarities", "avg_similarity", "maximum_similarity")
                if isinstance(s, dict):
                    s = next(iter(s.values()))
                try:
                    v = float(s)
                    if v <= 1.0:
                        v *= 100.0
                    out[frozenset((_norm(a), _norm(b)))] = v
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

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()