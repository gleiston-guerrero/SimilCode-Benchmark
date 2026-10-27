#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analisis_tipos_clon.py — Revision M1, paso 2: reclasifica los pares del
benchmark segun los tipos de clon de Roy, Cordy y Koschke (2009) y mide si
cada sistema separa las COPIAS (clones tipo 1-3) de las SOLUCIONES
INDEPENDIENTES del mismo ejercicio (clones tipo 4), que es la decision real
del docente al cribar plagio.

Criterio de clasificacion, independiente de los sistemas evaluados:
  tipo 1  par identico (categoria 'identical')
  tipo 2  secuencias de tokens identicas tras normalizar identificadores y
          literales y eliminar comentarios
  tipo 3  resto de pares 'structural' (copias con sentencias agregadas,
          eliminadas o modificadas)
  tipo 4  pares 'functional' (implementacion independiente, mismo comportamiento)
  sin relacion  pares 'different'
La regla es determinista y no usa ninguno de los sistemas evaluados.

Uso (desde la carpeta SimilCode-Benchmark):
  python analisis_tipos_clon.py
Salidas: tipos_clon.csv y resultados_tipos_clon.json
"""
import difflib
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy.stats import rankdata

SEED = 20260730
KW=set("""abstract as base bool break byte case catch char checked class const continue decimal default delegate do double else enum event explicit extern false finally fixed float for foreach goto if implicit in int interface internal is lock long namespace new null object operator out override params private protected public readonly ref return sbyte sealed short sizeof stackalloc static string struct switch this throw true try typeof uint ulong unchecked unsafe ushort using virtual void volatile while var get set value async await
boolean extends final implements import instanceof native package strictfp super synchronized throws transient var record yield""".split())
TOK=re.compile(r'''@?"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])'|\d+(?:\.\d+)?[fFdDmMlL]?|[A-Za-z_][A-Za-z0-9_]*|==|!=|<=|>=|&&|\|\||\+\+|--|=>|->|\+=|-=|\*=|/=|::|[{}()\[\];,.<>=+\-*/%!?:&|^~$]''')
def norm(src):
    src=re.sub(r'/\*.*?\*/','',src,flags=re.S); src=re.sub(r'//[^\n]*','',src)
    src=re.sub(r'\$"(?:\\.|[^"\\])*"','STR',src)
    out=[]
    for t in TOK.findall(src):
        if t[0] in '"\'@' : out.append('LIT')
        elif t[0].isdigit(): out.append('LIT')
        elif re.match(r'[A-Za-z_]',t): out.append(t if t in KW else 'ID')
        else: out.append(t)
    return out
def classify(a,b):
    ta,tb=norm(a),norm(b)
    if ta==tb: return 'type2',1.0
    r=difflib.SequenceMatcher(None,ta,tb,autojunk=False).ratio()
    return 'type3',r




def auc(pos, neg):
    pos = np.asarray(pos, float); neg = np.asarray(neg, float)
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    r = rankdata(np.concatenate([pos, neg]))
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def cluster_ci(gp, gn, B=5000):
    rng = np.random.default_rng(SEED)
    keys = sorted(set(gp) | set(gn))
    P = [np.asarray(gp.get(k, []), float) for k in keys]
    N = [np.asarray(gn.get(k, []), float) for k in keys]
    vals = []
    for _ in range(B):
        idx = rng.integers(0, len(keys), len(keys))
        p = np.concatenate([P[i] for i in idx]); n = np.concatenate([N[i] for i in idx])
        if len(p) and len(n):
            vals.append(auc(p, n))
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return [round(float(lo), 2), round(float(hi), 2)]



def analyze(root, ct, outp):
    d = pd.read_csv(root + "/resultados_replicas.csv"); d = d[d["global"].notna()]
    L = d.groupby(["case_id", "provider"])["global"].median().unstack("provider")
    b = pd.read_csv(root + "/baselines_raw.csv")
    b = b[b["mode"] == "cohorte"].pivot_table(index="case_id", columns="tool", values="similarity")
    X = ct.set_index("case_id").join(L).join(b)
    X["grp"] = X.language + "_" + X.reference_group.astype(str)
    systems = ["openai", "deepseek", "gemini", "anthropic", "moss", "jplag", "dolos"]
    comps = {"copies_T2T3_vs_independent_T4": (["type2", "type3"], ["type4"]),
             "copies_T1T2T3_vs_independent_T4": (["type1", "type2", "type3"], ["type4"]),
             "independent_T4_vs_unrelated": (["type4"], ["unrelated"])}

    def groups(types, s):
        sub = X[X.clone_type.isin(types)]
        return {g: v[s].dropna().values for g, v in sub.groupby("grp")}

    res = {"n_pairs": {k: int(v) for k, v in X.clone_type.value_counts().items()},
           "n_reference_programs": int(X.grp.nunique()), "auc": {}, "flag_rates": {}, "median_score": {}}
    for s in systems:
        res["auc"][s] = {}
        for name, (pos, neg) in comps.items():
            P = X[X.clone_type.isin(pos)][s].dropna(); N = X[X.clone_type.isin(neg)][s].dropna()
            res["auc"][s][name] = {"auc": round(auc(P, N), 2), "ci95_cluster": cluster_ci(groups(pos, s), groups(neg, s))}
        res["flag_rates"][s] = {}
        for t in (50, 70, 80, 90):
            res["flag_rates"][s][str(t)] = {
                "copies_T2T3_flagged_pct": round(100 * (X[X.clone_type.isin(["type2", "type3"])][s] >= t).mean(), 1),
                "independent_T4_flagged_pct": round(100 * (X[X.clone_type == "type4"][s] >= t).mean(), 1),
                "unrelated_flagged_pct": round(100 * (X[X.clone_type == "unrelated"][s] >= t).mean(), 1)}
        res["median_score"][s] = {k: float(X[X.clone_type == k][s].median())
                                  for k in ["type1", "type2", "type3", "type4", "unrelated"]}
    res["normalized_token_similarity"] = {
        k: {"median": round(float(v.median()), 2), "min": round(float(v.min()), 2), "max": round(float(v.max()), 2)}
        for k, v in ct.groupby("clone_type").normalized_token_similarity}
    json.dump(res, open(outp, "w"), indent=1)
    for s in systems:
        a = res["auc"][s]["copies_T2T3_vs_independent_T4"]; f = res["flag_rates"][s]
        print(f"{s:10s} AUC={a['auc']:.2f} {a['ci95_cluster']} | thr70 copias {f['70']['copies_T2T3_flagged_pct']} indep {f['70']['independent_T4_flagged_pct']} | thr80 copias {f['80']['copies_T2T3_flagged_pct']} indep {f['80']['independent_T4_flagged_pct']} | med T3 {res['median_score'][s]['type3']} T4 {res['median_score'][s]['type4']}")
    print(res["n_pairs"], res["normalized_token_similarity"])




def classify_all(root):
    m = pd.read_csv(os.path.join(root, "metadata.csv"), encoding="utf-8-sig")
    rows = []
    for _, x in m.iterrows():
        a = open(os.path.join(root, x.code_a_path), encoding="utf-8-sig").read()
        b = open(os.path.join(root, x.code_b_path), encoding="utf-8-sig").read()
        t, r = classify(a, b)
        if x.similarity_category == "identical":
            t = "type1"
        elif x.similarity_category != "structural":
            t = {"functional": "type4", "different": "unrelated"}[x.similarity_category]
        rows.append((x.case_id, x.language, x.reference_group, x.similarity_category, t, round(r, 3),
                     len(norm(a)), len(norm(b))))
    return pd.DataFrame(rows, columns=["case_id", "language", "reference_group", "category", "clone_type",
                                       "normalized_token_similarity", "tokens_a", "tokens_b"])


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    ct = classify_all(root)
    ct.to_csv(os.path.join(root, "tipos_clon.csv"), index=False)
    analyze(root, ct, os.path.join(root, "resultados_tipos_clon.json"))
