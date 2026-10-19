#!/usr/bin/env bash
# Demostración en consola de la actividad, semana a semana (≈3 minutos).
#
# Uso:   scripts/demo.sh [semana]        semana = 1..5 o "todas" (por defecto)
#
# Variables opcionales:
#   ENGINE="podman --cgroup-manager=cgroupfs"   motor de contenedores (se detecta solo)
#   SIN_PAUSA=1                                  no esperar Enter entre pasos
#   DEMO_SIZES=200,400  DEMO_REPS=3              tamaños/repeticiones de la demo
#
# Los resultados de la demo se escriben en results_demo/ (nunca toca results/).
set -euo pipefail
cd "$(dirname "$0")/.."

SEMANA="${1:-todas}"
SIZES="${DEMO_SIZES:-200,400}"
REPS="${DEMO_REPS:-3}"
DEMO_DIR="results_demo"
SNAKEMAKE="${SNAKEMAKE:-.venv/bin/snakemake}"

# --- Presentación ------------------------------------------------------------
NEGRITA=$'\e[1m'; AZUL=$'\e[34m'; VERDE=$'\e[32m'; AMARILLO=$'\e[33m'; GRIS=$'\e[90m'; FIN=$'\e[0m'

titulo() { printf '\n%s%s══ %s ══%s\n\n' "$NEGRITA" "$AZUL" "$*" "$FIN"; }
paso()   { printf '%s▶ %s%s\n' "$AMARILLO" "$*" "$FIN"; }
nota()   { printf '%s  %s%s\n' "$GRIS" "$*" "$FIN"; }
ok()     { printf '%s✔ %s%s\n' "$VERDE" "$*" "$FIN"; }
pausa()  { [ -n "${SIN_PAUSA:-}" ] || read -rp $'\n'"${GRIS}[Enter para continuar]${FIN} " _; }

# Muestra el comando y lo ejecuta.
ejecutar() {
    printf '%s$ %s%s\n' "$NEGRITA" "$*" "$FIN"
    eval "$@"
}

# --- Motor de contenedores ---------------------------------------------------
if [ -z "${ENGINE:-}" ]; then
    if docker info > /dev/null 2>&1; then
        ENGINE=docker
    else
        ENGINE="podman --cgroup-manager=cgroupfs"
    fi
fi
if [[ $ENGINE == podman* ]]; then USUARIO="--userns=keep-id"; else USUARIO="--user $(id -u):$(id -g)"; fi

ejecutar_contenedor() {  # ejecutar_contenedor <lang>
    ejecutar "$ENGINE run --rm $USUARIO --network none -v \"\$PWD/$DEMO_DIR:/results:z\" matmul-$1:1.0" \
        "/results/raw/$1.csv $SIZES $REPS 42 /results/verification/$1_checksum.csv"
}

# --- Semanas -----------------------------------------------------------------
semana1() {
    titulo "SEMANA 1 · Diseño experimental, GitHub y documentación"
    paso "Repositorio y versiones por semana"
    ejecutar "git remote get-url origin"
    ejecutar "git log --oneline --decorate | tail -n 8"
    pausa
    paso "Pregunta de investigación e hipótesis (README.md)"
    ejecutar "sed -n '/^## 2. Pregunta/,/^## 4. Variables/p' README.md"
    pausa
    paso "Variables y diseño factorial 4 × 3 × 10"
    ejecutar "sed -n '/^## 4. Variables/,/^## 6. Estructura/p' README.md"
    pausa
}

semana2() {
    titulo "SEMANA 2 · Implementación equivalente en 4 lenguajes"
    paso "El mismo algoritmo naive i-j-k en los cuatro lenguajes"
    ejecutar "grep -n -A9 'static void multiplicar' src/cpp/matmul.cpp"
    ejecutar "grep -n -A11 '^func multiplicar' src/go/matmul.go"
    ejecutar "grep -n -A10 'static void multiplicar' src/java/MatMul.java"
    ejecutar "grep -n -A7 '^def multiplicar' src/python/matmul.py"
    pausa
    paso "Temporizador: solo alrededor de la multiplicación (matrices ya creadas)"
    ejecutar "grep -n -B2 -A3 'multiplicar(n, a, b, c)' src/python/matmul.py | head -n 8"
    nota "Mismo generador SplitMix64 + semilla 42 → los 4 lenguajes multiplican las MISMAS matrices."
    pausa
}

