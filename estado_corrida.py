#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
estado_corrida.py
=================
Estado real de la corrida: cuenta combinaciones UNICAS (caso, modelo, replica)
completadas con exito, no filas del CSV (los reintentos anaden filas nuevas).

Uso:  python estado_corrida.py
"""
import collections
import csv
import os
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else "resultados_replicas.csv"
PROVIDERS = ("deepseek", "gemini", "openai", "anthropic")
REPLICAS = ("1", "2", "3")

if not os.path.isfile(PATH):
    sys.exit("No se encuentra " + PATH)

with open(PATH, "r", encoding="utf-8-sig", newline="") as fh:
    rows = list(csv.DictReader(fh))

ok = {(r["case_id"], r["provider"], r["replica"]) for r in rows if not r["error"]}
cases = {r["case_id"] for r in rows}
esperado = len(cases) * len(PROVIDERS) * len(REPLICAS)

faltan = collections.Counter()
for c in cases:
    for p in PROVIDERS:
        for rep in REPLICAS:
            if (c, p, rep) not in ok:
                faltan[p] += 1

print("Filas en el CSV        :", len(rows), "(incluye reintentos)")
print("Casos detectados       :", len(cases))
print("Completadas con exito  :", len(ok), "de", esperado,
      "(%.1f%%)" % (100.0 * len(ok) / esperado if esperado else 0))

print("\nCompletadas por modelo:")
por = collections.Counter(p for (_c, p, _r) in ok)
for p in PROVIDERS:
    print("   %-10s %4d / %d" % (p, por[p], len(cases) * 3))

if faltan:
    print("\nPendientes por modelo:")
    for p in PROVIDERS:
        if faltan[p]:
            print("   %-10s %4d" % (p, faltan[p]))
else:
    print("\nNo falta ninguna combinacion.")

err = [r for r in rows if r["error"]]
if err:
    print("\nFilas con error: %d" % len(err))
    print("Mensajes mas frecuentes:")
    for (p, e), n in collections.Counter(
            (r["provider"], " ".join(r["error"].split())[:140]) for r in err).most_common(6):
        print("   %3d x %-10s %s" % (n, p, e))

if len(ok) == esperado:
    print("\n>>> CORRIDA COMPLETA. Ya puedes ejecutar 'analyze'.")
else:
    print("\n>>> Faltan %d llamadas. Relanza el mismo comando 'run' para completarlas."
          % (esperado - len(ok)))