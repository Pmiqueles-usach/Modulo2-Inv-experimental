# Semana 2 – Implementación y ejecución del experimento

**Etiqueta git:** `semana-2`

## Lo que pide el módulo

- Implementar el algoritmo naive NxN en C++, Go, Java y Python, funcionalmente equivalentes
  (mismo algoritmo, tipo de dato, matrices de entrada y criterio de medición), sin librerías
  optimizadas.
- Matrices generadas con semilla definida; N = 500, 1000, 1500; 10 repeticiones.
- Medir solo la multiplicación (matrices creadas antes de iniciar el temporizador).
- Resultados en `cpp.csv`, `go.csv`, `python.csv`, `java.csv` con columnas
  `language,N,repetition,time_seconds`.
- Registrar el entorno (CPU, RAM, SO, arquitectura, versiones).
- Presentar implementaciones y primeros resultados, justificando la comparabilidad.

## Entregables

| Entregable | Ubicación | Estado |
|---|---|---|
| Implementación C++ | [src/cpp/matmul.cpp](../../src/cpp/matmul.cpp) | ✅ |
| Implementación Go | [src/go/matmul.go](../../src/go/matmul.go) | ✅ |
| Implementación Java | [src/java/MatMul.java](../../src/java/MatMul.java) | ✅ |
| Implementación Python | [src/python/matmul.py](../../src/python/matmul.py) | ✅ |
| Justificación de equivalencia y medición | [PROTOCOLO.md](../PROTOCOLO.md) | ✅ |
| CSV por lenguaje | [results/raw/](../../results/raw/) | ✅ |
| Verificación de equivalencia | [results/verification/equivalence_report.md](../../results/verification/equivalence_report.md) | ✅ |
| Registro del entorno | [results/environment/environment.md](../../results/environment/environment.md) | ✅ |

## Decisiones para asegurar comparabilidad

1. **Mismo generador en los 4 lenguajes (SplitMix64)** en vez del RNG nativo de cada lenguaje
   (`std::mt19937`, `math/rand`, `java.util.Random`, `random`), que producirían matrices
   distintas con la misma semilla.
2. **Arreglo plano row‑major** en los 4 lenguajes (mismo patrón de acceso a memoria).
3. **Orden i‑j‑k** con acumulador local, idéntico.
4. **Sin FMA** (`-ffp-contract=off`, conversión explícita en Go) → resultados bit a bit
   idénticos, verificables con checksum.
5. **C reservada fuera del temporizador**; reloj monotónico de alta resolución.
6. **Optimización por defecto** de cada ecosistema (`-O2`, `go build`, HotSpot, CPython).
7. **Calentamiento JIT de Java no descartado**: se reporta y se visualiza.

## Interfaz común de los programas

```
<programa> <salida.csv> <tamaños separados por coma> <repeticiones> <semilla> [checksum.csv]
```

## Primeros resultados

Ver [results/analysis/tables/descriptivos.md](../../results/analysis/tables/descriptivos.md) y la
sección 11 del README.

## Guion de presentación

1. Código lado a lado de la función `multiplicar` en los 4 lenguajes (idénticas).
2. Generador SplitMix64 y por qué no usar el RNG nativo.
3. Dónde empieza y termina el temporizador.
4. Reporte de equivalencia: checksums idénticos.
5. Tabla de tiempos medios y primeras observaciones.
