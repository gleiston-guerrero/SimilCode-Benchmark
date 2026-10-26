#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analisis_copias_ia.py — Analisis de la segunda corrida (revision M1):
copias reescritas con IA frente a soluciones independientes del mismo ejercicio.

Entradas (en copias_ia/):
  ../metadata_ia.csv         casos evaluados (construir_casos_ia.py)
  resultados_replicas_ia.csv respuestas de los modelos (benchmark_replicas.py run)
  baselines_raw_ia.csv       Moss, JPlag y Dolos en modo cohorte (baselines.py parsear)
  copias_ia_log.csv          registro de generacion (que modelo genero cada copia)
y ../resultados_replicas.csv (corrida original) para medir la deriva.

Salida: copias_ia/resultados_copias_ia.json y un resumen en pantalla.

Medidas (todas por sistema; puntaje del modelo = mediana de las 3 replicas):
  * AUC copia-IA frente a solucion independiente (todas, ligera, intensa),
    con IC 95 % bootstrap que remuestrea programas de referencia.
  * Porcentaje marcado a umbrales de revision 50/70/80/90: copias detectadas
    (sensibilidad) y soluciones independientes marcadas (falsos positivos).
  * Efecto de autoria: AUC de cada modelo evaluador sobre copias generadas por
    su propio proveedor frente a las generadas por otros.
  * Estabilidad entre replicas y deriva de las soluciones independientes
    respecto de la corrida original.
  * Costo: tokens de entrada y salida por llamada y por modelo.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LLMS = ["openai", "deepseek", "gemini", "anthropic"]
TOOLS = ["moss", "jplag", "dolos"]
SEED = 20260730


def auc(pos, neg):
    pos = np.asarray(pos, float); neg = np.asarray(neg, float)
    pos, neg = pos[~np.isnan(pos)], neg[~np.isnan(neg)]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    r = rankdata(np.concatenate([pos, neg]))
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def cluster_ci(df, s, pos_mask, neg_mask, B=5000):
    rng = np.random.default_rng(SEED)
    keys = sorted(df.grp.unique())
    gp = {k: df[(df.grp == k) & pos_mask][s].dropna().values for k in keys}
    gn = {k: df[(df.grp == k) & neg_mask][s].dropna().values for k in keys}
    vals = []
    for _ in range(B):
        idx = rng.integers(0, len(keys), len(keys))
        p = np.concatenate([gp[keys[i]] for i in idx]); n = np.concatenate([gn[keys[i]] for i in idx])
        if len(p) and len(n):
            vals.append(auc(p, n))
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return [round(float(lo), 2), round(float(hi), 2)]


