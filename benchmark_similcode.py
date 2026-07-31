#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
benchmark_replicas.py
=====================
Arnes de benchmark con REPLICAS para SimilCode (DeepSeek-V3 y Gemini 2.5 Pro).

Objetivo: abordar la preocupacion mayor #3 del informe de revision (falta de
replicas): cada par de codigo se evalua k veces por modelo, a temperatura 0,
registrando snapshot de modelo, latencia y respuesta cruda, para poder estimar
la ESTABILIDAD INTRA-MODELO del ranking de precision.

No requiere dependencias externas (usa solo la biblioteca estandar de Python).
Llama a las APIs por HTTP directo:
  - DeepSeek: endpoint compatible con OpenAI (POST /chat/completions).
  - Gemini:   generativelanguage v1beta (POST /models/{model}:generateContent).

USO BASICO (PowerShell en Windows):
  $env:DEEPSEEK_API_KEY = "sk-..."
  $env:GEMINI_API_KEY   = "AIza..."
  python benchmark_replicas.py run --cases casos.jsonl --prompt prompt.txt --replicas 3 --out resultados_replicas.csv
  python benchmark_replicas.py analyze --in resultados_replicas.csv --out resumen_estabilidad.csv

El comando 'run' es REANUDABLE: si se interrumpe, vuelve a lanzarlo con los
mismos argumentos y omitira las (caso, modelo, replica) ya completadas.
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from collections import defaultdict

# ----------------------------------------------------------------------------
# Configuracion de rangos esperados por categoria (EDITABLE).
# Deben COINCIDIR con la definicion publicada en tu manuscrito. Se exponen aqui
# para que puedas ademas probar la sensibilidad del ranking ante cambios de
# banda (preocupacion mayor #1 del informe). Formato: (limite_inf, limite_sup).
# ----------------------------------------------------------------------------
EXPECTED_RANGES = {
    "identico":    (90, 100),
    "funcional":   (70, 90),
    "estructural": (40, 60),
    "diferente":   (0, 30),
}

# Normalizacion de etiquetas de categoria (acepta variantes con/sin acento).
# La clave se compara tras quitar acentos y pasar a minusculas (ver _strip).
CATEGORY_ALIASES = {
    "identico": "identico", "identical": "identico", "igual": "identico",
    "funcional": "funcional", "functional": "funcional",
    "estructural": "estructural", "structural": "estructural",
    "diferente": "diferente", "different": "diferente", "distinto": "diferente",
}


def _strip(s):
    """Minusculas sin acentos, para comparar etiquetas de forma robusta."""
    trans = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuaeiouu")
    return str(s).strip().lower().translate(trans)

# Placeholders del prompt (Apendice A del manuscrito).
PLACEHOLDER_A = "[CÓDIGO_A_AQUÍ]"
PLACEHOLDER_B = "[CÓDIGO_B_AQUÍ]"

# Columnas del CSV de salida (formato long: una fila por caso-modelo-replica).
FIELDNAMES = [
    "run_ts", "case_id", "language", "category", "expected_low", "expected_high",
    "provider", "model", "model_snapshot", "replica", "latency_s",
    "lexica", "estructural", "estilistica", "funcional", "sintactica", "global",
    "within_expected", "justification_global", "error",
]


