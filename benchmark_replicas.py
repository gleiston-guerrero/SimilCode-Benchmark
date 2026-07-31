#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
benchmark_replicas.py
=====================
Arnes de benchmark con REPLICAS para SimilCode.

Soporta cuatro proveedores: DeepSeek, Gemini, OpenAI (GPT) y Anthropic (Claude).
Cada par de codigo se evalua k veces por modelo, a temperatura 0, registrando
snapshot de modelo, latencia y respuesta cruda, para estimar la ESTABILIDAD
INTRA-MODELO del ranking de precision (preocupacion mayor #3 del informe).

No requiere dependencias externas (solo la biblioteca estandar de Python).

Comandos:
  list-models   Consulta el catalogo REAL de modelos de cada proveedor con tu
                clave (para conocer el identificador vigente antes de correr).
  run           Ejecuta el benchmark con k replicas.
  analyze       Coincidencia + estabilidad intra-modelo (+ sensibilidad de banda).

Ejemplos (PowerShell):
  python benchmark_replicas.py list-models
  python benchmark_replicas.py run --cases metadata.csv --prompt prompt.txt --replicas 3 --out resultados_replicas.csv
  python benchmark_replicas.py analyze --in resultados_replicas.csv --out resumen_estabilidad.csv --sensitivity
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
# Rangos esperados por categoria (fallback si el CSV de casos no los trae).
# metadata.csv del repositorio ya incluye expected_similarity_min/max por caso,
# asi que normalmente estos NO se usan. Editables para pruebas de sensibilidad.
# ----------------------------------------------------------------------------
EXPECTED_RANGES = {
    "identico":    (100, 100),
    "funcional":   (70, 90),
    "estructural": (40, 60),
    "diferente":   (0, 20),
}

CATEGORY_ALIASES = {
    "identico": "identico", "identical": "identico", "igual": "identico",
    "funcional": "funcional", "functional": "funcional",
    "estructural": "estructural", "structural": "estructural",
    "diferente": "diferente", "different": "diferente", "distinto": "diferente",
}

PLACEHOLDER_A = "[CÓDIGO_A_AQUÍ]"
PLACEHOLDER_B = "[CÓDIGO_B_AQUÍ]"

FIELDNAMES = [
    "run_ts", "case_id", "language", "category", "expected_low", "expected_high",
    "provider", "model", "model_snapshot", "replica", "latency_s",
    "lexica", "estructural", "estilistica", "funcional", "sintactica", "global",
    "within_expected", "justification_global", "error",
]


def _strip(s):
    trans = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuaeiouu")
    return str(s).strip().lower().translate(trans)


# ----------------------------------------------------------------------------
# Carga de casos
# ----------------------------------------------------------------------------
def _read_code(value, base_dir):
    if not value:
        return ""
    candidate = value if os.path.isabs(value) else os.path.join(base_dir, value)
    if os.path.isfile(candidate):
        with open(candidate, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    return value


def load_cases(path):
    """Carga casos desde .jsonl, .json o .csv (incluye el metadata.csv del repo,
    con columnas similarity_category, code_a_path/code_b_path y
    expected_similarity_min/max)."""
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
        cat_raw = _strip(r.get("category") or r.get("similarity_category") or "")
        cat = CATEGORY_ALIASES.get(cat_raw)
        if cat is None:
            sys.exit(f"Categoria desconocida '{cat_raw}' en el caso indice {i}. "
                     f"Validas: {sorted(set(CATEGORY_ALIASES.values()))}.")
        code_a = _read_code(r.get("code_a") or r.get("code_a_path"), base_dir)
        code_b = _read_code(r.get("code_b") or r.get("code_b_path"), base_dir)
        elow = r.get("expected_similarity_min")
        ehigh = r.get("expected_similarity_max")
        expected = None
        if elow not in (None, "") and ehigh not in (None, ""):
            expected = (int(float(elow)), int(float(ehigh)))
        cases.append({
            "id": str(r.get("id") or r.get("case_id") or i),
            "language": str(r.get("language", "")),
            "category": cat,
            "code_a": code_a,
            "code_b": code_b,
            "expected": expected,
        })
    return cases


# ----------------------------------------------------------------------------
# Prompt y parsing
# ----------------------------------------------------------------------------
def build_prompt(template, code_a, code_b):
    out = template.replace(PLACEHOLDER_A, code_a).replace(PLACEHOLDER_B, code_b)
    if PLACEHOLDER_A not in template and PLACEHOLDER_B not in template:
        out = (template.rstrip() + "\n\nFRAGMENTO A:\n" + code_a +
               "\n\nFRAGMENTO B:\n" + code_b + "\n")
    return out


_NUM_RE = r"[:\s]*\[?\s*(\d{1,3})"


def _find_score(text, label):
    m = re.search(r"SIMILITUD\s+" + label + _NUM_RE, text, re.IGNORECASE)
    if m:
        return max(0, min(100, int(m.group(1))))
    return None


def parse_scores(text):
    scores = {
        "lexica": _find_score(text, "L[EÉ]XICA"),
        "estructural": _find_score(text, "ESTRUCTURAL"),
        "estilistica": _find_score(text, "ESTIL[IÍ]STICA"),
        "funcional": _find_score(text, "FUNCIONAL"),
        "sintactica": _find_score(text, "SINT[AÁ]CTICA"),
        "global": _find_score(text, "GLOBAL"),
    }
    jm = re.search(r"SIMILITUD\s+GLOBAL.*?Justificaci[oó]n\s*:?\s*(.+)",
                   text, re.IGNORECASE | re.DOTALL)
    scores["justification_global"] = " ".join(jm.group(1).split())[:800] if jm else ""
    return scores


# ----------------------------------------------------------------------------
# HTTP
# ----------------------------------------------------------------------------
def _http_post(url, payload, headers, timeout):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    return json.loads(body), time.time() - t0


def _http_get(url, headers, timeout=30):
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


# ---- Proveedores -----------------------------------------------------------
def call_deepseek(prompt, model, api_key, temperature, timeout):
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {api_key}"}
    payload = {"model": model, "temperature": temperature, "stream": False,
               "messages": [{"role": "user", "content": prompt}]}
    obj, latency = _http_post(url, payload, headers, timeout)
    text = obj["choices"][0]["message"]["content"]
    snap = obj.get("model") or obj.get("system_fingerprint") or model
    return text, latency, str(snap)


def call_openai(prompt, model, api_key, temperature, timeout):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {api_key}"}
    base = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    try:
        obj, latency = _http_post(url, dict(base, temperature=temperature),
                                  headers, timeout)
    except urllib.error.HTTPError as e:
        # Algunos modelos de razonamiento GPT-5.x solo aceptan temperature=1
        # (default) y rechazan 0; reintenta sin el parametro temperature.
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            pass
        if e.code == 400 and ("temperature" in body.lower() or "unsupported" in body.lower()):
            obj, latency = _http_post(url, base, headers, timeout)
        else:
            raise RuntimeError(f"HTTP {e.code}: {body[:300]}")
    text = obj["choices"][0]["message"]["content"]
    snap = obj.get("model") or model
    return text, latency, str(snap)


def call_gemini(prompt, model, api_key, temperature, timeout):
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{model}:generateContent?key={api_key}")
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"temperature": temperature}}
    obj, latency = _http_post(url, payload, headers, timeout)
    cand = obj["candidates"][0]
    parts = cand.get("content", {}).get("parts", [{}])
    text = "".join(p.get("text", "") for p in parts)
    snap = obj.get("modelVersion") or model
    return text, latency, str(snap)