def main():
    meta = pd.read_csv(os.path.join(ROOT, "metadata_ia.csv"), encoding="utf-8-sig")
    meta["grp"] = meta.language + "_" + meta.reference_group.astype(str)
    meta["cat"] = meta.similarity_category.str.lower().map(
        {"ia_ligera": "ia_ligera", "ia_intensa": "ia_intensa", "ia_api": "ia_api", "functional": "independiente",
         "structural": "copia_modificada"})
    res = pd.read_csv(os.path.join(HERE, "resultados_replicas_ia.csv"))
    ok = res[res["global"].notna() & res["error"].isna()]
    L = ok.groupby(["case_id", "provider"])["global"].median().unstack("provider")
    X = meta.set_index("case_id").join(L)
    bpath = os.path.join(HERE, "baselines_raw_ia.csv")
    if os.path.isfile(bpath):
        b = pd.read_csv(bpath)
        b = b[b["mode"] == "cohorte"].pivot_table(index="case_id", columns="tool", values="similarity")
        X = X.join(b)
    systems = [s for s in LLMS + TOOLS if s in X.columns]

    gen = {}
    lp = os.path.join(HERE, "copias_ia_log.csv")
    if os.path.isfile(lp):
        lg = pd.read_csv(lp)
        lg = lg[lg.status == "OK"].drop_duplicates("copy_id", keep="last")
        gen = dict(zip(lg.copy_id, lg.generator_provider))
    X["generator"] = X.code_b_id.map(gen)

    out = {"n_pairs": X.cat.value_counts().to_dict(), "n_reference_programs": int(X.grp.nunique()),
           "auc": {}, "flag_rates": {}, "median_score": {}, "self_generation": {},
           "stability": {}, "drift_independent": {}, "tokens": {}}
    neg = X.cat == "independiente"
    for s in systems:
        out["auc"][s] = {}
        for name, pos in (("ia_all", X.cat.isin(["ia_ligera", "ia_intensa"])),
                          ("ia_ligera", X.cat == "ia_ligera"), ("ia_intensa", X.cat == "ia_intensa"),
                          ("ia_api", X.cat == "ia_api"),
                          ("copia_modificada", X.cat == "copia_modificada")):
            if pos.sum() == 0:
                continue
            out["auc"][s][name] = {"auc": round(auc(X[pos][s], X[neg][s]), 2),
                                   "ci95_cluster": cluster_ci(X, s, pos, neg)}
        out["flag_rates"][s] = {}
        for t in (50, 70, 80, 90):
            out["flag_rates"][s][str(t)] = {
                "ia_ligera_flagged_pct": round(100 * (X[X.cat == "ia_ligera"][s] >= t).mean(), 1),
                "ia_intensa_flagged_pct": round(100 * (X[X.cat == "ia_intensa"][s] >= t).mean(), 1),
                "ia_api_flagged_pct": round(100 * (X[X.cat == "ia_api"][s] >= t).mean(), 1) if (X.cat == "ia_api").any() else None,
                "independent_flagged_pct": round(100 * (X[neg][s] >= t).mean(), 1)}
        out["median_score"][s] = {c: float(X[X.cat == c][s].median()) for c in X.cat.dropna().unique()}
        if s in LLMS and X.generator.notna().any():
            own = (X.cat == "ia_api") & (X.generator == s)
            other = (X.cat == "ia_api") & X.generator.notna() & (X.generator != s)
            out["self_generation"][s] = {"n_own": int(own.sum()), "n_other": int(other.sum()),
                                         "auc_own": round(auc(X[own][s], X[neg][s]), 2) if own.sum() else None,
                                         "auc_other": round(auc(X[other][s], X[neg][s]), 2) if other.sum() else None}

    for s in [p for p in LLMS if p in ok.provider.unique()]:
        g = ok[ok.provider == s].groupby("case_id")["global"]
        out["stability"][s] = {"mean_range": round(float((g.max() - g.min()).mean()), 2)}
        if "input_tokens" in ok.columns:
            t = ok[ok.provider == s]
            out["tokens"][s] = {"calls": int(len(t)),
                                "input_mean": round(float(pd.to_numeric(t.input_tokens, errors="coerce").mean()), 1),
                                "output_mean": round(float(pd.to_numeric(t.output_tokens, errors="coerce").mean()), 1)}

    orig_p = os.path.join(ROOT, "resultados_replicas.csv")
    if os.path.isfile(orig_p):
        o = pd.read_csv(orig_p); o = o[o["global"].notna()]
        Lo = o.groupby(["case_id", "provider"])["global"].median().unstack("provider")
        anchors = X[X.cat == "independiente"].copy()
        anchors["orig_id"] = anchors.index.str.replace("_R2", "", regex=False)
        for s in [p for p in LLMS if p in X.columns and p in Lo.columns]:
            diff = anchors[s].values - Lo.loc[anchors.orig_id, s].values
            out["drift_independent"][s] = {"mean_diff_new_minus_original": round(float(np.nanmean(diff)), 2),
                                           "mean_abs_diff": round(float(np.nanmean(np.abs(diff))), 2)}

    with open(os.path.join(HERE, "resultados_copias_ia.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print("Pares:", out["n_pairs"])
    for s in systems:
        a = out["auc"][s].get("ia_all", {})
        ap_ = out["auc"][s].get("ia_api", {})
        f = out["flag_rates"][s]["70"]
        print(f"{s:10s} AUC local = {a.get('auc')} {a.get('ci95_cluster')} | AUC api = {ap_.get('auc')} {ap_.get('ci95_cluster')} | "
              f"umbral 70: ligera {f['ia_ligera_flagged_pct']}% intensa {f['ia_intensa_flagged_pct']}% api {f.get('ia_api_flagged_pct')}% "
              f"independientes {f['independent_flagged_pct']}%")
    print("\nDetalle completo: copias_ia/resultados_copias_ia.json")


if __name__ == "__main__":
    sys.exit(main())
