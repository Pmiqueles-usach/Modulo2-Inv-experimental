# Comparación publicado vs reproducido (análisis uniforme del evaluador)

- Filas: publicado 120 · reproducido 120
- Columnas reproducido: `language,N,repetition,time_seconds`
- 12 celdas × 10 repeticiones en reproducido: sí

## Medias (s) y razón vs C++

| N | Lenguaje | Media publicada | Media reproducida | Razón/C++ publ. | Razón/C++ repr. |
|---|---|---:|---:|---:|---:|
| 500 | cpp | 0.1227 | 0.0749 | 1.00 | 1.00 |
| 500 | go | 0.1946 | 0.1232 | 1.59 | 1.65 |
| 500 | java | 0.1351 | 0.0929 | 1.10 | 1.24 |
| 500 | python | 17.8154 | 14.9807 | 145.15 | 200.14 |
| 1000 | cpp | 2.3455 | 0.4854 | 1.00 | 1.00 |
| 1000 | go | 3.2259 | 1.1940 | 1.38 | 2.46 |
| 1000 | java | 2.2509 | 0.7211 | 0.96 | 1.49 |
| 1000 | python | 142.1193 | 125.5105 | 60.59 | 258.58 |
| 1500 | cpp | 11.6088 | 3.7277 | 1.00 | 1.00 |
| 1500 | go | 14.8004 | 5.4641 | 1.27 | 1.47 |
| 1500 | java | 12.2101 | 7.1045 | 1.05 | 1.91 |
| 1500 | python | 491.3827 | 391.2435 | 42.33 | 104.96 |

## Orden de lenguajes (más rápido primero)

| N | Publicado | Reproducido | ¿Igual? |
|---|---|---|---|
| 500 | cpp < java < go < python | cpp < java < go < python | sí |
| 1000 | java < cpp < go < python | cpp < java < go < python | no |
| 1500 | cpp < java < go < python | cpp < go < java < python | no |

## ANOVA tipo II (p-valores)

| Escala | Efecto | p publicado | p reproducido | Decisión igual (α=0,05) |
|---|---|---:|---:|---|
| seg | C(language) | 6.92e-189 | 3.98e-78 | sí |
| seg | C(N) | 3.64e-165 | 2.35e-52 | sí |
| seg | C(language):C(N) | 1.02e-182 | 1.48e-70 | sí |
| log10 | C(language) | 1.51e-177 | 1.36e-157 | sí |
| log10 | C(N) | 1.91e-176 | 1.11e-144 | sí |
| log10 | C(language):C(N) | 2.07e-75 | 1.22e-48 | sí |

## Tukey HSD log10, pares de lenguajes NO significativos dentro de cada N

- Publicado: N=500: ninguno; N=1000: ninguno; N=1500: ninguno
- Reproducido: N=500: ninguno; N=1000: ninguno; N=1500: ninguno
