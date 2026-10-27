# Autoevaluación según ACM Artifact Review and Badging (v1.1)

Fuente: https://www.acm.org/publications/policies/artifact-review-and-badging-current
(consultada el 2026‑10‑17).

## 1. Terminología ACM (armonizada con NISO)

| Concepto | Equipo | Montaje experimental | En este artifact |
|---|---|---|---|
| **Repeatability** | mismo | mismo | El autor re‑ejecuta `snakemake --forceall` en su máquina |
| **Reproducibility** | distinto | mismo (artifacts del autor) | Evaluación cruzada de la Semana 5 con este artifact |
| **Replicability** | distinto | distinto (artifacts propios) | Otro estudiante implementa el benchmark desde cero y compara |

## 2. Badges y criterios

ACM define tres badges independientes: **Artifacts Evaluated** (Functional o Reusable),
**Artifacts Available** y **Results Validated** (Reproduced o Replicated).

### 2.1 Artifacts Evaluated – Functional (objetivo Semana 3)

> *Los artifacts están documentados, son consistentes, completos, ejercitables e incluyen
> evidencia adecuada de verificación y validación.*

| Criterio ACM | Evidencia en el artifact | Estado |
|---|---|---|
| **Documented**: inventario de artifacts y descripción suficiente para ejercitarlos | README §3.6 (inventario), §5.4 y §6.4 (instrucciones paso a paso), `docs/PROTOCOLO.md` | ✅ |
| **Consistent**: relevantes y contribuyen a los resultados principales | Cada archivo participa en la cadena código → CSV → análisis | ✅ |
| **Complete**: todos los componentes incluidos | Código de 4 lenguajes, 5 Dockerfile, scripts, configuración; sin componentes propietarios | ✅ |
| **Exercisable**: los scripts se ejecutan y los datos se pueden manipular | `docker run` por lenguaje genera `<lang>.csv`; CSV legibles con cualquier herramienta | ✅ |
| **Verificación y validación** | `results/verification/equivalence_report.md`: las 4 implementaciones producen la misma matriz **bit a bit**; `merge_results.py` valida columnas, duplicados y tiempos | ✅ |

### 2.2 Artifacts Evaluated – Reusable (objetivo Semana 4)

> *Calidad que excede significativamente la funcionalidad mínima: muy bien documentados y
> estructurados para facilitar reutilización y readaptación; se respetan las normas de la
> comunidad.*

| Aspecto | Evidencia | Estado |
|---|---|---|
| Automatización completa | `workflow/Snakefile`: un único comando ejecuta contenedores → CSV → `benchmark.csv` → ANOVA/Tukey → tablas/figuras | ✅ |
| Parametrización | `config/config.yaml` (N, repeticiones, semilla, motor, directorio) sobrescribible con `--config` | ✅ |
| Entornos fijados | Imágenes base con versión exacta; dependencias de análisis con versión exacta (`docker/analysis/requirements.txt`) | ✅ |
| Interfaz común y extensible | Mismo CLI para los 4 programas; guía para agregar lenguajes (README §10) | ✅ |
| Normas de la comunidad | Estructura estándar de Snakemake (`workflow/`, `config/`, perfiles), OCI labels, CITATION.cff, licencias SPDX, datasheet FAIR | ✅ |
| Prueba rápida | `results_dir=results_smoke 'sizes=[50,100]'` | ✅ |
| Portabilidad del motor | Docker o Podman sin cambios en los Dockerfile | ✅ |

### 2.3 Artifacts Available (objetivo Semana 5)

> *Los artifacts se depositan en un repositorio de archivo público, con DOI o enlace con
> identificador único. Las páginas personales no son aceptables; GitHub por sí solo no es un
> archivo permanente.*

| Requisito | Acción | Estado |
|---|---|---|
| Repositorio de archivo con plan de permanencia | Zenodo (CERN) mediante integración GitHub → release `v1.0.0` | ⏳ |
| DOI | Copiar DOI al README, CITATION.cff y README §7.5 | ⏳ |
| Contenido mínimo exigido por el módulo | Ver checklist en `docs/ZENODO.md` | ✅ preparado |

### 2.4 Results Validated – Reproduced (evaluación cruzada, Semana 5)

> *Los resultados principales son obtenidos por otra persona usando, en parte, los artifacts
> del autor. No se exige igualdad exacta: deben concordar dentro de una tolerancia aceptable y
> las diferencias no deben cambiar las conclusiones principales.*

Criterio de concordancia propuesto para este experimento (los tiempos absolutos dependen del
hardware, por lo que se evalúan las **conclusiones**):

1. Checksums idénticos a los publicados (equivalencia funcional: igualdad exacta).
2. Misma decisión sobre H₀ para el efecto del lenguaje (α = 0,05).
3. Misma decisión sobre la interacción lenguaje × N.
4. Mismo ordenamiento de lenguajes por tiempo medio en cada N (o diferencias explicadas por
   pares no significativos en Tukey).
5. Razones de tiempo respecto de C++ del mismo orden de magnitud.

Plantilla: [evaluacion-cruzada/PLANTILLA_EVALUACION.md](evaluacion-cruzada/PLANTILLA_EVALUACION.md).

## 3. Historial de autoevaluaciones

| Fecha | Semana | Badge objetivo | Resultado | Observaciones |
|---|---|---|---|---|
| 2026‑10‑17 | 1 | (discusión de criterios) | — | Criterios incorporados al diseño |
| 2026‑10‑17 | 3 | Functional | Cumple | Ejecución verificada con Podman 5.8 (Docker CLI equivalente) |
| 2026‑10‑17 | 4 | Reusable | Cumple | Pipeline completo verificado (`results_smoke` y `results`) |
| — | 5 | Available / Reproduced | Pendiente | Requiere DOI y revisor externo |
