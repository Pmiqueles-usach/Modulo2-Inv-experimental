# Comparación publicado vs reproducido (análisis uniforme del evaluador)

- Filas: publicado 120 · reproducido 120
- Columnas reproducido: `language,N,repetition,time_seconds`
- 12 celdas × 10 repeticiones en reproducido: sí

## Medias (s) y razón vs C++

| N | Lenguaje | Media publicada | Media reproducida | Razón/C++ publ. | Razón/C++ repr. |
|---|---|---:|---:|---:|---:|
| 500 | cpp | 0.5048 | 1.1905 | 1.00 | 1.00 |
| 500 | go | 0.1293 | 0.2143 | 0.26 | 0.18 |
| 500 | java | 0.0821 | 0.1686 | 0.16 | 0.14 |
| 500 | python | 7.7150 | 10.4065 | 15.28 | 8.74 |
| 1000 | cpp | 7.8935 | 14.5542 | 1.00 | 1.00 |
| 1000 | go | 1.9476 | 3.4720 | 0.25 | 0.24 |
| 1000 | java | 1.3487 | 1.5311 | 0.17 | 0.11 |
| 1000 | python | 63.3216 | 84.6825 | 8.02 | 5.82 |
| 1500 | cpp | 34.8558 | 53.8449 | 1.00 | 1.00 |
| 1500 | go | 9.6570 | 15.3362 | 0.28 | 0.28 |
| 1500 | java | 15.4794 | 15.7003 | 0.44 | 0.29 |
| 1500 | python | 233.6134 | 317.4758 | 6.70 | 5.90 |

## Orden de lenguajes (más rápido primero)

| N | Publicado | Reproducido | ¿Igual? |
|---|---|---|---|
| 500 | java < go < cpp < python | java < go < cpp < python | sí |
| 1000 | java < go < cpp < python | java < go < cpp < python | sí |
| 1500 | go < java < cpp < python | go < java < cpp < python | sí |

## ANOVA tipo II (p-valores)

| Escala | Efecto | p publicado | p reproducido | Decisión igual (α=0,05) |
|---|---|---:|---:|---|
| seg | C(language) | 2.16e-164 | 1.1e-132 | sí |
| seg | C(N) | 9.64e-152 | 1.04e-120 | sí |
| seg | C(language):C(N) | 5.08e-159 | 8.94e-128 | sí |
| log10 | C(language) | 3.63e-149 | 1.82e-137 | sí |
| log10 | C(N) | 4.41e-158 | 7.22e-144 | sí |
| log10 | C(language):C(N) | 6.16e-69 | 1.23e-48 | sí |

## Tukey HSD log10, pares de lenguajes NO significativos dentro de cada N

- Publicado: N=500: ninguno; N=1000: ninguno; N=1500: ninguno
- Reproducido: N=500: ninguno; N=1000: ninguno; N=1500: go–java
