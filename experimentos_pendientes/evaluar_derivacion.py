#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evaluar_derivacion.py — Experimento PENDIENTE (requiere claves de API; no ejecutado).

Pregunta directa de derivacion con dimensiones definidas (prompt_derivacion.txt),
para comprobar fuera de muestra la puntuacion de derivacion del manuscrito, que se
definio despues de analizar la similitud global. Se fija ANTES de ejecutar:

  Hipotesis H1: en copias convencionales (tipos 2-3) frente a soluciones
  independientes (tipo 4), el AUC de PROBABILIDAD DE DERIVACION es >= 0.90 para
  cada modelo. H2: en copias de modelos comerciales (ia_api) frente a soluciones
  independientes puntuadas en la misma sesion, el AUC es < 0.80 para cada modelo.
  Analisis: mismos AUC, bootstrap por conglomerados (30 programas de referencia,
  5 000 remuestreos, semilla 20260730) y umbrales 50/70/80/90 que analisis_dimensiones.py.

Casos: los 30 pares tipo 2-3 y los 30 tipo 4 de la primera corrida y los 30 ia_api
con los 30 funcionales de la segunda corrida (90 pares distintos; los funcionales
se puntuan una vez y sirven para ambas comparaciones). 90 pares x 4 modelos x 3
replicas = 1 080 llamadas.

Uso (Windows, PowerShell, desde la carpeta SimilCode-Benchmark):
  $env:OPENAI_API_KEY="..."; $env:DEEPSEEK_API_KEY="..."; $env:GEMINI_API_KEY="..."; $env:ANTHROPIC_API_KEY="..."
  python experimentos_pendientes\\evaluar_derivacion.py run --only openai,deepseek,gemini,anthropic
  python experimentos_pendientes\\evaluar_derivacion.py analyze
"""
import argparse
import csv
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import benchmark_replicas as br  # noqa: E402

OUT = os.path.join(HERE, "resultados_derivacion.csv")
FIELDS = ["run_ts", "case_id", "language", "category", "provider", "model", "model_snapshot", "replica",
          "latency_s", "lexica", "estructural", "estilistica", "funcional", "sintactica", "derivacion",
          "justificacion", "error"]


def select_cases():
    tipos = {r["case_id"]: r["clone_type"] for r in csv.DictReader(open(os.path.join(ROOT, "tipos_clon.csv"), encoding="utf-8-sig"))}
    first = [c for c in br.load_cases(os.path.join(ROOT, "metadata.csv")) if tipos.get(c["id"]) in ("type2", "type3")]
    second = [c for c in br.load_cases(os.path.join(ROOT, "metadata_ia.csv")) if c["category"] in ("ia_api", "funcional")]
    return first + second


def parse(text):
    def num(label):
        m = re.search(label + r"[:\s]*\[?\s*(\d{1,3})", text, re.IGNORECASE)
        return max(0, min(100, int(m.group(1)))) if m else None
    j = re.search(r"Justificaci[oó]n\s*:?\s*(.+)", text, re.IGNORECASE | re.DOTALL)
    return {"lexica": num(r"SIMILITUD\s+L[EÉ]XICA"), "estructural": num(r"SIMILITUD\s+ESTRUCTURAL"),
            "estilistica": num(r"SIMILITUD\s+ESTIL[IÍ]STICA"), "funcional": num(r"SIMILITUD\s+FUNCIONAL"),
            "sintactica": num(r"SIMILITUD\s+SINT[AÁ]CTICA"), "derivacion": num(r"PROBABILIDAD\s+DE\s+DERIVACI[OÓ]N"),
            "justificacion": " ".join(j.group(1).split())[:800] if j else ""}


def cmd_run(a):
    template = open(os.path.join(HERE, "prompt_derivacion.txt"), encoding="utf-8").read()
    provs = [p.strip() for p in a.only.split(",") if p.strip()]
    done = set()
    if os.path.exists(OUT):
        for r in csv.DictReader(open(OUT, encoding="utf-8")):
            if not r["error"]:
                done.add((r["case_id"], r["provider"], r["replica"]))
    new = not os.path.exists(OUT)
    run_ts = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(OUT, "a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new:
            w.writeheader()
        for c in select_cases():
            prompt = br.build_prompt(template, c["code_a"], c["code_b"])
            for p in provs:
                key = os.environ.get(br.PROVIDER_CFG[p]["env"])
                model = br.PROVIDER_CFG[p]["default_model"]
                for rep in range(1, a.replicas + 1):
                    if (c["id"], p, str(rep)) in done:
                        continue
                    row = {k: "" for k in FIELDS}
                    row.update(run_ts=run_ts, case_id=c["id"], language=c["language"], category=c["category"],
                               provider=p, model=model, replica=rep)
                    try:
                        text, lat, snap = br.call_with_retries(p, prompt, model, key, 0.0, 180, 4, 2.0)
                        row.update(model_snapshot=snap, latency_s=round(lat, 3), **parse(text))
                    except Exception as e:  # noqa: BLE001
                        row["error"] = str(e)[:200]
                    w.writerow(row); fh.flush()
                    print(c["id"], p, rep, "ERROR" if row["error"] else row["derivacion"], flush=True)


def cmd_analyze(_):
    import numpy as np
    import pandas as pd
    from analisis_robustez import evaluate
    df = pd.read_csv(OUT)
    df = df[df.error.isna() & df.derivacion.notna()]
    M = df.groupby(["case_id", "provider"])[["derivacion", "funcional"]].median()
    tipos = pd.read_csv(os.path.join(ROOT, "tipos_clon.csv")).set_index("case_id")
    meta = pd.read_csv(os.path.join(ROOT, "metadata_ia.csv"), encoding="utf-8-sig").set_index("case_id")
    conv = tipos[tipos.clone_type.isin(["type2", "type3"])].assign(grp=lambda d: d.language + "_" + d.reference_group.astype(str), pos=True)[["grp", "pos"]]
    indep = meta[meta.similarity_category.str.lower() == "functional"].assign(grp=lambda d: d.language + "_" + d.reference_group.astype(str), pos=False)[["grp", "pos"]]
    api = meta[meta.similarity_category.str.lower() == "ia_api"].assign(grp=lambda d: d.language + "_" + d.reference_group.astype(str), pos=True)[["grp", "pos"]]
    res = {}
    for name, base in (("conventional_vs_indep", pd.concat([conv, indep])), ("ia_api_vs_indep", pd.concat([api, indep]))):
        res[name] = {}
        for p in sorted(M.index.get_level_values(1).unique()):
            X = base.join(M.xs(p, level="provider")).dropna()
            r = evaluate(X, ["derivacion", "funcional"], X.pos, ~X.pos)
            r["flag70"] = {"copy": round(100 * float((X.loc[X.pos, "derivacion"] >= 70).mean()), 1),
                           "independent": round(100 * float((X.loc[~X.pos, "derivacion"] >= 70).mean()), 1)}
            res[name][p] = r
    json.dump(res, open(os.path.join(HERE, "resultados_derivacion.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("--only", default="openai,deepseek,gemini,anthropic"); r.add_argument("--replicas", type=int, default=3)
    sub.add_parser("analyze")
    a = ap.parse_args()
    cmd_run(a) if a.cmd == "run" else cmd_analyze(a)


if __name__ == "__main__":
    main()
