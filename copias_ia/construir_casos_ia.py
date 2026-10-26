#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
construir_casos_ia.py — Construye metadata_ia.csv (en la raiz del repositorio) con los pares que
se evaluaran en la segunda corrida (revision M1).

Incluye:
  * Pares de COPIA REESCRITA CON IA (positivos): referencia frente a cada copia
    que verificar_equivalencia.py declaro equivalente.
      CASE_IAL_CS_001 ... (ligera)   CASE_IAI_CS_001 ... (intensa)
  * Pares de SOLUCION INDEPENDIENTE (negativos, clon tipo 4): los 30 pares
    'functional' del benchmark original, re-evaluados en la misma sesion para
    que positivos y negativos se comparen con la misma version de cada modelo.
      CASE_CODE_CS_002_R2 ...
  * Opcional (--con-estructurales): los 30 pares 'structural' (copias
    modificadas, clones tipo 2-3) como ancla para medir la deriva de los
    modelos respecto de la corrida de julio-agosto de 2026.

Uso (desde la carpeta SimilCode-Benchmark):
  python copias_ia/construir_casos_ia.py
  python copias_ia/construir_casos_ia.py --con-estructurales
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def loc_and_methods(path):
    txt = open(os.path.join(ROOT, path), encoding="utf-8-sig").read()
    loc = sum(1 for ln in txt.splitlines() if ln.strip())
    methods = len(re.findall(r"\b(?:public|private|protected|static|internal)\b[^;{=]*\([^;{]*\)\s*(?:throws[^{]*)?\{", txt))
    return loc, methods


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--con-estructurales", action="store_true")
    ap.add_argument("--incluir-no-verificadas", action="store_true",
                    help="Incluye copias sin verificacion de equivalencia (NO recomendado).")
    args = ap.parse_args()

    meta_path = os.path.join(ROOT, "metadata.csv")
    with open(meta_path, encoding="utf-8-sig", newline="") as fh:
        rd = csv.DictReader(fh)
        fields = rd.fieldnames
        meta = list(rd)

    eq = {}
    eq_path = os.path.join(HERE, "equivalencia_resumen.csv")
    if os.path.isfile(eq_path):
        with open(eq_path, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                eq[r["copy_id"]] = r["equivalent"] == "1"
    elif not args.incluir_no_verificadas:
        sys.exit("Falta copias_ia/equivalencia_resumen.csv. Ejecute antes verificar_equivalencia.py.")

    gen = {}
    log_path = os.path.join(HERE, "copias_ia_log.csv")
    if os.path.isfile(log_path):
        with open(log_path, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r["status"] == "OK":
                    gen[r["copy_id"]] = f'{r.get("generator_provider", "")}:{r.get("generator_model", "")}'

    out, skipped = [], []
    for r in meta:
        cat = r["similarity_category"].strip().lower()
        if cat == "identical":
            for tag, level in (("IAL", "ia_ligera"), ("IAI", "ia_intensa"), ("IAP", "ia_api")):
                lang = "CS" if r["language"] == "C#" else "JAVA"
                ext = ".cs" if lang == "CS" else ".java"
                folder = "csharp" if lang == "CS" else "java"
                cid = f"CODE_{tag}_{lang}_{int(r['reference_group']):03d}"
                path = f"{folder}/{cid}{ext}"
                if not os.path.isfile(os.path.join(ROOT, path)):
                    skipped.append((cid, "no existe")); continue
                if not args.incluir_no_verificadas and not eq.get(cid, False):
                    skipped.append((cid, "no equivalente o sin verificar")); continue
                loc_b, met_b = loc_and_methods(path)
                n = dict(r)
                n.update({"case_id": f"CASE_{tag}_{lang}_{int(r['reference_group']):03d}",
                          "similarity_category": level,
                          "code_b_id": cid, "code_b_filename": os.path.basename(path),
                          "code_b_path": path, "code_b_loc": loc_b, "code_b_methods": met_b,
                          "expected_similarity_min": 70, "expected_similarity_max": 100,
                          "evaluator": "", "evaluation_date": "",
                          "notes": f"copia reescrita con IA; generador {gen.get(cid, 'desconocido')}"})
                out.append(n)
        elif cat == "functional" or (cat == "structural" and args.con_estructurales):
            n = dict(r)
            n["case_id"] = r["case_id"] + "_R2"
            n["notes"] = (r.get("notes") or "") + " re-evaluacion en la sesion de revision M1"
            out.append(n)

    # En la raiz del repositorio: las rutas code_a_path/code_b_path son relativas a ella
    # (benchmark_replicas.py las resuelve respecto de la carpeta del CSV).
    dest = os.path.join(ROOT, "metadata_ia.csv")
    with open(dest, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader(); w.writerows(out)
    counts = {}
    for r in out:
        counts[r["similarity_category"]] = counts.get(r["similarity_category"], 0) + 1
    print("Escrito", dest, counts)
    for cid, why in skipped:
        print(f"  omitida {cid}: {why}")


if __name__ == "__main__":
    main()