def call_anthropic(prompt, model, api_key, temperature, timeout):
    url = "https://api.anthropic.com/v1/messages"
    headers = {"Content-Type": "application/json", "x-api-key": api_key,
               "anthropic-version": "2023-06-01"}
    base = {"model": model, "max_tokens": 2048,
            "messages": [{"role": "user", "content": prompt}]}
    try:
        obj, latency = _http_post(url, dict(base, temperature=temperature),
                                  headers, timeout)
    except urllib.error.HTTPError as e:
        # Modelos de razonamiento (p.ej. claude-opus-5 con thinking) rechazan
        # temperature=0 (solo aceptan 1). Ante 400, reintenta SIN temperature.
        if e.code == 400:
            try:
                obj, latency = _http_post(url, base, headers, timeout)
            except urllib.error.HTTPError as e2:
                b2 = ""
                try:
                    b2 = e2.read().decode("utf-8", errors="replace")
                except Exception:  # noqa: BLE001
                    pass
                raise RuntimeError(f"HTTP {e2.code}: {b2[:300]}")
        else:
            b = ""
            try:
                b = e.read().decode("utf-8", errors="replace")
            except Exception:  # noqa: BLE001
                pass
            raise RuntimeError(f"HTTP {e.code}: {b[:300]}")
    text = "".join(b.get("text", "") for b in obj.get("content", [])
                   if b.get("type") == "text")
    snap = obj.get("model") or model
    return text, latency, str(snap)


# Config por proveedor: funcion, variable de entorno y modelo por defecto
# (los defaults reproducen las versiones PUBLICADAS del estudio; usa list-models
# y --*-model para actualizar a la version vigente de forma consciente).
PROVIDER_CFG = {
    "deepseek":  {"fn": call_deepseek,  "env": "DEEPSEEK_API_KEY",  "default_model": "deepseek-v4-pro"},
    "gemini":    {"fn": call_gemini,    "env": "GEMINI_API_KEY",    "default_model": "gemini-3.1-pro-preview"},
    "openai":    {"fn": call_openai,    "env": "OPENAI_API_KEY",    "default_model": "gpt-5.5-2026-04-23"},
    "anthropic": {"fn": call_anthropic, "env": "ANTHROPIC_API_KEY", "default_model": "claude-opus-5"},
}


def call_with_retries(provider, prompt, model, api_key, temperature, timeout,
                      max_retries, backoff):
    fn = PROVIDER_CFG[provider]["fn"]
    last_err = None
    for attempt in range(max_retries + 1):
        try:
            return fn(prompt, model, api_key, temperature, timeout)
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}"
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries:
                time.sleep(backoff * (2 ** attempt)); continue
            break
        except Exception as e:  # noqa: BLE001
            last_err = str(e)[:300]
            # Errores 4xx son permanentes: no reintentar (evita perder tiempo).
            if last_err.startswith("HTTP 4"):
                break
            if attempt < max_retries:
                time.sleep(backoff * (2 ** attempt)); continue
            break
    raise RuntimeError(last_err or "fallo desconocido")


