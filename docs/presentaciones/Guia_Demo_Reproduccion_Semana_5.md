# Guía de demostración – Semana 5: cómo reproducir un artifact desde la consola

Apoyo para la presentación final. Primero muestra cómo se reproduce el artifact de un compañero
(Alejandro Pirez, que trae una prueba corta incluida) y después cómo un tercero reproduce el
artifact propio. Los comandos parten de `~/Documentos/000-DOCTORADO-2DOsem/`.

## A. Reproducir el artifact de un compañero (Pirez, DOI 10.5281/zenodo.23954875)

**1. Descargar desde Zenodo, no desde GitHub.** El script verifica el MD5 y no ejecuta nada.

```bash
cd ~/Documentos/000-DOCTORADO-2DOsem/Inv-Experimental_Modulo2
python3 scripts/descargar_zenodo.py 10.5281/zenodo.23954875 ../demo-pirez
cd ../demo-pirez/contenido
```

**2. Leer su README.** Es lo único que se permite usar.

```bash
less README.md
```

**3. Preparar el motor de contenedores.** En este equipo se usa Podman porque el usuario no
pertenece al grupo `docker`. El adaptador traduce `docker` → `podman` y no modifica el artifact.

```bash
export PATH=~/Documentos/000-DOCTORADO-2DOsem/eval-cruzada/bin:$PATH
docker --version
```

**4. Construir manualmente las 4 imágenes** desde sus Dockerfile.

```bash
docker build -t matrix-bench-cpp:1.0 cpp
docker build -t matrix-bench-go:1.0 go
docker build -t matrix-bench-java:1.0 java
docker build -t matrix-bench-python:1.0 python
docker images | grep matrix-bench
```

**5. Instalar sus dependencias** en un entorno aislado.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

**6. Ver el plan del pipeline sin ejecutarlo.**

```bash
python -m snakemake --cores 1 --resources machine=1 -n
```

**7a. Demo en clase (≈ 1–2 min):** la prueba corta de su README (N = 40 y 50).

```bash
python -m snakemake --cores 1 --resources machine=1 --config smoke=true
```

**7b. Corrida completa (≈ 66 min en este equipo).**

```bash
python -m snakemake --cores 1 --resources machine=1
```

**8. Verificar lo que exige el enunciado.** Si se corrió la prueba corta, cambiar `results` por
`results/smoke`.

```bash
ls results/{cpp,go,java,python}.csv
head -1 results/cpp.csv              # language,N,repetition,time_seconds
wc -l results/benchmark.csv          # 121 = encabezado + 120 filas
ls results/analysis results/analysis/figuras
```

**9. Comparar lo publicado con lo reproducido** usando el mismo análisis en ambos. Requiere pandas,
numpy y statsmodels; el venv de Pirez los trae, así que se ejecuta con el venv del paso 5 activado.

```bash
python ~/Documentos/000-DOCTORADO-2DOsem/Inv-Experimental_Modulo2/scripts/comparar_evaluacion.py \
  ../../pirez/contenido/results/benchmark.csv results/benchmark.csv comparacion.md
```

## B. Cómo reproduce un tercero el artifact propio (DOI 10.5281/zenodo.23954259)

```bash
cd ~/Documentos/000-DOCTORADO-2DOsem/Inv-Experimental_Modulo2
python3 scripts/descargar_zenodo.py 10.5281/zenodo.23954259 ../repro-propio
cd ../repro-propio/contenido
ENGINE="podman --cgroup-manager=cgroupfs" scripts/build_images.sh
python3 -m venv .venv && .venv/bin/pip install -r requirements-host.txt
.venv/bin/snakemake --config engine="podman --cgroup-manager=cgroupfs" \
  results_dir=results_smoke 'sizes=[50,100]' repetitions=3
cat results_smoke/verification/equivalence_report.md   # debe decir EQUIVALENTES
```

- Con Docker normal se omiten `ENGINE=...` y `--config engine=...`.
- La corrida completa (≈ 1,5 h) se lanza con `--config results_dir=results_repro`, para no
  sobrescribir los resultados publicados en `results/`.

## C. Respuestas breves a preguntas probables

| Pregunta | Respuesta |
|---|---|
| ¿Por qué descargar desde Zenodo? | La evaluación debe usar solo el artifact archivado, que es inmutable y tiene DOI. |
| ¿Modificaste algo de los artifacts? | No. Solo se adaptó el entorno: el adaptador `docker` → `podman` y el registro `docker.io` para los nombres cortos de imagen. |
| ¿Por qué no coinciden los segundos? | Dependen del hardware. Se comparan las decisiones del ANOVA, el orden de los lenguajes y las razones; en Valenzuela, además, los checksums son idénticos. |
| ¿Cuánto tardó cada uno? | Pirez 66 min · Fornes 95 min · Valenzuela 102 min · Fuertes 113 min. |
| ¿Corrieron en paralelo? | Sí, los 4 pipelines a la vez para tener resultados el mismo día. Dentro de cada uno, los contenedores corrieron de a uno. Es una limitación declarada. |
| ¿Dónde está el detalle? | `docs/evaluacion-cruzada/` (resumen en `README.md` y una evaluación por compañero). |

