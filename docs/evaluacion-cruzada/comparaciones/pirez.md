# Comparación publicado vs reproducido (análisis uniforme del evaluador)

- Filas: publicado 120 · reproducido 120
- Columnas reproducido: `language,N,repetition,time_seconds`
- 12 celdas × 10 repeticiones en reproducido: sí

## Medias (s) y razón vs C++

| N | Lenguaje | Media publicada | Media reproducida | Razón/C++ publ. | Razón/C++ repr. |
|---|---|---:|---:|---:|---:|
| 500 | cpp | 0.1105 | 0.0677 | 1.00 | 1.00 |
| 500 | go | 0.1276 | 0.1030 | 1.15 | 1.52 |
| 500 | java | 0.1289 | 0.0873 | 1.17 | 1.29 |
| 500 | python | 8.1163 | 7.2417 | 73.45 | 107.01 |
| 1000 | cpp | 0.9602 | 0.6724 | 1.00 | 1.00 |
| 1000 | go | 1.1316 | 1.1704 | 1.18 | 1.74 |
| 1000 | java | 1.1077 | 1.1047 | 1.15 | 1.64 |
| 1000 | python | 113.6422 | 69.9113 | 118.36 | 103.97 |
| 1500 | cpp | 4.4397 | 3.9335 | 1.00 | 1.00 |
| 1500 | go | 6.1317 | 6.3445 | 1.38 | 1.61 |
| 1500 | java | 7.2286 | 5.8765 | 1.63 | 1.49 |
| 1500 | python | 441.2087 | 294.7918 | 99.38 | 74.94 |

## Orden de lenguajes (más rápido primero)

| N | Publicado | Reproducido | ¿Igual? |
|---|---|---|---|
| 500 | cpp < go < java < python | cpp < java < go < python | no |
| 1000 | cpp < java < go < python | cpp < java < go < python | sí |
| 1500 | cpp < go < java < python | cpp < java < go < python | no |

## ANOVA tipo II (p-valores)

| Escala | Efecto | p publicado | p reproducido | Decisión igual (α=0,05) |
|---|---|---:|---:|---|
| seg | C(language) | 7.83e-92 | 4.22e-120 | sí |
| seg | C(N) | 1.79e-69 | 1.15e-98 | sí |
| seg | C(language):C(N) | 1.01e-88 | 1.41e-117 | sí |
| log10 | C(language) | 3.66e-154 | 1.04e-154 | sí |
| log10 | C(N) | 7.93e-147 | 2.7e-150 | sí |
| log10 | C(language):C(N) | 8.71e-24 | 3.33e-19 | sí |

## Tukey HSD log10, pares de lenguajes NO significativos dentro de cada N

- Publicado: N=500: go–java; N=1000: go–java; N=1500: ninguno
- Reproducido: N=500: ninguno; N=1000: go–java; N=1500: go–java
