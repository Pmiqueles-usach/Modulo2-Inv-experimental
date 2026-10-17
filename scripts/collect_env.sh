#!/usr/bin/env bash
# Registra las características del entorno de ejecución del experimento.
# Uso: scripts/collect_env.sh <salida.md> [motor: docker|podman] [tag]
set -euo pipefail

SALIDA="${1:-results/environment/environment.md}"
MOTOR="${2:-docker}"
TAG="${3:-1.0}"
mkdir -p "$(dirname "$SALIDA")"

# Ejecuta un comando dentro de la imagen indicada (sin usar el ENTRYPOINT del benchmark).
en_imagen() {
    local imagen="$1"; shift
    $MOTOR run --rm --entrypoint sh "$imagen" -c "$*" 2>&1 | head -n 3 || echo "(no disponible)"
}

{
    echo "# Entorno de ejecución"
    echo
    echo "Registrado: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo
    echo "## Host"
    echo
    echo '```'
    echo "Procesador:        $(lscpu | sed -n 's/^Model name:[[:space:]]*//p')"
    echo "Núcleos lógicos:   $(nproc)"
    echo "Arquitectura:      $(uname -m)"
    echo "RAM total:         $(free -h | awk '/^Mem:/ {print $2}')"
    echo "Sistema operativo: $(. /etc/os-release && echo "$PRETTY_NAME")"
    echo "Kernel:            $(uname -r)"
    echo "Gobernador CPU:    $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo 'n/d')"
    echo "Motor contenedores: $($MOTOR --version)"
    echo '```'
    echo
    echo '```'
    lscpu | grep -E '^(Model name|Socket|Core|Thread|CPU\(s\)|L1d|L2|L3|CPU max MHz|CPU min MHz)' || true
    echo '```'
    echo
    echo "## Imágenes y versiones de lenguajes"
    echo
    for lang in cpp go java python analysis; do
        img="matmul-${lang}:${TAG}"
        echo "### ${img}"
        echo
        echo '```'
        echo "Image ID: $($MOTOR image inspect --format '{{.Id}}' "$img" 2>/dev/null || echo 'no construida')"
        case "$lang" in
            cpp)      en_imagen "$img" "g++ --version | head -n1; echo 'Flags: -O2 -std=c++17 -ffp-contract=off'; cat /etc/os-release | grep PRETTY" ;;
            go)       en_imagen "$img" "go version; cat /etc/os-release | grep PRETTY" ;;
            java)     en_imagen "$img" "java -version 2>&1; echo 'JVM flags: -Xms1g -Xmx1g'" ;;
            python)   en_imagen "$img" "python --version; cat /etc/os-release | grep PRETTY" ;;
            analysis) en_imagen "$img" "python --version; pip freeze | grep -Ei 'numpy|pandas|scipy|statsmodels|matplotlib'" ;;
        esac
        echo '```'
        echo
    done
} > "$SALIDA"
echo "Entorno registrado en $SALIDA" >&2
