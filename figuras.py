$env:#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
figuras.py
==========
Regenera TODAS las figuras del benchmark a partir del CSV de resultados nuevo
(M7), con TODO el texto en INGLES (M8), directamente desde los datos para que
coincidan con las tablas (evita la inconsistencia detectada en la Figura 5).

Entrada : resultados_replicas.csv (formato long de benchmark_replicas.py).
Salida  : PNG a 300 dpi en --outdir. Requiere matplotlib.

Uso:
  python figuras.py --in resultados_replicas.csv --outdir figuras
"""

import argparse
import csv
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Etiquetas de modelo legibles en ingles (ajusta si cambias de version).
MODEL_LABELS = {
    "deepseek": "DeepSeek", "gemini": "Gemini",
    "openai": "GPT", "anthropic": "Claude",
}
CATEGORY_LABELS = {
    "identico": "Identical", "funcional": "Functional",
    "estructural": "Structural", "diferente": "Different",
}
CAT_ORDER = ["identico", "funcional", "estructural", "diferente"]
PALETTE = ["#2f6db0", "#e08a1e", "#3a9d6a", "#b0413e", "#7a5aa0"]


def load(path):
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if not r.get("error") and r.get("global") not in ("", None):
                rows.append(r)
    return rows


def _coincidence(rows, key=lambda r: True):
    """% de casos (voto mayoritario de replicas) dentro del rango esperado,
    para el subconjunto que cumple key."""
    by_pc = defaultdict(list)
    for r in rows:
        if key(r):
            by_pc[(r["provider"], r["case_id"])].append(r)
    prov = defaultdict(lambda: [0, 0])
    for (p, _c), reps in by_pc.items():
        votes = [int(x["within_expected"]) for x in reps if x["within_expected"] != ""]
        if not votes:
            continue
        prov[p][0] += 1 if sum(votes) * 2 >= len(votes) else 0
        prov[p][1] += 1
    return {p: 100.0 * c / n for p, (c, n) in prov.items() if n}


def _providers(rows):
    seen = []
    for r in rows:
        if r["provider"] not in seen:
            seen.append(r["provider"])
    return seen


def _label(p):
    return MODEL_LABELS.get(p, p)


def _save(fig, outdir, name):
    path = os.path.join(outdir, name)
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def fig_coincidence(rows, outdir):
    provs = _providers(rows)
    vals = _coincidence(rows)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    bars = ax.bar([_label(p) for p in provs], [vals.get(p, 0) for p in provs],
                  color=PALETTE[:len(provs)])
    ax.set_ylabel("Agreement with expected range (%)")
    ax.set_title("Detection agreement by model")
    ax.set_ylim(0, 100)
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1,
                f"{b.get_height():.1f}", ha="center", va="bottom", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    return _save(fig, outdir, "fig_coincidence_by_model.png")


def fig_by_language(rows, outdir):
    provs = _providers(rows)
    langs = sorted({r["language"] for r in rows if r["language"]})
    if len(langs) < 2:
        return None
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    width = 0.8 / len(langs)
    x = range(len(provs))
    for li, lang in enumerate(langs):
        vals = _coincidence(rows, key=lambda r, L=lang: r["language"] == L)
        ax.bar([xi + li * width for xi in x], [vals.get(p, 0) for p in provs],
               width, label=lang, color=PALETTE[li])
    ax.set_xticks([xi + width * (len(langs) - 1) / 2 for xi in x])
    ax.set_xticklabels([_label(p) for p in provs])
    ax.set_ylabel("Agreement with expected range (%)")
    ax.set_title("Detection agreement by model and language")
    ax.set_ylim(0, 100); ax.legend(title="Language"); ax.grid(axis="y", alpha=0.3)
    return _save(fig, outdir, "fig_coincidence_by_language.png")


def fig_by_category(rows, outdir):
    provs = _providers(rows)
    cats = [c for c in CAT_ORDER if any(r["category"] == c for r in rows)]
    fig, ax = plt.subplots(figsize=(8, 4.4))
    width = 0.8 / len(provs)
    x = range(len(cats))
    for pi, p in enumerate(provs):
        ys = []
        for c in cats:
            vals = _coincidence(rows, key=lambda r, P=p, C=c: r["provider"] == P and r["category"] == C)
            ys.append(vals.get(p, 0))
        ax.bar([xi + pi * width for xi in x], ys, width, label=_label(p),
               color=PALETTE[pi])
    ax.set_xticks([xi + width * (len(provs) - 1) / 2 for xi in x])
    ax.set_xticklabels([CATEGORY_LABELS.get(c, c) for c in cats])
    ax.set_ylabel("Agreement with expected range (%)")
    ax.set_title("Agreement by similarity category")
    ax.set_ylim(0, 100); ax.legend(title="Model"); ax.grid(axis="y", alpha=0.3)
    return _save(fig, outdir, "fig_agreement_by_category.png")


def fig_latency(rows, outdir):
    provs = _providers(rows)
    lat = defaultdict(list)
    for r in rows:
        if r.get("latency_s") not in ("", None):
            lat[r["provider"]].append(float(r["latency_s"]))
    if not any(lat.values()):
        return None
    fig, ax = plt.subplots(figsize=(7, 4.2))
    data = [lat.get(p, [0]) for p in provs]
    bp = ax.boxplot(data, patch_artist=True, showfliers=False)
    ax.set_xticks(range(1, len(provs) + 1))
    ax.set_xticklabels([_label(p) for p in provs])
    for patch, c in zip(bp["boxes"], PALETTE):
        patch.set_facecolor(c); patch.set_alpha(0.7)
    ax.set_ylabel("Response time (s)")
    ax.set_title("Response time by model")
    ax.grid(axis="y", alpha=0.3)
    return _save(fig, outdir, "fig_response_time_by_model.png")


def fig_stability(rows, outdir):
    """Estabilidad intra-modelo: dispersion media del GLOBAL entre replicas."""
    provs = _providers(rows)
    by_pc = defaultdict(list)
    for r in rows:
        by_pc[(r["provider"], r["case_id"])].append(int(r["global"]))
    span = defaultdict(list)
    for (p, _c), gs in by_pc.items():
        span[p].append(max(gs) - min(gs))
    fig, ax = plt.subplots(figsize=(7, 4.2))
    means = [sum(span[p]) / len(span[p]) if span[p] else 0 for p in provs]
    bars = ax.bar([_label(p) for p in provs], means, color=PALETTE[:len(provs)])
    ax.set_ylabel("Mean GLOBAL score range across replicas")
    ax.set_title("Intra-model stability (lower = more deterministic)")
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.1,
                f"{b.get_height():.1f}", ha="center", va="bottom", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    return _save(fig, outdir, "fig_intramodel_stability.png")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="infile", required=True)
    ap.add_argument("--outdir", default="figuras")
    args = ap.parse_args()
    rows = load(args.infile)
    if not rows:
        raise SystemExit("No hay filas validas en el CSV de resultados.")
    os.makedirs(args.outdir, exist_ok=True)
    made = [fig_coincidence(rows, args.outdir), fig_by_language(rows, args.outdir),
            fig_by_category(rows, args.outdir), fig_latency(rows, args.outdir),
            fig_stability(rows, args.outdir)]
    for m in made:
        if m:
            print("  generada:", m)
    print(f"\nListo. Figuras (texto en ingles, 300 dpi) en: {args.outdir}")


if __name__ == "__main__":
    main()python benchmark_replicas.py list-models
