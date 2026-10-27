# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
[versionado semántico](https://semver.org/lang/es/).

## [1.0.0] – Semana 5 (pendiente de publicación en Zenodo)
- Reproducible también en **Windows** (Docker Desktop + PowerShell): el Snakefile lanza los
  contenedores con `subprocess` (sin bash); `collect_env` y `check_artifact` pasan a Python;
  nuevos `scripts/build_images.ps1`, `run_container.ps1` y `reproducir.ps1`; `.gitattributes`
  fija finales de línea LF. Guía paso a paso en el README (§2.2 y una sección por semana).
- README reescrito como guía completa semana a semana (§3–§7), con paso a paso para Linux y
  Windows, resultados esperados, guía de replicación desde cero (§9) y solución de problemas (§11).
- Metadatos de publicación (`.zenodo.json`, `CITATION.cff`), licencias, datasheet FAIR.
- Script `check_artifact.sh` y plantilla de evaluación cruzada.

## [0.4.0] – Semana 4
- Pipeline Snakemake (`workflow/Snakefile`) con perfil secuencial y configuración.
- Integración `benchmark.csv`, ANOVA de dos factores, Tukey HSD, Kruskal‑Wallis, tablas y gráficos.
- Imagen `matmul-analysis` con dependencias fijadas.

## [0.3.0] – Semana 3
- Dockerfile para C++, Go, Java y Python con imágenes base versionadas.
- Instrucciones de construcción/ejecución manual; autoevaluación *Functional*.

## [0.2.0] – Semana 2
- Implementaciones equivalentes en C++, Go, Java y Python (SplitMix64, row‑major, i‑j‑k).
- Verificación de equivalencia por checksum; registro del entorno; protocolo.

## [0.1.0] – Semana 1
- README inicial: objetivo, pregunta, hipótesis, variables y diseño experimental.
- Comentarios sobre ACM Artifact Review & Badging; presentación de la Semana 1.
