#!/usr/bin/env bash
# ejecutar_nicad.sh — Experimento PENDIENTE (no ejecutado en la sesion de analisis).
# NiCad 7 (Roy y Cordy, 2008) sobre las mismas cohortes que Moss, JPlag y Dolos.
# Ejecutar en WSL (Ubuntu) desde la carpeta SimilCode-Benchmark:
#   bash experimentos_pendientes/ejecutar_nicad.sh
# Requisitos: gcc, make, curl. Instala OpenTxl 11.3.7 y NiCad en ~/nicad (sin sudo).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
W="$HOME/nicad"; mkdir -p "$W"; cd "$W"
if [ ! -x "$W/txl/bin/txl" ]; then
	curl -sSL -o txl.tgz https://github.com/CordyJ/OpenTxl/releases/download/v11.3.7/opentxl-11.3.7-linux-x64.tar.gz
	tar xzf txl.tgz && rm -rf txl && mv opentxl-11.3.7-linux-x64 txl
	sed -i "s#TXLBIN=/usr/local/bin#TXLBIN=$W/txl/bin#; s#TXLLIB=/usr/local/lib/txl#TXLLIB=$W/txl/lib#" txl/bin/txlc txl/bin/txl2c txl/bin/txlp
fi
export PATH="$W/txl/bin:$PATH"
[ -d Open-NiCad ] || git clone --depth 1 https://github.com/CordyJ/Open-NiCad
cd Open-NiCad && make >/dev/null && cd ..
# Cohortes: un directorio por lenguaje con los archivos de los pares de cada corrida.
python3 "$ROOT/experimentos_pendientes/nicad_resultados.py" prepare --out "$W/cohortes"
for c in "$W"/cohortes/*; do
	lang=$(basename "$c" | cut -d_ -f1)    # java o cs
	( cd Open-NiCad && ./nicad functions "$lang" "$c" default ) || true
done
python3 "$ROOT/experimentos_pendientes/nicad_resultados.py" collect --work "$W/cohortes"
