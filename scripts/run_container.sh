#!/usr/bin/env bash
# Ejecuta manualmente (sin Snakemake) el benchmark de un lenguaje dentro de su contenedor.
# Uso: scripts/run_container.sh <cpp|go|java|python> [tamaños] [repeticiones] [semilla] [dir_resultados]
# Variables opcionales: ENGINE=docker|podman (por defecto docker), TAG=1.0
set -euo pipefail

LANG_ID="$1"
TAMANOS="${2:-500,1000,1500}"
REPS="${3:-10}"
SEMILLA="${4:-42}"
RESULTADOS="$(realpath -m "${5:-results}")"
ENGINE="${ENGINE:-docker}"
TAG="${TAG:-1.0}"

mkdir -p "$RESULTADOS/raw" "$RESULTADOS/verification" "$RESULTADOS/logs"

# Los archivos generados quedan a nombre del usuario actual.
if [[ $ENGINE == podman* ]]; then
    USUARIO=(--userns=keep-id)
else
    USUARIO=(--user "$(id -u):$(id -g)")
fi

$ENGINE run --rm "${USUARIO[@]}" \
    --network none \
    -v "$RESULTADOS:/results:z" \
    "matmul-${LANG_ID}:${TAG}" \
    "/results/raw/${LANG_ID}.csv" "$TAMANOS" "$REPS" "$SEMILLA" \
    "/results/verification/${LANG_ID}_checksum.csv" \
    2> >(tee "$RESULTADOS/logs/${LANG_ID}.log" >&2)
