#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validar_bigo.py
===============
Ejecuta la validacion del componente de estimacion Big O contra la API oficial
del proveedor elegido (debe ser el del modelo integrado en produccion),
sobre el corpus de algoritmos
canonicos y/o el conjunto adversarial. Produce un CSV de predicciones apto para
evaluar_bigo.py.

Sin dependencias externas (solo biblioteca estandar).

Uso (PowerShell):
  $env:OPENAI_API_KEY = "sk-..."
  python validar_bigo.py --corpus corpus --prompt bigo_prompt.txt --replicas 3 \
      --proveedor openai --model gpt-5.5-2026-04-23 --out predicciones_api.csv
  python evaluar_bigo.py --pred predicciones_api.csv --truth ground_truth.csv --out resultados_bigo.csv
"""
import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

PLACEHOLDER = "[CÓDIGO_AQUÍ]"
CLASSES = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)", "O(n^3)", "O(2^n)"]


REINTENTABLES = {408, 409, 429, 500, 502, 503, 504, 529}


def _post(url, payload, headers, timeout):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", errors="replace")), time.time() - t0


def call_openai(prompt, model, key, timeout):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + key}
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    obj, latency = _post(url, payload, headers, timeout)
    text = obj["choices"][0]["message"]["content"]
    return text, latency, str(obj.get("model") or model)


def call_deepseek(prompt, model, key, timeout):
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + key}
    payload = {"model": model, "stream": False,
               "messages": [{"role": "user", "content": prompt}]}
    obj, latency = _post(url, payload, headers, timeout)
    text = obj["choices"][0]["message"]["content"]
    return text, latency, str(obj.get("model") or model)


def call_gemini(prompt, model, key, timeout):
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           "%s:generateContent?key=%s" % (model, key))
    obj, latency = _post(url, {"contents": [{"parts": [{"text": prompt}]}]},
                         {"Content-Type": "application/json"}, timeout)
    parts = obj["candidates"][0].get("content", {}).get("parts", [{}])
    text = "".join(p.get("text", "") for p in parts)
    return text, latency, str(obj.get("modelVersion") or model)


PROVEEDORES = {
    "anthropic": {"env": "ANTHROPIC_API_KEY", "default": "claude-opus-5"},
    "openai": {"env": "OPENAI_API_KEY", "default": "gpt-5.5-2026-04-23"},
    "deepseek": {"env": "DEEPSEEK_API_KEY", "default": "deepseek-v4-pro"},
    "gemini": {"env": "GEMINI_API_KEY", "default": "gemini-3.1-pro-preview"},
}


def call_anthropic(prompt, model, key, timeout):
    url = "https://api.anthropic.com/v1/messages"
    headers = {"Content-Type": "application/json", "x-api-key": key,
               "anthropic-version": "2023-06-01"}
    payload = {"model": model, "max_tokens": 2048,
               "messages": [{"role": "user", "content": prompt}]}
    obj, latency = _post(url, payload, headers, timeout)
    text = "".join(b.get("text", "") for b in obj.get("content", [])
                   if b.get("type") == "text")
    return text, latency, str(obj.get("model") or model)


def llamar(proveedor, prompt, model, key, timeout, intentos=6, base=4.0):
    """Invoca al proveedor con reintentos y espera exponencial.

    Un 429 (limite de tasa) o un 529 (sobrecarga) son transitorios: rendirse
    ante ellos convierte un corte momentaneo en un hueco permanente en los
    datos. Un 400 por saldo o por credencial no lo es y falla de inmediato."""
    fn = {"anthropic": call_anthropic, "openai": call_openai,
          "deepseek": call_deepseek, "gemini": call_gemini}[proveedor]
    for intento in range(1, intentos + 1):
        try:
            return fn(prompt, model, key, timeout)
        except urllib.error.HTTPError as e:
            if e.code not in REINTENTABLES or intento == intentos:
                raise
            espera = base * (2 ** (intento - 1))
            try:
                ra = e.headers.get("retry-after")
                if ra:
                    espera = max(espera, float(ra))
            except (TypeError, ValueError):
                pass
            print("      HTTP %d; reintento %d/%d en %.0f s"
                  % (e.code, intento, intentos - 1, espera), flush=True)
            time.sleep(espera)
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if intento == intentos:
                raise
            espera = base * (2 ** (intento - 1))
            print("      red (%s); reintento %d/%d en %.0f s"
                  % (str(e)[:60], intento, intentos - 1, espera), flush=True)
            time.sleep(espera)


def normalize(raw):
    """Lleva la respuesta a una de las siete clases canonicas."""
    s = " ".join(str(raw).strip().split()).replace("Θ", "O").replace("θ", "O")
    s = s.replace("**", "^").replace("O(2^N)", "O(2^n)")
    s = re.sub(r"\s*\^\s*", "^", s)
    s = re.sub(r"O\s*\(", "O(", s)
    low = s.lower().replace(" ", "")
    table = {
        "o(1)": "O(1)", "o(logn)": "O(log n)", "o(log2n)": "O(log n)",
        "o(n)": "O(n)", "o(nlogn)": "O(n log n)", "o(nlog2n)": "O(n log n)",
        "o(n^2)": "O(n^2)", "o(n2)": "O(n^2)",
        "o(n^3)": "O(n^3)", "o(n3)": "O(n^3)",
        "o(2^n)": "O(2^n)", "o(2n)": "O(2^n)",
    }
    return table.get(low, s)


def parse(text):
    t = re.search(r"COMPLEJIDAD\s+TEMPORAL[^:]*:\s*\[?\s*([^\]\n]+)", text, re.I)
    s = re.search(r"COMPLEJIDAD\s+ESPACIAL[^:]*:\s*\[?\s*([^\]\n]+)", text, re.I)
    j = re.search(r"COMPLEJIDAD\s+TEMPORAL.*?Justificaci[oó]n\s*:?\s*(.+?)(?:\n\s*\n|COMPLEJIDAD|$)",
                  text, re.I | re.S)
    return (normalize(t.group(1)) if t else "",
            normalize(s.group(1)) if s else "",
            " ".join(j.group(1).split())[:400] if j else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="corpus",
                    help="Carpeta con subcarpetas java/ y csharp/.")
    ap.add_argument("--prompt", default="bigo_prompt.txt")
    ap.add_argument("--out", default="predicciones_api.csv")
    ap.add_argument("--proveedor", choices=sorted(PROVEEDORES),
                    default="openai",
                    help="Proveedor de la API. Debe ser el del modelo integrado "
                         "en produccion (por defecto, openai).")
    ap.add_argument("--model", default=None,
                    help="Identificador del modelo. Si se omite, el valor por "
                         "defecto del proveedor elegido.")
    ap.add_argument("--replicas", type=int, default=1)
    ap.add_argument("--intentos", type=int, default=6,
                    help="Intentos por llamada ante fallos transitorios.")
    ap.add_argument("--resume", action="store_true",
                    help="Continua sobre un --out existente sin repetir lo ya resuelto.")
    ap.add_argument("--sleep", type=float, default=0.8)
    ap.add_argument("--timeout", type=float, default=120.0)
    args = ap.parse_args()

    cfg = PROVEEDORES[args.proveedor]
    key = os.environ.get(cfg["env"])
    if not key:
        sys.exit("Falta la variable de entorno %s." % cfg["env"])
    if not args.model:
        args.model = cfg["default"]
    print("Proveedor: %s | modelo: %s" % (args.proveedor, args.model))

    with open(args.prompt, "r", encoding="utf-8") as fh:
        template = fh.read()

    files = []
    for sub, ext in (("java", ".java"), ("csharp", ".cs")):
        d = os.path.join(args.corpus, sub)
        if os.path.isdir(d):
            for name in sorted(os.listdir(d)):
                if name.endswith(ext):
                    files.append((name, os.path.join(d, name)))
    if not files:
        sys.exit("No se encontraron archivos de codigo en " + args.corpus)

    cols = ["filename", "replica", "provider", "model_requested", "model_snapshot",
            "timestamp_utc", "latency_s", "pred_time", "pred_space",
            "justification", "error"]

    # Reanudable: no repite las combinaciones (archivo, replica) ya resueltas sin error.
    hechas = set()
    modo = "w"
    if args.resume and os.path.exists(args.out):
        with open(args.out, "r", encoding="utf-8-sig", newline="") as fh:
            lector = csv.DictReader(fh)
            previas = lector.fieldnames or []
            for r in lector:
                if not str(r.get("error", "")).strip() and r.get("pred_time"):
                    hechas.add((r["filename"], str(r["replica"])))
        modo = "a"
        if previas and set(previas) != set(cols):
            # Respeta el esquema del archivo existente para no desalinear columnas.
            print("AVISO: %s tiene un esquema anterior; se conservan sus columnas.\n"
                  "       Las columnas nuevas (%s) no se escribiran. Borra el archivo "
                  "y reejecuta si las quieres."
                  % (args.out, ", ".join(sorted(set(cols) - set(previas)))))
            cols = previas
        print("Reanudando: %d respuestas validas ya presentes en %s"
              % (len(hechas), args.out))

    total = len(files) * args.replicas
    i = 0
    with open(args.out, modo, encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        if modo == "w":
            w.writeheader()
        for name, path in files:
            with open(path, "r", encoding="utf-8", errors="replace") as cf:
                code = cf.read()
            prompt = (template.replace(PLACEHOLDER, code)
                      if PLACEHOLDER in template
                      else template.rstrip() + "\n\nCODIGO:\n" + code + "\n")
            for rep in range(1, args.replicas + 1):
                i += 1
                if (name, str(rep)) in hechas:
                    print(f"[{i}/{total}] {name} rep {rep} -> ya hecho", flush=True)
                    continue
                row = {k: "" for k in cols}
                row.update({"filename": name, "replica": rep})
                if "provider" in row:
                    row["provider"] = args.proveedor
                if "model_requested" in row:
                    row["model_requested"] = args.model
                if "timestamp_utc" in row:
                    row["timestamp_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                         time.gmtime())
                try:
                    text, lat, snap = llamar(args.proveedor, prompt, args.model,
                                             key, args.timeout, args.intentos)
                    pt, ps, just = parse(text)
                    row.update({"model_snapshot": snap, "latency_s": round(lat, 3),
                                "pred_time": pt, "pred_space": ps,
                                "justification": just})
                    state = "OK" if pt in CLASSES else f"OK(revisar: {pt})"
                except urllib.error.HTTPError as e:
                    body = ""
                    try:
                        body = e.read().decode("utf-8", errors="replace")
                    except Exception:  # noqa: BLE001
                        pass
                    row["error"] = f"HTTP {e.code}: {body[:200]}"
                    state = f"ERROR HTTP {e.code}: {body[:120]}"
                except Exception as e:  # noqa: BLE001
                    row["error"] = str(e)[:200]
                    state = "ERROR " + str(e)[:120]
                w.writerow(row)
                fh.flush()
                print(f"[{i}/{total}] {name} rep {rep} -> {state}", flush=True)
                if args.sleep > 0:
                    time.sleep(args.sleep)
    print("\nListo. Predicciones en:", args.out)


if __name__ == "__main__":
    main()
