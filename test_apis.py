#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueba minima de las 4 APIs: imprime estado y CUERPO del error si falla.
No imprime las claves. Uso: python test_apis.py"""
import json, os, urllib.request, urllib.error

def post(url, payload, headers):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return "OK (200)"
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        return f"HTTP {e.code} -> {body[:500]}"
    except Exception as e:
        return f"FALLO: {str(e)[:300]}"

ds = os.environ.get("DEEPSEEK_API_KEY", "")
gm = os.environ.get("GEMINI_API_KEY", "")
oa = os.environ.get("OPENAI_API_KEY", "")
an = os.environ.get("ANTHROPIC_API_KEY", "")

print("Longitud de claves (deben ser >0 y sin duplicar):")
print("  DEEPSEEK:", len(ds), "| GEMINI:", len(gm), "| OPENAI:", len(oa), "| ANTHROPIC:", len(an))
print()

print("OPENAI (gpt-5.5-2026-04-23):")
print(" ", post("https://api.openai.com/v1/chat/completions",
    {"model": "gpt-5.5-2026-04-23", "messages": [{"role": "user", "content": "hola"}]},
    {"Content-Type": "application/json", "Authorization": "Bearer " + oa}))
print()

print("ANTHROPIC (claude-opus-5):")
print(" ", post("https://api.anthropic.com/v1/messages",
    {"model": "claude-opus-5", "max_tokens": 32, "messages": [{"role": "user", "content": "hola"}]},
    {"Content-Type": "application/json", "x-api-key": an, "anthropic-version": "2023-06-01"}))