# ----------------------------------------------------------------------------
# Comando: list-models
# ----------------------------------------------------------------------------
def cmd_list_models(args):
    def get_key(prov):
        return os.environ.get(PROVIDER_CFG[prov]["env"])
    provs = [args.provider] if args.provider else list(PROVIDER_CFG)
    for prov in provs:
        key = get_key(prov)
        print(f"\n== {prov} ({PROVIDER_CFG[prov]['env']}) ==")
        if not key:
            print("  (sin clave en variable de entorno; omitido)")
            continue
        try:
            if prov == "deepseek":
                obj = _http_get("https://api.deepseek.com/models",
                                {"Authorization": f"Bearer {key}"})
                ids = [m.get("id") for m in obj.get("data", [])]
            elif prov == "openai":
                obj = _http_get("https://api.openai.com/v1/models",
                                {"Authorization": f"Bearer {key}"})
                ids = sorted(m.get("id") for m in obj.get("data", []))
            elif prov == "gemini":
                obj = _http_get("https://generativelanguage.googleapis.com/"
                                f"v1beta/models?key={key}", {})
                ids = [m.get("name", "").replace("models/", "")
                       for m in obj.get("models", [])
                       if "generateContent" in m.get("supportedGenerationMethods", [])]
            elif prov == "anthropic":
                obj = _http_get("https://api.anthropic.com/v1/models",
                                {"x-api-key": key, "anthropic-version": "2023-06-01"})
                ids = [m.get("id") for m in obj.get("data", [])]
            for mid in ids:
                print(f"  {mid}")
        except Exception as e:  # noqa: BLE001
            print(f"  ERROR consultando catalogo: {str(e)[:160]}")


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

    selected = ([p.strip() for p in args.only.split(",") if p.strip()]
                if args.only else ["deepseek", "gemini"])
    model_override = {
        "deepseek": args.deepseek_model, "gemini": args.gemini_model,
        "openai": args.openai_model, "anthropic": args.anthropic_model,
    }
    targets = []  # (provider, model, key)
    for prov in selected:
        if prov not in PROVIDER_CFG:
            sys.exit(f"Proveedor desconocido: {prov}. Validos: {list(PROVIDER_CFG)}")
        key = os.environ.get(PROVIDER_CFG[prov]["env"])
        if not key:
            sys.exit(f"Falta la variable de entorno {PROVIDER_CFG[prov]['env']}.")
        model = model_override.get(prov) or PROVIDER_CFG[prov]["default_model"]
        targets.append((prov, model, key))

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
            low, high = case.get("expected") or EXPECTED_RANGES[case["category"]]
            for provider, model, key in targets:
                for rep in range(1, args.replicas + 1):
                    counter += 1
                    if (case["id"], provider, str(rep)) in done:
                        continue
                    row = {k: "" for k in FIELDNAMES}
                    row.update({
                        "run_ts": run_ts, "case_id": case["id"],
                        "language": case["language"], "category": case["category"],
                        "expected_low": low, "expected_high": high,
                        "provider": provider, "model": model, "replica": rep,
                    })
                    try:
                        text, latency, snap = call_with_retries(
                            provider, prompt, model, key, args.temperature,
                            args.timeout, args.max_retries, args.backoff)
                        sc = parse_scores(text)
                        g = sc["global"]
                        row.update({
                            "model_snapshot": snap, "latency_s": round(latency, 3),
                            "lexica": sc["lexica"], "estructural": sc["estructural"],
                            "estilistica": sc["estilistica"], "funcional": sc["funcional"],
                            "sintactica": sc["sintactica"], "global": g,
                            "within_expected": ("" if g is None else int(low <= g <= high)),
                            "justification_global": sc["justification_global"],
                        })
                        state = "OK" if g is not None else "OK(sin global)"
                    except Exception as e:  # noqa: BLE001
                        row["error"] = str(e)[:200]; state = "ERROR"
                    writer.writerow(row); fh.flush()
                    print(f"[{counter}/{total}] {provider} caso {case['id']} "
                          f"rep {rep} -> {state}", flush=True)
                    if args.sleep > 0:
                        time.sleep(args.sleep)
    print(f"\nListo. Resultados en: {args.out}")


# ----------------------------------------------------------------------------
# Comando: analyze  (+ sensibilidad de banda, M1a)
# ----------------------------------------------------------------------------
def _load_results(path):
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if not r.get("error") and r.get("global") not in ("", None):
                rows.append(r)
    return rows


def _coincidence_by_provider(rows, delta=0):
    """Coincidencia por proveedor con la banda esperada ensanchada 'delta'
    puntos a cada lado. Voto mayoritario de replicas por caso."""
    by_pc = defaultdict(list)
    for r in rows:
        by_pc[(r["provider"], r["case_id"])].append(r)
    prov = defaultdict(lambda: [0, 0])  # [casos_coincide, casos_total]
    for (provider, _case), reps in by_pc.items():
        votes = []
        for x in reps:
            lo = int(x["expected_low"]) - delta
            hi = int(x["expected_high"]) + delta
            votes.append(int(lo <= int(x["global"]) <= hi))
        majority = 1 if sum(votes) * 2 >= len(votes) else 0
        prov[provider][0] += majority
        prov[provider][1] += 1
    return {p: 100.0 * c / n for p, (c, n) in prov.items()}


