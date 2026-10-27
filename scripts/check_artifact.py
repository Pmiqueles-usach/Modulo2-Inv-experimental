"""Verifica que el artifact contenga todos los elementos exigidos por el módulo
(checklist de publicación en Zenodo) y que los CSV tengan la estructura correcta.

Funciona en Linux, macOS y Windows (solo usa la biblioteca estándar de Python).

Uso: python scripts/check_artifact.py [dir_resultados]
Código de salida: número de elementos con problemas (0 = artifact completo).
"""

import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CABECERA = "language,N,repetition,time_seconds"
LANGS = ["cpp", "go", "python", "java"]


def main() -> int:
    os.chdir(RAIZ)
    r = sys.argv[1] if len(sys.argv) > 1 else "results"
    fallas = 0

    def revisar(desc, *rutas):
        nonlocal fallas
        for ruta in rutas:
            if not Path(ruta).exists():
                print(f"  [FALTA] {desc:<45} {ruta}")
                fallas += 1
                return
        print(f"  [ OK  ] {desc}")

    print("== Contenido mínimo del artifact ==")
    revisar("Código fuente (4 lenguajes)", "src/cpp/matmul.cpp", "src/go/matmul.go",
            "src/java/MatMul.java", "src/python/matmul.py")
    revisar("README.md", "README.md")
    revisar("Dockerfile (4 lenguajes + análisis)",
            *[f"docker/{l}/Dockerfile" for l in ["cpp", "go", "java", "python", "analysis"]])
    revisar("Pipeline Snakefile", "workflow/Snakefile", "config/config.yaml")
    revisar("CSV por lenguaje", *[f"{r}/raw/{l}.csv" for l in LANGS])
    revisar("benchmark.csv", f"{r}/benchmark.csv")
    revisar("Análisis estadístico", f"{r}/analysis/reporte_estadistico.md",
            f"{r}/analysis/tables/anova_tiempo.csv")
    revisar("Tablas y gráficos", f"{r}/analysis/tables/descriptivos.csv",
            f"{r}/analysis/figures/boxplot_tiempos.png")
    revisar("Licencia", "LICENSE", "LICENSE-DATA")
    revisar("Mini datasheet FAIR", "docs/DATASHEET_FAIR.md")
    revisar("Registro del entorno", f"{r}/environment/environment.md")
    revisar("Verificación de equivalencia", f"{r}/verification/equivalence_report.md")

    print("== Estructura de los CSV ==")
    for f in [f"{r}/raw/{l}.csv" for l in LANGS] + [f"{r}/benchmark.csv"]:
        if not Path(f).is_file():
            continue
        lineas = Path(f).read_text(encoding="utf-8").splitlines()
        if lineas and lineas[0].strip() == CABECERA:
            print(f"  [ OK  ] {f:<32} {len(lineas) - 1:4d} filas")
        else:
            print(f"  [ERROR] {f:<32} cabecera: {lineas[0] if lineas else '(vacío)'}")
            fallas += 1

    reporte = Path(f"{r}/verification/equivalence_report.md")
    if reporte.is_file() and "EQUIVALENTES" in reporte.read_text(encoding="utf-8"):
        print("  [ OK  ] Implementaciones equivalentes (checksums idénticos)")
    else:
        print("  [ERROR] Equivalencia no verificada")
        fallas += 1

    if "PENDIENTE" in Path("README.md").read_text(encoding="utf-8"):
        print("  [AVISO] README.md aún no contiene el DOI de Zenodo")

    print()
    print("Artifact completo." if fallas == 0 else f"Elementos con problemas: {fallas}")
    return fallas


if __name__ == "__main__":
    sys.exit(main())
