# Semana 4 – Automatización y análisis estadístico

**Etiqueta git:** `semana-4` · **Objetivo ACM:** *Artifacts Evaluated – Reusable*

## Lo que pide el módulo

- Pipeline Snakemake que coordine la ejecución de los 4 contenedores (imágenes construidas
  manualmente; prohibido usar imágenes publicadas en registros).
- N = 500, 1000, 1500; 10 repeticiones; generar los 4 CSV; integrarlos en `benchmark.csv`.
- Ejecutar automáticamente el análisis estadístico (ANOVA de dos factores con interacción y
  Tukey HSD) y generar tablas y gráficos.
- Dependencias explícitas entre etapas; un único comando o secuencia mínima documentada.
- Revisión ACM orientada a *Reusable*.

## Entregables

| Entregable | Ubicación | Estado |
|---|---|---|
| Snakefile | [workflow/Snakefile](../../workflow/Snakefile) | ✅ |
| Perfil (ejecución secuencial) | [workflow/profiles/default/config.yaml](../../workflow/profiles/default/config.yaml) | ✅ |
| Parámetros | [config/config.yaml](../../config/config.yaml) | ✅ |
| Integración | [scripts/merge_results.py](../../scripts/merge_results.py) → `results/benchmark.csv` | ✅ |
| Análisis estadístico | [scripts/analysis.py](../../scripts/analysis.py) | ✅ |
| Imagen de análisis (versiones fijadas) | [docker/analysis/](../../docker/analysis/) | ✅ |
| Reporte, tablas y gráficos | [results/analysis/](../../results/analysis/) | ✅ |
| Autoevaluación *Reusable* | [ACM_BADGES.md §2.2](../ACM_BADGES.md) | ✅ |

## Reglas del pipeline y dependencias

| Regla | Entrada | Salida |
|---|---|---|
| `check_image` | imagen local `matmul-<x>:1.0` | marca temporal; **falla** si la imagen no fue construida |
| `run_benchmark` | imagen del lenguaje | `raw/<lang>.csv`, `verification/<lang>_checksum.csv` |
| `merge` | 4 CSV | `benchmark.csv` |
| `verify_equivalence` | 4 checksums | `equivalence_report.md` |
| `analysis` | `benchmark.csv` | tablas, figuras, `reporte_estadistico.md` |
| `environment` | imágenes | `environment.md` |

Los benchmarks usan el recurso `benchmark_slot=1`: nunca corren dos lenguajes a la vez,
aunque se invoque Snakemake con más núcleos (evita contención de CPU).

## Análisis estadístico

- Modelo: `time ~ C(language) * C(N)`, ANOVA tipo II, con η² parcial.
- Supuestos: Shapiro‑Wilk sobre residuos y Levene (mediana) entre las 12 celdas.
- Dado que los tiempos difieren en órdenes de magnitud (heterocedasticidad), se ajusta el mismo
  modelo sobre **log10(tiempo)** (efectos multiplicativos) y se usa Kruskal‑Wallis por N como
  contraste no paramétrico.
- Post‑hoc Tukey HSD: lenguaje global, lenguaje dentro de cada N y las 12 combinaciones.

## Comando único

```bash
.venv/bin/snakemake            # (o --config engine=podman)
```

## Demostración (guion)

1. `snakemake -n` (plan de ejecución) y `snakemake --dag`.
2. Ejecución con una configuración corta: `--config results_dir=results_demo 'sizes=[100,200]' repetitions=3`.
3. Mostrar `benchmark.csv`, `reporte_estadistico.md` y figuras.
4. Mostrar que borrar `results_demo/benchmark.csv` y re‑ejecutar solo recalcula lo necesario.
