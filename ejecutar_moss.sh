#!/usr/bin/env bash
# ============================================================================
# ejecutar_moss.sh
# ----------------------------------------------------------------------------
# Ejecuta el protocolo de comparacion con Moss en modo cohorte, con los mismos
# parametros que se emplearon en el estudio, y descarga los informes.
#
# El cliente Perl `moss` NO se distribuye con este repositorio, por dos razones.
# Es codigo de Stanford, entregado individualmente a cada solicitante, y cada
# copia incorpora el identificador de quien la pidio. Publicar una copia ajena
# no ahorraria ningun paso: para ejecutar Moss hace falta un identificador
# propio, y quien lo solicita recibe con el su propia copia del script.
#
# Solicitalo escribiendo a  moss-request@cs.stanford.edu  siguiendo las
# instrucciones publicadas por Stanford. Cuando lo recibas, coloca el archivo
# `moss` en la raiz de este repositorio y ejecuta este guion.
#
# Requiere un entorno Unix. En Windows, WSL:  wsl --install -d Ubuntu
#
# Uso:
#   bash ejecutar_moss.sh
#   bash ejecutar_moss.sh --solo csharp
# ============================================================================

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MOSS="$RAIZ/moss"
TRABAJO="$RAIZ/baselines_work/cohorte"
SOLO="${2:-}"

rojo()  { printf '\033[31m%s\033[0m\n' "$*" >&2; }
info()  { printf '  %s\n' "$*"; }

# --- 1. El cliente tiene que estar presente ---------------------------------
if [[ ! -f "$MOSS" ]]; then
    rojo "No encuentro el cliente 'moss' en la raiz del repositorio."
    cat >&2 <<'AYUDA'

  El cliente Perl de Moss no se distribuye con este repositorio: es codigo de
  Stanford y cada copia lleva dentro el identificador de su solicitante.

  Para obtener el tuyo:

    1. Escribe a  moss-request@cs.stanford.edu  siguiendo las instrucciones
       publicadas por Stanford para el registro.
    2. Recibiras un script llamado `moss` con tu propio `$userid=`.
    3. Coloca ese archivo en la raiz de este repositorio.
    4. Vuelve a ejecutar este guion.

  IMPORTANTE: ese identificador es una credencial. No lo publiques ni versiones
  el archivo `moss`; el `.gitignore` de este repositorio ya lo excluye. Si el
  numero llega a aparecer en un sitio publico, solicita otro: retirarlo del
  lugar donde aparecio no revierte la exposicion.

AYUDA
    exit 1
fi

# --- 2. Tiene que llevar un identificador propio ----------------------------
if ! grep -q '\$userid *= *[0-9]\{4,\}' "$MOSS"; then
    rojo "El archivo 'moss' no contiene un identificador valido en \$userid."
    rojo "Comprueba que es el script original que te envio Stanford."
    exit 1
fi

# --- 3. No debe estar versionado --------------------------------------------
# Comprobacion barata que evita el accidente mas probable de este repositorio.
if git -C "$RAIZ" ls-files --error-unmatch moss >/dev/null 2>&1; then
    rojo "El archivo 'moss' esta VERSIONADO en este repositorio."
    rojo "Contiene tu identificador. Retiralo antes de continuar:"
    rojo "    git rm --cached moss  &&  echo moss >> .gitignore"
    exit 1
fi

chmod u+x "$MOSS"

if [[ ! -d "$TRABAJO" ]]; then
    rojo "No encuentro $TRABAJO."
    rojo "Genera primero el arbol de trabajo:  python baselines.py preparar"
    exit 1
fi

# --- 4. Ejecucion -----------------------------------------------------------
# Parametros del estudio, que deben mantenerse para que los resultados sean
# comparables con los reportados:
#   -d        cada directorio es una entrega independiente (modo cohorte)
#   -m 10     descuento de plantilla; valor por defecto, equivalente al de Dolos
#   -n 1000   amplia el numero de coincidencias mostradas (por defecto 250)
#   sin -b    no se suministra archivo base, igual que a JPlag y a Dolos
ejecutar() {
    local lenguaje="$1" ext="$2" salida="$3"
    local dir="$TRABAJO/$lenguaje"
    [[ -d "$dir" ]] || { rojo "No existe $dir"; return 1; }

    info "Enviando la cohorte de $lenguaje al servidor de Stanford..."
    local url
    url="$("$MOSS" -l "$lenguaje" -d -m 10 -n 1000 \
                   -c "SimilCode cohorte $lenguaje" \
                   "$dir"/*/*."$ext" | tail -n 1)"

    if [[ ! "$url" =~ ^http ]]; then
        rojo "Moss no devolvio una URL. Salida recibida: $url"
        return 1
    fi

    info "URL de resultados: $url"
    curl -fsS -o "$RAIZ/$salida" "$url"
    info "Informe guardado en $salida"
    printf '%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$lenguaje" "$url" \
        >> "$RAIZ/moss_urls.tsv"
}

echo "Protocolo de Moss, modo cohorte"
[[ "$SOLO" == "java"   ]] || ejecutar csharp cs   moss_cs.html
[[ "$SOLO" == "csharp" ]] || ejecutar java   java moss_java.html

cat <<'FIN'

Listo. Las URL de resultados quedan registradas en moss_urls.tsv; caducan con
el tiempo, de modo que los informes HTML descargados son la evidencia
archivable.

Siguiente paso, para integrar estos resultados con los de JPlag y Dolos:

  python baselines.py parsear --pares baselines_work/pares.csv \
      --entrada moss:cohorte:moss_cs.html moss:cohorte:moss_java.html \
      --out baselines_raw.csv --faltantes-cero
  python baselines.py evaluar --in baselines_raw.csv --tol-identico 5

FIN