# Evaluación cruzada del artifact de Jorge Fornes

> Evaluación inspirada en ACM Artifact Review & Badging v1.1. Se usó **únicamente** el
> artifact publicado en Zenodo, su README.md y sus archivos de configuración/automatización.
> Entorno común a las cuatro evaluaciones y procedimiento: [README.md](README.md).

## 1. Identificación

| Campo | Valor |
|---|---|
| Evaluador | Pier Miqueles |
| Autor del artifact evaluado | Jorge Fornes (cuenta GitHub `jffp-alt`) |
| DOI / versión evaluada | [10.5281/zenodo.23987654](https://doi.org/10.5281/zenodo.23987654) · v1.0.1 · `matrix-benchmark-v1.0.1.zip` (MD5 `bdc1b7a330b966f142cebd8a2f8a4194`, verificado) |
| Fecha de inicio / término | 2026-11-09 10:18 / 2026-11-09 12:00 (UTC−5) |
| Tiempo total invertido | ≈ 1 h 55 min (lectura 15 min · builds 2 min · pipeline 95 min) |

## 2. Entorno del evaluador

| Campo | Valor |
|---|---|
| CPU / núcleos | Intel Core Ultra 7 165H · 22 hilos |
| RAM | 30,8 GB |
| Sistema operativo / arquitectura | Fedora 42 (kernel 6.18.8) · x86_64 |
| Docker o Podman (versión) | Podman 5.8.2 rootless (vía adaptador `docker` → `podman`, ver §5) |
| Snakemake (versión) | 9.27.1 (última disponible: el artifact no fija versión), Python 3.13.13 en el host |

## 3. Registro de la reproducción

| Paso | Comando ejecutado | ¿Funcionó? | Tiempo | Observaciones |
|---|---|---|---|---|
| Descarga desde Zenodo | `scripts/descargar_zenodo.py 10.5281/zenodo.23987654 …` | Sí | < 1 min | MD5 coincide. El README pide clonar GitHub; se usó el zip de Zenodo |
| Build de las 4 imágenes | `./build_docker.sh` | Sí (2.º intento) | 108 s en total | 1.er intento: el script viene **sin permiso de ejecución** (`Permission denied`); el README sí indica `chmod +x`. Además, Podman no resuelve `gcc:13` (ver §5) |
| Build imagen análisis | — | n/a | — | El análisis corre en el host |
| Instalar dependencias | `pip install -r analysis/requirements.txt` + `pip install snakemake` | Sí | ≈ 1 min | Versiones solo con `>=`; Snakemake no está en el archivo de requisitos |
| Ejecución pipeline Snakemake | `snakemake --cores 1 --forceall` (con el venv activo, porque la regla `analysis` llama a `python`) | Sí | 5 706 s (95 min) | 19/19 pasos |

## 4. Verificaciones obligatorias del módulo

| Verificación | Sí/No | Evidencia |
|---|---|---|
| Los 4 contenedores se ejecutan correctamente | Sí | 12 trabajos `run_benchmark` sin errores |
| Se generan `cpp.csv`, `go.csv`, `python.csv`, `java.csv` | Sí | `results/` |
| Los 4 archivos tienen columnas `language,N,repetition,time_seconds` | Sí | Encabezado escrito por `merge_language` |
| Se integran automáticamente en `benchmark.csv` (120 filas) | Sí | Regla `merge_all` (no valida el número de filas; se contó: 120, 12 × 10) |
| Se ejecuta el análisis estadístico (ANOVA 2 factores + Tukey) | Sí | `anova_results.txt`, `tukey_results.txt` |
| Se generan tablas y gráficos | Sí | `descriptive_stats.csv` y 7 PNG |
| Checksums idénticos a los publicados | **Parcial** | No se publican checksums; el pipeline solo los imprime en stderr y no los compara. En el log, C++ y Go coinciden exactamente; Java coincide en los dígitos impresos. Python difiere en el 15.º–16.º dígito significativo (p. ej. N=1000: …583,6396 vs …583,6567), probablemente porque `sum()` de Python ≥ 3.12 usa suma compensada |

## 5. Problemas encontrados

| # | Tipo | Descripción | Modificación necesaria | Severidad |
|---|---|---|---|---|
| 1 | Otro (diseño) | **C++ se compila con `-O0`** mientras Go y Java usan sus compiladores optimizados por defecto. Además, el `multiply` de C++ reserva C dentro de la zona medida, con `vector<vector<double>>`. Por eso C++ resulta 3–7 veces más lento que Go y Java, lo que contradice la equivalencia de condiciones entre lenguajes. Está documentado como decisión intencional. | Ninguna para ejecutar. | **Alta** (validez de la comparación) |
| 2 | Otro | No hay verificación automática de equivalencia numérica: el checksum se imprime en stderr y se pierde en el log. | Revisar el log a mano. | Media |
| 3 | Dependencia | `analysis/requirements.txt` sin versiones fijas (`>=`) y sin `snakemake`; imágenes base por etiqueta móvil (`gcc:13`, `golang:1.22`, `eclipse-temurin:21`, `python:3.12-slim`). | Instalar Snakemake aparte. | Media |
| 4 | Ambigüedad doc. | El README dice "DOI: Pendiente" y el paso 1 manda a clonar GitHub en lugar de usar el depósito archivado. | Usar el zip de Zenodo. | Baja |
| 5 | Error | `build_docker.sh`, `run_experiment.sh`, etc. vienen sin bit de ejecución en el zip. | `chmod +x` (documentado). | Baja |
| 6 | Otro | Tamaños, repeticiones y semilla están fijos en el `Snakefile` (no hay archivo de configuración). La regla `analysis` usa `shell: python …`, que depende del intérprete activo. | Activar el venv antes de ejecutar. | Baja |
| 7 | Ambigüedad doc. | Los resultados publicados se midieron de forma nativa en Windows/MinGW; el pipeline Docker usa otro compilador y otro SO. | Ninguna. | Baja |
| 8 | Otro (entorno) | `docker` fijo en el `shell:`; Podman exige nombre de registro calificado. | Adaptador `docker` → `podman` y `unqualified-search-registries` en el entorno del evaluador. | Baja (propia del evaluador) |

## 6. Comparación de resultados

| Indicador | Publicado | Reproducido | ¿Concuerda? |
|---|---|---|---|
| p‑valor efecto lenguaje (segundos, análisis del autor) | 2,16 × 10⁻¹⁶⁴ | 1,1 × 10⁻¹³² | Sí |
| p‑valor interacción lenguaje×N (segundos) | 5,08 × 10⁻¹⁵⁹ | 8,9 × 10⁻¹²⁸ | Sí |
| p‑valor interacción lenguaje×N (log10, análisis del evaluador) | 6,2 × 10⁻⁶⁹ | 1,2 × 10⁻⁴⁸ | Sí |
| Decisión sobre H₀ | Se rechaza | Se rechaza | Sí |
| Tukey global del autor (colapsando N) | C++, Go, Java n.s. entre sí; los 3 ≠ Python | Idéntico | Sí |
| Hallazgo destacado en el README: "Go vs Java **sí** difiere en N=1500" | Sí (p < 0,001) | **No** (p = 1,0) | **No** |
| Orden de lenguajes N=500 | java < go < cpp < python | java < go < cpp < python | Sí |
| Orden de lenguajes N=1000 | java < go < cpp < python | java < go < cpp < python | Sí |
| Orden de lenguajes N=1500 | go < java < cpp < python | go < java < cpp < python | Sí (go–java n.s. en la reproducción) |
| Razón Python/C++ N=1500 | 6,70 | 5,90 | Sí |
| Razón Java/C++ N=1500 | 0,44 | 0,29 | Sí (C++ más lento por `-O0`) |
| Razón Go/C++ N=1500 | 0,28 | 0,28 | Sí |

## 7. Dictamen (badges ACM)

| Badge | ¿Otorgaría? | Justificación |
|---|---|---|
| Artifacts Available | **Sí** | Zenodo con DOI y licencia MIT. El README archivado no incluye el DOI y remite a GitHub. |
| Artifacts Evaluated – Functional | **Sí, con reservas** | Ejecutable de punta a punta y genera todo lo exigido. Pero la equivalencia entre implementaciones no se verifica automáticamente y C++ no se compila en condiciones comparables (`-O0`). |
| Artifacts Evaluated – Reusable | **No** | Dependencias sin fijar (Snakemake ni siquiera está listado), imágenes base sin fijar, parámetros fijos en el código y scripts sin permiso de ejecución. Readaptarlo exige editar el `Snakefile`. |
| Results Reproduced | **Sí (conclusiones generales)** | Mismas decisiones del ANOVA, el mismo orden de lenguajes en los 3 N y el mismo Tukey global. **No** se reproduce el hallazgo puntual Go ≠ Java en N=1500 que destaca el README. |

## 8. Recomendaciones al autor

- Compilar C++ con `-O2` (o justificar por qué el resto de los lenguajes sí se optimiza) y sacar la reserva de C de la zona medida; en el estado actual, el experimento compara configuraciones de compilación además de lenguajes.
- Comparar automáticamente los checksums en una regla de Snakemake y documentar la tolerancia (suma compensada en Python ≥ 3.12).
- Fijar versiones en `requirements.txt` (incluido Snakemake) y fijar las imágenes base por digest; mover N, repeticiones y semilla a un `config.yaml`.
- Poner el DOI en el README y cambiar el "Paso 1" para que use el depósito de Zenodo.
