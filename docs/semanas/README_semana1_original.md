# Benchmark reproducible de multiplicación de matrices NxN

## 1. Descripción del proyecto

Este proyecto tiene como finalidad diseñar y desarrollar un experimento computacional reproducible para comparar el tiempo de ejecución del algoritmo *naive* de multiplicación de matrices cuadradas NxN implementado en C++, Go, Java y Python.

El proyecto forma parte del curso Experimentación Computacional, en el módulo Documentación de experimentos (Reproducibilidad y Replicabilidad).

## 2. Objetivo general

Comparar experimentalmente el tiempo de ejecución de implementaciones equivalentes del algoritmo *naive* de multiplicación de matrices en cuatro lenguajes de programación, evaluando cómo varía el rendimiento según el lenguaje y el tamaño de las matrices.

## 3. Pregunta de investigación

¿Existen diferencias estadísticamente significativas en el tiempo de ejecución del algoritmo *naive* de multiplicación de matrices NxN entre implementaciones equivalentes desarrolladas en C++, Go, Java y Python, y cómo varían estas diferencias según el tamaño de la matriz?

## 4. Hipótesis

**Hipótesis nula (H0):** El lenguaje de implementación no produce diferencias estadísticamente significativas en el tiempo de ejecución del algoritmo de multiplicación de matrices.

**Hipótesis alternativa (H1):** Al menos uno de los lenguajes presenta un tiempo de ejecución significativamente diferente de los demás.

## 5. Variables experimentales

### Variables independientes

- **Lenguaje de programación:** C++, Go, Java y Python.
- **Tamaño de la matriz:** N = 500, N = 1000 y N = 1500.

### Variable dependiente

- **Tiempo de ejecución:** tiempo medido en segundos durante la operación de multiplicación de matrices.

### Variables y condiciones controladas

- Utilización del mismo algoritmo *naive* en los cuatro lenguajes.
- Equivalencia funcional de las implementaciones.
- Generación controlada de los datos mediante una semilla definida.
- Utilización de un criterio común para medir el tiempo.
- Exclusión de la generación e inicialización de matrices del tiempo medido.
- Registro de las características del entorno de ejecución.

No se utilizarán bibliotecas optimizadas para multiplicación de matrices.

## 6. Diseño experimental

El experimento considera cuatro lenguajes de programación y tres tamaños de matriz. Se realizarán diez repeticiones para cada combinación de lenguaje y tamaño.

Esto corresponde a 12 combinaciones experimentales y 120 ejecuciones en total.

| Factor | Valores |
|---|---|
| Lenguaje | C++, Go, Java, Python |
| Tamaño de matriz | 500, 1000, 1500 |
| Repeticiones | 10 por combinación |
| Variable medida | Tiempo de ejecución en segundos |

Las matrices deberán estar completamente generadas antes de iniciar la medición. El temporizador comenzará inmediatamente antes de ejecutar el algoritmo y finalizará cuando se obtenga la matriz resultante.

Se registrarán el procesador, la memoria RAM, el sistema operativo, la arquitectura y las versiones de los lenguajes, compiladores o máquinas virtuales utilizados.

## 7. Recolección de resultados

Los resultados se almacenarán en archivos CSV independientes por lenguaje:

- `cpp.csv`
- `go.csv`
- `java.csv`
- `python.csv`

Todos utilizarán las siguientes columnas:

`language,N,repetition,time_seconds`

Cada fila representará una ejecución experimental.

## 8. Reproducibilidad y documentación

El repositorio GitHub será utilizado para mantener el código fuente, la documentación del diseño experimental y el control de versiones del proyecto.

Durante las siguientes etapas se incorporarán las instrucciones de ejecución, los entornos Docker, la automatización con Snakemake y los resultados del análisis estadístico.

El proyecto utilizará como referencia los criterios ACM Artifact Review & Badging para documentar y evaluar las características del artifact experimental.

Referencia: https://www.acm.org/publications/policies/artifact-review-and-badging-current

## 9. Estado del proyecto

- [x] Definición inicial del objetivo experimental.
- [x] Formulación de la pregunta de investigación.
- [x] Definición de las hipótesis.
- [x] Identificación de las variables experimentales.
- [x] Diseño experimental inicial.
- [ ] Implementación de los cuatro algoritmos.
- [ ] Ejecución del benchmark y registro de resultados.
- [ ] Construcción manual de los entornos Docker.
- [ ] Automatización del experimento y análisis estadístico.
- [ ] Publicación del artifact y evaluación cruzada.
