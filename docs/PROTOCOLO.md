# Protocolo experimental y decisiones de equivalencia

Este documento justifica las decisiones adoptadas para que las cuatro implementaciones
(C++, Go, Java y Python) sean **funcionalmente equivalentes** y sus tiempos **comparables**
(entregable de la Semana 2).

## 1. Algoritmo

Multiplicación naive `C = A × B` con triple bucle en orden **i‑j‑k** y acumulador local:

```
para i en 0..N-1:
  para j en 0..N-1:
    suma = 0.0
    para k en 0..N-1:
      suma += A[i*N + k] * B[k*N + j]
    C[i*N + j] = suma
```

- No se usa ninguna librería optimizada (BLAS, Eigen, NumPy, gonum, etc.).
- No se reordenan bucles (i‑k‑j), no hay *tiling*, ni paralelismo, ni vectorización manual.

## 2. Tipo y representación de datos

| Aspecto | Decisión | Motivo |
|---|---|---|
| Tipo | `double` IEEE‑754 de 64 bits (`double`, `float64`, `double`, `float`) | Mismo tipo en los 4 lenguajes |
| Almacenamiento | Arreglo **plano row‑major** de N×N (`std::vector<double>`, `[]float64`, `double[]`, `list`) | Mismo patrón de acceso a memoria |
| Matriz C | Reservada **antes** del temporizador y reutilizada entre repeticiones | La reserva de memoria no forma parte de la multiplicación |

## 3. Generación controlada de las matrices

- Generador **SplitMix64** implementado de forma idéntica en los 4 lenguajes (aritmética
  entera sin signo de 64 bits; en Python con máscara `& 0xFFFFFFFFFFFFFFFF`, en Java con `>>>`).
- Conversión a real en `[0, 1)`: `(x >> 11) × 2⁻⁵³` (53 bits de mantisa, exacta).
- Para cada N el generador se reinicia con la **semilla 42**; se genera primero A y luego B.
- Por lo tanto, **los cuatro lenguajes multiplican exactamente las mismas matrices**.

## 4. Medición del tiempo

| Lenguaje | Reloj | Tipo |
|---|---|---|
| C++ | `std::chrono::steady_clock` | monotónico |
| Go | `time.Now()` / `time.Since()` | monotónico |
| Java | `System.nanoTime()` | monotónico |
| Python | `time.perf_counter_ns()` | monotónico |

El temporizador se inicia **inmediatamente antes** de llamar a `multiplicar` y se detiene
**inmediatamente después** de obtener C. Quedan fuera de la medición: generación de A y B,
reserva de C, cálculo del checksum y escritura de CSV.

## 5. Verificación de equivalencia funcional

Tras cada repetición (fuera del temporizador) se calcula la suma de todos los elementos de C
y se registran `C[0,0]` y `C[N-1,N-1]` en `results/verification/<lang>_checksum.csv`.
El script `scripts/verify_equivalence.py` exige **igualdad exacta (bit a bit)** entre
lenguajes. Esto es posible porque:

- el orden de las operaciones de punto flotante es idéntico en los 4 programas, y
- se desactiva la fusión *multiply‑add* (FMA): C++ con `-ffp-contract=off`; en Go la
  conversión explícita `float64(a*b)` impide la fusión; Java (≥17) es estrictamente IEEE;
  CPython no fusiona.

El cálculo del checksum también impide que el compilador elimine la multiplicación como
código muerto.

## 6. Condiciones de compilación/ejecución

| Lenguaje | Imagen base | Compilación / ejecución |
|---|---|---|
| C++ | `gcc:14.2.0` | `g++ -O2 -std=c++17 -ffp-contract=off` |
| Go | `golang:1.23.4-bookworm` | `go build` (gc, optimizaciones por defecto, `CGO_ENABLED=0`) |
| Java | `eclipse-temurin:21.0.5_11-jdk` | `javac`; `java -Xms1g -Xmx1g` (HotSpot JIT por defecto) |
| Python | `python:3.12.8-slim-bookworm` | CPython 3.12 interpretado, sin dependencias |

Se usa el nivel de optimización **habitual** de cada ecosistema (no el máximo posible): el
objetivo es comparar implementaciones típicas, no la mejor implementación posible.

## 7. Ejecución

- 4 lenguajes × 3 tamaños (N = 500, 1000, 1500) × 10 repeticiones = **120 mediciones**.
- Cada lenguaje se ejecuta en **su propio contenedor**, uno a la vez (Snakemake con
  `cores: 1` y recurso `benchmark_slot=1`), sin red (`--network none`).
- Dentro de un contenedor, las 10 repeticiones de cada N se ejecutan en el mismo proceso.
  La repetición 1 de Java incluye el calentamiento del JIT: se **conserva** (no se descarta)
  y se analiza en `tiempo_por_repeticion.png`.

## 8. Amenazas a la validez

| Amenaza | Mitigación |
|---|---|
| Ruido del sistema (otros procesos, *turbo boost*, temperatura) | Ejecución secuencial; 10 repeticiones; registro del entorno; recomendación de máquina en reposo |
| Calentamiento JIT (Java) | Se documenta y visualiza; repetición 1 conservada |
| Arquitectura híbrida (núcleos P/E de Intel Core Ultra) | Se registra la CPU; opcionalmente fijar núcleo con `--cpuset-cpus` |
| Diferencias de optimización entre compiladores | Se usan los niveles por defecto documentados en la sección 6 |
| Heterocedasticidad (tiempos en distintos órdenes de magnitud) | ANOVA también sobre log10(tiempo) y Kruskal‑Wallis como robustez |
| Sobrecarga de contenedores | Igual para los 4 lenguajes; se mide solo dentro del proceso |
