#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_copias_ia.py — Genera copias reescritas con IA de los 30 programas de
referencia del benchmark SimilCode (revision M1).

Para cada programa de referencia (CODE_IDENT_*) se piden dos reescrituras:
  ligera  -> cambia nombres, comentarios y orden (prompt_reescritura_ligera.txt)
  intensa -> cambia ademas la estructura      (prompt_reescritura_intensa.txt)

Las copias se guardan junto al corpus:
  csharp/CODE_IAL_CS_001.cs   (ligera)    csharp/CODE_IAI_CS_001.cs   (intensa)
  java/CODE_IAL_JAVA_001.java (ligera)    java/CODE_IAI_JAVA_001.java (intensa)
y cada llamada queda registrada en copias_ia/copias_ia_log.csv, con la
respuesta completa en copias_ia/respuestas/.

Generadores: se indican como proveedor:modelo y se reparten en rotacion entre
los programas, de modo que cada generador produce el mismo numero de copias
de cada nivel. Proveedores admitidos:
  ollama     modelo local (http://localhost:11434), sin costo
  openai, anthropic, gemini, deepseek  (claves en variables de entorno, igual
                                        que benchmark_replicas.py)

Ejemplos (PowerShell, desde la carpeta SimilCode-Benchmark):
  python copias_ia/generar_copias_ia.py --generadores ollama:qwen2.5-coder:14b
  python copias_ia/generar_copias_ia.py --generadores ollama:qwen2.5-coder:14b,openai:gpt-5.5-2026-04-23
  python copias_ia/generar_copias_ia.py --solo CODE_IAI_CS_004 --generadores ollama:qwen2.5-coder:14b

Las claves de API se leen SOLO de variables de entorno; nunca se escriben en
archivos ni en el registro.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.request

# Las llamadas al modelo local no deben pasar por un proxy corporativo.
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")
os.environ.setdefault("no_proxy", "localhost,127.0.0.1")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import benchmark_replicas as br  # noqa: E402

LEVELS = {"ligera": "IAL", "intensa": "IAI", "api": "IAP"}  # api: mismo prompt intenso, generado con modelos por API
LOG_FIELDS = ["timestamp", "copy_id", "reference_id", "language", "level",
              "generator_provider", "generator_model", "model_snapshot",
              "temperature", "prompt_sha256", "latency_s", "input_tokens",
              "output_tokens", "attempt", "status", "error", "copy_path",
              "response_path"]


def call_ollama(prompt, model, api_key, temperature, timeout):
    """Modelo local servido por Ollama (https://ollama.com)."""
    url = os.environ.get("OLLAMA_URL", "http://localhost:11434") + "/api/chat"
    payload = {"model": model, "stream": False,
               "options": {"temperature": temperature},
               "messages": [{"role": "user", "content": prompt}]}
    obj, latency = br._http_post(url, payload, {"Content-Type": "application/json"}, timeout)
    return obj["message"]["content"], latency, str(obj.get("model") or model)


def call_generator(provider, model, prompt, temperature, timeout):
    if provider == "ollama":
        return call_ollama(prompt, model, None, temperature, timeout)
    if provider not in br.PROVIDER_CFG:
        sys.exit(f"Proveedor desconocido: {provider}")
    key = os.environ.get(br.PROVIDER_CFG[provider]["env"])
    if not key:
        sys.exit(f"Falta la variable de entorno {br.PROVIDER_CFG[provider]['env']}.")
    return br.call_with_retries(provider, prompt, model, key, temperature,
                                timeout, 4, 2.0)


def extract_code(text, language):
    """Toma el bloque de codigo mas largo de la respuesta."""
    blocks = re.findall(r"```[a-zA-Z#+]*\s*\n(.*?)```", text, re.S)
    code = max(blocks, key=len) if blocks else text
    return code.strip() + "\n"


def load_references():
    path = os.path.join(ROOT, "metadata.csv")
    refs = []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["similarity_category"].strip().lower() == "identical":
                refs.append({"id": r["code_a_id"], "path": r["code_a_path"],
                             "language": r["language"], "group": int(r["reference_group"])})
    refs.sort(key=lambda x: (x["language"], x["group"]))
    return refs


def copy_id(ref, level):
    tag = LEVELS[level]
    lang = "CS" if ref["language"] == "C#" else "JAVA"
    return f"CODE_{tag}_{lang}_{ref['group']:03d}"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--generadores", required=True,
                    help="Lista proveedor:modelo separada por comas.")
    ap.add_argument("--niveles", default="ligera,intensa")
    ap.add_argument("--temperatura", type=float, default=0.7,
                    help="Temperatura de generacion (por defecto 0.7, como un uso normal).")
    ap.add_argument("--timeout", type=float, default=300.0)
    ap.add_argument("--solo", default=None,
                    help="Ids de copia a (re)generar, separados por comas.")
    ap.add_argument("--sobrescribir", action="store_true",
                    help="Regenera aunque la copia ya exista.")
    ap.add_argument("--solo-fallidas", action="store_true",
                    help="Regenera solo las copias que verificar_equivalencia.py marco como no equivalentes.")
    args = ap.parse_args()

    gens = []
    for g in args.generadores.split(","):
        prov, _, model = g.strip().partition(":")
        if not model:
            sys.exit(f"Generador mal indicado: {g} (use proveedor:modelo)")
        gens.append((prov, model))
    levels = [x.strip() for x in args.niveles.split(",") if x.strip()]
    only = set(x.strip() for x in args.solo.split(",")) if args.solo else None
    if args.solo_fallidas:
        rp = os.path.join(HERE, "equivalencia_resumen.csv")
        if not os.path.isfile(rp):
            sys.exit("Falta copias_ia/equivalencia_resumen.csv: ejecute antes verificar_equivalencia.py")
        with open(rp, encoding="utf-8", newline="") as fh:
            only = {r["copy_id"] for r in csv.DictReader(fh)
                    if r["equivalent"] != "1" and "revision_manual" not in r["statuses"]}
        if not only:
            print("No hay copias fallidas que regenerar.")
            return
        print(f"Regenerando {len(only)} copias fallidas: {', '.join(sorted(only))}")

    prompts = {}
    for lv in levels:
        with open(os.path.join(HERE, f"prompt_reescritura_{lv}.txt"), encoding="utf-8") as fh:
            prompts[lv] = fh.read()

    os.makedirs(os.path.join(HERE, "respuestas"), exist_ok=True)
    log_path = os.path.join(HERE, "copias_ia_log.csv")
    new_log = not os.path.isfile(log_path)
    refs = load_references()
    previous = {}
    if not new_log:
        with open(log_path, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                previous[r["copy_id"]] = previous.get(r["copy_id"], 0) + 1

    with open(log_path, "a", encoding="utf-8", newline="") as lf:
        w = csv.DictWriter(lf, fieldnames=LOG_FIELDS)
        if new_log:
            w.writeheader()
        for i, ref in enumerate(refs):
            src = open(os.path.join(ROOT, ref["path"]), encoding="utf-8-sig").read()
            for j, lv in enumerate(levels):
                cid = copy_id(ref, lv)
                if only and cid not in only:
                    continue
                ext = ".cs" if ref["language"] == "C#" else ".java"
                folder = "csharp" if ext == ".cs" else "java"
                out_rel = f"{folder}/{cid}{ext}"
                out_abs = os.path.join(ROOT, out_rel)
                if os.path.isfile(out_abs) and not args.sobrescribir and not only:
                    print(f"{cid}: ya existe, se omite")
                    continue
                # Rotacion equilibrada: generador distinto para cada nivel.
                prov, model = gens[(i + j) % len(gens)]
                lang_name = "C#" if ext == ".cs" else "Java"
                prompt = prompts[lv].replace("[LENGUAJE]", lang_name).replace("[CÓDIGO_AQUÍ]", src)
                psha = hashlib.sha256(prompts[lv].encode("utf-8")).hexdigest()
                previous[cid] = previous.get(cid, 0) + 1
                attempt = previous[cid]
                row = {k: "" for k in LOG_FIELDS}
                row.update({"timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"), "copy_id": cid,
                            "reference_id": ref["id"], "language": ref["language"], "level": lv,
                            "generator_provider": prov, "generator_model": model,
                            "temperature": args.temperatura, "prompt_sha256": psha,
                            "attempt": attempt, "copy_path": out_rel})
                try:
                    text, latency, snap = call_generator(prov, model, prompt, args.temperatura, args.timeout)
                    tin, tout = br.extract_usage(prov, br.LAST_RESPONSE)
                    resp_rel = f"copias_ia/respuestas/{cid}_{time.strftime('%Y%m%dT%H%M%S')}.txt"
                    with open(os.path.join(ROOT, resp_rel), "w", encoding="utf-8") as fh:
                        fh.write(text)
                    code = extract_code(text, ref["language"])
                    with open(out_abs, "w", encoding="utf-8") as fh:
                        fh.write(code)
                    row.update({"model_snapshot": snap, "latency_s": round(latency, 2),
                                "input_tokens": tin or "", "output_tokens": tout or "",
                                "status": "OK", "response_path": resp_rel})
                    print(f"{cid}: OK ({prov}:{model}, {latency:.1f} s)")
                except SystemExit:
                    raise
                except Exception as e:  # noqa: BLE001
                    row.update({"status": "ERROR", "error": str(e)[:200]})
                    print(f"{cid}: ERROR {str(e)[:120]}")
                w.writerow(row)
                lf.flush()
    print("\nListo. Siguiente paso: python copias_ia/verificar_equivalencia.py")


if __name__ == "__main__":
    main()
