#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
similitud_tokens_ia.py — Similitud de tokens normalizada (misma regla que
analisis_tipos_clon.py) entre cada par de metadata_ia.csv: copias reescritas con
IA (ia_ligera, ia_intensa, ia_api) y soluciones independientes (functional).

Uso (desde la carpeta SimilCode-Benchmark):
  python copias_ia/similitud_tokens_ia.py
Salida: copias_ia/similitud_tokens_ia.csv y un resumen por categoria.
"""
import csv, os, statistics as st, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(ROOT, "analisis_tipos_clon.py"), encoding="utf-8").read().split("if __name__")[0]
g = {}; exec(src, g)
rows = list(csv.DictReader(open(os.path.join(ROOT, "metadata_ia.csv"), encoding="utf-8-sig")))
out = []
for r in rows:
    a = open(os.path.join(ROOT, r["code_a_path"]), encoding="utf-8-sig").read()
    b = open(os.path.join(ROOT, r["code_b_path"]), encoding="utf-8-sig").read()
    t, ratio = g["classify"](a, b)[:2]
    out.append({"case_id": r["case_id"], "category": r["similarity_category"], "clone_type_rule": t, "token_similarity": round(ratio, 4)})
with open(os.path.join(HERE, "similitud_tokens_ia.csv"), "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for c in ["ia_ligera", "ia_intensa", "ia_api", "functional"]:
    v = [x["token_similarity"] for x in out if x["category"] == c]
    print(f"{c:11s} n={len(v):2d} mediana={st.median(v):.3f} min={min(v):.3f} max={max(v):.3f} >=0.90: {sum(x >= 0.9 for x in v)}")
