#!/usr/bin/env bash
# Construye MANUALMENTE las cinco imágenes a partir de los Dockerfile del artifact.
# No descarga imágenes del benchmark desde registros: solo las imágenes base oficiales.
# Uso: scripts/build_images.sh   (variables: ENGINE=docker|podman, TAG=1.0)
set -euo pipefail
ENGINE="${ENGINE:-docker}"
TAG="${TAG:-1.0}"
cd "$(dirname "$0")/.."
for lang in cpp go java python analysis; do
    echo ">> Construyendo matmul-${lang}:${TAG}" >&2
    $ENGINE build -f "docker/${lang}/Dockerfile" -t "matmul-${lang}:${TAG}" .
done
$ENGINE images --filter "reference=matmul-*"
