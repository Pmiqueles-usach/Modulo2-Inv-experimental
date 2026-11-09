# Evaluación cruzada del artifact de Alejandro Pirez

> Evaluación inspirada en ACM Artifact Review & Badging v1.1. Se usó **únicamente** el
> artifact publicado en Zenodo, su README.md y sus archivos de configuración/automatización.
> Entorno común a las cuatro evaluaciones y procedimiento: [README.md](README.md).

## 1. Identificación

| Campo | Valor |
|---|---|
| Evaluador | Pier Miqueles |
| Autor del artifact evaluado | Alejandro Jesús Pirez Prendes |
| DOI / versión evaluada | [10.5281/zenodo.23954875](https://doi.org/10.5281/zenodo.23954875) · versión 1.0 · `benchmark-matrices-zenodo.zip` (MD5 `94cabaea5bf021591c542dcb719bb9b0`, verificado) |
| Fecha de inicio / término | 2026-11-09 10:18 / 2026-11-09 11:31 (UTC−5) |
| Tiempo total invertido | ≈ 1 h 25 min (lectura 15 min · builds 2 min · pipeline 66 min) |

## 2. Entorno del evaluador

| Campo | Valor |
|---|---|
| CPU / núcleos | Intel Core Ultra 7 165H · 22 hilos |
| RAM | 30,8 GB |
| Sistema operativo / arquitectura | Fedora 42 (kernel 6.18.8) · x86_64 |
| Docker o Podman (versión) | Podman 5.8.2 rootless (vía adaptador `docker` → `podman`, ver §5) |
| Snakemake (versión) | 9.27.1 (de `requirements.txt`), Python 3.13.13 en el host |

## 3. Registro de la reproducción

| Paso | Comando ejecutado | ¿Funcionó? | Tiempo | Observaciones |
|---|---|---|---|---|
| Descarga desde Zenodo | `scripts/descargar_zenodo.py https://zenodo.org/records/23954875 …` | Sí | < 1 min | MD5 coincide |
| Build imagen C++ | `docker build -t matrix-bench-cpp:1.0 cpp` | Sí (2.º intento) | 4 s | 1.er intento: Podman no resuelve el nombre corto `gcc:14.2` (ver §5) |
| Build imagen Go | `docker build -t matrix-bench-go:1.0 go` | Sí | 38 s | |
| Build imagen Java | `docker build -t matrix-bench-java:1.0 java` | Sí (2.º intento) | 53 s | Ídem con `eclipse-temurin:17-jdk` |
| Build imagen Python | `docker build -t matrix-bench-python:1.0 python` | Sí | 9 s | |
| Build imagen análisis | — | n/a | — | El análisis corre en el host |
| Instalar dependencias | `python -m pip install -r requirements.txt` (venv) | Sí | ≈ 1 min | Versiones fijadas; README pide Python 3.12, funcionó con 3.13 |
| Ejecución pipeline Snakemake | `python -m snakemake --cores 1 --resources machine=1` | Sí | 3 964 s (66 min) | 19/19 pasos, sin modificar nada |

## 4. Verificaciones obligatorias del módulo

| Verificación | Sí/No | Evidencia |
|---|---|---|
| Los 4 contenedores se ejecutan correctamente | Sí | 12 corridas (lenguaje × N), cada una validada por `docker_run._validate` |
| Se generan `cpp.csv`, `go.csv`, `python.csv`, `java.csv` | Sí | `results/` |
| Los 4 archivos tienen columnas `language,N,repetition,time_seconds` | Sí | Validado por el propio pipeline |
| Se integran automáticamente en `benchmark.csv` (120 filas) | Sí | Regla `integrate_benchmark` |
| Se ejecuta el análisis estadístico (ANOVA 2 factores + Tukey) | Sí | `anova.csv`, `anova_log10.csv`, `tukey_hsd.csv`, `tukey_log10.csv`, `supuestos.csv` |
| Se generan tablas y gráficos | Sí | `descriptivos.csv`, `figuras/{interaccion,interaccion_segundos,boxplot}.png` |
| Checksums idénticos a los publicados | **No aplica** | El artifact no calcula ni publica checksums del resultado: no hay evidencia automática de que las 4 implementaciones produzcan la misma matriz C |

## 5. Problemas encontrados

| # | Tipo | Descripción | Modificación necesaria | Severidad |
|---|---|---|---|---|
| 1 | Otro | No existe verificación de equivalencia numérica entre lenguajes (checksum o comparación de C). La equivalencia se afirma solo por revisión de código. | Ninguna para ejecutar; recomendable agregarla. | Media |
| 2 | Ambigüedad doc. | Los CSV y el análisis publicados provienen de una **medición local en Windows sin contenedores** (ENVIRONMENT.md), no del pipeline Docker que se pide reproducir. | Ninguna; se compara local (autor) vs contenedor (evaluador). | Media |
| 3 | Otro | La corrida por defecto escribe en `results/` y **sobrescribe** los datos archivados de la copia de trabajo (el README lo advierte). | Trabajar sobre una copia; recomendable usar `results_dir` distinto por defecto. | Baja |
| 4 | Dependencia | Imágenes base por etiqueta móvil (`gcc:14.2`, `golang:1.26`, `eclipse-temurin:17-jdk`, `python:3.12-slim`), sin digest. Podman exige nombre calificado (`docker.io/…`). | Configurar `unqualified-search-registries=["docker.io"]` en el entorno del evaluador. | Baja (propia de Podman) |
| 5 | Otro (entorno) | El pipeline invoca `docker` fijo. | Adaptador `docker` → `podman` en el `PATH` del evaluador. | Baja (propia del evaluador) |

## 6. Comparación de resultados

| Indicador | Publicado (local, Windows) | Reproducido (contenedores, Linux) | ¿Concuerda? |
|---|---|---|---|
| p‑valor efecto lenguaje (log10) | 3,7 × 10⁻¹⁵⁴ | 1,0 × 10⁻¹⁵⁴ | Sí |
| p‑valor interacción lenguaje×N (log10) | 8,7 × 10⁻²⁴ | 3,3 × 10⁻¹⁹ | Sí |
| Decisión sobre H₀ | Se rechaza (segundos y log10) | Se rechaza (segundos y log10) | Sí |
| Tukey en segundos (análisis del autor) | Solo Python difiere; C++/Go/Java n.s. en los 3 N | Idéntico | Sí |
| Tukey log10, pares n.s. | N=500 go–java · N=1000 go–java · N=1500 ninguno | N=500 ninguno · N=1000 go–java · N=1500 go–java | Parcial (go–java es el par frontera) |
| Orden de lenguajes N=500 | cpp < go < java < python | cpp < java < go < python | Parcial (go/java se invierten) |
| Orden de lenguajes N=1000 | cpp < java < go < python | cpp < java < go < python | Sí |
| Orden de lenguajes N=1500 | cpp < go < java < python | cpp < java < go < python | Parcial (go/java se invierten) |
| Razón Python/C++ N=1500 | 99,4 | 74,9 | Mismo orden de magnitud |
| Razón Java/C++ N=1500 | 1,63 | 1,49 | Sí |
| Razón Go/C++ N=1500 | 1,38 | 1,61 | Sí |

## 7. Dictamen (badges ACM)

| Badge | ¿Otorgaría? | Justificación |
|---|---|---|
| Artifacts Available | **Sí** | Zenodo con DOI, que además aparece en el README archivado; licencia MIT y DATASHEET. |
| Artifacts Evaluated – Functional | **Sí** | El pipeline corrió completo sin modificar el artifact. Valida encabezado, filas y repeticiones de cada contenedor y serializa las mediciones con un candado. |
| Artifacts Evaluated – Reusable | **Sí** | `config.yaml`, prueba corta (`--config smoke=true`), dependencias fijadas, ANOVA en dos escalas con supuestos y etiquetas OCI en las imágenes. Le falta la verificación de equivalencia numérica (§5.1). |
| Results Reproduced | **Sí** | Mismas decisiones del ANOVA (segundos y log10) y del Tukey en segundos. C++ es el más rápido y Python el más lento en todos los N. El orden Go/Java cambia, pero es el par con diferencias pequeñas (n.s. en segundos). |

## 8. Recomendaciones al autor

- Imprimir y comparar automáticamente un checksum de C en las 4 implementaciones (por ejemplo, en `collect_language`).
- Publicar en Zenodo también una medición hecha con el pipeline en contenedores, para que lo archivado y lo reproducible sean el mismo procedimiento.
- Usar por defecto un `results_dir` distinto de `results/`, para no sobrescribir los datos archivados.
- Fijar las imágenes base por digest.
