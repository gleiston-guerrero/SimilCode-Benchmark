#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fiabilidad.py
=============
Instrumentos de fiabilidad para atender las preocupaciones del informe:

  M6 (alpha)   : alfa de Cronbach del cuestionario de validacion con expertos.
  M2 (kappa)   : kappa de Cohen entre dos evaluadores que reclasifican las 120
                 PAREJAS (casos) en categorias (identico/funcional/estructural/
                 diferente), a ciegas de la etiqueta original.
  M4 (icc)     : ICC(2,1) entre dos evaluadores ciegos que puntuan la calidad de
                 las justificaciones en escala continua 0-100.
  make-sheets  : genera las hojas ciegas de calificacion para M2 y M4.

Solo biblioteca estandar. Ejemplos:
  python fiabilidad.py alpha --in respuestas_encuesta_similcode_wide.csv --id-col participant
  python fiabilidad.py make-sheets --metadata metadata.csv --results resultados_replicas.csv --outdir hojas --sample 40
  python fiabilidad.py kappa --in hojas/categorias_evaluador2.csv --col1 categoria_ref --col2 categoria_evaluador2
  python fiabilidad.py icc   --in hojas/calidad_consolidada.csv --col1 calidad_eval1 --col2 calidad_eval2
"""

import argparse
import csv
import os
import sys
from collections import defaultdict


# ----------------------------------------------------------------------------
def _read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def _to_float(v):
    try:
        return float(str(v).strip())
    except (ValueError, AttributeError):
        return None


def _mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def _var(xs, ddof=1):
    if len(xs) <= ddof:
        return float("nan")
    m = _mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - ddof)


# ----------------------------------------------------------------------------
# M6 - Alfa de Cronbach
# ----------------------------------------------------------------------------
def cronbach_alpha(matrix):
    """matrix: lista de filas (participantes); cada fila lista de items (float).
    alpha = k/(k-1) * (1 - sum(var_item)/var_total)."""
    n = len(matrix)
    k = len(matrix[0])
    item_vars = []
    for j in range(k):
        col = [matrix[i][j] for i in range(n)]
        item_vars.append(_var(col, ddof=1))
    totals = [sum(row) for row in matrix]
    total_var = _var(totals, ddof=1)
    if total_var == 0 or total_var != total_var:
        return float("nan")
    return (k / (k - 1)) * (1 - sum(item_vars) / total_var)


def cmd_alpha(args):
    rows = _read_csv(args.infile)
    if not rows:
        sys.exit("CSV vacio.")
    cols = list(rows[0].keys())
    id_cols = {c for c in cols if c == args.id_col} if args.id_col else set()
    # Items = columnas numericas (excluye la de id).
    item_cols = []
    for c in cols:
        if c in id_cols:
            continue
        vals = [_to_float(r.get(c)) for r in rows]
        if all(v is not None for v in vals):
            item_cols.append(c)
    if len(item_cols) < 2:
        sys.exit("No se detectaron >=2 columnas de items numericas. "
                 "Usa --id-col para excluir la columna identificadora.")
    matrix = [[_to_float(r[c]) for c in item_cols] for r in rows]

    print(f"Participantes: {len(matrix)} | Items detectados: {len(item_cols)}")
    a_total = cronbach_alpha(matrix)
    print(f"\nAlfa de Cronbach (total, {len(item_cols)} items): {a_total:.3f}")

    # Subescalas opcionales: --groups \"1-7,8-13,14-18\" (indices 1-based sobre item_cols)
    if args.groups:
        for grp in args.groups.split(","):
            lo, hi = grp.split("-")
            idx = list(range(int(lo) - 1, int(hi)))
            sub = [[row[j] for j in idx] for row in matrix]
            print(f"  Subescala items {grp}: alpha = {cronbach_alpha(sub):.3f}")
    print("\nInterpretacion orientativa: >=0.70 aceptable, >=0.80 bueno, "
          ">=0.90 excelente (Nunnally). Con n pequeno, reporta el IC si puedes.")


# ----------------------------------------------------------------------------
# M2 - Kappa de Cohen
# ----------------------------------------------------------------------------
def cohen_kappa(pairs):
    """pairs: lista de (etiqueta_a, etiqueta_b)."""
    n = len(pairs)
    cats = sorted({a for a, _ in pairs} | {b for _, b in pairs})
    idx = {c: i for i, c in enumerate(cats)}
    obs = sum(1 for a, b in pairs if a == b) / n
    ra = defaultdict(int); rb = defaultdict(int)
    for a, b in pairs:
        ra[a] += 1; rb[b] += 1
    exp = sum((ra[c] / n) * (rb[c] / n) for c in cats)
    kappa = (obs - exp) / (1 - exp) if (1 - exp) else float("nan")
    return kappa, obs, cats


def cmd_kappa(args):
    rows = _read_csv(args.infile)
    pairs = [( _strip(r[args.col1]), _strip(r[args.col2]) )
             for r in rows if r.get(args.col1) and r.get(args.col2)]
    if not pairs:
        sys.exit("No hay filas con ambas columnas de categoria.")
    kappa, obs, cats = cohen_kappa(pairs)
    print(f"Parejas evaluadas: {len(pairs)} | Categorias: {cats}")
    print(f"Acuerdo observado: {obs*100:.1f}%")
    print(f"Kappa de Cohen: {kappa:.3f}")
    print("\nLandis & Koch: <0 pobre, 0-0.20 leve, 0.21-0.40 aceptable, "
          "0.41-0.60 moderado, 0.61-0.80 sustancial, 0.81-1.0 casi perfecto.")


def _strip(s):
    trans = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuaeiouu")
    return str(s).strip().lower().translate(trans)


# ----------------------------------------------------------------------------
# M4 - ICC(2,1) dos evaluadores, escala continua
# ----------------------------------------------------------------------------
def icc_2_1(rater1, rater2):
    """ICC(2,1) two-way random, absolute agreement, single measures.
    rater1, rater2: listas alineadas por sujeto."""
    n = len(rater1)
    k = 2
    rows = [[rater1[i], rater2[i]] for i in range(n)]
    grand = _mean(rater1 + rater2)
    row_means = [ _mean(r) for r in rows ]
    col_means = [ _mean(rater1), _mean(rater2) ]
    # Sumas de cuadrados
    ss_total = sum((rows[i][j] - grand) ** 2 for i in range(n) for j in range(k))
    ss_row = k * sum((rm - grand) ** 2 for rm in row_means)
    ss_col = n * sum((cm - grand) ** 2 for cm in col_means)
    ss_err = ss_total - ss_row - ss_col
    df_row = n - 1
    df_col = k - 1
    df_err = (n - 1) * (k - 1)
    msr = ss_row / df_row if df_row else float("nan")
    msc = ss_col / df_col if df_col else float("nan")
    mse = ss_err / df_err if df_err else float("nan")
    denom = msr + (k - 1) * mse + (k / n) * (msc - mse)
    icc = (msr - mse) / denom if denom else float("nan")
    return icc, msr, msc, mse


def _pearson(x, y):
    n = len(x); mx = _mean(x); my = _mean(y)
    num = sum((x[i]-mx)*(y[i]-my) for i in range(n))
    den = (sum((v-mx)**2 for v in x) * sum((v-my)**2 for v in y)) ** 0.5
    return num/den if den else float("nan")


def cmd_icc(args):
    rows = _read_csv(args.infile)
    x, y = [], []
    for r in rows:
        a, b = _to_float(r.get(args.col1)), _to_float(r.get(args.col2))
        if a is not None and b is not None:
            x.append(a); y.append(b)
    if len(x) < 3:
        sys.exit("Se requieren >=3 sujetos con ambas puntuaciones.")
    icc, msr, msc, mse = icc_2_1(x, y)
    print(f"Sujetos (justificaciones) evaluados por ambos: {len(x)}")
    print(f"ICC(2,1) acuerdo absoluto: {icc:.3f}")
    print(f"Correlacion de Pearson r: {_pearson(x, y):.3f}")
    print(f"Diferencia media absoluta: {_mean([abs(x[i]-y[i]) for i in range(len(x))]):.2f} (0-100)")
    print("\nCicchetti: <0.40 pobre, 0.40-0.59 aceptable, 0.60-0.74 bueno, "
          ">=0.75 excelente.")


# ----------------------------------------------------------------------------
# make-sheets : hojas ciegas para M2 y M4
# ----------------------------------------------------------------------------
def _deterministic_order(keys, seed):
    """Permutacion reproducible sin depender de random global."""
    return sorted(keys, key=lambda s: (hash((seed, s)) & 0xffffffff))


def cmd_make_sheets(args):
    os.makedirs(args.outdir, exist_ok=True)

    # ---- M2: hoja de reclasificacion de categorias (120 parejas) ----
    if args.metadata:
        meta = _read_csv(args.metadata)
        order = _deterministic_order([r["case_id"] for r in meta], args.seed)
        by_id = {r["case_id"]: r for r in meta}
        out2 = os.path.join(args.outdir, "categorias_evaluador2.csv")
        with open(out2, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["orden", "case_id", "language", "code_a_path", "code_b_path",
                        "categoria_evaluador2"])
            for i, cid in enumerate(order, 1):
                r = by_id[cid]
                w.writerow([i, cid, r.get("language", ""),
                            r.get("code_a_path", ""), r.get("code_b_path", ""), ""])
        # Clave con la categoria original (la conserva el PI; NO se da al evaluador).
        key2 = os.path.join(args.outdir, "clave_categorias_ref.csv")
        with open(key2, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh); w.writerow(["case_id", "categoria_ref"])
            for cid in order:
                w.writerow([cid, by_id[cid].get("similarity_category", "")])
        print(f"M2: {out2}  (columna 'categoria_evaluador2' en blanco, orden barajado)")
        print(f"M2: {key2}  (clave con la categoria original; NO entregar al evaluador)")

    # ---- M4: hoja de calidad 0-100, con modelo cegado ----
    if args.results:
        res = [r for r in _read_csv(args.results)
               if not r.get("error") and r.get("justification_global")]
        # Toma la 1a replica por (caso, proveedor); opcionalmente muestrea N por modelo.
        seen = {}
        for r in res:
            k = (r["case_id"], r["provider"])
            if k not in seen:
                seen[k] = r
        items = list(seen.values())
        if args.sample:
            by_prov = defaultdict(list)
            for r in items:
                by_prov[r["provider"]].append(r)
            sampled = []
            for prov, lst in by_prov.items():
                lst2 = _deterministic_order([x["case_id"] for x in lst], args.seed)
                pick = set(lst2[:args.sample])
                sampled += [x for x in lst if x["case_id"] in pick]
            items = sampled
        order = _deterministic_order([f'{r["case_id"]}|{r["provider"]}' for r in items], args.seed + 1)
        by_key = {f'{r["case_id"]}|{r["provider"]}': r for r in items}
        out4 = os.path.join(args.outdir, "calidad_ciega.csv")
        key4 = os.path.join(args.outdir, "clave_calidad.csv")
        with open(out4, "w", encoding="utf-8", newline="") as fh, \
             open(key4, "w", encoding="utf-8", newline="") as fk:
            w = csv.writer(fh); w.writerow(["item_id", "justificacion",
                                            "calidad_eval1", "calidad_eval2"])
            wk = csv.writer(fk); wk.writerow(["item_id", "case_id", "provider", "model"])
            for i, key in enumerate(order, 1):
                r = by_key[key]
                item_id = f"J{i:04d}"
                w.writerow([item_id, r.get("justification_global", ""), "", ""])
                wk.writerow([item_id, r["case_id"], r["provider"], r.get("model", "")])
        print(f"M4: {out4}  (justificaciones con identidad de modelo CEGADA; "
              f"columnas calidad_eval1/2 en blanco, escala 0-100)")
        print(f"M4: {key4}  (clave item->modelo; NO entregar a los evaluadores)")
    print("\nFlujo: cada evaluador llena su columna a ciegas; luego consolidas "
          "ambas columnas en un CSV y corres 'kappa' (M2) o 'icc' (M4).")


# ----------------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pa = sub.add_parser("alpha", help="Alfa de Cronbach (M6).")
    pa.add_argument("--in", dest="infile", required=True)
    pa.add_argument("--id-col", default=None, help="Columna identificadora a excluir.")
    pa.add_argument("--groups", default=None, help='Subescalas, p.ej. "1-7,8-13,14-18".')
    pa.set_defaults(func=cmd_alpha)

    pk = sub.add_parser("kappa", help="Kappa de Cohen entre dos categorizadores (M2).")
    pk.add_argument("--in", dest="infile", required=True)
    pk.add_argument("--col1", required=True)
    pk.add_argument("--col2", required=True)
    pk.set_defaults(func=cmd_kappa)

    pi = sub.add_parser("icc", help="ICC(2,1) de calidad 0-100 entre dos evaluadores (M4).")
    pi.add_argument("--in", dest="infile", required=True)
    pi.add_argument("--col1", required=True)
    pi.add_argument("--col2", required=True)
    pi.set_defaults(func=cmd_icc)

    pm = sub.add_parser("make-sheets", help="Genera hojas ciegas para M2 y M4.")
    pm.add_argument("--metadata", default=None, help="metadata.csv (para M2).")
    pm.add_argument("--results", default=None, help="resultados_replicas.csv (para M4).")
    pm.add_argument("--outdir", default="hojas")
    pm.add_argument("--sample", type=int, default=None, help="N justificaciones por modelo (M4).")
    pm.add_argument("--seed", type=int, default=20260730)
    pm.set_defaults(func=cmd_make_sheets)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
