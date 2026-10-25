#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
marcar_revision_manual.py - Registra el resultado de la revision manual de las
copias cuyo programa de referencia no es determinista (estado revision_manual).

Uso (desde SimilCode-Benchmark):
  python copias_ia/marcar_revision_manual.py --ids CODE_IAL_JAVA_007,CODE_IAI_JAVA_007 \
      --equivalente 1 --revisor "G. Guerrero" --motivo "..."
Modifica solo las filas indicadas de copias_ia/equivalencia_resumen.csv.
"""
import argparse, csv, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--ids", required=True)
ap.add_argument("--equivalente", choices=["0", "1"], required=True)
ap.add_argument("--revisor", required=True)
ap.add_argument("--motivo", required=True)
a = ap.parse_args()
ids = {x.strip() for x in a.ids.split(",") if x.strip()}
path = os.path.join(HERE, "equivalencia_resumen.csv")
with open(path, encoding="utf-8", newline="") as fh:
    rd = csv.DictReader(fh); fields = rd.fieldnames; rows = list(rd)
hechos = set()
for r in rows:
    if r["copy_id"] in ids:
        if "revision_manual" not in r["statuses"]:
            sys.exit(f"{r['copy_id']} no esta en revision_manual; no se modifica.")
        r["equivalent"] = a.equivalente
        r["nota"] = f"Revision manual ({a.revisor}, {time.strftime('%Y-%m-%d')}): {a.motivo}"
        hechos.add(r["copy_id"])
if ids - hechos:
    sys.exit(f"No encontradas: {', '.join(sorted(ids - hechos))}")
with open(path, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
ok = sum(r["equivalent"] == "1" for r in rows)
for c in sorted(hechos): print(f"{c}: equivalente = {a.equivalente}")
print(f"\nEquivalentes: {ok} de {len(rows)}. Siguiente paso: python copias_ia/construir_casos_ia.py")