def cmd_analyze(args):
    rows = _load_results(args.infile)
    by_pc = defaultdict(list)
    for r in rows:
        by_pc[(r["provider"], r["case_id"])].append(r)

    prov_cases = defaultdict(list)
    for (provider, _case), reps in by_pc.items():
        within = [int(x["within_expected"]) for x in reps if x["within_expected"] != ""]
        globals_ = [int(x["global"]) for x in reps]
        lat = [float(x["latency_s"]) for x in reps if x["latency_s"] != ""]
        if within:
            majority = 1 if sum(within) * 2 >= len(within) else 0
            agree = sum(1 for w in within if w == majority) / len(within)
            coincide = 1 if majority == 1 else 0
        else:
            agree, coincide = float("nan"), 0
        prov_cases[provider].append({
            "agree": agree, "coincide": coincide,
            "span": (max(globals_) - min(globals_)) if globals_ else 0,
            "lat": sum(lat) / len(lat) if lat else float("nan"),
        })

    summary = []
    for provider, items in prov_cases.items():
        n = len(items)
        agrees = [x["agree"] for x in items if x["agree"] == x["agree"]]
        summary.append({
            "provider": provider, "n_casos": n,
            "coincidencia_pct": round(100.0 * sum(x["coincide"] for x in items) / n, 1),
            "estabilidad_intra_pct": round(100.0 * sum(agrees) / len(agrees), 1) if agrees else "NA",
            "rango_global_medio": round(sum(x["span"] for x in items) / n, 1),
            "latencia_media_s": round(sum(x["lat"] for x in items if x["lat"] == x["lat"]) /
                                      max(1, len([x for x in items if x["lat"] == x["lat"]])), 3),
        })
    summary.sort(key=lambda x: x["coincidencia_pct"], reverse=True)
    cols = ["provider", "n_casos", "coincidencia_pct", "estabilidad_intra_pct",
            "rango_global_medio", "latencia_media_s"]
    print("\n== Resumen por modelo ==")
    print(" | ".join(cols))
    for s in summary:
        print(" | ".join(str(s[c]) for c in cols))
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(summary)
        print(f"\nResumen escrito en: {args.out}")

    if args.sensitivity:
        deltas = [-10, -5, 0, 5, 10]
        provs = [s["provider"] for s in summary]
        table = {d: _coincidence_by_provider(rows, d) for d in deltas}
        print("\n== Sensibilidad de banda (coincidencia_pct por delta de +-puntos) ==")
        print("delta | " + " | ".join(provs))
        for d in deltas:
            print(f"{d:+d}    | " + " | ".join(f"{table[d].get(p, float('nan')):.1f}" for p in provs))
        # Estabilidad del ranking: ¿el orden se mantiene en todos los deltas?
        base_order = provs
        stable = all([sorted(table[d], key=lambda p: table[d][p], reverse=True) == base_order
                      for d in deltas])
        print(f"\nRanking estable ante +-10 puntos de banda: {'SI' if stable else 'NO'}")
        if args.sens_out:
            with open(args.sens_out, "w", encoding="utf-8", newline="") as fh:
                w = csv.writer(fh); w.writerow(["delta"] + provs)
                for d in deltas:
                    w.writerow([d] + [round(table[d].get(p, float("nan")), 1) for p in provs])
            print(f"Sensibilidad escrita en: {args.sens_out}")

    print("\nNotas: coincidencia_pct = % de casos cuyo voto mayoritario de replicas "
          "cae en el rango esperado. estabilidad_intra_pct = acuerdo medio entre "
          "replicas del mismo caso (100% = ranking estable). rango_global_medio = "
          "dispersion media del GLOBAL entre replicas (0 = determinista).")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list-models", help="Lista los modelos vigentes de cada proveedor.")
    pl.add_argument("--provider", choices=list(PROVIDER_CFG), default=None)
    pl.set_defaults(func=cmd_list_models)

    pr = sub.add_parser("run", help="Ejecuta el benchmark con replicas.")
    pr.add_argument("--cases", required=True)
    pr.add_argument("--prompt", required=True)
    pr.add_argument("--out", default="resultados_replicas.csv")
    pr.add_argument("--replicas", type=int, default=3)
    pr.add_argument("--temperature", type=float, default=0.0)
    pr.add_argument("--only", default=None,
                    help="Proveedores separados por coma (deepseek,gemini,openai,anthropic). "
                         "Por defecto: deepseek,gemini.")
    pr.add_argument("--deepseek-model", default=None)
    pr.add_argument("--gemini-model", default=None)
    pr.add_argument("--openai-model", default=None)
    pr.add_argument("--anthropic-model", default=None)
    pr.add_argument("--sleep", type=float, default=0.5)
    pr.add_argument("--timeout", type=float, default=120.0)
    pr.add_argument("--max-retries", type=int, default=4)
    pr.add_argument("--backoff", type=float, default=2.0)
    pr.set_defaults(func=cmd_run)

    pa = sub.add_parser("analyze", help="Coincidencia, estabilidad y sensibilidad de banda.")
    pa.add_argument("--in", dest="infile", required=True)
    pa.add_argument("--out", default=None)
    pa.add_argument("--sensitivity", action="store_true",
                    help="Recalcula coincidencia con banda +-5 y +-10 (M1a).")
    pa.add_argument("--sens-out", default=None, help="CSV de la tabla de sensibilidad.")
    pa.set_defaults(func=cmd_analyze)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
