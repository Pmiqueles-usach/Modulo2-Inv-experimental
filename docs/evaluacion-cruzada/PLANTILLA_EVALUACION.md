# Evaluación cruzada del artifact (inspirada en ACM Artifact Review & Badging)

> Copiar este archivo como `evaluacion-<apellido-evaluado>.md` y completarlo.
> El evaluador debe usar **únicamente** el artifact publicado en Zenodo, su README.md y los
> archivos de configuración/automatización incluidos.

## 1. Identificación

| Campo | Valor |
|---|---|
| Evaluador | |
| Autor del artifact evaluado | |
| DOI / versión evaluada | |
| Fecha de inicio / término | |
| Tiempo total invertido | |

## 2. Entorno del evaluador

| Campo | Valor |
|---|---|
| CPU / núcleos | |
| RAM | |
| Sistema operativo / arquitectura | |
| Docker o Podman (versión) | |
| Snakemake (versión) | |

## 3. Registro de la reproducción

| Paso | Comando ejecutado | ¿Funcionó? | Tiempo | Observaciones |
|---|---|---|---|---|
| Descarga desde Zenodo | | | | |
| Build imagen C++ | | | | |
| Build imagen Go | | | | |
| Build imagen Java | | | | |
| Build imagen Python | | | | |
| Build imagen análisis | | | | |
| Ejecución pipeline Snakemake | | | | |

## 4. Verificaciones obligatorias del módulo

| Verificación | Sí/No | Evidencia |
|---|---|---|
| Los 4 contenedores se ejecutan correctamente | | |
| Se generan `cpp.csv`, `go.csv`, `python.csv`, `java.csv` | | |
| Los 4 archivos tienen columnas `language,N,repetition,time_seconds` | | |
| Se integran automáticamente en `benchmark.csv` (120 filas) | | |
| Se ejecuta el análisis estadístico (ANOVA 2 factores + Tukey) | | |
| Se generan tablas y gráficos | | |
| Checksums idénticos a los publicados | | |

## 5. Problemas encontrados

| # | Tipo (dependencia faltante / error / ambigüedad doc. / otro) | Descripción | Modificación necesaria | Severidad (baja/media/alta) |
|---|---|---|---|---|
| 1 | | | | |

## 6. Comparación de resultados

| Indicador | Publicado | Reproducido | ¿Concuerda? |
|---|---|---|---|
| p‑valor efecto lenguaje (log10) | | | |
| p‑valor interacción lenguaje×N (log10) | | | |
| Decisión sobre H₀ | | | |
| Orden de lenguajes N=500 | | | |
| Orden de lenguajes N=1000 | | | |
| Orden de lenguajes N=1500 | | | |
| Razón Python/C++ N=1500 | | | |
| Razón Java/C++ N=1500 | | | |
| Razón Go/C++ N=1500 | | | |

## 7. Dictamen (badges ACM)

| Badge | ¿Otorgaría? | Justificación |
|---|---|---|
| Artifacts Available | | |
| Artifacts Evaluated – Functional | | |
| Artifacts Evaluated – Reusable | | |
| Results Reproduced | | |

## 8. Recomendaciones al autor

-
