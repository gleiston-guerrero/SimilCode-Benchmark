#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analisis_dimensiones.py — Separacion de copias y soluciones independientes por
dimension de similitud (reanalisis de las respuestas archivadas, sin llamadas a API).

Motivo. El prompt de similitud pide cinco puntuaciones por dimension y una
similitud global ponderada (funcional 40 %, estructural 30 %, lexica 20 %,
estilistica 10 %). Las soluciones independientes a un mismo ejercicio hacen lo
mismo por definicion (clones tipo 4), de modo que la dimension funcional las
puntua alto aunque no sean copias. Este script mide la separacion
copia / solucion independiente con cada dimension por separado y con una
puntuacion de derivacion definida a partir del propio prompt: la misma
ponderacion sin la dimension funcional, renormalizada,
    derivacion = (0.30 estructural + 0.20 lexica + 0.10 estilistica) / 0.60.
No hay parametros ajustados a los datos: los pesos son los del prompt.

Entradas
  resultados_replicas.csv, tipos_clon.csv, baselines_raw.csv     (primera corrida)
  metadata_ia.csv, copias_ia/resultados_replicas_ia.csv,
  copias_ia/baselines_raw_ia.csv                                 (segunda corrida)
Salida
  resultados_dimensiones.json y un resumen en pantalla.

Medidas (puntaje de un LLM = mediana de sus 3 replicas, por dimension)
  * AUC copia frente a solucion independiente, con IC 95 % bootstrap que
    remuestrea los 30 programas de referencia (5 000 remuestreos, semilla fija).
  * Diferencia de AUC derivacion - global, con IC 95 % bootstrap pareado por
    conglomerados.
  * Porcentaje de copias y de soluciones independientes que alcanzan los
    umbrales de revision 50, 70, 80 y 90.
  * Mediana de cada dimension en copias y en soluciones independientes.

Uso (desde la carpeta SimilCode-Benchmark):
  python analisis_dimensiones.py