benchmark_replicas.py
=====================
Arnes de benchmark con REPLICAS para SimilCode.

Soporta cuatro proveedores: DeepSeek, Gemini, OpenAI (GPT) y Anthropic (Claude).
Cada par de codigo se evalua k veces por modelo, a temperatura 0, registrando
snapshot de modelo, latencia y respuesta cruda, para estimar la ESTABILIDAD
INTRA-MODELO del ranking de precision (preocupacion mayor #3 del informe).

No requiere dependencias externas (solo la biblioteca estandar de Python).

Comandos:
  list-models   Consulta el catalogo REAL de modelos de cada proveedor con tu
                clave (para conocer el identificador vigente antes de correr).
  run           Ejecuta el benchmark con k replicas.
  analyze       Coincidencia + estabilidad intra-modelo (+ sensibilidad de banda).

Ejemplos (PowerShell):
  python benchmark_replicas.py list-models
  python benchmark_replicas.py run --cases metadata.csv --prompt prompt.txt --replicas 3 --out resultados_replicas.csv
  python benchmark_replicas.py analyze --in resultados_replicas.csv --out resumen_estabilidad.csv --sensitivity
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
# Rangos esperados por categoria (fallback si el CSV de casos no los trae).
# metadata.csv del repositorio ya incluye expected_similarity_min/max por caso,
# asi que normalmente estos NO se usan. Editables para pruebas de sensibilidad.
# ----------------------------------------------------------------------------
EXPECTED_RANGES = {
    "identico":    (100, 100),
    "funcional":   (70, 90),
    "estructural": (40, 60),
    "diferente":   (0, 20),
}

CATEGORY_ALIASES = {
    "identico": "identico", "identical": "identico", "igual": "identico",
    "funcional": "funcional", "functional": "funcional",
    "estructural": "estructural", "structural": "estructural",
    "diferente": "diferente", "different": "diferente", "distinto": "diferente",
}

PLACEHOLDER_A = "[CÓDIGO_A_AQUÍ]"
PLACEHOLDER_B = "[CÓDIGO_B_AQUÍ]"

FIELDNAMES = [
    "run_ts", "case_id", "language", "category", "expected_low", "expected_high",
    "provider", "model", "model_snapshot", "replica", "latency_s",
    "lexica", "estructural", "estilistica", "funcional", "sintactica", "global",
    "within_expected", "justification_global", "error",
]


def _strip(s):
    trans = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuaeiouu")
    return str(s).strip().lower().translate(trans)


# ----------------------------------------------------------------------------
# Carga de casos
# ----------------------------------------------------------------------------
def _read_code(value, base_dir):
    if not value:
        return ""
    candidate = value if os.path.isabs(value) else os.path.join(base_dir, value)
    if os.path.isfile(candidate):
        with open(candidate, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    return value


def load_cases(path):
    """Carga casos desde .jsonl, .json o .csv (incluye el metadata.csv del repo,
    con columnas similarity_category, code_a_path/code_b_path y
    expected_similarity_min/max)."""
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
        cat_raw = _strip(r.get("category") or r.get("similarity_category") or "")
        cat = CATEGORY_ALIASES.get(cat_raw)
        if cat is None:
            sys.exit(f"Categoria desconocida '{cat_raw}' en el caso indice {i}. "
                     f"Validas: {sorted(set(CATEGORY_ALIASES.values()))}.")
        code_a = _read_code(r.get("code_a") or r.get("code_a_path"), base_dir)
        code_b = _read_code(r.get("code_b") or r.get("code_b_path"), base_dir)
        elow = r.get("expected_similarity_min")
        ehigh = r.get("expected_similarity_max")
        expected = None
        if elow not in (None, "") and ehigh not in (None, ""):
            expected = (int(float(elow)), int(float(ehigh)))
        cases.append({
            "id": str(r.get("id") or r.get("case_id") or i),
            "language": str(r.get("language", "")),
            "category": cat,
            "code_a": code_a,
            "code_b": code_b,
            "expected": expected,
        })
    return cases


# ----------------------------------------------------------------------------
# Prompt y parsing
# ----------------------------------------------------------------------------
def build_prompt(template, code_a, code_b):
    out = template.replace(PLACEHOLDER_A, code_a).replace(PLACEHOLDER_B, code_b)
    if PLACEHOLDER_A not in template and PLACEHOLDER_B not in template:
        out = (template.rstrip() + "\n\nFRAGMENTO A:\n" + code_a +
               "\n\nFRAGMENTO B:\n" + code_b + "\n")
    return out


_NUM_RE = r"[:\s]*\[?\s*(\d{1,3})"


def _find_score(text, label):
    m = re.search(r"SIMILITUD\s+" + label + _NUM_RE, text, re.IGNORECASE)
    if m:
        return max(0, min(100, int(m.group(1))))
    return None


def parse_scores(text):
    scores = {
        "lexica": _find_score(text, "L[EÉ]XICA"),
        "estructural": _find_score(text, "ESTRUCTURAL"),
        "estilistica": _find_score(text, "ESTIL[IÍ]STICA"),
        "funcional": _find_score(text, "FUNCIONAL"),
        "sintactica": _find_score(text, "SINT[AÁ]CTICA"),
        "global": _find_score(text, "GLOBAL"),
    }
    jm = re.search(r"SIMILITUD\s+GLOBAL.*?Justificaci[oó]n\s*:?\s*(.+)",
                   text, re.IGNORECASE | re.DOTALL)
    scores["justification_global"] = " ".join(jm.group(1).split())[:800] if jm else ""
    return scores


# ----------------------------------------------------------------------------
# HTTP
# ----------------------------------------------------------------------------
def _http_post(url, payload, headers, timeout):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    return json.loads(body), time.time() - t0


def _http_get(url, headers, timeout=30):
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


# ---- Proveedores -----------------------------------------------------------
def call_deepseek(prompt, model, api_key, temperature, timeout):
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {api_key}"}
    payload = {"model": model, "temperature": temperature, "stream": False,
               "messages": [{"role": "user", "content": prompt}]}
    obj, latency = _http_post(url, payload, headers, timeout)
    text = obj["choices"][0]["message"]["content"]
    snap = obj.get("model") or obj.get("system_fingerprint") or model
    return text, latency, str(snap)


def call_openai(prompt, model, api_key, temperature, timeout):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {api_key}"}
    base = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    try:
        obj, latency = _http_post(url, dict(base, temperature=temperature),
                                  headers, timeout)
    except urllib.error.HTTPError as e:
        # Algunos modelos de razonamiento GPT-5.x solo aceptan temperature=1
        # (default) y rechazan 0; reintenta sin el parametro temperature.
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            pass
        if e.code == 400 and ("temperature" in body.lower() or "unsupported" in body.lower()):
            obj, latency = _http_post(url, base, headers, timeout)
        else:
            raise RuntimeError(f"HTTP {e.code}: {body[:300]}")
    text = obj["choices"][0]["message"]["content"]
    snap = obj.get("model") or model
    return text, latency, str(snap)


def call_gemini(prompt, model, api_key, temperature, timeout):
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{model}:generateContent?key={api_key}")
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"temperature": temperature}}
    obj, latency = _http_post(url, payload, headers, timeout)
    cand = obj["candidates"][0]
    parts = cand.get("content", {}).get("parts", [{}])
    text = "".join(p.get("text", "") for p in parts)
    snap = obj.get("modelVersion") or model
    return text, latency, str(snap)


