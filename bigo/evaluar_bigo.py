#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evaluar_bigo.py
===============
Compara las clasificaciones Big O producidas por el modelo contra la verdad de
terreno documentada y reporta exactitud, exactitud por clase y matriz de
confusion (M5 del plan de validacion).

Uso:
  python evaluar_bigo.py --pred predicciones_opus5.csv --truth ground_truth.csv \
      --out resultados_bigo.csv
"""
import argparse
import csv
from collections import defaultdict

ORDER = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)", "O(n^3)", "O(2^n)"]
SHORT = {"O(1)": "1", "O(log n)": "log n", "O(n)": "n", "O(n log n)": "n log n",
         "O(n^2)": "n^2", "O(n^3)": "n^3", "O(2^n)": "2^n"}


def norm(s):
    return " ".join(str(s).strip().replace("Θ", "O").split())


def read(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def confusion(pairs, label):
    M = {a: {b: 0 for b in ORDER} for a in ORDER}
    for real, pred in pairs:
        if real in M and pred in M[real]:
            M[real][pred] += 1
    width = max(len(SHORT[c]) for c in ORDER) + 1
    print(f"\n== Matriz de confusion — {label} (fila = documentado, col = estimado) ==")
    header = " " * 10 + "".join(f"{SHORT[c]:>{width}}" for c in ORDER)
    print(header)
    for a in ORDER:
        row = "".join(f"{M[a][b]:>{width}}" for b in ORDER)
        print(f"{SHORT[a]:>9} {row}")
    return M


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred", required=True)
    ap.add_argument("--truth", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--voto", choices=["todas", "mayoria"], default="todas",
                    help="Con varias replicas: 'todas' puntua cada respuesta por "
                         "separado; 'mayoria' consolida por voto mayoritario y "
                         "puntua una vez por algoritmo. Debe declararse en Metodos.")
    args = ap.parse_args()

    truth = {r["filename"]: r for r in read(args.truth)}
    preds = read(args.pred)
    preds = [p for p in preds if not str(p.get("error", "")).strip()]

    # --- Consistencia entre replicas (determinismo), previa a cualquier puntuacion
    por_archivo = defaultdict(list)
    for p in preds:
        por_archivo[p["filename"]].append(p)
    n_rep = max((len(v) for v in por_archivo.values()), default=1)
    if n_rep > 1:
        est_t = sum(1 for v in por_archivo.values()
                    if len({norm(x["pred_time"]) for x in v}) == 1)
        est_s = sum(1 for v in por_archivo.values()
                    if len({norm(x["pred_space"]) for x in v}) == 1)
        nf = len(por_archivo)
        print("== Consistencia entre replicas (%d replicas por algoritmo) ==" % n_rep)
        print("  Tiempo  identico en las %d replicas: %d/%d = %.1f%%"
              % (n_rep, est_t, nf, 100.0 * est_t / nf))
        print("  Espacio identico en las %d replicas: %d/%d = %.1f%%"
              % (n_rep, est_s, nf, 100.0 * est_s / nf))
        print()

    if args.voto == "mayoria":
        consolidadas = []
        for f, v in por_archivo.items():
            def moda(campo):
                c = defaultdict(int)
                for x in v:
                    c[norm(x[campo])] += 1
                return max(sorted(c), key=lambda k: c[k])
            base = dict(v[0])
            base["pred_time"], base["pred_space"] = moda("pred_time"), moda("pred_space")
            consolidadas.append(base)
        preds = consolidadas
        print("Puntuacion por VOTO MAYORITARIO sobre %d algoritmos.\n" % len(preds))

    rows, t_pairs, s_pairs = [], [], []
    for p in preds:
        f = p["filename"]
        if f not in truth:
            print("AVISO: sin verdad de terreno para", f)
            continue
        t = truth[f]
        rt, pt = norm(t["worst_case_time"]), norm(p["pred_time"])
        rs, ps = norm(t["space_complexity"]), norm(p["pred_space"])
        t_pairs.append((rt, pt))
        s_pairs.append((rs, ps))
        rows.append({
            "algo_id": t["algo_id"], "filename": f, "language": t["language"],
            "algorithm": t["algorithm"],
            "time_documented": rt, "time_predicted": pt, "time_correct": int(rt == pt),
            "space_documented": rs, "space_predicted": ps, "space_correct": int(rs == ps),
        })

    n = len(rows)
    if n == 0:
        raise SystemExit(
            "Ninguna prediccion cruzo con la verdad de terreno. Comprueba que "
            "--pred y --truth se refieren al mismo conjunto (canonico o "
            "adversarial) y que la columna 'filename' coincide.")
    t_ok = sum(r["time_correct"] for r in rows)
    s_ok = sum(r["space_correct"] for r in rows)
    print(f"Algoritmos evaluados: {n}")
    print(f"Exactitud TIEMPO  (peor caso): {t_ok}/{n} = {100.0*t_ok/n:.1f}%")
    print(f"Exactitud ESPACIO (peor caso): {s_ok}/{n} = {100.0*s_ok/n:.1f}%")

    print("\n== Exactitud por clase (tiempo) ==")
    per = defaultdict(lambda: [0, 0])
    for r in rows:
        per[r["time_documented"]][1] += 1
        per[r["time_documented"]][0] += r["time_correct"]
    for c in ORDER:
        if per[c][1]:
            ok, tot = per[c]
            print(f"  {c:<11} {ok}/{tot} = {100.0*ok/tot:5.1f}%")

    print("\n== Exactitud por lenguaje (tiempo) ==")
    lang = defaultdict(lambda: [0, 0])
    for r in rows:
        lang[r["language"]][1] += 1
        lang[r["language"]][0] += r["time_correct"]
    for L, (ok, tot) in sorted(lang.items()):
        print(f"  {L:<6} {ok}/{tot} = {100.0*ok/tot:5.1f}%")

    confusion(t_pairs, "complejidad TEMPORAL")
    confusion(s_pairs, "complejidad ESPACIAL")

    errs = [r for r in rows if not r["time_correct"] or not r["space_correct"]]
    print(f"\n== Discrepancias ({len(errs)}) ==")
    for r in errs:
        if not r["time_correct"]:
            print(f"  TIEMPO  {r['filename']}: documentado {r['time_documented']} "
                  f"-> estimado {r['time_predicted']}")
        if not r["space_correct"]:
            print(f"  ESPACIO {r['filename']}: documentado {r['space_documented']} "
                  f"-> estimado {r['space_predicted']}")
    if not errs:
        print("  (ninguna)")

    if args.out:
        cols = ["algo_id", "filename", "language", "algorithm",
                "time_documented", "time_predicted", "time_correct",
                "space_documented", "space_predicted", "space_correct"]
        with open(args.out, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        print(f"\nDetalle escrito en: {args.out}")


if __name__ == "__main__":
    main()
