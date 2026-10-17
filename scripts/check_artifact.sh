#!/usr/bin/env bash
# Verifica que el artifact contenga todos los elementos exigidos por el módulo
# (checklist de publicación en Zenodo) y que los CSV tengan la estructura correcta.
# Uso: scripts/check_artifact.sh [dir_resultados]
set -uo pipefail
cd "$(dirname "$0")/.."
R="${1:-results}"
fallas=0

revisar() {  # revisar <descripción> <ruta>...
    local desc="$1"; shift
    for ruta in "$@"; do
        if [ ! -e "$ruta" ]; then
            printf '  [FALTA] %-45s %s\n' "$desc" "$ruta"; fallas=$((fallas + 1)); return
        fi
    done
    printf '  [ OK  ] %s\n' "$desc"
}

echo "== Contenido mínimo del artifact =="
revisar "Código fuente (4 lenguajes)" src/cpp/matmul.cpp src/go/matmul.go src/java/MatMul.java src/python/matmul.py
revisar "README.md" README.md
revisar "Dockerfile (4 lenguajes + análisis)" docker/{cpp,go,java,python,analysis}/Dockerfile
revisar "Pipeline Snakefile" workflow/Snakefile config/config.yaml
revisar "CSV por lenguaje" "$R"/raw/{cpp,go,python,java}.csv
revisar "benchmark.csv" "$R"/benchmark.csv
revisar "Análisis estadístico" "$R"/analysis/reporte_estadistico.md "$R"/analysis/tables/anova_tiempo.csv
revisar "Tablas y gráficos" "$R"/analysis/tables/descriptivos.csv "$R"/analysis/figures/boxplot_tiempos.png
revisar "Licencia" LICENSE LICENSE-DATA
revisar "Mini datasheet FAIR" docs/DATASHEET_FAIR.md
revisar "Registro del entorno" "$R"/environment/environment.md
revisar "Verificación de equivalencia" "$R"/verification/equivalence_report.md

echo "== Estructura de los CSV =="
for f in "$R"/raw/{cpp,go,python,java}.csv "$R"/benchmark.csv; do
    [ -f "$f" ] || continue
    cabecera=$(head -n1 "$f")
    filas=$(($(wc -l < "$f") - 1))
    if [ "$cabecera" = "language,N,repetition,time_seconds" ]; then
        printf '  [ OK  ] %-32s %4d filas\n' "$f" "$filas"
    else
        printf '  [ERROR] %-32s cabecera: %s\n' "$f" "$cabecera"; fallas=$((fallas + 1))
    fi
done

if grep -q "EQUIVALENTES" "$R/verification/equivalence_report.md" 2>/dev/null; then
    echo "  [ OK  ] Implementaciones equivalentes (checksums idénticos)"
else
    echo "  [ERROR] Equivalencia no verificada"; fallas=$((fallas + 1))
fi

if grep -q "PENDIENTE" README.md; then
    echo "  [AVISO] README.md aún no contiene el DOI de Zenodo"
fi

echo
[ "$fallas" -eq 0 ] && echo "Artifact completo." || echo "Elementos con problemas: $fallas"
exit "$fallas"
