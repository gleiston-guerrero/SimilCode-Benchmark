#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analisis_manuscrito.py — reproduce every figure reported in the manuscript
=========================================================================

Recomputes, from the archived raw files only (no API calls), all the numbers
reported in the Results section of the SimilCode manuscript (version 13,
Discover Computing):

  * LLM benchmark (resultados_replicas.csv): majority-vote coincidence,
    individual coincidence, stability, BCa intervals, Cochran's Q, exact
    McNemar with Bonferroni, latency (Friedman, Wilcoxon, paired Hedges g),
    profile by category and language, band sensitivity, formula fidelity and
    the functional score required to reach the band.
  * Classical detectors (baselines_raw.csv): coincidence, sensitivity,
    specificity, profile by category, Moss tolerance sensitivity.
  * Big O (bigo/predicciones_api*.csv): accuracy against the corrected and
    the original ground truth, replica agreement.
  * Ground truth (fiabilidad/): Cohen's kappa.

Quality of the justifications and the expert questionnaire are analysed in
the SimilCode-Validation repository (calidad_justificaciones.py,
panel_jueces.py, fiabilidad.py). Use --validation to point to a local copy
of that repository and include them here.

Decisions fixed before the analysis (declared in the manuscript):
  * A response is coincident if expected_low <= global <= expected_high.
  * Primary outcome: majority verdict per pair, coincident in >= 2 of the 3
    replicas. A response without a parsable global score counts as
    NON-coincident (4 Claude Opus 5 responses).
  * Tolerance of 5 points in the identical category (95-100), applied to all
    systems; the different band is 0-20 (0-30 reported as sensitivity).
  * Band sensitivity: every NON-identical band widened (+d) or narrowed (-d);
    the identical band is never changed.
  * Bootstrap: BCa, 10,000 resamples, seed 20260730.

Usage:
    python analisis_manuscrito.py [--validation ../SimilCode-Validation]