def call_anthropic(prompt, model, api_key, temperature, timeout):
    url = "https://api.anthropic.com/v1/messages"
    headers = {"Content-Type": "application/json", "x-api-key": api_key,
               "anthropic-version": "2023-06-01"}
    base = {"model": model, "max_tokens": 2048,
            "messages": [{"role": "user", "content": prompt}]}
    try:
        obj, latency = _http_post(url, dict(base, temperature=temperature),
                                  headers, timeout)
    except urllib.error.HTTPError as e:
        # Modelos de razonamiento (p.ej. claude-opus-5 con thinking) rechazan
        # temperature=0 (solo aceptan 1). Ante 400, reintenta SIN temperature.
        if e.code == 400:
            try:
                obj, latency = _http_post(url, base, headers, timeout)
            except urllib.error.HTTPError as e2:
                b2 = ""
                try:
                    b2 = e2.read().decode("utf-8", errors="replace")
                except Exception:  # noqa: BLE001
                    pass
                raise RuntimeError(f"HTTP {e2.code}: {b2[:300]}")
        else:
            b = ""
            try:
                b = e.read().decode("utf-8", errors="replace")
            except Exception:  # noqa: BLE001
                pass
            raise RuntimeError(f"HTTP {e.code}: {b[:300]}")
    text = "".join(b.get("text", "") for b in obj.get("content", [])
                   if b.get("type") == "text")
    snap = obj.get("model") or model
    return text, latency, str(snap)


# Config por proveedor: funcion, variable de entorno y modelo por defecto
# (los defaults reproducen las versiones PUBLICADAS del estudio; usa list-models
# y --*-model para actualizar a la version vigente de forma consciente).
PROVIDER_CFG = {
    "deepseek":  {"fn": call_deepseek,  "env": "DEEPSEEK_API_KEY",  "default_model": "deepseek-v4-pro"},
    "gemini":    {"fn": call_gemini,    "env": "GEMINI_API_KEY",    "default_model": "gemini-3.1-pro-preview"},
    "openai":    {"fn": call_openai,    "env": "OPENAI_API_KEY",    "default_model": "gpt-5.5-2026-04-23"},
    "anthropic": {"fn": call_anthropic, "env": "ANTHROPIC_API_KEY", "default_model": "claude-opus-5"},
}


def call_with_retries(provider, prompt, model, api_key, temperature, timeout,
                      max_retries, backoff):
    fn = PROVIDER_CFG[provider]["fn"]
    last_err = None
    for attempt in range(max_retries + 1):
        try:
            return fn(prompt, model, api_key, temperature, timeout)
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}"
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries:
                time.sleep(backoff * (2 ** attempt)); continue
            break
        except Exception as e:  # noqa: BLE001
            last_err = str(e)[:300]
            # Errores 4xx son permanentes: no reintentar (evita perder tiempo).
            if last_err.startswith("HTTP 4"):
                break
            if attempt < max_retries:
                time.sleep(backoff * (2 ** attempt)); continue
            break
    raise RuntimeError(last_err or "fallo desconocido")


