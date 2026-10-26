#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verificar_equivalencia.py — Comprueba que cada copia reescrita con IA hace lo
mismo que su programa de referencia (equivalencia funcional observable).

Para cada copia CODE_IAL_* / CODE_IAI_* se compilan y ejecutan el original y
la copia con los mismos conjuntos de entrada por teclado (stdin) y se compara
la salida de consola. Una copia se considera equivalente solo si la salida
coincide en todos los conjuntos de entrada.

Requisitos:
  C#   : .NET SDK 8 o superior (comando `dotnet`)
  Java : JDK 17 o superior (comandos `javac` y `java`)

Uso (desde la carpeta SimilCode-Benchmark):
  python copias_ia/verificar_equivalencia.py
  python copias_ia/verificar_equivalencia.py --solo CODE_IAI_CS_004

Resultado: copias_ia/equivalencia.csv (una fila por copia y conjunto de entrada)
y copias_ia/equivalencia_resumen.csv (una fila por copia).
Las copias no equivalentes se regeneran con generar_copias_ia.py --solo <id>.
Si el programa de referencia no es determinista (por ejemplo, usa Random sin
semilla), el estado es 'revision_manual': un docente compara el codigo y, si la
copia es equivalente, escribe 1 en 'equivalent' y el motivo en 'nota'.
"""
from __future__ import annotations

import argparse
import csv
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Conjuntos de entrada: solo enteros (evita diferencias por el separador
# decimal de la configuracion regional). Sobran lineas a proposito: un
# programa que lee menos, ignora el resto.
INPUT_SETS = {
    "E1": "\n".join(["1", "2", "3", "4", "5", "6", "7", "8", "0", "0", "0", "0"] * 3) + "\n",
    "E2": "\n".join(["2", "10", "20", "30", "40", "5", "3", "0", "0", "0", "0", "0"] * 3) + "\n",
    "E3": "\n".join(["3", "7", "15", "1", "9", "12", "4", "0", "0", "0", "0", "0"] * 3) + "\n",
}
TIMEOUT = 15


def norm_output(s):
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in s.split("\n")).strip()


# ---------------------------------------------------------------- Java -------
def java_build(src_path, workdir):
    code = open(src_path, encoding="utf-8-sig").read()
    m = re.search(r"public\s+(?:final\s+|abstract\s+)*class\s+(\w+)", code)
    fname = (m.group(1) if m else "Main") + ".java"
    os.makedirs(os.path.join(workdir, "out"), exist_ok=True)
    with open(os.path.join(workdir, fname), "w", encoding="utf-8") as fh:
        fh.write(code)
    p = subprocess.run(["javac", "-encoding", "UTF-8", "-d", "out", fname],
                       cwd=workdir, capture_output=True, text=True)
    if p.returncode != 0:
        return None, p.stderr[-500:]
    # Clase con main: la que declara 'static void main'
    mains = []
    for cls_m in re.finditer(r"class\s+(\w+)", code):
        rest = code[cls_m.end():]
        nxt = re.search(r"\bclass\s+\w+", rest)
        body = rest[: nxt.start()] if nxt else rest
        if re.search(r"static\s+void\s+main\s*\(", body):
            mains.append(cls_m.group(1))
    pkg = re.search(r"^\s*package\s+([\w.]+)\s*;", code, re.M)
    main_cls = (mains[0] if mains else (m.group(1) if m else "Main"))
    if pkg:
        main_cls = pkg.group(1) + "." + main_cls
    cmd = ["java", "-Dfile.encoding=UTF-8", "-Dstdout.encoding=UTF-8",
           "-cp", "out", main_cls]
    return cmd, ""


# ---------------------------------------------------------------- C# ---------
_CS_PROJECT = """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>disable</ImplicitUsings>
    <Nullable>disable</Nullable>
    <TreatWarningsAsErrors>false</TreatWarningsAsErrors>
    <InvariantGlobalization>false</InvariantGlobalization>
  </PropertyGroup>