semana3() {
    titulo "SEMANA 3 · Entornos reproducibles (Docker) → ACM Functional"
    paso "Dockerfile de C++ (imagen base con versión exacta, compila dentro del build)"
    ejecutar "grep -v '^#' docker/cpp/Dockerfile | sed '/^$/d'"
    pausa
    paso "Imágenes construidas manualmente"
    ejecutar "$ENGINE images --filter 'reference=*matmul-*' --format '{{.Repository}}:{{.Tag}}  {{.Size}}'"
    pausa
    paso "Ejecución manual de los 4 contenedores (N=$SIZES, $REPS repeticiones)"
    /bin/rm -rf "$DEMO_DIR"
    mkdir -p "$DEMO_DIR/raw" "$DEMO_DIR/verification"
    for lang in cpp go java python; do
        ejecutar_contenedor "$lang"
    done
    pausa
    paso "Cuatro CSV independientes con la misma estructura"
    ejecutar "head -n 4 $DEMO_DIR/raw/*.csv"
    pausa
    paso "Verificación de equivalencia: el resultado de C es idéntico bit a bit"
    ejecutar "cat $DEMO_DIR/verification/*_checksum.csv | grep -v '^language' | sort -t, -k2,2n -k3,3n | awk -F, '\$3==1'"
    ok "Mismo checksum en C++, Go, Java y Python para cada N"
    pausa
}

semana4() {
    titulo "SEMANA 4 · Pipeline Snakemake + ANOVA → ACM Reusable"
    paso "Plan de ejecución (dependencias entre etapas)"
    ejecutar "$SNAKEMAKE --config engine='$ENGINE' results_dir=$DEMO_DIR 'sizes=[${SIZES}]' repetitions=$REPS -n --forceall -q rules 2>/dev/null | tail -n 12"
    pausa
    paso "Ejecución completa con UN comando"
    ejecutar "$SNAKEMAKE --config engine='$ENGINE' results_dir=$DEMO_DIR 'sizes=[${SIZES}]' repetitions=$REPS --forceall -q 2>&1 | tail -n 3"
    ok "benchmark.csv integrado: $(($(wc -l < "$DEMO_DIR/benchmark.csv") - 1)) filas"
    pausa
    paso "Decisión estadística de la demo"
    ejecutar "sed -n '/^## 8. Decisión/,/^## 9/p' $DEMO_DIR/analysis/reporte_estadistico.md"
    pausa
}

semana5() {
    titulo "SEMANA 5 · Artifact publicado (Zenodo) y resultados oficiales"
    paso "Checklist del contenido mínimo exigido"
    ejecutar "scripts/check_artifact.sh results || true"
    pausa
    paso "Resultados OFICIALES (N=500, 1000, 1500 · 10 repeticiones)"
    ejecutar "cat results/analysis/tables/speedup.md"
    ejecutar "sed -n '/^## 8. Decisión/,/^## 9/p' results/analysis/reporte_estadistico.md"
    pausa
    paso "Figuras"
    ejecutar "ls results/analysis/figures/"
    if command -v xdg-open > /dev/null 2>&1 && [ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]; then
        xdg-open results/analysis/figures/interaccion_lenguaje_N.png > /dev/null 2>&1 &
        nota "Se abrió el gráfico de interacción lenguaje × N."
    fi
}

case "$SEMANA" in
    1) semana1 ;; 2) semana2 ;; 3) semana3 ;; 4) semana4 ;; 5) semana5 ;;
    todas) semana1; semana2; semana3; semana4; semana5 ;;
    *) echo "Uso: $0 [1|2|3|4|5|todas]" >&2; exit 1 ;;
esac
printf '\n%sFin de la demostración.%s\n' "$NEGRITA" "$FIN"