# ----------------------------------------------------------------------------
# Comando: list-models
# ----------------------------------------------------------------------------
def cmd_list_models(args):
    def get_key(prov):
        return os.environ.get(PROVIDER_CFG[prov]["env"])
    provs = [args.provider] if args.provider else list(PROVIDER_CFG)
    for prov in provs:
        key = get_key(prov)
        print(f"\n== {prov} ({PROVIDER_CFG[prov]['env']}) ==")
        if not key:
            print("  (sin clave en variable de entorno; omitido)")
            continue
        try:
            if prov == "deepseek":
                obj = _http_get("https://api.deepseek.com/models",
                                {"Authorization": f"Bearer {key}"})
                ids = [m.get("id") for m in obj.get("data", [])]
            elif prov == "openai":
                obj = _http_get("https://api.openai.com/v1/models",
                                {"Authorization": f"Bearer {key}"})
                ids = sorted(m.get("id") for m in obj.get("data", []))
            elif prov == "gemini":
                obj = _http_get("https://generativelanguage.googleapis.com/"
                                f"v1beta/models?key={key}", {})
                ids = [m.get("name", "").replace("models/", "")
                       for m in obj.get("models", [])
                       if "generateContent" in m.get("supportedGenerationMethods", [])]
            elif prov == "anthropic":
                obj = _http_get("https://api.anthropic.com/v1/models",
                                {"x-api-key": key, "anthropic-version": "2023-06-01"})
                ids = [m.get("id") for m in obj.get("data", [])]
            for mid in ids:
                print(f"  {mid}")
        except Exception as e:  # noqa: BLE001
            print(f"  ERROR consultando catalogo: {str(e)[:160]}")


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

    selected = ([p.strip() for p in args.only.split(",") if p.strip()]
                if args.only else ["deepseek", "gemini"])
    model_override = {
        "deepseek": args.deepseek_model, "gemini": args.gemini_model,
        "openai": args.openai_model, "anthropic": args.anthropic_model,
    }
    targets = []  # (provider, model, key)
    for prov in selected:
        if prov not in PROVIDER_CFG:
            sys.exit(f"Proveedor desconocido: {prov}. Validos: {list(PROVIDER_CFG)}")
        key = os.environ.get(PROVIDER_CFG[prov]["env"])
        if not key:
            sys.exit(f"Falta la variable de entorno {PROVIDER_CFG[prov]['env']}.")
        model = model_override.get(prov) or PROVIDER_CFG[prov]["default_model"]
        targets.append((prov, model, key))

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
            low, high = case.get("expected") or EXPECTED_RANGES[case["category"]]
            for provider, model, key in targets:
                for rep in range(1, args.replicas + 1):
                    counter += 1
                    if (case["id"], provider, str(rep)) in done:
                        continue
                    row = {k: "" for k in FIELDNAMES}
                    row.update({
                        "run_ts": run_ts, "case_id": case["id"],
                        "language": case["language"], "category": case["category"],
                        "expected_low": low, "expected_high": high,
                        "provider": provider, "model": model, "replica": rep,
                    })
                    try:
                        text, latency, snap = call_with_retries(
                            provider, prompt, model, key, args.temperature,
                            args.timeout, args.max_retries, args.backoff)
                        sc = parse_scores(text)
                        g = sc["global"]
                        row.update({
                            "model_snapshot": snap, "latency_s": round(latency, 3),
                            "lexica": sc["lexica"], "estructural": sc["estructural"],
                            "estilistica": sc["estilistica"], "funcional": sc["funcional"],
                            "sintactica": sc["sintactica"], "global": g,
                            "within_expected": ("" if g is None else int(low <= g <= high)),
                            "justification_global": sc["justification_global"],
                        })
                        state = "OK" if g is not None else "OK(sin global)"
                    except Exception as e:  # noqa: BLE001
                        row["error"] = str(e)[:200]; state = "ERROR"
                    writer.writerow(row); fh.flush()
                    print(f"[{counter}/{total}] {provider} caso {case['id']} "
                          f"rep {rep} -> {state}", flush=True)
                    if args.sleep > 0:
                        time.sleep(args.sleep)
    print(f"\nListo. Resultados en: {args.out}")


# ----------------------------------------------------------------------------
# Comando: analyze  (+ sensibilidad de banda, M1a)
# ----------------------------------------------------------------------------
def _load_results(path):
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if not r.get("error") and r.get("global") not in ("", None):
                rows.append(r)
    return rows


def _coincidence_by_provider(rows, delta=0):
    """Coincidencia por proveedor con la banda esperada ensanchada 'delta'
    puntos a cada lado. Voto mayoritario de replicas por caso."""
    by_pc = defaultdict(list)
    for r in rows:
        by_pc[(r["provider"], r["case_id"])].append(r)
    prov = defaultdict(lambda: [0, 0])  # [casos_coincide, casos_total]
    for (provider, _case), reps in by_pc.items():
        votes = []
        for x in reps:
            lo = int(x["expected_low"]) - delta
            hi = int(x["expected_high"]) + delta
            votes.append(int(lo <= int(x["global"]) <= hi))
        majority = 1 if sum(votes) * 2 >= len(votes) else 0
        prov[provider][0] += majority
        prov[provider][1] += 1
    return {p: 100.0 * c / n for p, (c, n) in prov.items()}