</Project>
"""


def cs_build(src_path, workdir):
    with open(os.path.join(workdir, "Runner.csproj"), "w", encoding="utf-8") as fh:
        fh.write(_CS_PROJECT)
    shutil.copy(src_path, os.path.join(workdir, "Program.cs"))
    env = dict(os.environ, DOTNET_CLI_TELEMETRY_OPTOUT="1", DOTNET_NOLOGO="1")
    p = subprocess.run(["dotnet", "build", "-c", "Release", "-o", "out", "-nologo",
                        "-v", "q"], cwd=workdir, capture_output=True, text=True, env=env)
    if p.returncode != 0:
        return None, (p.stdout + p.stderr)[-500:]
    return ["dotnet", os.path.join(workdir, "out", "Runner.dll")], ""


def run(cmd, stdin_text, cwd):
    try:
        p = subprocess.run(cmd, input=stdin_text, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=TIMEOUT, cwd=cwd)
        return norm_output(p.stdout), p.returncode, False
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        return norm_output(out), None, True


def build(src_path, workdir):
    return (cs_build if src_path.endswith(".cs") else java_build)(src_path, workdir)


def reference_for(copy_path):
    base = os.path.basename(copy_path)
    m = re.match(r"CODE_IA[LIP]_(CS|JAVA)_(\d{3})\.(cs|java)$", base)
    lang, num, ext = m.groups()
    return os.path.join(ROOT, "csharp" if ext == "cs" else "java", f"CODE_IDENT_{lang}_{num}.{ext}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--solo", default=None)
    args = ap.parse_args()
    only = set(x.strip() for x in args.solo.split(",")) if args.solo else None

    copies = sorted(glob.glob(os.path.join(ROOT, "csharp", "CODE_IA?_CS_*.cs")) +
                    glob.glob(os.path.join(ROOT, "java", "CODE_IA?_JAVA_*.java")))
    if only:
        copies = [c for c in copies if os.path.splitext(os.path.basename(c))[0] in only]
    if not copies:
        sys.exit("No hay copias CODE_IAL_/CODE_IAI_ en csharp/ ni java/.")

    det_rows, sum_rows = [], []
    ref_cache = {}
    for cp in copies:
        cid = os.path.splitext(os.path.basename(cp))[0]
        ref = reference_for(cp)
        rid = os.path.splitext(os.path.basename(ref))[0]
        with tempfile.TemporaryDirectory() as wref, tempfile.TemporaryDirectory() as wcp:
            if rid not in ref_cache:
                cmd_r, err_r = build(ref, wref)
                outs, nondet = {}, False
                if cmd_r:
                    for k, txt in INPUT_SETS.items():
                        outs[k] = run(cmd_r, txt, wref)
                    # Programa no determinista (p. ej. Random sin semilla): dos
                    # ejecuciones con la misma entrada dan salidas distintas.
                    nondet = run(cmd_r, INPUT_SETS["E1"], wref)[0] != outs["E1"][0]
                ref_cache[rid] = (cmd_r is not None, err_r, outs, nondet)
            ok_r, err_r, outs_r, nondet_r = ref_cache[rid]
            cmd_c, err_c = build(cp, wcp)
            statuses = []
            for k, txt in INPUT_SETS.items():
                if not ok_r:
                    st, note = "error_compilacion_referencia", err_r[:200]
                elif cmd_c is None:
                    st, note = "error_compilacion_copia", err_c[:200]
                else:
                    out_c, rc_c, to_c = run(cmd_c, txt, wcp)
                    out_r, rc_r, to_r = outs_r[k]
                    if nondet_r:
                        st, note = "revision_manual", "la referencia no es determinista; compare a mano"
                    elif out_c == out_r:
                        st, note = ("iguales" if not (to_c or to_r) else "iguales_hasta_tiempo_agotado"), ""
                    else:
                        st = "distintas"
                        a, b = out_r.split("\n"), out_c.split("\n")
                        i = next((n for n in range(min(len(a), len(b))) if a[n] != b[n]), min(len(a), len(b)))
                        note = f"primera diferencia en linea {i + 1}: ref={a[i] if i < len(a) else '<fin>'!r} copia={b[i] if i < len(b) else '<fin>'!r}"[:200]
                statuses.append(st)
                det_rows.append({"copy_id": cid, "reference_id": rid, "input_set": k,
                                 "status": st, "detail": note})
        eq = all(s.startswith("iguales") for s in statuses)
        manual = any(s == "revision_manual" for s in statuses)
        sum_rows.append({"copy_id": cid, "reference_id": rid,
                         "equivalent": int(eq), "statuses": ";".join(statuses), "nota": ""})
        label = "EQUIVALENTE" if eq else ("REVISION MANUAL" if manual else "NO equivalente")
        print(f"{cid}: {label} ({', '.join(statuses)})")

    # Con --solo se conservan las filas previas de las demas copias.
    done_ids = {r["copy_id"] for r in sum_rows}
    for name, rows in (("equivalencia.csv", det_rows), ("equivalencia_resumen.csv", sum_rows)):
        p = os.path.join(HERE, name)
        if os.path.isfile(p):
            with open(p, encoding="utf-8", newline="") as fh:
                old = [r for r in csv.DictReader(fh) if r["copy_id"] not in done_ids]
            rows[:0] = old
    det_rows.sort(key=lambda r: (r["copy_id"], r["input_set"]))
    sum_rows.sort(key=lambda r: r["copy_id"])
    with open(os.path.join(HERE, "equivalencia.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["copy_id", "reference_id", "input_set", "status", "detail"])
        w.writeheader(); w.writerows(det_rows)
    with open(os.path.join(HERE, "equivalencia_resumen.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["copy_id", "reference_id", "equivalent", "statuses", "nota"])
        w.writeheader(); w.writerows(sum_rows)
    n_eq = sum(int(r["equivalent"]) for r in sum_rows)
    print(f"\nEquivalentes: {n_eq} de {len(sum_rows)}. Detalle en copias_ia/equivalencia.csv")


if __name__ == "__main__":
    main()
