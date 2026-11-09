# Evaluación cruzada del artifact de Jonathan Valenzuela

> Evaluación inspirada en ACM Artifact Review & Badging v1.1. Se usó **únicamente** el
> artifact publicado en Zenodo, su README.md y sus archivos de configuración/automatización.
> Entorno común a las cuatro evaluaciones y procedimiento: [README.md](README.md).

## 1. Identificación

| Campo | Valor |
|---|---|
| Evaluador | Pier Miqueles |
| Autor del artifact evaluado | Jonathan Alexis Valenzuela Tapia |
| DOI / versión evaluada | [10.5281/zenodo.23891451](https://doi.org/10.5281/zenodo.23891451) · v1.0.0 · `matmul-benchmark-v1.0.0.zip` (MD5 `2dd162bed7a7507cdcf382460fc85643`, verificado) |
| Fecha de inicio / término | 2026-11-09 10:18 / 2026-11-09 12:07 (UTC−5) |
| Tiempo total invertido | ≈ 1 h 50 min (lectura 15 min · builds 3 min · pipeline 102 min) |

## 2. Entorno del evaluador

| Campo | Valor |
|---|---|
| CPU / núcleos | Intel Core Ultra 7 165H · 22 hilos |
| RAM | 30,8 GB |
| Sistema operativo / arquitectura | Fedora 42 (kernel 6.18.8) · x86_64 |
| Docker o Podman (versión) | Podman 5.8.2 rootless (vía adaptador `docker` → `podman`, ver §5) |
| Snakemake (versión) | 9.27.1 (de `requirements-lock.txt`), Python 3.13.13 en el host |

## 3. Registro de la reproducción

| Paso | Comando ejecutado | ¿Funcionó? | Tiempo | Observaciones |
|---|---|---|---|---|
| Descarga desde Zenodo | `scripts/descargar_zenodo.py 10.5281/zenodo.23891451 …` | Sí | < 1 min | MD5 coincide |
| Build imagen C++ | `docker build --pull -f docker/Dockerfile.cpp -t matmul-cpp .` | Sí | 84 s | `ubuntu:24.04` + g++ |
| Build imagen Go | `docker build --pull -f docker/Dockerfile.go -t matmul-go .` | Sí | 27 s | |
| Build imagen Java | `docker build --pull -f docker/Dockerfile.java -t matmul-java .` | Sí | 38 s | OpenJDK 21 |
| Build imagen Python | `docker build --pull -f docker/Dockerfile.python -t matmul-python .` | Sí | 31 s | |
| Build imagen análisis | — | n/a | — | El análisis corre en el host (no hay imagen de análisis) |
| Instalar dependencias | `pip install -r requirements-lock.txt` (venv) | Sí | ≈ 1 min | Lockfile para Python 3.12; instaló sin conflictos en 3.13 |
| Ejecución pipeline Snakemake | `snakemake --cores 1 --forceall` | Sí | 6 145 s (102 min) | 8/8 pasos; `validated.ok` generado |

## 4. Verificaciones obligatorias del módulo

| Verificación | Sí/No | Evidencia |
|---|---|---|
| Los 4 contenedores se ejecutan correctamente | Sí | `results/logs/{cpp,go,java,python}.log` sin errores |
| Se generan `cpp.csv`, `go.csv`, `python.csv`, `java.csv` | Sí | `results/` |
| Los 4 archivos tienen columnas `language,N,repetition,time_seconds` | Sí | Encabezado verificado |
| Se integran automáticamente en `benchmark.csv` (120 filas) | Sí | Regla `merge_results`; 12 celdas × 10 repeticiones |
| Se ejecuta el análisis estadístico (ANOVA 2 factores + Tukey) | Sí | `anova.csv`, `tukey_hsd.csv`, `analysis.md` |
| Se generan tablas y gráficos | Sí | `descriptive.csv`, `benchmark_by_language.png` |
| Checksums idénticos a los publicados | **Sí** | `diff` de `results/checksums.txt` publicado vs reproducido: idénticos (12 líneas, 4 lenguajes × 3 N) |

## 5. Problemas encontrados

| # | Tipo | Descripción | Modificación necesaria | Severidad |
|---|---|---|---|---|
| 1 | Ambigüedad doc. | El README (v1.0.0 archivada) dice "DOI Zenodo pendiente de publicación" y pide no citar DOI, aunque el registro ya existe. | Ninguna para ejecutar; actualizar README/CITATION.cff con el DOI. | Baja |
| 2 | Ambigüedad doc. | Se indica ejecutar "desde la carpeta `mm/`", que no existe en el zip (la raíz es `matmul-benchmark-v1.0.0/`). | Ejecutar desde la raíz del zip. | Baja |
| 3 | Ambigüedad doc. | La estructura del README lista `docker/Dockerfile.all`, `docker/run_lang.sh` y `results_semana2_windows/`, que no vienen en el depósito. | Ninguna (no se usan en el pipeline). | Baja |
| 4 | Otro (entorno) | `scripts/run_container.py` invoca `docker` fijo; el evaluador no tiene acceso al daemon Docker. | Adaptador `docker` → `podman --cgroup-manager=cgroupfs` en el `PATH` del evaluador (sin tocar el artifact). | Baja (propia del evaluador) |
| 5 | Otro | Con `snakemake --cores 1` (comando del README) no se re-mide nada porque `results/` ya contiene las salidas publicadas; hay que leer más abajo que se requiere `--forceall`. | Usar `--forceall`, como indica §"Pipeline automatizado". | Baja |
| 6 | Otro | En `benchmark_by_language.png` el color de algunas cajas no coincide con la leyenda (p. ej. Python N=500 aparece naranja). | Ninguna. | Baja |

## 6. Comparación de resultados

Comparación con el mismo procedimiento para publicado y reproducido (script del evaluador
[`scripts/comparar_evaluacion.py`](../../scripts/comparar_evaluacion.py)) y con el análisis propio del autor.

| Indicador | Publicado | Reproducido | ¿Concuerda? |
|---|---|---|---|
| p‑valor efecto lenguaje (segundos, análisis del autor) | 3,74 × 10⁻¹⁵³ | 1,06 × 10⁻¹⁰⁹ | Sí (significativo) |
| p‑valor interacción lenguaje×N (segundos, análisis del autor) | 2,90 × 10⁻¹⁴⁸ | 2,87 × 10⁻¹⁰⁵ | Sí (significativa) |
| p‑valor interacción lenguaje×N (log10, análisis del evaluador) | 0,148 | 5,2 × 10⁻³¹ | **No** (el autor no reporta esta escala) |
| Decisión sobre H₀ | Se rechaza | Se rechaza | Sí |
| Tukey del autor (segundos, por N) | Solo Python difiere; C++/Go/Java n.s. en los 3 N | Idéntico | Sí |
| Orden de lenguajes N=500 | cpp < go < java < python | cpp < java < go < python | Sí, salvo par go–java no significativo (Tukey del autor) |
| Orden de lenguajes N=1000 | cpp < go < java < python | cpp < java < go < python | Ídem |
| Orden de lenguajes N=1500 | cpp < go < java < python | cpp < java < go < python | Ídem |
| Razón Python/C++ N=1500 | 67,9 | 132,8 | Mismo orden de magnitud (10²) |
| Razón Java/C++ N=1500 | 1,35 | 1,68 | Sí |
| Razón Go/C++ N=1500 | 1,24 | 1,98 | Sí |

## 7. Dictamen (badges ACM)

| Badge | ¿Otorgaría? | Justificación |
|---|---|---|
| Artifacts Available | **Sí** | Depósito en Zenodo con DOI, licencias MIT (código) y CC BY 4.0 (datos), CITATION.cff. El README no muestra el DOI. |
| Artifacts Evaluated – Functional | **Sí** | Documentado, completo y ejecutable con un comando; validación automática de filas y checksums entre lenguajes. |
| Artifacts Evaluated – Reusable | **Sí** | Lockfile de dependencias, `config.yaml` con tamaños/repeticiones/semilla/α, DATASHEET FAIR, scripts modulares. Mejorable: imágenes base por etiqueta (`ubuntu:24.04` + `apt`) y no por digest. |
| Results Reproduced | **Sí** | Checksums idénticos; mismas decisiones del ANOVA y del Tukey del autor; Python siempre significativamente más lento; las diferencias C++/Go/Java siguen sin ser significativas. |

## 8. Recomendaciones al autor

- Agregar el DOI al README y a CITATION.cff, y quitar la referencia a la carpeta `mm/` y a los archivos que no vienen en el depósito.
- Fijar las imágenes base por digest y las versiones de `g++`/`golang-go`/`openjdk` instaladas con `apt` (hoy dependen del día del build).
- Reportar también el ANOVA en log10: en esta reproducción la interacción en log10 sí es significativa, mientras que en la versión publicada no lo era (p = 0,148). Es una conclusión sensible al hardware.
- Corregir los colores de las cajas del gráfico para que coincidan con la leyenda.
