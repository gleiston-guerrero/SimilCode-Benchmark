#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analisis_robustez.py — Robustez de la puntuacion de derivacion y linea base de
deteccion de clones basada en representaciones de codigo (sin llamadas a API de LLM).

1. Sensibilidad de la ponderacion. La puntuacion de derivacion usa los pesos del
   prompt sin la dimension funcional: (0.30 S + 0.20 L + 0.10 T) / 0.60. Se definio
   despues de analizar la similitud global, de modo que conviene comprobar que la
   conclusion no depende de esos pesos. Se calcula el AUC copia / solucion
   independiente para variantes sin parametros ajustados a los datos:
     derivacion   pesos del prompt sin la funcional (definicion del manuscrito)
     igual3       media simple de estructural, lexica y estilistica
     igual4       media simple de estructural, lexica, estilistica y sintactica
     sin_estilo   (0.30 S + 0.20 L) / 0.50
     max_SL       maximo de estructural y lexica
   y se informa el rango de AUC entre variantes por LLM y escenario.

2. Linea base con embeddings de codigo. Similitud coseno entre las
   representaciones de los dos programas de cada par, con dos modelos de codigo
   preentrenados que la literatura de deteccion de clones usa como referencia:
   UniXcoder (microsoft/unixcoder-base) y CodeBERT (microsoft/codebert-base).
   Representacion = media de los estados de la ultima capa; UniXcoder recibe el
   prefijo <encoder-only> de su uso oficial. Los programas mas largos que la
   ventana del modelo (512 posiciones) se dividen en ventanas y se promedian,
   ponderadas por su longitud. Sin ajuste fino: es una linea base de similitud
   semantica, no un detector entrenado.

Mismos escenarios, misma unidad de remuestreo (30 programas de referencia),
misma semilla y mismo numero de remuestreos que analisis_dimensiones.py.

Entradas: metadata.csv, tipos_clon.csv, resultados_replicas.csv, baselines_raw.csv,
          metadata_ia.csv, copias_ia/resultados_replicas_ia.csv, copias_ia/baselines_raw_ia.csv,
          y los archivos de codigo en csharp/ y java/.
Salidas:  embeddings_similitud.csv (cache de similitudes por par y modelo),
          resultados_robustez.json y un resumen en pantalla.

Uso (desde la carpeta SimilCode-Benchmark):
  pip install torch --index-url https://download.pytorch.org/whl/cpu
  pip install transformers
  python analisis_robustez.py
