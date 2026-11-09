# Comparación publicado vs reproducido (análisis uniforme del evaluador)

- Filas: publicado 120 · reproducido 120
- Columnas reproducido: `language,N,repetition,time_seconds`
- 12 celdas × 10 repeticiones en reproducido: sí

## Medias (s) y razón vs C++

| N | Lenguaje | Media publicada | Media reproducida | Razón/C++ publ. | Razón/C++ repr. |
|---|---|---:|---:|---:|---:|
| 500 | cpp | 0.1763 | 0.0745 | 1.00 | 1.00 |
| 500 | go | 0.1825 | 0.1039 | 1.04 | 1.39 |
| 500 | java | 0.2361 | 0.0949 | 1.34 | 1.27 |
| 500 | python | 10.7756 | 14.5810 | 61.13 | 195.62 |
| 1000 | cpp | 1.1924 | 0.6999 | 1.00 | 1.00 |
| 1000 | go | 1.3590 | 1.1803 | 1.14 | 1.69 |
| 1000 | java | 1.8134 | 0.9228 | 1.52 | 1.32 |
| 1000 | python | 90.4817 | 121.0289 | 75.88 | 172.92 |
| 1500 | cpp | 4.8935 | 3.4545 | 1.00 | 1.00 |
| 1500 | go | 6.0858 | 6.8462 | 1.24 | 1.98 |
| 1500 | java | 6.6192 | 5.8056 | 1.35 | 1.68 |
| 1500 | python | 332.2424 | 458.7149 | 67.89 | 132.79 |

## Orden de lenguajes (más rápido primero)

| N | Publicado | Reproducido | ¿Igual? |
|---|---|---|---|
| 500 | cpp < go < java < python | cpp < java < go < python | no |
| 1000 | cpp < go < java < python | cpp < java < go < python | no |
| 1500 | cpp < go < java < python | cpp < java < go < python | no |

## ANOVA tipo II (p-valores)

| Escala | Efecto | p publicado | p reproducido | Decisión igual (α=0,05) |
|---|---|---:|---:|---|
| seg | C(language) | 3.74e-153 | 1.06e-109 | sí |
| seg | C(N) | 5.04e-129 | 2.4e-85 | sí |
| seg | C(language):C(N) | 2.9e-148 | 2.87e-105 | sí |
| log10 | C(language) | 7.35e-118 | 1.14e-159 | sí |
| log10 | C(N) | 4.85e-108 | 6.59e-148 | sí |
| log10 | C(language):C(N) | 0.148 | 5.18e-31 | NO |

## Tukey HSD log10, pares de lenguajes NO significativos dentro de cada N

- Publicado: N=500: cpp–go, go–java; N=1000: ninguno; N=1500: go–java
- Reproducido: N=500: go–java; N=1000: ninguno; N=1500: ninguno
