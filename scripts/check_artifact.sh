#!/usr/bin/env bash
# Envoltorio: la verificación está en scripts/check_artifact.py (multiplataforma).
# Uso: scripts/check_artifact.sh [dir_resultados]
exec python3 "$(dirname "$0")/check_artifact.py" "$@"
