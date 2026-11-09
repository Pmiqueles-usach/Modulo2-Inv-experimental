# Evaluación cruzada del artifact de Joel Fuertes

> Evaluación inspirada en ACM Artifact Review & Badging v1.1. Se usó **únicamente** el
> artifact publicado en Zenodo, su README.md y sus archivos de configuración/automatización.
> Entorno común a las cuatro evaluaciones y procedimiento: [README.md](README.md).

## 1. Identificación

| Campo | Valor |
|---|---|
| Evaluador | Pier Miqueles |
| Autor del artifact evaluado | Joel Fuertes |
| DOI / versión evaluada | [10.5281/zenodo.23988249](https://doi.org/10.5281/zenodo.23988249) · `artifact_multiplicacion_matrices_v1.0.0.zip` (MD5 `ec4f95fc84fd5b7fbabe4bc8d4e1f38b`, verificado) |
| Fecha de inicio / término | 2026-11-09 10:17 / 2026-11-09 12:18 (UTC−5) |
| Tiempo total invertido | ≈ 2 h 10 min (lectura 20 min · builds 2 min · pipeline 113 min) |

## 2. Entorno del evaluador

| Campo | Valor |
|---|---|
| CPU / núcleos | Intel Core Ultra 7 165H · 22 hilos |
| RAM | 30,8 GB |
| Sistema operativo / arquitectura | Fedora 42 (kernel 6.18.8) · x86_64 (Linux nativo, no WSL) |
| Docker o Podman (versión) | Podman 5.8.2 rootless (vía adaptador `docker` → `podman`, ver §5) |
| Snakemake (versión) | 9.27.1 (de `requirements.txt`), Python 3.13.13 en el host |

## 3. Registro de la reproducción

| Paso | Comando ejecutado | ¿Funcionó? | Tiempo | Observaciones |
|---|---|---|---|---|
| Descarga desde Zenodo | `scripts/descargar_zenodo.py 10.5281/zenodo.23988249 …` | Sí | < 1 min | MD5 coincide |
| Build imagen C++ | `docker build -f 01_docker/cpp/Dockerfile -t matrices-cpp:semana4 .` | Sí (2.º intento) | 59 s | Base fijada por digest (`gcc@sha256:…`); Podman pidió registro calificado (ver §5) |
| Build imagen Go | `docker build -f 01_docker/go/Dockerfile -t matrices-go:semana4 .` | Sí | 45 s | `GOMAXPROCS=1` |
| Build imagen Java | `docker build -f 01_docker/java/Dockerfile -t matrices-java:semana4 .` | Sí (2.º intento) | 15 s | `-XX:ActiveProcessorCount=1 -XX:+UseSerialGC` |
| Build imagen Python | `docker build -f 01_docker/python/Dockerfile -t matrices-python:semana4 .` | Sí | 9 s | |
| Build imagen análisis | — | n/a | — | El análisis corre en el host |
| Instalar dependencias | `python -m pip install -r requirements.txt` (venv) | Sí | ≈ 1 min | Versiones completamente fijadas |
| Simulación | `snakemake --cores 1 --forceall --rerun-incomplete --dry-run` | Sí | < 5 s | 4 trabajos, como indica el README |
| Ejecución pipeline Snakemake | `snakemake --cores 1 --forceall --rerun-incomplete` | Sí | 6 767 s (113 min) | 4/4 pasos; "Experimento terminado: 120 mediciones verificadas" |

## 4. Verificaciones obligatorias del módulo

| Verificación | Sí/No | Evidencia |
|---|---|---|
| Los 4 contenedores se ejecutan correctamente | Sí | 12 bloques en orden aleatorizado (`05_resultados/orden.csv`), con `--cpus=1` |
| Se generan `cpp.csv`, `go.csv`, `python.csv`, `java.csv` | Sí | `05_resultados/` |
| Los 4 archivos tienen columnas `language,N,repetition,time_seconds` | Sí | Verificado por `revisar_archivos.py` |
| Se integran automáticamente en `benchmark.csv` (120 filas) | Sí | Regla `integrar` |
| Se ejecuta el análisis estadístico (ANOVA 2 factores + Tukey) | Sí (Tukey condicionado) | ANOVA en log10 (principal) y en segundos. Tukey **no se ejecuta** porque los diagnósticos de supuestos fallan, igual que en la versión publicada |
| Se generan tablas y gráficos | Sí | `08_analisis/`: 6 CSV/TXT y 3 PNG (cajas, interacción, diagnóstico) |
| Checksums idénticos a los publicados | **Sí (equivalente)** | Cada multiplicación se valida contra `control.txt` (suma total, C[0], centro, último) en los 4 lenguajes; ninguna falló. Los SHA-256 de entradas y fuentes se comparan contra las imágenes antes de medir |

## 5. Problemas encontrados

| # | Tipo | Descripción | Modificación necesaria | Severidad |
|---|---|---|---|---|
| 1 | Ambigüedad doc. | La guía (824 líneas) está escrita para Windows + WSL + Docker Desktop, con rutas fijas (`~/avance_semana4`, `~/entornos/semana4`). No hay instrucciones directas para Linux nativo ni un resumen de "comandos mínimos". | Adaptar las rutas a mano. | Baja |
| 2 | Otro (entorno) | `ejecutar.py` usa `docker info --format {{.OSType}}`, un campo que Podman no expone. | El adaptador del evaluador responde `linux` a esa consulta; el resto se traduce a `podman`. | Baja (propia del evaluador) |
| 3 | Dependencia | Los `FROM` usan solo digest, sin registro; Podman exige un nombre calificado. | `unqualified-search-registries=["docker.io"]` en el entorno del evaluador. | Baja (propia de Podman) |
| 4 | Otro | Tukey se omite si los diagnósticos fallan. La decisión es prudente, pero la pregunta de investigación (¿qué lenguajes difieren?) queda sin respuesta post-hoc en las dos corridas. | Ninguna. | Baja |
| 5 | Otro | El `--cpus=1` limita CPU por contenedor; con Podman rootless y cgroupfs puede que no se aplique (no hubo error). | Ninguna. | Baja |

## 6. Comparación de resultados

| Indicador | Publicado | Reproducido | ¿Concuerda? |
|---|---|---|---|
| p‑valor efecto lenguaje (log10, modelo principal del autor) | 1,51 × 10⁻¹⁷⁷ | 1,36 × 10⁻¹⁵⁷ | Sí |
| p‑valor interacción lenguaje×N (log10) | 2,07 × 10⁻⁷⁵ | 1,22 × 10⁻⁴⁸ | Sí |
| Decisión sobre H₀ | Se rechaza | Se rechaza | Sí |
| Decisión sobre Tukey | No se ejecuta (diagnósticos) | No se ejecuta (diagnósticos) | Sí |
| Orden de lenguajes N=500 | cpp < java < go < python | cpp < java < go < python | Sí |
| Orden de lenguajes N=1000 | java < cpp < go < python | cpp < java < go < python | **No** (cpp/java se invierten) |
| Orden de lenguajes N=1500 | cpp < java < go < python | cpp < go < java < python | **No** (go/java se invierten) |
| Razón Python/C++ N=1500 | 42,3 | 105,0 | Mismo orden de magnitud (10²) |
| Razón Java/C++ N=1500 | 1,05 | 1,91 | Parcial |
| Razón Go/C++ N=1500 | 1,27 | 1,47 | Sí |

Nota: el autor no hace afirmaciones sobre el orden entre C++, Go y Java, porque no ejecuta Tukey.
Con el Tukey uniforme del evaluador (log10, por N) todos los pares resultan significativos,
tanto en los datos publicados como en los reproducidos. Por lo tanto, el orden entre los
lenguajes compilados **depende del hardware**: con las mismas imágenes, en su equipo C++ tardó
11,6 s (N=1500) y en el del evaluador 3,7 s.

## 7. Dictamen (badges ACM)

| Badge | ¿Otorgaría? | Justificación |
|---|---|---|
| Artifacts Available | **Sí** | Zenodo con DOI, licencia MIT y DATASHEET FAIR. |
| Artifacts Evaluated – Functional | **Sí** | Corrió completo con los comandos del README. Verifica fuentes, entradas e imágenes (SHA-256) y valida cada multiplicación contra matrices de control. |
| Artifacts Evaluated – Reusable | **Sí** | Imágenes base fijadas por digest, dependencias completamente fijadas, registro automático del equipo y de las versiones, orden aleatorizado con semilla y calentamientos. Mejorable: guía muy atada a Windows/WSL. |
| Results Reproduced | **Sí** | Todas las conclusiones declaradas por el autor se reproducen: efectos de lenguaje, tamaño e interacción significativos en log10, y omisión de Tukey por supuestos. El orden entre C++/Go/Java no se reproduce, pero el autor no lo afirma. |

## 8. Recomendaciones al autor

- Agregar una sección breve "Linux nativo / Podman" con los comandos mínimos y sin rutas fijas de usuario.
- Usar `docker version`/`docker info --format '{{.OperatingSystem}}'`, o capturar el error, para que la comprobación del SO no dependa de un campo exclusivo de Docker.
- Escribir los `FROM` como `docker.io/library/gcc@sha256:…` para que funcionen también en Podman.
- Ofrecer una alternativa no paramétrica (o Games-Howell) cuando fallan los supuestos, para no dejar sin respuesta qué lenguajes difieren.