"""
import json
import os

import numpy as np
import pandas as pd

from analisis_dimensiones import (B, LLMS, ROOT, SEED, TOOLS, auc, prepare)

EMB_MODELS = {"unixcoder": "microsoft/unixcoder-base", "codebert": "microsoft/codebert-base"}
VARIANTS = {
    "derivacion": lambda d: (0.30 * d.estructural + 0.20 * d.lexica + 0.10 * d.estilistica) / 0.60,
    "igual3": lambda d: (d.estructural + d.lexica + d.estilistica) / 3,
    "igual4": lambda d: (d.estructural + d.lexica + d.estilistica + d.sintactica) / 4,
    "sin_estilo": lambda d: (0.30 * d.estructural + 0.20 * d.lexica) / 0.50,
    "max_SL": lambda d: np.maximum(d.estructural, d.lexica),
}
SCENARIOS = ("conventional_T2T3", "ia_api", "ia_intensa", "ia_ligera")


# ---------------------------------------------------------------- embeddings
def read_code(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8-sig", errors="replace") as fh:
        return fh.read()


def embed_all(paths, model_name):
    import torch
    from transformers import AutoModel, AutoTokenizer
    torch.manual_seed(0)
    tok = AutoTokenizer.from_pretrained(model_name)
    mod = AutoModel.from_pretrained(model_name).eval()
    out = {}
    with torch.no_grad():
        for p in paths:
            ids = tok(read_code(p), add_special_tokens=False)["input_ids"]
            vecs, weights = [], []
            # UniXcoder en modo codificador: [CLS] <encoder-only> [SEP] codigo [SEP] (uso oficial)
            head = ([tok.cls_token_id, tok.convert_tokens_to_ids("<encoder-only>"), tok.sep_token_id]
                    if "unixcoder" in model_name else [tok.cls_token_id])
            win = 511 - len(head)
            for s in range(0, max(len(ids), 1), win):
                chunk = head + ids[s:s + win] + [tok.sep_token_id]
                h = mod(input_ids=torch.tensor([chunk])).last_hidden_state[0]
                vecs.append(h.mean(0).numpy()); weights.append(len(chunk))
            out[p] = np.average(np.vstack(vecs), axis=0, weights=weights)
    return out


def embedding_similarities():
    cache = os.path.join(ROOT, "embeddings_similitud.csv")
    if os.path.exists(cache):
        return pd.read_csv(cache).set_index("case_id")
    pairs = pd.concat([pd.read_csv(os.path.join(ROOT, f), encoding="utf-8-sig")
                       for f in ("metadata.csv", "metadata_ia.csv")])
    paths = sorted(set(pairs.code_a_path) | set(pairs.code_b_path))
    sim = pd.DataFrame({"case_id": pairs.case_id.values})
    for short, name in EMB_MODELS.items():
        E = embed_all(paths, name)
        cos = [float(np.dot(E[a], E[b]) / (np.linalg.norm(E[a]) * np.linalg.norm(E[b])))
               for a, b in zip(pairs.code_a_path, pairs.code_b_path)]
        sim[short] = np.round(100 * np.array(cos), 3)
    sim.to_csv(cache, index=False)
    return sim.set_index("case_id")


# ---------------------------------------------------------------- bootstrap
def boot_ci(X, cols, pos, neg):
    rng = np.random.default_rng(SEED)
    keys = sorted(X.grp.unique())
    idx_by = {k: np.where(X.grp.values == k)[0] for k in keys}
    pos, neg = pos.values, neg.values
    draws = {c: [] for c in cols}
    for _ in range(B):
        sel = np.concatenate([idx_by[keys[i]] for i in rng.integers(0, len(keys), len(keys))])
        p, n = sel[pos[sel]], sel[neg[sel]]
        if len(p) == 0 or len(n) == 0:
            continue
        for c in cols:
            draws[c].append(auc(X[c].values[p], X[c].values[n]))
    return {c: [round(float(v), 2) for v in np.nanpercentile(draws[c], [2.5, 97.5])] for c in cols}


def evaluate(X, cols, pos, neg, with_ci=True):
    ci = boot_ci(X, cols, pos, neg) if with_ci else {}
    return {c: {"auc": round(auc(X.loc[pos, c], X.loc[neg, c]), 2), **({"ci95_cluster": ci[c]} if with_ci else {})}
            for c in cols}


# ---------------------------------------------------------------- scenarios
def llm_scores(path):
    raw = pd.read_csv(path)
    raw = raw[raw["global"].notna()].copy()
    if "error" in raw.columns:
        raw = raw[raw["error"].isna()]
    for c in ("lexica", "estructural", "estilistica", "sintactica", "funcional", "global"):
        raw[c] = pd.to_numeric(raw[c], errors="coerce")
    for v, f in VARIANTS.items():
        raw[v] = f(raw)
    return raw.groupby(["case_id", "provider"])[list(VARIANTS)].median()


def scenario_frames():
    """Devuelve {escenario: (base, etiqueta_pos, etiqueta_neg)} con columna grp."""
    ct = pd.read_csv(os.path.join(ROOT, "tipos_clon.csv")).set_index("case_id")
    ct["grp"] = ct.language + "_" + ct.reference_group.astype(str)
    ct = ct[ct.clone_type.isin(["type2", "type3", "type4"])]
    ct["pos"] = ct.clone_type.isin(["type2", "type3"])
    meta = pd.read_csv(os.path.join(ROOT, "metadata_ia.csv"), encoding="utf-8-sig").set_index("case_id")
    meta["grp"] = meta.language + "_" + meta.reference_group.astype(str)
    cat = meta.similarity_category.str.lower()
    frames = {"conventional_T2T3": ct[["grp", "pos"]]}
    for s in ("ia_api", "ia_intensa", "ia_ligera"):
        m = meta[cat.isin([s, "functional"])].copy()
        m["pos"] = cat[m.index] == s
        frames[s] = m[["grp", "pos"]]
    return frames


def main():
    frames = scenario_frames()
    L1 = llm_scores(os.path.join(ROOT, "resultados_replicas.csv"))
    L2 = llm_scores(os.path.join(ROOT, "copias_ia", "resultados_replicas_ia.csv"))
    b1 = pd.read_csv(os.path.join(ROOT, "baselines_raw.csv"))
    b2 = pd.read_csv(os.path.join(ROOT, "copias_ia", "baselines_raw_ia.csv"))
    tools = pd.concat([b1, b2])
    tools = tools[tools["mode"] == "cohorte"].pivot_table(index="case_id", columns="tool", values="similarity")
    emb = embedding_similarities()

    out = {"variants": {"derivacion": "(0.30 S + 0.20 L + 0.10 T) / 0.60", "igual3": "(S + L + T) / 3",
                        "igual4": "(S + L + T + Sy) / 4", "sin_estilo": "(0.30 S + 0.20 L) / 0.50",
                        "max_SL": "max(S, L)"},
           "embedding_models": EMB_MODELS, "sensitivity": {}, "detectors": {}}
    for s, base in frames.items():
        L = L1 if s == "conventional_T2T3" else L2
        out["sensitivity"][s] = {}
        for p in LLMS:
            X = base.join(L.xs(p, level="provider"))
            r = evaluate(X, list(VARIANTS), X.pos, ~X.pos, with_ci=True)
            a = [r[v]["auc"] for v in VARIANTS]
            r["range"] = [min(a), max(a)]
            out["sensitivity"][s][p] = r
        X = base.join(tools).join(emb)
        out["detectors"][s] = evaluate(X, TOOLS + list(EMB_MODELS), X.pos, ~X.pos)
        out["detectors"][s]["n_copies"] = int(X.pos.sum())
        out["detectors"][s]["n_independent"] = int((~X.pos).sum())

    with open(os.path.join(ROOT, "resultados_robustez.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)

    for s in SCENARIOS:
        d = out["detectors"][s]
        print(f"\n== {s} (copias {d['n_copies']}, independientes {d['n_independent']})")
        for p in LLMS:
            r = out["sensitivity"][s][p]
            print(f"{p:10s} " + " ".join(f"{v}={r[v]['auc']:.2f}" for v in VARIANTS) + f" | rango {r['range']}")
        print("detectores " + " ".join(f"{t}={d[t]['auc']:.2f}{d[t]['ci95_cluster']}" for t in TOOLS + list(EMB_MODELS)))
    print("\nDetalle completo: resultados_robustez.json")


if __name__ == "__main__":
    main()