## D. Comparación por compañero: publicado → reproducido

Es el mismo contenido de las láminas 10–18 de la presentación. Tiempos medios en segundos
(publicado → reproducido). Detalle completo en `docs/evaluacion-cruzada/`.

### D.1 Resumen de dictámenes

| Compañero | DOI | Pipeline | Tiempo | Available | Functional | Reusable | Reproduced |
|---|---|---|---:|:-:|:-:|:-:|:-:|
| Joel Fuertes | 10.5281/zenodo.23988249 | 4/4 pasos | 113 min | ✓ | ✓ | ✓ | ✓ |
| Jorge Fornes | 10.5281/zenodo.23987654 | 19/19 pasos | 95 min | ✓ | ✓ con reservas | ✗ | ✓ (conclusiones generales) |
| Alejandro Pirez | 10.5281/zenodo.23954875 | 19/19 pasos | 66 min | ✓ | ✓ | ✓ | ✓ |
| Jonathan Valenzuela | 10.5281/zenodo.23891451 | 8/8 pasos | 102 min | ✓ | ✓ | ✓ | ✓ |

### D.2 Joel Fuertes: mismas decisiones; el orden entre C++, Go y Java cambia

| Lenguaje | N = 500 | N = 1000 | N = 1500 |
|---|---|---|---|
| C++ | 0,123 → 0,075 | 2,35 → 0,49 | 11,6 → 3,7 |
| Go | 0,195 → 0,123 | 3,23 → 1,19 | 14,8 → 5,5 |
| Java | 0,135 → 0,093 | 2,25 → 0,72 | 12,2 → 7,1 |
| Python | 17,8 → 15,0 | 142 → 126 | 491 → 391 |

| Indicador | Publicado | Reproducido | ¿Concuerda? |
|---|---|---|---|
| Efecto lenguaje (log10) | p = 1,5·10⁻¹⁷⁷ | p = 1,4·10⁻¹⁵⁷ | ✓ |
| Interacción lenguaje × N | p = 2,1·10⁻⁷⁵ | p = 1,2·10⁻⁴⁸ | ✓ |
| Post-hoc (Tukey) | omitido por supuestos | omitido por supuestos | ✓ |
| Orden N = 1000 / 1500 | java<cpp<go / cpp<java<go | cpp<java<go / cpp<go<java | No (depende del hardware) |
| Razón Python / C++ (N = 1500) | 42× | 105× | ✓ mismo orden de magnitud |

- **Pasos:** imágenes fijadas por digest; `snakemake --cores 1 --forceall --rerun-incomplete`; 12 bloques en orden aleatorio con calentamientos; cada producto se valida contra `control.txt`.
- **Dificultades:** README de 824 líneas pensado para Windows y WSL, con rutas fijas. El README archivado no incluye el DOI.
- **Conclusión:** se reproducen todas las conclusiones que declara el autor. El orden entre C++, Go y Java depende del hardware, y el autor no afirma ningún orden.

### D.3 Jorge Fornes: se reproduce lo general, pero no la diferencia Go ≠ Java en N = 1500

| Lenguaje | N = 500 | N = 1000 | N = 1500 |
|---|---|---|---|
| C++ (-O0) | 0,505 → 1,19 | 7,89 → 14,6 | 34,9 → 53,8 |
| Go | 0,129 → 0,214 | 1,95 → 3,47 | 9,66 → 15,3 |
| Java | 0,082 → 0,169 | 1,35 → 1,53 | 15,5 → 15,7 |
| Python | 7,71 → 10,4 | 63,3 → 84,7 | 234 → 317 |

| Indicador | Publicado | Reproducido | ¿Concuerda? |
|---|---|---|---|
| Efecto lenguaje (segundos) | p = 2,2·10⁻¹⁶⁴ | p = 1,1·10⁻¹³² | ✓ |
| Interacción lenguaje × N | p = 5,1·10⁻¹⁵⁹ | p = 8,9·10⁻¹²⁸ | ✓ |
| Tukey global (C++, Go y Java no difieren) | sí | sí | ✓ |
| Go ≠ Java en N = 1500 | sí (p < 0,001) | no (p = 1,0) | **No** |
| Orden de lenguajes (3 N) | go/java < cpp < python | idéntico | ✓ |

- **Dificultades:** C++ se compila con `-O0` mientras Go y Java van optimizados, por eso C++ resulta 3–7× más lento que Go y Java. Las dependencias no tienen versión fija y Snakemake no aparece en los requisitos. El README dice "DOI pendiente" y manda a clonar GitHub. Los scripts vienen sin permiso de ejecución.
- **Conclusión:** se reproducen las decisiones generales y el orden. No se reproduce el hallazgo que el README destaca (Go ≠ Java en N = 1500).

### D.4 Alejandro Pirez: de Windows a contenedores, las decisiones se mantienen

