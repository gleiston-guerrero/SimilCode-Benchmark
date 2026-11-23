#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nicad_resultados.py — prepara las cohortes para NiCad y convierte sus clones de
funciones en una similitud por par de archivos (Experimento PENDIENTE).

Similitud del par (A, B) = porcentaje de lineas de funciones de B que forman parte de
un clon con alguna funcion de A (configuracion default de NiCad: umbral de
diferencia 0.30, funciones de al menos 10 lineas), simetrizado con el maximo de
ambas direcciones. Luego se calcula el AUC copia / solucion independiente con el
mismo bootstrap que analisis_dimensiones.py y se guarda nicad_similitud.csv.
"""
import argparse
import glob
import os
import shutil
import sys
import xml.etree.ElementTree as ET

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)


def pairs():
    a = pd.read_csv(os.path.join(ROOT, "metadata.csv"), encoding="utf-8-sig").assign(run="r1")
    b = pd.read_csv(os.path.join(ROOT, "metadata_ia.csv"), encoding="utf-8-sig").assign(run="r2")
    return pd.concat([a, b])


def prepare(out):
    for (run, lang), g in pairs().groupby(["run", "language"]):
        d = os.path.join(out, ("cs" if lang == "C#" else "java") + "_" + run)
        os.makedirs(d, exist_ok=True)
        for p in set(g.code_a_path) | set(g.code_b_path):
            shutil.copy(os.path.join(ROOT, p), d)
    print("Cohortes en", out)


def lines_covered(xml_path):
    """{(archivo_x, archivo_y): conjunto de (linea) de x en clones con y}."""
    cov = {}
    for cl in ET.parse(xml_path).getroot().iter("clone"):
        src = [(os.path.basename(s.get("file")), int(s.get("startline")), int(s.get("endline"))) for s in cl.iter("source")]
        for i, (fx, sx, ex) in enumerate(src):
            for j, (fy, _, _) in enumerate(src):
                if i != j and fx != fy:
                    cov.setdefault((fx, fy), set()).update(range(sx, ex + 1))
    return cov


def function_lines(xml_path):
    tot = {}
    for s in ET.parse(xml_path).getroot().iter("source"):
        f = os.path.basename(s.get("file"))
        tot.setdefault(f, set()).update(range(int(s.get("startline")), int(s.get("endline")) + 1))
    return tot


def collect(work):
    from analisis_robustez import evaluate
    rows = []
    for d in sorted(glob.glob(os.path.join(work, "*_r[12]"))):
        clones = glob.glob(d + "_functions-blind-clones/*withsource.xml") or glob.glob(d + "_functions*-clones/*.xml")
        funcs = glob.glob(d + "_functions.xml")
        if not clones or not funcs:
            print("Sin resultados de NiCad para", d); continue
        cov, tot = lines_covered(clones[0]), function_lines(funcs[0])
        lang, run = os.path.basename(d).split("_")
        P = pairs()
        P = P[(P.run == run) & (P.language == ("C#" if lang == "cs" else "Java"))]
        for _, r in P.iterrows():
            fa, fb = os.path.basename(r.code_a_path), os.path.basename(r.code_b_path)
            if fa == fb:
                s = 100.0
            else:
                s = max(100 * len(cov.get((x, y), set())) / max(len(tot.get(x, [])), 1) for x, y in ((fb, fa), (fa, fb)))
            rows.append({"case_id": r.case_id, "nicad": round(s, 1)})
    sim = pd.DataFrame(rows).set_index("case_id")
    sim.to_csv(os.path.join(HERE, "nicad_similitud.csv"))
    import analisis_robustez as ar
    for s, base in ar.scenario_frames().items():
        X = base.join(sim).dropna()
        print(s, evaluate(X, ["nicad"], X.pos, ~X.pos))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare"); p.add_argument("--out", required=True)
    c = sub.add_parser("collect"); c.add_argument("--work", required=True)
    a = ap.parse_args()
    prepare(a.out) if a.cmd == "prepare" else collect(a.work)