"""
import json
import os

import numpy as np
import pandas as pd
from scipy.stats import rankdata

ROOT = os.path.dirname(os.path.abspath(__file__))
SEED = 20260730
B = 5000
LLMS = ["openai", "deepseek", "gemini", "anthropic"]
TOOLS = ["moss", "jplag", "dolos"]
DIMS = ["lexica", "estructural", "estilistica", "sintactica", "funcional", "global"]
SCORES = DIMS + ["derivacion"]
THRESHOLDS = (50, 70, 80, 90)


def auc(pos, neg):
    pos = np.asarray(pos, float); neg = np.asarray(neg, float)
    pos, neg = pos[~np.isnan(pos)], neg[~np.isnan(neg)]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    r = rankdata(np.concatenate([pos, neg]))
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def prepare(df):
    df = df[df["global"].notna()].copy()
    if "error" in df.columns:
        df = df[df["error"].isna()]
    for c in DIMS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["derivacion"] = (0.30 * df.estructural + 0.20 * df.lexica + 0.10 * df.estilistica) / 0.60
    return df.groupby(["case_id", "provider"])[SCORES].median()


def cluster_boot(X, cols, pos, neg):
    """IC 95 % del AUC de cada columna y de la diferencia derivacion - global."""
    rng = np.random.default_rng(SEED)
    keys = sorted(X.grp.unique())
    idx_by = {k: np.where(X.grp.values == k)[0] for k in keys}
    pos = pos.values; neg = neg.values
    draws = {c: [] for c in cols}
    diffs = []
    for _ in range(B):
        sel = np.concatenate([idx_by[keys[i]] for i in rng.integers(0, len(keys), len(keys))])
        p, n = sel[pos[sel]], sel[neg[sel]]
        if len(p) == 0 or len(n) == 0:
            continue
        a = {c: auc(X[c].values[p], X[c].values[n]) for c in cols}
        for c in cols:
            draws[c].append(a[c])
        if "derivacion" in cols and "global" in cols:
            diffs.append(a["derivacion"] - a["global"])
    ci = {c: [round(float(v), 2) for v in np.nanpercentile(draws[c], [2.5, 97.5])] for c in cols}
    dci = [round(float(v), 2) for v in np.nanpercentile(diffs, [2.5, 97.5])] if diffs else None
    return ci, dci


def summarize(X, cols, pos, neg):
    ci, dci = cluster_boot(X, cols, pos, neg)
    out = {}
    for c in cols:
        P, N = X.loc[pos, c], X.loc[neg, c]
        out[c] = {"auc": round(auc(P, N), 2), "ci95_cluster": ci[c],
                  "median_copy": round(float(P.median()), 1), "median_independent": round(float(N.median()), 1),
                  "flagged_pct": {str(t): {"copy": round(100 * float((P >= t).mean()), 1),
                                           "independent": round(100 * float((N >= t).mean()), 1)}
                                  for t in THRESHOLDS}}
    if dci is not None:
        out["diff_derivacion_minus_global"] = {
            "auc_diff": round(out["derivacion"]["auc"] - out["global"]["auc"], 2), "ci95_cluster": dci}
    return out


def first_run():
    L = prepare(pd.read_csv(os.path.join(ROOT, "resultados_replicas.csv")))
    ct = pd.read_csv(os.path.join(ROOT, "tipos_clon.csv"))
    b = pd.read_csv(os.path.join(ROOT, "baselines_raw.csv"))
    b = b[b["mode"] == "cohorte"].pivot_table(index="case_id", columns="tool", values="similarity")
    res = {}
    base = ct.set_index("case_id")
    base["grp"] = base.language + "_" + base.reference_group.astype(str)
    for name, pos_types in (("conventional_T2T3", ["type2", "type3"]), ("all_T1T3", ["type1", "type2", "type3"])):
        res[name] = {}
        for p in LLMS:
            X = base.join(L.xs(p, level="provider"))
            X = X[X.clone_type.isin(pos_types + ["type4"])]
            res[name][p] = summarize(X, SCORES, X.clone_type.isin(pos_types), X.clone_type == "type4")
        X = base.join(b)
        X = X[X.clone_type.isin(pos_types + ["type4"])]
        for t in TOOLS:
            res[name][t] = summarize(X, [t], X.clone_type.isin(pos_types), X.clone_type == "type4")[t]
    return res


def second_run():
    meta = pd.read_csv(os.path.join(ROOT, "metadata_ia.csv"), encoding="utf-8-sig")
    meta["grp"] = meta.language + "_" + meta.reference_group.astype(str)
    meta["cat"] = meta.similarity_category.str.lower().map(
        {"ia_ligera": "ia_ligera", "ia_intensa": "ia_intensa", "ia_api": "ia_api", "functional": "independiente"})
    L = prepare(pd.read_csv(os.path.join(ROOT, "copias_ia", "resultados_replicas_ia.csv")))
    b = pd.read_csv(os.path.join(ROOT, "copias_ia", "baselines_raw_ia.csv"))
    b = b[b["mode"] == "cohorte"].pivot_table(index="case_id", columns="tool", values="similarity")
    base = meta.set_index("case_id")
    res = {}
    for name in ("ia_api", "ia_intensa", "ia_ligera"):
        res[name] = {}
        for p in LLMS:
            X = base.join(L.xs(p, level="provider"))
            X = X[X.cat.isin([name, "independiente"])]
            res[name][p] = summarize(X, SCORES, X.cat == name, X.cat == "independiente")
        X = base.join(b)
        X = X[X.cat.isin([name, "independiente"])]
        for t in TOOLS:
            res[name][t] = summarize(X, [t], X.cat == name, X.cat == "independiente")[t]
    return res


def main():
    out = {"definition": "derivacion = (0.30*estructural + 0.20*lexica + 0.10*estilistica) / 0.60",
           "first_run": first_run(), "second_run": second_run()}
    with open(os.path.join(ROOT, "resultados_dimensiones.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    for run, comp in (("first_run", "conventional_T2T3"), ("second_run", "ia_api")):
        print(f"\n== {run}: {comp}")
        for s in LLMS:
            r = out[run][comp][s]
            d = r["diff_derivacion_minus_global"]
            print(f"{s:10s} " + " ".join(f"{c[:5]}={r[c]['auc']:.2f}" for c in SCORES)
                  + f" | deriv CI {r['derivacion']['ci95_cluster']} | diff {d['auc_diff']:+.2f} {d['ci95_cluster']}"
                  + f" | deriv>=70 copia {r['derivacion']['flagged_pct']['70']['copy']} indep {r['derivacion']['flagged_pct']['70']['independent']}")
        for t in TOOLS:
            r = out[run][comp][t]
            print(f"{t:10s} AUC={r['auc']:.2f} {r['ci95_cluster']} >=70 copia {r['flagged_pct']['70']['copy']} indep {r['flagged_pct']['70']['independent']}")
    print("\nDetalle completo: resultados_dimensiones.json")


if __name__ == "__main__":
    main()
