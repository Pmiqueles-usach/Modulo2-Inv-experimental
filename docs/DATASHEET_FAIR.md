# Mini datasheet FAIR – Benchmark de multiplicación de matrices NxN

Inspirado en *Datasheets for Datasets* (Gebru et al., 2021) y los principios FAIR
(Wilkinson et al., 2016).

## 1. Identificación

| Campo | Valor |
|---|---|
| Título | Benchmark reproducible de multiplicación naive de matrices NxN en C++, Go, Java y Python |
| Versión | 1.0.0 |
| Identificador persistente | DOI Zenodo: **PENDIENTE** (Semana 5) |
| Repositorio de desarrollo | https://github.com/Pmiqueles-usach/Modulo2-Inv-experimental |
| Licencia de los datos | CC BY 4.0 (código: MIT) |
| Contacto | Pmiqueles-usach (GitHub) |

## 2. Motivación

Datos generados para responder si el lenguaje de implementación (C++, Go, Java, Python) produce
diferencias significativas en el tiempo de ejecución del algoritmo naive de multiplicación de
matrices y cómo esas diferencias varían con N. Generados como actividad del curso
*Experimentación Computacional* (Doctorado, USACH).

## 3. Composición

| Archivo | Filas | Descripción |
|---|---|---|
| `results/raw/cpp.csv`, `go.csv`, `java.csv`, `python.csv` | 30 c/u + encabezado | Tiempos por lenguaje |
| `results/benchmark.csv` | 120 + encabezado | Integración de los 4 archivos |
| `results/verification/<lang>_checksum.csv` | 30 c/u | Suma de C, C[0,0], C[N‑1,N‑1] (equivalencia) |
| `results/verification/equivalence_report.md` | — | Reporte de equivalencia funcional |
| `results/analysis/tables/*.csv|md` | — | Descriptivos, ANOVA, supuestos, Tukey, Kruskal |
| `results/analysis/figures/*.png` | — | Gráficos |
| `results/environment/environment.md` | — | Hardware, SO y versiones |

Diccionario de `benchmark.csv`:

| Columna | Tipo | Unidad | Dominio |
|---|---|---|---|
| `language` | categórica | — | {cpp, go, java, python} |
| `N` | entero | elementos por lado | {500, 1000, 1500} |
| `repetition` | entero | — | 1–10 |
| `time_seconds` | real ≥ 0 | segundos | precisión de 1 ns, 9 decimales |

Formato: CSV UTF‑8, separador coma, punto decimal, encabezado en la primera fila, sin
valores faltantes.

## 4. Procedencia (proceso de recolección)

1. Matrices A y B de N×N generadas con SplitMix64 (semilla 42), valores uniformes en [0,1).
2. Multiplicación naive i‑j‑k en cada lenguaje, ejecutada en contenedores construidos desde los
   Dockerfile del artifact (`docker/`), uno a la vez, sin red.
3. Tiempo medido con reloj monotónico solo alrededor de la multiplicación.
4. Pipeline Snakemake (`workflow/Snakefile`) integra y analiza.
5. Entorno exacto en `results/environment/environment.md`.

## 5. Preprocesamiento

Ninguno: no se eliminan valores atípicos ni repeticiones de calentamiento. `benchmark.csv`
solo concatena y ordena los 4 archivos. El análisis aplica log10 en una variante del ANOVA,
sin modificar los datos.

## 6. Limitaciones

- Los **tiempos absolutos dependen del hardware** (CPU híbrida Intel Core Ultra 7 165H con
  núcleos P/E, frecuencia variable, *turbo boost*), de la carga del sistema y del motor de
  contenedores. Lo reproducible son las relaciones y conclusiones, no los valores exactos.
- Una sola máquina, una sola semilla, 10 repeticiones: no se modela la variabilidad entre
  máquinas.
- Algoritmo naive deliberadamente no optimizado: los resultados **no** representan el
  rendimiento máximo alcanzable en cada lenguaje (BLAS, NumPy, vectorización, etc.).
- Java se mide con el JIT en frío en la repetición 1 de cada N.

## 7. Usos previstos y no previstos

- **Previstos:** docencia sobre reproducibilidad, comparación de lenguajes en un escenario
  CPU‑bound simple, ejemplo de análisis factorial (ANOVA de dos factores).
- **No recomendados:** concluir sobre el rendimiento general de un lenguaje o elegir
  tecnologías de producción a partir de estos datos.

## 8. Principios FAIR

| Principio | Cómo se cumple |
|---|---|
| **F**indable | DOI de Zenodo; metadatos en `.zenodo.json` y `CITATION.cff`; palabras clave |
| **A**ccessible | Acceso abierto vía HTTPS (Zenodo y GitHub), sin autenticación |
| **I**nteroperable | CSV estándar, Markdown, PNG; vocabulario explícito de columnas; Dockerfile OCI |
| **R**eusable | Licencias CC BY 4.0 / MIT; procedencia documentada; pipeline para regenerar los datos |

## 9. Mantenimiento

Versionado semántico con etiquetas git; cada versión publicada en Zenodo recibe su propio DOI
(más un *concept DOI* que apunta siempre a la última versión).