def cmd_analyze(args):
    rows = _load_results(args.infile)
    by_pc = defaultdict(list)
    for r in rows:
        by_pc[(r["provider"], r["case_id"])].append(r)

    prov_cases = defaultdict(list)
    for (provider, _case), reps in by_pc.items():
        within = [int(x["within_expected"]) for x in reps if x["within_expected"] != ""]
        globals_ = [int(x["global"]) for x in reps]
        lat = [float(x["latency_s"]) for x in reps if x["latency_s"] != ""]
        if within:
            majority = 1 if sum(within) * 2 >= len(within) else 0
            agree = sum(1 for w in within if w == majority) / len(within)
            coincide = 1 if majority == 1 else 0
        else:
            agree, coincide = float("nan"), 0
        prov_cases[provider].append({
            "agree": agree, "coincide": coincide,
            "span": (max(globals_) - min(globals_)) if globals_ else 0,
            "lat": sum(lat) / len(lat) if lat else float("nan"),
        })

    summary = []
    for provider, items in prov_cases.items():
        n = len(items)
        agrees = [x["agree"] for x in items if x["agree"] == x["agree"]]
        summary.append({
            "provider": provider, "n_casos": n,
            "coincidencia_pct": round(100.0 * sum(x["coincide"] for x in items) / n, 1),
            "estabilidad_intra_pct": round(100.0 * sum(agrees) / len(agrees), 1) if agrees else "NA",
            "rango_global_medio": round(sum(x["span"] for x in items) / n, 1),
            "latencia_media_s": round(sum(x["lat"] for x in items if x["lat"] == x["lat"]) /
                                      max(1, len([x for x in items if x["lat"] == x["lat"]])), 3),
        })
    summary.sort(key=lambda x: x["coincidencia_pct"], reverse=True)
    cols = ["provider", "n_casos", "coincidencia_pct", "estabilidad_intra_pct",
            "rango_global_medio", "latencia_media_s"]
    print("\n== Resumen por modelo ==")
    print(" | ".join(cols))
    for s in summary:
        print(" | ".join(str(s[c]) for c in cols))
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(summary)
        print(f"\nResumen escrito en: {args.out}")

    if args.sensitivity:
        deltas = [-10, -5, 0, 5, 10]
        provs = [s["provider"] for s in summary]
        table = {d: _coincidence_by_provider(rows, d) for d in deltas}
        print("\n== Sensibilidad de banda (coincidencia_pct por delta de +-puntos) ==")
        print("delta | " + " | ".join(provs))
        for d in deltas:
            print(f"{d:+d}    | " + " | ".join(f"{table[d].get(p, float('nan')):.1f}" for p in provs))
        # Estabilidad del ranking: ¿el orden se mantiene en todos los deltas?
        base_order = provs
        stable = all([sorted(table[d], key=lambda p: table[d][p], reverse=True) == base_order
                      for d in deltas])
        print(f"\nRanking estable ante +-10 puntos de banda: {'SI' if stable else 'NO'}")
        if args.sens_out:
            with open(args.sens_out, "w", encoding="utf-8", newline="") as fh:
                w = csv.writer(fh); w.writerow(["delta"] + provs)
                for d in deltas:
                    w.writerow([d] + [round(table[d].get(p, float("nan")), 1) for p in provs])
            print(f"Sensibilidad escrita en: {args.sens_out}")

    print("\nNotas: coincidencia_pct = % de casos cuyo voto mayoritario de replicas "
          "cae en el rango esperado. estabilidad_intra_pct = acuerdo medio entre "
          "replicas del mismo caso (100% = ranking estable). rango_global_medio = "
          "dispersion media del GLOBAL entre replicas (0 = determinista).")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list-models", help="Lista los modelos vigentes de cada proveedor.")
    pl.add_argument("--provider", choices=list(PROVIDER_CFG), default=None)
    pl.set_defaults(func=cmd_list_models)

    pr = sub.add_parser("run", help="Ejecuta el benchmark con replicas.")
    pr.add_argument("--cases", required=True)
    pr.add_argument("--prompt", required=True)
    pr.add_argument("--out", default="resultados_replicas.csv")
    pr.add_argument("--replicas", type=int, default=3)
    pr.add_argument("--temperature", type=float, default=0.0)
    pr.add_argument("--only", default=None,
                    help="Proveedores separados por coma (deepseek,gemini,openai,anthropic). "
                         "Por defecto: deepseek,gemini.")
    pr.add_argument("--deepseek-model", default=None)
    pr.add_argument("--gemini-model", default=None)
    pr.add_argument("--openai-model", default=None)
    pr.add_argument("--anthropic-model", default=None)
    pr.add_argument("--sleep", type=float, default=0.5)
    pr.add_argument("--timeout", type=float, default=120.0)
    pr.add_argument("--max-retries", type=int, default=4)
    pr.add_argument("--backoff", type=float, default=2.0)
    pr.set_defaults(func=cmd_run)

    pa = sub.add_parser("analyze", help="Coincidencia, estabilidad y sensibilidad de banda.")
    pa.add_argument("--in", dest="infile", required=True)
    pa.add_argument("--out", default=None)
    pa.add_argument("--sensitivity", action="store_true",
                    help="Recalcula coincidencia con banda +-5 y +-10 (M1a).")
    pa.add_argument("--sens-out", default=None, help="CSV de la tabla de sensibilidad.")
    pa.set_defaults(func=cmd_analyze)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
