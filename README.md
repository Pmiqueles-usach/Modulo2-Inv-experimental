# Benchmark reproducible de multiplicación de matrices NxN en C++, Go, Java y Python

[![DOI](https://zenodo.org/badge/DOI/PENDIENTE.svg)](https://doi.org/PENDIENTE)
<!-- Semana 5: reemplazar PENDIENTE por el DOI entregado por Zenodo -->

Artifact científico del **Módulo 2 – Documentación de experimentos (Reproducibilidad y
Replicabilidad)**, curso *Experimentación Computacional* (Doctorado, USACH).
Se construye siguiendo la política
[ACM Artifact Review and Badging v1.1](https://www.acm.org/publications/policies/artifact-review-and-badging-current).

| Estado del artifact (autoevaluación ACM) | |
|---|---|
| Artifacts Evaluated – **Functional** | ✅ autoevaluado (Semana 3) – ver [docs/ACM_BADGES.md](docs/ACM_BADGES.md) |
| Artifacts Evaluated – **Reusable** | ✅ autoevaluado (Semana 4) |
| Artifacts **Available** | ⏳ pendiente de DOI en Zenodo (Semana 5) |
| Results **Reproduced** | ⏳ evaluación cruzada por un compañero (Semana 5) |

> La autoevaluación no equivale a un badge oficial: los badges ACM los otorga el comité de
> evaluación de artifacts de cada conferencia/revista.

---

## 1. Objetivo

Diseñar y ejecutar un experimento computacional **reproducible** que compare el tiempo de
ejecución del algoritmo **naive** de multiplicación de matrices cuadradas NxN implementado
de forma equivalente en **C++, Go, Java y Python**.

## 2. Pregunta de investigación

> ¿Existen diferencias estadísticamente significativas en el tiempo de ejecución del algoritmo
> naive de multiplicación de matrices NxN entre implementaciones equivalentes desarrolladas en
> C++, Go, Java y Python, y cómo varían estas diferencias según el tamaño de la matriz?

## 3. Hipótesis

- **H₀:** El lenguaje de implementación no produce diferencias estadísticamente significativas
  en el tiempo de ejecución del algoritmo de multiplicación de matrices.
- **H₁:** Al menos uno de los lenguajes presenta un tiempo de ejecución significativamente
  diferente de los demás.

Hipótesis complementaria (interacción): el efecto del lenguaje depende del tamaño N.

## 4. Variables

| Tipo | Variable | Niveles / unidad |
|---|---|---|
| Independiente (factor A) | Lenguaje de programación | C++, Go, Java, Python |
| Independiente (factor B) | Tamaño de la matriz N | 500, 1000, 1500 |
| Dependiente | Tiempo de ejecución de la multiplicación | segundos (`time_seconds`) |
| Controladas | Algoritmo (naive i‑j‑k), tipo `double`, matrices de entrada (SplitMix64, semilla 42), reloj monotónico, solo se mide la multiplicación, ejecución secuencial en contenedores | — |
| Registradas | CPU, RAM, SO, arquitectura, versiones de compiladores/VM | [results/environment/environment.md](results/environment/environment.md) |

## 5. Diseño experimental

Diseño **factorial completo 4 × 3** con **10 repeticiones** por celda → **120 mediciones**.

| Lenguaje | N = 500 | N = 1000 | N = 1500 | Total |
|---|---|---|---|---|
| C++ | 10 | 10 | 10 | 30 |
| Go | 10 | 10 | 10 | 30 |
| Java | 10 | 10 | 10 | 30 |
| Python | 10 | 10 | 10 | 30 |

- Análisis: **ANOVA de dos factores con interacción** (lenguaje, N, lenguaje×N) y
  **Tukey HSD** post‑hoc; verificación de supuestos (Shapiro‑Wilk, Levene); análisis
  complementario sobre log10(tiempo) y Kruskal‑Wallis por N.
- Protocolo detallado y justificación de equivalencia: [docs/PROTOCOLO.md](docs/PROTOCOLO.md).

## 6. Estructura del repositorio

```
.
├── README.md                  ← este documento (instrucciones de reproducción)
├── LICENSE / LICENSE-DATA     ← MIT (código) / CC BY 4.0 (datos y resultados)
├── CITATION.cff, .zenodo.json ← metadatos de cita y de publicación en Zenodo
├── CHANGELOG.md               ← historia de versiones por semana
├── config/config.yaml         ← parámetros del experimento (N, repeticiones, semilla, motor)
├── src/{cpp,go,java,python}/  ← las 4 implementaciones equivalentes
├── docker/<lang>/Dockerfile   ← entornos reproducibles (+ docker/analysis para estadística)
├── workflow/Snakefile         ← pipeline de automatización
├── workflow/profiles/default/ ← perfil Snakemake (ejecución secuencial)
├── scripts/                   ← integración, verificación, análisis, registro del entorno
├── results/
│   ├── raw/{cpp,go,java,python}.csv   ← resultados por lenguaje
│   ├── benchmark.csv                  ← resultados integrados
│   ├── verification/                  ← checksums y reporte de equivalencia
│   ├── analysis/{tables,figures}/     ← ANOVA, Tukey, tablas y gráficos
│   ├── analysis/reporte_estadistico.md
│   ├── environment/environment.md     ← hardware y versiones
│   └── logs/
└── docs/
    ├── semanas/semana-{1..5}.md       ← entregables de cada semana
    ├── PROTOCOLO.md, ACM_BADGES.md, DATASHEET_FAIR.md, ZENODO.md
    ├── evaluacion-cruzada/            ← plantilla e informe de revisión cruzada
    └── presentaciones/
```

## 7. Requisitos

| Herramienta | Versión probada | Uso |
|---|---|---|
| Docker **o** Podman | Docker 29.4 / Podman 5.8 | construir y ejecutar los contenedores |
| Python | ≥ 3.11 (host) | solo para instalar Snakemake |
| Snakemake | 9.27.0 (`requirements-host.txt`) | pipeline |
| Linux x86_64 | Fedora 42 | (cualquier Linux con Docker debería funcionar) |

No se requiere instalar compiladores ni librerías en el host: todo se ejecuta en contenedores.
Hardware: ≥ 4 GB RAM libre; ~3 GB de disco para las imágenes. Duración total ≈ 1,5 h
(dominada por Python con N = 1500).

## 8. Reproducción completa (secuencia mínima)

```bash
# 0) Obtener el artifact
git clone https://github.com/Pmiqueles-usach/Modulo2-Inv-experimental.git
cd Modulo2-Inv-experimental

# 1) Construir MANUALMENTE las 5 imágenes desde los Dockerfile (no se usan imágenes publicadas)
docker build -f docker/cpp/Dockerfile      -t matmul-cpp:1.0 .
docker build -f docker/go/Dockerfile       -t matmul-go:1.0 .
docker build -f docker/java/Dockerfile     -t matmul-java:1.0 .
docker build -f docker/python/Dockerfile   -t matmul-python:1.0 .
docker build -f docker/analysis/Dockerfile -t matmul-analysis:1.0 .
#    (equivalente: scripts/build_images.sh)

# 2) Instalar Snakemake
python3 -m venv .venv && .venv/bin/pip install -r requirements-host.txt

# 3) Ejecutar TODO el flujo con un único comando
.venv/bin/snakemake --config results_dir=results_repro
```

> El repositorio ya contiene los resultados publicados en `results/`. Por eso, un simple
> `snakemake` responde "Nothing to be done". Para **reproducir** el experimento use un
> directorio nuevo (`results_dir=results_repro`) y compare con `results/`; para regenerar los
> resultados publicados, use `snakemake --forceall`.

Con **Podman** (o si el usuario no pertenece al grupo `docker`):

```bash
ENGINE=podman scripts/build_images.sh
.venv/bin/snakemake --config engine=podman results_dir=results_repro
# Si podman falla con "sd-bus call ... Input/output error" (sin sesión systemd):
ENGINE="podman --cgroup-manager=cgroupfs" scripts/build_images.sh
.venv/bin/snakemake --config engine="podman --cgroup-manager=cgroupfs" results_dir=results_repro
```

Prueba rápida (≈ 1,5 min) en un directorio separado, sin tocar los resultados publicados:

```bash
.venv/bin/snakemake --config results_dir=results_smoke 'sizes=[50,100]' repetitions=3
```

Para regenerar desde cero: `.venv/bin/snakemake --forceall`.

### Grafo del pipeline

```
run_benchmark(cpp|go|java|python) ─► raw/<lang>.csv ─► merge ─► benchmark.csv ─► analysis ─► tables/ figures/ reporte
                                 └─► verification/<lang>_checksum.csv ─► verify_equivalence ─► equivalence_report.md
environment ─► environment/environment.md

Antes de ejecutarse, cada regla comprueba que su imagen exista localmente; si falta, se detiene
e indica el comando `build` exacto.
```

`snakemake --dag | dot -Tpng > dag.png` genera el grafo real.

## 9. Ejecución manual por contenedor (sin Snakemake)

```bash
mkdir -p results/raw results/verification
docker run --rm --user "$(id -u):$(id -g)" --network none -v "$PWD/results:/results:z" matmul-cpp:1.0
docker run --rm --user "$(id -u):$(id -g)" --network none -v "$PWD/results:/results:z" matmul-go:1.0
docker run --rm --user "$(id -u):$(id -g)" --network none -v "$PWD/results:/results:z" matmul-java:1.0
docker run --rm --user "$(id -u):$(id -g)" --network none -v "$PWD/results:/results:z" matmul-python:1.0
```

Cada imagen ejecuta por defecto N = 500, 1000, 1500 con 10 repeticiones y semilla 42, y escribe
`results/raw/<lang>.csv` y `results/verification/<lang>_checksum.csv`. Los argumentos se pueden
cambiar: `docker run ... matmul-go:1.0 /results/raw/go.csv 200,400 5 42` o con
`scripts/run_container.sh <lang> [tamaños] [reps] [semilla]`.

### Demostración en consola (clase)

`scripts/demo.sh` recorre las 5 semanas con comandos visibles y pausas (≈3 min, en
`results_demo/`). Guía: [docs/DEMO.md](docs/DEMO.md).

## 10. Formato de los datos

`results/raw/<lang>.csv` y `results/benchmark.csv`:

| columna | tipo | descripción |
|---|---|---|
| `language` | texto | `cpp`, `go`, `java`, `python` |
| `N` | entero | tamaño de la matriz |
| `repetition` | entero | número de ejecución (1–10) |
| `time_seconds` | real | tiempo de la multiplicación en segundos (9 decimales) |

Descripción FAIR completa: [docs/DATASHEET_FAIR.md](docs/DATASHEET_FAIR.md).

## 11. Resultados

<!-- RESULTADOS:INICIO -->
Corrida oficial del 2026‑10‑17 (Intel Core Ultra 7 165H, 30 GB RAM, Fedora 42 / kernel 6.18,
Podman 5.8.2; entorno completo en [results/environment/environment.md](results/environment/environment.md)).
Duración total del pipeline: 2 h 33 min.

**Tiempo medio de la multiplicación [s] (10 repeticiones; entre paréntesis, razón respecto de C++)**

| N | C++ | Go | Java | Python |
|---|---|---|---|---|
| 500 | 0,080 | 0,118 (1,47×) | 0,163 (2,03×) | 20,0 (249×) |
| 1000 | 0,889 | 1,460 (1,64×) | 1,220 (1,37×) | 178,2 (200×) |
| 1500 | 5,519 | 9,415 (1,71×) | 8,724 (1,58×) | 688,5 (125×) |

**ANOVA de dos factores con interacción**

| Efecto | F (tiempo) | p (tiempo) | F (log10) | p (log10) | η² parcial (log10) |
|---|---|---|---|---|---|
| Lenguaje | 6091 | 2,8·10⁻¹²⁰ | 15 740 | 1,8·10⁻¹⁴² | 0,998 |
| N | 3109 | 3,5·10⁻⁹⁶ | 14 230 | 1,5·10⁻¹³¹ | 0,996 |
| Lenguaje × N | 2828 | 2,8·10⁻¹¹⁶ | 37,6 | 2,5·10⁻²⁴ | 0,676 |

**Conclusiones**

1. **Se rechaza H₀** (α = 0,05): el lenguaje produce diferencias significativas en el tiempo
   de ejecución. Tukey HSD encuentra diferencias significativas en **los 6 pares de lenguajes
   para cada uno de los 3 tamaños** (18/18 comparaciones); Kruskal‑Wallis lo confirma en cada N
   (p < 2·10⁻⁷).
2. **La interacción lenguaje × N es significativa**: la diferencia entre lenguajes depende del
   tamaño de la matriz. Se observa en dos hechos:
   - **Go y Java intercambian posiciones**: con N = 500 Go es más rápido que Java, mientras que
     con N = 1000 y 1500 Java supera a Go.
   - **La desventaja relativa de Python disminuye** al crecer N (249× → 125×). Una explicación posible es que, en los
     lenguajes compilados el costo de los accesos a memoria por columnas de B (fallos de caché)
     crecería más rápido que el costo del intérprete. Es una hipótesis plausible que este
     experimento no pone a prueba.
3. Orden de los lenguajes, de más rápido a más lento: C++ < Go < Java ≪ Python con N = 500;
   C++ < Java < Go ≪ Python con N = 1000 y 1500.
4. **Supuestos:** los residuos no son normales y las varianzas no son homogéneas, ni siquiera
   en log10 (Shapiro p = 0,002; Levene p < 10⁻⁵). Aun así, con diferencias de esta magnitud,
   el modelo log10 y la prueba no paramétrica llegan a la misma conclusión.
5. **Equivalencia funcional:** las 4 implementaciones producen la **misma matriz bit a bit**
   (checksums idénticos en los 3 tamaños,
   [equivalence_report.md](results/verification/equivalence_report.md)).
6. **Observación de estabilidad:** en Python con N = 1500, las repeticiones 7–10 fueron
   ~8 % más rápidas (634–667 s frente a 704–727 s). Es compatible con cambios de frecuencia o
   de carga del equipo durante una corrida de ~2 h; queda registrada como amenaza a la validez.

Reporte completo: [results/analysis/reporte_estadistico.md](results/analysis/reporte_estadistico.md)

![Interacción lenguaje × N](results/analysis/figures/interaccion_lenguaje_N.png)
![Razón respecto de C++](results/analysis/figures/speedup_vs_cpp.png)
<!-- RESULTADOS:FIN -->

## 12. Reutilización y extensión

- **Otros tamaños / repeticiones / semilla:** editar `config/config.yaml` o usar `--config`.
- **Agregar un lenguaje (p. ej. Rust):** crear `src/rust/`, `docker/rust/Dockerfile` respetando
  la interfaz `<salida.csv> <tamaños> <repeticiones> <semilla> [checksum.csv]` y el protocolo de
  [docs/PROTOCOLO.md](docs/PROTOCOLO.md), y añadir `rust` a `languages` en la configuración.
  `verify_equivalence` comprobará automáticamente que produce la misma matriz.
- **Otro análisis:** `scripts/analysis.py` lee cualquier `benchmark.csv` con las 4 columnas.

## 13. Avance por semana

| Semana | Tema | Documento | Etiqueta git |
|---|---|---|---|
| 1 | Diseño experimental, GitHub y documentación | [semana-1.md](docs/semanas/semana-1.md) | `semana-1` |
| 2 | Implementación y ejecución | [semana-2.md](docs/semanas/semana-2.md) | `semana-2` |
| 3 | Entorno reproducible (Docker) – Functional | [semana-3.md](docs/semanas/semana-3.md) | `semana-3` |
| 4 | Snakemake + ANOVA/Tukey – Reusable | [semana-4.md](docs/semanas/semana-4.md) | `semana-4` |
| 5 | Zenodo (DOI) y evaluación cruzada – Available | [semana-5.md](docs/semanas/semana-5.md) | `v1.0.0` |

## 14. Licencia y cita

- Código: [MIT](LICENSE). Datos, resultados, figuras y documentación: [CC BY 4.0](LICENSE-DATA).
- Cómo citar: ver [CITATION.cff](CITATION.cff) (DOI de Zenodo tras la Semana 5).

## 15. Referencias

- ACM. *Artifact Review and Badging – Current (v1.1)*. https://www.acm.org/publications/policies/artifact-review-and-badging-current
- National Academies of Sciences, Engineering, and Medicine (2019). *Reproducibility and Replicability in Science*. https://doi.org/10.17226/25303
- Fehr, J. et al. (2016). *Best Practices for Replicability, Reproducibility and Reusability of Computer-Based Experiments Exemplified by Model Reduction Software*. https://arxiv.org/abs/1607.01191