Requirements: pandas, numpy, scipy, statsmodels, pingouin, scikit-learn.
"""
import argparse
import itertools
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import cohen_kappa_score
from statsmodels.stats.contingency_tables import cochrans_q, mcnemar

ROOT = Path(__file__).resolve().parent
P = ["openai", "deepseek", "gemini", "anthropic"]
CATS = ["identico", "funcional", "estructural", "diferente"]
SEED = 20260730


def within(df, d=0, tol_ident=0, dif_hi=None, col="global"):
    lo = df.expected_low.astype(float).copy()
    hi = df.expected_high.astype(float).copy()
    non_id = df.category != "identico"
    lo[non_id] = lo[non_id] - d
    hi[non_id] = hi[non_id] + d
    lo[~non_id] = 100 - tol_ident
    hi[~non_id] = 100
    if dif_hi is not None:
        hi[df.category == "diferente"] = dif_hi
    s = df[col]
    return ((s >= lo) & (s <= hi) & s.notna()).astype(int)


def bca(x, rng):
    r = stats.bootstrap((np.asarray(x, float),), np.mean, n_resamples=10000,
                        method="BCa", random_state=rng)
    return [round(r.confidence_interval.low, 3), round(r.confidence_interval.high, 3)]


def hedges_paired(d):
    dz = d.mean() / d.std(ddof=1)
    return round(dz * (1 - 3 / (4 * (len(d) - 1) - 1)), 2)


def llm(out):
    r = pd.read_csv(ROOT / "resultados_replicas.csv")
    v = r[r["error"].isna()].copy()
    assert len(v) == 1440, "expected 1440 valid evaluations"
    out["retries_by_provider_error"] = {f"{k[0]} / {k[1]}": int(n) for k, n in
                                        r[r["error"].notna()].groupby(["provider", "error"]).size().items()}
    out["unparsable_global"] = int(v["global"].isna().sum())
    rng = np.random.default_rng(SEED)

    def majority(**kw):
        ok = v.assign(ok=within(v, **kw)).groupby(["case_id", "provider"]).ok.sum().unstack()[P]
        return (ok >= 2).astype(int), ok

    M, votes = majority()
    meta = v.drop_duplicates("case_id").set_index("case_id")[["language", "category"]]
    n, k = M.shape
    q = cochrans_q(M.values)
    out["coincidence_majority"] = {p: round(M[p].mean() * 100, 1) for p in P}
    out["coincidence_ci"] = {p: [round(c * 100, 1) for c in bca(M[p], rng)] for p in P}
    out["coincidence_individual"] = {p: round(within(v[v.provider == p]).mean() * 100, 1) for p in P}
    out["stability"] = {p: round(((votes[p] == 0) | (votes[p] == 3)).mean() * 100, 1) for p in P}
    rng_glob = v.groupby(["case_id", "provider"])["global"].agg(lambda s: s.max() - s.min()).unstack()
    out["mean_replica_range"] = {p: round(rng_glob[p].mean(), 2) for p in P}
    out["cochran"] = {"Q": round(q.statistic, 2), "p": float(q.pvalue), "W": round(q.statistic / (n * (k - 1)), 3)}
    mc = {}
    for a, b in itertools.combinations(P, 2):
        t = pd.crosstab(M[a], M[b]).reindex(index=[0, 1], columns=[0, 1], fill_value=0)
        p = mcnemar(t.values, exact=True).pvalue
        mc[f"{a} vs {b}"] = {"p_bonferroni": round(min(1.0, p * 6), 4)}
    out["mcnemar"] = mc
    out["by_category"] = {p: {c: round(M.loc[meta.category == c, p].mean() * 100, 1) for c in CATS} for p in P}
    out["by_language"] = {p: {l: round(M.loc[meta.language == l, p].mean() * 100, 1) for l in ["C#", "Java"]} for p in P}
    out["mean_global_by_category"] = v.groupby(["provider", "category"])["global"].mean().round(1).unstack().to_dict()
    sens = {}
    for d in [-10, -5, 0, 5, 10]:
        Md, _ = majority(d=d, tol_ident=5)
        sens[f"{d:+d}"] = {p: round(Md[p].mean() * 100, 1) for p in P}
    Mr, _ = majority(tol_ident=5, dif_hi=30)
    sens["different_0_30"] = {p: round(Mr[p].mean() * 100, 1) for p in P}
    out["band_sensitivity"] = sens
    full = v.dropna(subset=["funcional", "estructural", "lexica", "estilistica", "global"])
    diff = full["global"] - (0.4 * full.funcional + 0.3 * full.estructural + 0.2 * full.lexica + 0.1 * full.estilistica)
    out["formula_fidelity"] = {"n": int(len(full)), "within_5": round((diff.abs() <= 5).mean() * 100, 1),
                               "mean_diff": round(diff.mean(), 2)}
    f = full[full.category == "funcional"].copy()
    f["required_functional"] = (70 - 0.3 * f.estructural - 0.2 * f.lexica - 0.1 * f.estilistica) / 0.4
    out["functional_pairs"] = f.groupby("provider")[["required_functional", "funcional", "estructural"]].mean().round(1).to_dict()
    L = v.groupby(["case_id", "provider"]).latency_s.mean().unstack()[P]
    out["latency"] = {p: {"mean": round(L[p].mean(), 2), "sd": round(L[p].std(), 2),
                          "median": round(L[p].median(), 2), "ci": [round(x, 2) for x in bca(L[p], rng)],
                          "C#": round(L.loc[meta.language == "C#", p].mean(), 2),
                          "Java": round(L.loc[meta.language == "Java", p].mean(), 2)} for p in P}
    out["latency_shapiro_p"] = {p: float(stats.shapiro(L[p]).pvalue) for p in P}
    fr = stats.friedmanchisquare(*[L[p] for p in P])
    out["latency_friedman"] = {"chi2": round(fr.statistic, 2), "p": float(fr.pvalue), "W": round(fr.statistic / (n * (k - 1)), 3)}
    wl = {}
    for a, b in itertools.combinations(P, 2):
        w = stats.wilcoxon(L[a], L[b])
        wl[f"{a} vs {b}"] = {"p_bonferroni": float(min(1.0, w.pvalue * 6)), "hedges_g": hedges_paired(L[a] - L[b]),
                             "mean_diff_s": round((L[a] - L[b]).mean(), 2)}
    out["latency_wilcoxon"] = wl


def baselines(out):
    b = pd.read_csv(ROOT / "baselines_raw.csv")
    res = {}
    for (tool, mode), g in b.groupby(["tool", "mode"]):
        g = g.rename(columns={"similarity": "s"})
        ok = within(g, tol_ident=5, col="s")
        pos = g.category != "diferente"
        res[f"{tool}/{mode}"] = {
            "coincidence": round(ok.mean() * 100, 1),
            "sensitivity": round(ok[pos].mean() * 100, 1),
            "specificity": round(ok[~pos].mean() * 100, 1),
            "different_0_30": round(within(g, tol_ident=5, dif_hi=30, col="s").mean() * 100, 1),
            "by_category": {c: round(ok[g.category == c].mean() * 100, 1) for c in CATS},
            "mean_similarity": g.groupby("category").s.mean().round(1).to_dict(),
        }
    moss = b[b.tool == "moss"].rename(columns={"similarity": "s"})
    res["moss_identical_tolerance"] = {t: round(within(moss, tol_ident=t, col="s").mean() * 100, 1) for t in [0, 5, 10, 20, 25]}
    res["moss_unreported_functional"] = int((moss[moss.category == "funcional"].s == 0).sum())
    jp = b[b.tool == "jplag"]
    res["jplag_structural_exactly_100"] = int((jp[jp.category == "estructural"].similarity == 100).sum())
    out["baselines"] = res


def norm(s):
    return re.sub(r"\s+", "", str(s)).lower().replace("²", "^2").replace("³", "^3").replace("ⁿ", "^n")


def bigo(out):
    res = {}
    for name, pred, gt in [("canonical", "predicciones_api.csv", "ground_truth.csv"),
                           ("adversarial", "predicciones_api_adv.csv", "ground_truth_adversarial.csv")]:
        p = pd.read_csv(ROOT / "bigo" / pred)
        m = p.merge(pd.read_csv(ROOT / "bigo" / gt), on="filename", how="left")
        t = [norm(a) == norm(b) for a, b in zip(m.pred_time, m.worst_case_time)]
        s = [norm(a) == norm(b) for a, b in zip(m.pred_space, m.space_complexity)]
        cons = p.groupby("filename").agg(nt=("pred_time", "nunique"), ns=("pred_space", "nunique"))
        res[name] = {"responses": len(p), "programs": p.filename.nunique(), "model": sorted(p.model_snapshot.unique()),
                     "time_acc": round(np.mean(t) * 100, 1), "space_acc": round(np.mean(s) * 100, 1),
                     "replicas_agree": round(((cons.nt == 1) & (cons.ns == 1)).mean() * 100, 1)}
    p = pd.read_csv(ROOT / "bigo" / "predicciones_api.csv").merge(
        pd.read_csv(ROOT / "bigo" / "ground_truth_v1_original.csv"), on="filename")
    res["canonical_space_acc_original_ground_truth"] = round(
        np.mean([norm(a) == norm(b) for a, b in zip(p.pred_space, p.space_complexity)]) * 100, 1)
    out["bigo"] = res


def ground_truth(out):
    e = pd.read_csv(ROOT / "fiabilidad" / "categorias_evaluador2.csv")
    k = pd.read_csv(ROOT / "fiabilidad" / "clave_categorias_ref.csv")
    m = e.merge(k, on="case_id")
    out["ground_truth"] = {"n": len(m), "kappa": round(cohen_kappa_score(m.categoria_evaluador2, m.categoria_ref), 3),
                           "agreement": round((m.categoria_evaluador2 == m.categoria_ref).mean() * 100, 1)}


def validation(out, vdir):
    import pingouin as pg
    C = ["correccion", "especificidad", "explicacion", "utilidad"]
    vdir = Path(vdir)
    sheets = []
    for i in range(1, 8):
        d = pd.read_csv(vdir / "sheets" / f"norm_sheet_eval{i}.csv")
        d["rater"] = f"E{i}"
        sheets.append(d)
    h = pd.concat(sheets)
    h["score"] = h[C].mean(axis=1)
    icc = pg.intraclass_corr(h, targets="item_id", raters="rater", ratings="score").set_index("Type")
    key = pd.read_csv(vdir / "sheets" / "CLAVE_ANCLA_NO_ABRIR.csv")
    item = h.groupby("item_id").score.mean().reset_index().merge(key, on="item_id")
    kw = stats.kruskal(*[g.score for _, g in item.groupby("provider")])
    panel = pd.read_csv(vdir / "responses" / "panel_jueces.csv")
    panel = panel[panel.error.isna()].copy()
    panel["score"] = panel[C].mean(axis=1)
    panel["z"] = panel.groupby("judge_provider").score.transform(lambda s: (s - s.mean()) / s.std())
    zz = panel.groupby(["case_id", "author_provider"]).z.mean().unstack()
    fr = stats.friedmanchisquare(*[zz[c] for c in zz.columns])
    strata = {}
    for a, g in panel.groupby("author_provider"):
        t = pg.intraclass_corr(g, targets="case_id", raters="judge_provider", ratings="score").set_index("Type")
        strata[a] = [round(t.loc["ICC(A,1)", "ICC"], 2), round(t.loc["ICC(A,k)", "ICC"], 2)]
    pi = panel.groupby(["case_id", "author_provider"]).score.mean().reset_index().rename(columns={"author_provider": "provider"})
    ov = item.merge(pi, on=["case_id", "provider"], suffixes=("_human", "_panel"))
    w = pd.read_csv(vdir / "responses" / "responses_anonymised_wide.csv")
    sec = {s: [c for c in w.columns if c.startswith(s + "_")] for s in "ABC"}
    per = pd.DataFrame({s: w[c].mean(axis=1) for s, c in sec.items()})
    per["all"] = w[sum(sec.values(), [])].mean(axis=1)
    out["quality"] = {
        "human_ICC21": round(icc.loc["ICC(A,1)", "ICC"], 3), "human_ICC21_ci": list(icc.loc["ICC(A,1)", "CI95"]),
        "human_ICC2k": round(icc.loc["ICC(A,k)", "ICC"], 3), "human_ICC2k_ci": list(icc.loc["ICC(A,k)", "CI95"]),
        "rater_means": h.groupby("rater").score.mean().round(1).to_dict(),
        "human_by_model": item.groupby("provider").score.mean().round(1).to_dict(),
        "human_kruskal": {"H": round(kw.statistic, 2), "p": round(kw.pvalue, 3)},
        "panel_judgements": len(panel), "panel_ICC_by_author": strata,
        "panel_friedman": {"chi2": round(fr.statistic, 2), "p": float(fr.pvalue), "W": round(fr.statistic / (len(zz) * 3), 2)},
        "panel_by_model_z": panel.groupby("author_provider").z.mean().round(2).to_dict(),
        "panel_length_spearman": round(stats.spearmanr(panel.n_palabras_just, panel.score)[0], 3),
        "human_vs_panel_spearman": round(stats.spearmanr(ov.score_human, ov.score_panel)[0], 3),
        "panel_minus_human": round((ov.score_panel - ov.score_human).mean(), 1),
        "panel_by_model_on_shared": ov.groupby("provider").score_panel.mean().round(1).to_dict(),
    }
    out["expert_questionnaire"] = {"section_means": per.mean().round(2).to_dict(), "section_sd": per.std().round(2).to_dict(),
                                   "experience_years": w.anios_experiencia_num.describe()[["min", "50%", "max"]].to_dict()}



def extras(out, vdir=None):
    """Additional quantities quoted in the manuscript (v14)."""
    from sklearn.metrics import roc_auc_score
    r = pd.read_csv(ROOT / "resultados_replicas.csv")
    v = r[r["error"].isna()].copy()
    meta = v.drop_duplicates("case_id").set_index("case_id")
    cat = meta.category
    # band-free discrimination: median global score of the 3 replicas vs. detector similarity
    med = v.groupby(["case_id", "provider"])["global"].median().unstack()[P]
    b = pd.read_csv(ROOT / "baselines_raw.csv")
    b = b[b["mode"] == "cohorte"].pivot(index="case_id", columns="tool", values="similarity")
    S = med.join(b)
    order = cat.map({"diferente": 0, "estructural": 1, "funcional": 2, "identico": 3})

    def auc(s, a, z):
        m = cat.isin([a, z])
        return round(roc_auc_score((cat[m] == a).astype(int), s[m]), 3)

    out["rank_metrics"] = {t: {"spearman_with_category_order": round(stats.spearmanr(S[t], order)[0], 3),
                               "auc_functional_vs_different": auc(S[t], "funcional", "diferente"),
                               "auc_structural_vs_different": auc(S[t], "estructural", "diferente"),
                               "auc_functional_vs_structural": auc(S[t], "funcional", "estructural")}
                           for t in S.columns}
    j100 = cat.index[(cat == "estructural") & (b["jplag"].reindex(cat.index) == 100)]
    rest = cat.index[(cat == "estructural")].difference(j100)
    out["structural_jplag100"] = {"n": len(j100), "llm_mean_on_these": med.loc[j100].mean().round(1).to_dict(),
                                  "llm_mean_on_other_structural": med.loc[rest].mean().round(1).to_dict()}
    v["ok"] = within(v)
    M = (v.groupby(["case_id", "provider"]).ok.sum().unstack()[P] >= 2).astype(int)
    pos = cat[M.index] != "diferente"
    out["llm_band_sensitivity_specificity"] = {p: {"sensitivity": round(M.loc[pos, p].mean() * 100, 1),
                                                   "specificity": round(M.loc[~pos, p].mean() * 100, 1)} for p in P}
    a = v[v.provider == "anthropic"]
    out["claude_ignoring_unparsable"] = round(
        a.groupby("case_id").apply(lambda x: x.ok[x["global"].notna()].mean() >= 0.5).mean() * 100, 1)
    out["missing_dimension_scores"] = v[v["global"].notna()][["lexica", "estructural", "estilistica", "funcional", "sintactica"]].isna().sum().to_dict()
    g38 = v[v.case_id == "CASE_CODE_CS_038"]["global"]
    out["case_CS_038_global_range"] = [g38.min(), g38.max(), int(len(g38))]
    sess = v.drop_duplicates("case_id")
    out["pairs_by_run_session_and_language"] = {f"{k[0]} / {k[1]}": int(n) for k, n in sess.groupby(["run_ts", "language"]).size().items()}
    moss = pd.read_csv(ROOT / "baselines_raw.csv")
    mi = moss[(moss.tool == "moss") & (moss.category == "identico")].similarity
    out["moss_identical_min_median_max"] = [mi.min(), mi.median(), mi.max()]
    an = pd.read_csv(ROOT / "antlr_cs.csv")
    files = set(an.submission)
    md = pd.read_csv(ROOT / "metadata.csv")
    md = md[md.language == "C#"]
    stem = lambda p: Path(str(p)).stem
    aff = md[md.code_a_path.map(stem).isin(files) | md.code_b_path.map(stem).isin(files)]
    out["jplag_cs_parse_errors"] = {"submissions_with_errors": len(files), "errors": int(an.n_errores.sum()),
                                    "pairs_affected": int(len(aff)),
                                    "pairs_affected_by_category": aff.similarity_category.value_counts().to_dict()}
    if vdir:
        import pingouin as pg
        vdir = Path(vdir)
        C = ["correccion", "especificidad", "explicacion", "utilidad"]
        h = pd.concat([pd.read_csv(vdir / "sheets" / f"norm_sheet_eval{i}.csv").assign(rater=f"E{i}") for i in range(1, 8)])
        h["score"] = h[C].mean(axis=1)
        out["rater_score_ranges"] = {k: [round(g.score.min(), 1), round(g.score.max(), 1)] for k, g in h.groupby("rater")}
        key = pd.read_csv(vdir / "sheets" / "CLAVE_ANCLA_NO_ABRIR.csv")
        item = h.groupby("item_id").score.mean().reset_index().merge(key, on="item_id")
        pnl = pd.read_csv(vdir / "responses" / "panel_jueces.csv")
        pnl = pnl[pnl.error.isna()].copy()
        pnl["score"] = pnl[C].mean(axis=1)
        pi = pnl.groupby(["case_id", "author_provider"]).score.mean().reset_index().rename(columns={"author_provider": "provider"})
        ov = item.merge(pi, on=["case_id", "provider"], suffixes=("_human", "_panel"))
        rho = stats.spearmanr(ov.score_human, ov.score_panel)
        long = pd.concat([ov[["item_id", "score_human"]].rename(columns={"score_human": "y"}).assign(src="h"),
                          ov[["item_id", "score_panel"]].rename(columns={"score_panel": "y"}).assign(src="p")])
        icc = pg.intraclass_corr(long, targets="item_id", raters="src", ratings="y").set_index("Type")
        out["human_vs_panel"] = {"n": len(ov), "spearman": round(rho[0], 3), "p": round(rho[1], 4),
                                 "ICC21": round(icc.loc["ICC(A,1)", "ICC"], 3),
                                 "human_rank": item.groupby("provider").score.mean().sort_values(ascending=False).index.tolist(),
                                 "panel_rank_on_shared": ov.groupby("provider").score_panel.mean().sort_values(ascending=False).index.tolist()}
        w = pd.read_csv(vdir / "responses" / "responses_anonymised_wide.csv")
        sec = {s: [c for c in w.columns if c.startswith(s + "_")] for s in "ABC"}
        alpha = {}
        for s, cols in list(sec.items()) + [("all", sum(sec.values(), []))]:
            sd = w[cols].std(axis=1)
            alpha[s] = {"cronbach_alpha": round(pg.cronbach_alpha(w[cols])[0], 3),
                        "experts_with_constant_answers": int((sd == 0).sum())}
        out["expert_questionnaire_reliability"] = alpha
        out["expert_items_without_variance"] = [c.split("_")[1] for c in sum(sec.values(), []) if w[c].nunique() == 1]

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--validation", help="path to a local copy of SimilCode-Validation")
    ap.add_argument("--out", default="resultados_manuscrito.json")
    a = ap.parse_args()
    out = {}
    llm(out)
    baselines(out)
    bigo(out)
    ground_truth(out)
    if a.validation:
        validation(out, a.validation)
    extras(out, a.validation)
    Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