# ----------------------------------------------------------------------------
# Carga de casos
# ----------------------------------------------------------------------------
def _read_code(value, base_dir):
    """Si 'value' apunta a un archivo existente, lee su contenido; si no, lo
    devuelve tal cual (codigo en linea)."""
    if not value:
        return ""
    candidate = value if os.path.isabs(value) else os.path.join(base_dir, value)
    if os.path.isfile(candidate):
        with open(candidate, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    return value


def load_cases(path):
    """Carga casos desde .jsonl, .json o .csv.
    Campos esperados por caso:
      id, language, category, y (code_a|code_a_path) + (code_b|code_b_path).
    Los *_path se resuelven relativos al directorio del archivo de casos."""
    base_dir = os.path.dirname(os.path.abspath(path))
    ext = os.path.splitext(path)[1].lower()
    rows = []
    if ext == ".jsonl":
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    elif ext == ".json":
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            rows = data if isinstance(data, list) else data.get("cases", [])
    elif ext == ".csv":
        with open(path, "r", encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
    else:
        sys.exit("Extension de casos no soportada (usa .jsonl, .json o .csv).")

    cases = []
    for i, r in enumerate(rows):
        cat_raw = _strip(r.get("category", ""))
        cat = CATEGORY_ALIASES.get(cat_raw)
        if cat is None:
            sys.exit(f"Categoria desconocida '{cat_raw}' en el caso indice {i}. "
                     f"Validas: {sorted(set(CATEGORY_ALIASES.values()))}.")
        code_a = _read_code(r.get("code_a") or r.get("code_a_path"), base_dir)
        code_b = _read_code(r.get("code_b") or r.get("code_b_path"), base_dir)
        cases.append({
            "id": str(r.get("id", i)),
            "language": str(r.get("language", "")),
            "category": cat,
            "code_a": code_a,
            "code_b": code_b,
        })
    return cases


# ----------------------------------------------------------------------------
# Prompt y parsing
# ----------------------------------------------------------------------------
def build_prompt(template, code_a, code_b):
    out = template.replace(PLACEHOLDER_A, code_a).replace(PLACEHOLDER_B, code_b)
    # Fallback si el template no trae los placeholders exactos.
    if PLACEHOLDER_A not in template and PLACEHOLDER_B not in template:
        out = (template.rstrip() +
               "\n\nFRAGMENTO A:\n" + code_a +
               "\n\nFRAGMENTO B:\n" + code_b + "\n")
    return out


_NUM_RE = r"[:\s]*\[?\s*(\d{1,3})"


def _find_score(text, label):
    m = re.search(r"SIMILITUD\s+" + label + _NUM_RE, text, re.IGNORECASE)
    if m:
        v = int(m.group(1))
        return max(0, min(100, v))
    return None


def parse_scores(text):
    """Extrae las 5 dimensiones + global + justificacion global del texto."""
    scores = {
        "lexica": _find_score(text, "L[EÉ]XICA"),
        "estructural": _find_score(text, "ESTRUCTURAL"),
        "estilistica": _find_score(text, "ESTIL[IÍ]STICA"),
        "funcional": _find_score(text, "FUNCIONAL"),
        "sintactica": _find_score(text, "SINT[AÁ]CTICA"),
        "global": _find_score(text, "GLOBAL"),
    }
    jm = re.search(
        r"SIMILITUD\s+GLOBAL.*?Justificaci[oó]n\s*:?\s*(.+)",
        text, re.IGNORECASE | re.DOTALL)
    just = ""
    if jm:
        just = " ".join(jm.group(1).split())[:800]
    scores["justification_global"] = just
    return scores


# ----------------------------------------------------------------------------
# Llamadas HTTP
# ----------------------------------------------------------------------------
def _http_post(url, payload, headers, timeout):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    return json.loads(body), time.time() - t0


def call_deepseek(prompt, model, api_key, temperature, timeout):
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {api_key}"}
    payload = {
        "model": model,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    obj, latency = _http_post(url, payload, headers, timeout)
    text = obj["choices"][0]["message"]["content"]
    snapshot = obj.get("model") or obj.get("system_fingerprint") or model
    return text, latency, str(snapshot)


def call_gemini(prompt, model, api_key, temperature, timeout):
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{model}:generateContent?key={api_key}")
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperature},
    }
    obj, latency = _http_post(url, payload, headers, timeout)
    cand = obj["candidates"][0]
    parts = cand.get("content", {}).get("parts", [{}])
    text = "".join(p.get("text", "") for p in parts)
    snapshot = obj.get("modelVersion") or model
    return text, latency, str(snapshot)


PROVIDERS = {
    "deepseek": call_deepseek,
    "gemini": call_gemini,
}


def call_with_retries(provider, prompt, model, api_key, temperature, timeout,
                      max_retries, backoff):
    fn = PROVIDERS[provider]
    last_err = None
    for attempt in range(max_retries + 1):
        try:
            return fn(prompt, model, api_key, temperature, timeout)
        except urllib.error.HTTPError as e:
            code = e.code
            last_err = f"HTTP {code}"
            if code in (429, 500, 502, 503, 504) and attempt < max_retries:
                time.sleep(backoff * (2 ** attempt))
                continue
            break
        except Exception as e:  # noqa: BLE001
            last_err = str(e)[:200]
            if attempt < max_retries:
                time.sleep(backoff * (2 ** attempt))
                continue
            break
    raise RuntimeError(last_err or "fallo desconocido")


# ----------------------------------------------------------------------------
# Reanudacion
# ----------------------------------------------------------------------------
def load_done(out_path):
    done = set()
    if os.path.isfile(out_path):
        with open(out_path, "r", encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                if not row.get("error"):
                    done.add((row["case_id"], row["provider"], row["replica"]))
    return done


# ----------------------------------------------------------------------------
# Comando: run
# ----------------------------------------------------------------------------
def cmd_run(args):
    cases = load_cases(args.cases)
    with open(args.prompt, "r", encoding="utf-8") as fh:
        template = fh.read()

    targets = []  # (provider, model, env_key)
    if not args.only or args.only == "deepseek":
        targets.append(("deepseek", args.deepseek_model, "DEEPSEEK_API_KEY"))
    if not args.only or args.only == "gemini":
        targets.append(("gemini", args.gemini_model, "GEMINI_API_KEY"))

    keys = {}
    for provider, _, env_key in targets:
        k = os.environ.get(env_key)
        if not k:
            sys.exit(f"Falta la variable de entorno {env_key}.")
        keys[provider] = k

    done = load_done(args.out)
    is_new = not os.path.isfile(args.out)
    run_ts = time.strftime("%Y-%m-%dT%H:%M:%S")

    total = len(cases) * len(targets) * args.replicas
    counter = 0
    with open(args.out, "a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        if is_new:
            writer.writeheader()
        for case in cases:
            prompt = build_prompt(template, case["code_a"], case["code_b"])
            low, high = EXPECTED_RANGES[case["category"]]
            for provider, model, _ in targets:
                for rep in range(1, args.replicas + 1):
                    counter += 1
                    key = (case["id"], provider, str(rep))
                    if key in done:
                        continue
                    row = {
                        "run_ts": run_ts, "case_id": case["id"],
                        "language": case["language"], "category": case["category"],
                        "expected_low": low, "expected_high": high,
                        "provider": provider, "model": model,
                        "model_snapshot": "", "replica": rep, "latency_s": "",
                        "lexica": "", "estructural": "", "estilistica": "",
                        "funcional": "", "sintactica": "", "global": "",
                        "within_expected": "", "justification_global": "",
                        "error": "",
                    }
                    try:
                        text, latency, snap = call_with_retries(
                            provider, prompt, model, keys[provider],
                            args.temperature, args.timeout,
                            args.max_retries, args.backoff)
                        sc = parse_scores(text)
                        g = sc["global"]
                        row.update({
                            "model_snapshot": snap,
                            "latency_s": round(latency, 3),
                            "lexica": sc["lexica"], "estructural": sc["estructural"],
                            "estilistica": sc["estilistica"],
                            "funcional": sc["funcional"],
                            "sintactica": sc["sintactica"], "global": g,
                            "within_expected": ("" if g is None
                                                else int(low <= g <= high)),
                            "justification_global": sc["justification_global"],
                        })
                        state = "OK" if g is not None else "OK(sin global)"
                    except Exception as e:  # noqa: BLE001
                        row["error"] = str(e)[:200]
                        state = "ERROR"
                    writer.writerow(row)
                    fh.flush()
                    print(f"[{counter}/{total}] {provider} caso {case['id']} "
                          f"rep {rep} -> {state}", flush=True)
                    if args.sleep > 0:
                        time.sleep(args.sleep)
    print(f"\nListo. Resultados en: {args.out}")


# ----------------------------------------------------------------------------
# Comando: analyze  (estabilidad intra-modelo + coincidencia)
# ----------------------------------------------------------------------------
def cmd_analyze(args):
    rows = []
    with open(args.infile, "r", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if not r.get("error") and r.get("global") not in ("", None):
                rows.append(r)

    # Agrupa por (provider, case) las replicas.
    by_pc = defaultdict(list)
    for r in rows:
        by_pc[(r["provider"], r["case_id"])].append(r)

    # Metricas por proveedor.
    prov_cases = defaultdict(list)
    for (provider, case_id), reps in by_pc.items():
        within = [int(x["within_expected"]) for x in reps if x["within_expected"] != ""]
        globals_ = [int(x["global"]) for x in reps]
        lat = [float(x["latency_s"]) for x in reps if x["latency_s"] != ""]
        # Estabilidad: fraccion de replicas que coinciden con el voto mayoritario
        # de 'within_expected' para ese caso (1.0 = todas las replicas de acuerdo).
        if within:
            majority = 1 if sum(within) * 2 >= len(within) else 0
            agree = sum(1 for w in within if w == majority) / len(within)
            case_coincide = 1 if majority == 1 else 0
        else:
            agree, case_coincide = float("nan"), 0
        span = (max(globals_) - min(globals_)) if globals_ else 0
        prov_cases[provider].append({
            "agree": agree, "coincide": case_coincide, "span": span,
            "lat": sum(lat) / len(lat) if lat else float("nan"),
        })

    summary = []
    for provider, items in prov_cases.items():
        n = len(items)
        agrees = [x["agree"] for x in items if x["agree"] == x["agree"]]
        coincide_pct = 100.0 * sum(x["coincide"] for x in items) / n if n else 0
        stability = 100.0 * (sum(agrees) / len(agrees)) if agrees else float("nan")
        mean_span = sum(x["span"] for x in items) / n if n else 0
        mean_lat = ([x["lat"] for x in items if x["lat"] == x["lat"]])
        mean_lat = sum(mean_lat) / len(mean_lat) if mean_lat else float("nan")
        summary.append({
            "provider": provider,
            "n_casos": n,
            "coincidencia_pct": round(coincide_pct, 1),
            "estabilidad_intra_pct": round(stability, 1),
            "rango_global_medio": round(mean_span, 1),
            "latencia_media_s": round(mean_lat, 3),
        })

    summary.sort(key=lambda x: x["coincidencia_pct"], reverse=True)
    cols = ["provider", "n_casos", "coincidencia_pct",
            "estabilidad_intra_pct", "rango_global_medio", "latencia_media_s"]
    print("\n== Resumen por modelo ==")
    print(" | ".join(cols))
    for s in summary:
        print(" | ".join(str(s[c]) for c in cols))

    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(summary)
        print(f"\nResumen escrito en: {args.out}")
    print("\nNotas: 'coincidencia_pct' = % de casos cuyo voto mayoritario de "
          "replicas cae en el rango esperado. 'estabilidad_intra_pct' = acuerdo "
          "medio entre replicas del mismo caso (100% = ranking estable). "
          "'rango_global_medio' = dispersion media del puntaje GLOBAL entre "
          "replicas (0 = determinista).")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("run", help="Ejecuta el benchmark con replicas.")
    pr.add_argument("--cases", required=True, help="Archivo de casos (.jsonl/.json/.csv).")
    pr.add_argument("--prompt", required=True, help="Plantilla de prompt (.txt).")
    pr.add_argument("--out", default="resultados_replicas.csv")
    pr.add_argument("--replicas", type=int, default=3)
    pr.add_argument("--temperature", type=float, default=0.0)
    pr.add_argument("--deepseek-model", default="deepseek-chat")
    pr.add_argument("--gemini-model", default="gemini-2.5-pro")
    pr.add_argument("--only", choices=["deepseek", "gemini"], default=None,
                    help="Ejecutar solo un proveedor.")
    pr.add_argument("--sleep", type=float, default=0.5, help="Pausa entre llamadas (s).")
    pr.add_argument("--timeout", type=float, default=120.0)
    pr.add_argument("--max-retries", type=int, default=4)
    pr.add_argument("--backoff", type=float, default=2.0)
    pr.set_defaults(func=cmd_run)

    pa = sub.add_parser("analyze", help="Calcula coincidencia y estabilidad intra-modelo.")
    pa.add_argument("--in", dest="infile", required=True)
    pa.add_argument("--out", default=None)
    pa.set_defaults(func=cmd_analyze)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()