| Lenguaje | N = 500 | N = 1000 | N = 1500 |
|---|---|---|---|
| C++ | 0,110 → 0,068 | 0,96 → 0,67 | 4,44 → 3,93 |
| Go | 0,128 → 0,103 | 1,13 → 1,17 | 6,13 → 6,34 |
| Java | 0,129 → 0,087 | 1,11 → 1,10 | 7,23 → 5,88 |
| Python | 8,12 → 7,24 | 114 → 70 | 441 → 295 |

| Indicador | Publicado | Reproducido | ¿Concuerda? |
|---|---|---|---|
| Efecto lenguaje (log10) | p = 3,7·10⁻¹⁵⁴ | p = 1,0·10⁻¹⁵⁴ | ✓ |
| Interacción lenguaje × N (log10) | p = 8,7·10⁻²⁴ | p = 3,3·10⁻¹⁹ | ✓ |
| Tukey en segundos (del autor) | solo Python difiere | solo Python difiere | ✓ |
| Orden N = 500 / 1500 | cpp<go<java | cpp<java<go | Parcial (Go y Java se invierten) |
| Razón Python / C++ (N = 1500) | 99× | 75× | ✓ mismo orden de magnitud |

- **Dificultades:** no hay checksum, así que la equivalencia entre lenguajes solo se afirma. Los CSV publicados se midieron en Windows sin contenedores. La corrida sobrescribe `results/`, aunque el README lo advierte.
- **Conclusión:** se reproducen las decisiones del ANOVA y del Tukey. Solo se invierte el par Go–Java, que es el de menor diferencia.

### D.5 Jonathan Valenzuela: mismo código, mismas decisiones estadísticas

| Lenguaje | N = 500 | N = 1000 | N = 1500 |
|---|---|---|---|
| C++ | 0,176 → 0,075 | 1,19 → 0,70 | 4,89 → 3,45 |
| Go | 0,182 → 0,104 | 1,36 → 1,18 | 6,09 → 6,85 |
| Java | 0,236 → 0,095 | 1,81 → 0,92 | 6,62 → 5,81 |
| Python | 10,8 → 14,6 | 90,5 → 121 | 332 → 459 |

| Indicador | Publicado | Reproducido | ¿Concuerda? |
|---|---|---|---|
| Checksums (4 lenguajes × 3 N) | publicados | idénticos | ✓ |
| Efecto lenguaje (segundos) | p = 3,7·10⁻¹⁵³ | p = 1,1·10⁻¹⁰⁹ | ✓ |
| Interacción lenguaje × N | p = 2,9·10⁻¹⁴⁸ | p = 2,9·10⁻¹⁰⁵ | ✓ |
| Tukey del autor (por N) | solo Python difiere | solo Python difiere | ✓ |
| Orden C++ < Go/Java < Python | cpp<go<java | cpp<java<go | ✓ (Go y Java no difieren según su Tukey) |

- **Dificultades:** el README archivado dice "DOI pendiente", pide ejecutar desde una carpeta `mm/` que no existe y lista archivos que no vienen en el zip. `snakemake --cores 1` no vuelve a medir porque `results/` ya existe; se necesita `--forceall`.
- **Conclusión:** se reproduce todo lo que el autor concluye. Go y Java se invierten, pero su propio Tukey los declara no significativos.

### D.6 Síntesis

- En los 4 artifacts se rechaza H₀ con la misma decisión que publicó el autor, y Python queda 1 a 2 órdenes de magnitud más lento.
- Los segundos y el orden fino entre C++, Go y Java **no** se reproducen, porque dependen del hardware.
- Lo que más facilitó reproducir fue fijar versiones (digest y lockfile) y verificar la equivalencia con checksum automático.

## E. ¿Qué es el checksum?

Un **checksum** es un número corto calculado a partir de un dato grande que funciona como su
"huella": si el dato cambia, aunque sea un poco, el checksum cambia. Aquí aparece con dos usos:

1. **Checksum del resultado (equivalencia).** Cada programa calcula, por ejemplo, la suma de todos
   los elementos de la matriz C. Si los 4 lenguajes dan el mismo valor, hacen exactamente el mismo
   cálculo y las diferencias de tiempo se deben al lenguaje. Si el valor reproducido coincide con
   el publicado, el código se comporta igual en otra máquina. Ejemplo de Valenzuela con N = 1500:
   `843097455.74871671` en C++, Go, Java y Python.
2. **Checksum del archivo (integridad).** Es el MD5 que publica Zenodo para cada zip. Al
   recalcularlo tras la descarga se comprueba que el archivo llegó intacto y es exactamente lo que
   el autor archivó.

> Frase para la presentación: "El checksum es la huella numérica del resultado: si coincide entre
> lenguajes, los programas son equivalentes; si coincide con el publicado, el código se comporta
> igual en mi máquina y las diferencias de tiempo son solo del hardware."

> Antes de la clase conviene probar los pasos A.1–A.7a: las imágenes ya están construidas, así que
> el paso 4 es casi instantáneo.
