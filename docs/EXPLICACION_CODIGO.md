# Explicación del código, parte por parte

Esta guía explica los cuatro programas (`src/cpp/matmul.cpp`, `src/go/matmul.go`,
`src/java/MatMul.java` y `src/python/matmul.py`) **siempre en relación con lo que pide la
actividad**. Los ejemplos usan C++, pero los cuatro tienen las mismas partes, con los mismos
nombres y en el mismo orden.

---

## 0. Qué pide la actividad y qué parte del código lo cumple

| La actividad pide… | Parte del código | Sección |
|---|---|---|
| Multiplicar matrices N×N con el algoritmo naive | `multiplicar()` | 4 |
| Probar N = 500, 1000 y 1500 | lectura de argumentos (valor ②) | 1 |
| 10 repeticiones por N | ciclo `for r = 1..repeticiones` | 5 |
| Medir el tiempo de ejecución | `inicio` / `fin` alrededor de `multiplicar()` | 5 |
| Un CSV por lenguaje con `language,N,repetition,time_seconds` | escritura del CSV | 6 |
| Que la comparación sea justa (mismo problema en los 4 lenguajes) | `SplitMix64` + semilla 42 + `checksum` | 2 y 7 |

Todo lo demás (Docker, Snakemake, ANOVA) usa los CSV que generan estos programas.

---

## Vista general: el programa en 5 pasos

```
1. Leer argumentos   →  archivo de salida, tamaños N, repeticiones, semilla
2. Para cada N:
     generar A y B (números "aleatorios" pero siempre los mismos)
     reservar C
3.   Repetir 10 veces:
        iniciar cronómetro → C = A × B → detener cronómetro
4.      escribir una línea en el CSV
5.      (opcional) escribir el checksum de C para comprobar equivalencia
```

---

## 1. Leer los argumentos (de dónde sale N)

```cpp
const std::string salida = argv[1];                      // ① archivo CSV
const std::vector<int> tamanos = parsear_tamanos(argv[2]); // ② "500,1000,1500" → [500, 1000, 1500]
const int repeticiones = std::stoi(argv[3]);             // ③ 10
const uint64_t semilla = std::stoull(argv[4]);           // ④ 42
```

- `argv` es la lista de lo que se escribió en la terminal después del nombre del programa.
- `parsear_tamanos` corta el texto `"500,1000,1500"` en cada coma y convierte cada trozo a número.
- **Por qué así:** N no está fijo en el código. Se cambia en el comando, y como los cuatro
  programas reciben los mismos argumentos, es imposible que un lenguaje use otro N por error.

En Java los índices empiezan uno antes (`args[0]` es el archivo) porque Java no incluye el nombre
del programa en la lista. Es la misma información.

---

## 2. Generar las matrices: `SplitMix64` y la semilla

```cpp
struct SplitMix64 {
    uint64_t state;
    uint64_t next() {
        state += 0x9E3779B97F4A7C15ULL;
        uint64_t z = state;
        z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
        z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
        return z ^ (z >> 31);
    }
    double next_double() { return static_cast<double>(next() >> 11) * 0x1.0p-53; }
};
```

**Qué es:** un generador de números pseudoaleatorios. A partir de un número inicial (la
*semilla*, 42) produce una secuencia que parece aleatoria, pero es **siempre la misma**.

**Por qué no se usa `rand()` o `random()` de cada lenguaje:** cada lenguaje tiene su propio
generador y, con la misma semilla, cada uno daría números distintos. C++, Go, Java y Python
multiplicarían entonces matrices diferentes y la comparación no sería justa. SplitMix64 es un
algoritmo corto y público que se puede escribir igual en los cuatro lenguajes, y así los cuatro
producen exactamente los mismos números.

**Cómo leerlo sin entrar en detalle:**

- Los números hexadecimales largos (`0x9E37…`) son constantes fijas del algoritmo publicado. No
  se cambian.
- `^` (XOR) y `>>` (desplazar bits) mezclan los bits para que el resultado parezca aleatorio.
- `next_double()` convierte el entero de 64 bits en un real entre 0 y 1: se queda con 53 bits
  (`>> 11`), porque un `double` guarda exactamente 53 bits de precisión, y divide por 2⁵³
  (`0x1.0p-53` significa 2⁻⁵³).

**Diferencias por lenguaje (mismo resultado):**

| Lenguaje | Detalle | Motivo |
|---|---|---|
| Python | `& MASCARA_64` después de cada operación | Los enteros de Python no tienen límite; la máscara los recorta a 64 bits como en C++ |
| Java | `long` y `>>>` en lugar de `>>` | Java no tiene enteros sin signo; `>>>` desplaza como si no tuvieran signo |
| Go | `uint64` | Igual que C++ |

```cpp
static void generar_matrices(int n, uint64_t semilla, ...) {
    SplitMix64 rng(semilla);                    // se reinicia con 42 para cada N
    for (auto& x : a) x = rng.next_double();    // primero todos los de A
    for (auto& x : b) x = rng.next_double();    // luego todos los de B
}
```

El orden importa: **primero A, luego B**, en los cuatro lenguajes. Si uno llenara B primero, sus
matrices serían distintas.

---

## 3. La matriz "plana" (row-major)

En vez de una tabla `A[i][k]`, cada matriz es **una sola lista de N·N números**, guardada fila por
fila:

```
Matriz 3×3                 Lista plana (row-major)
| a b c |                  índice: 0 1 2 3 4 5 6 7 8
| d e f |         →        valor:  a b c d e f g h i
| g h i |
```

El elemento de la fila `i`, columna `k` está en la posición **`i * n + k`**.
Ejemplo: `f` está en la fila 1, columna 2 → `1*3 + 2 = 5`.

**Por qué así:** una "lista de listas" se guarda de forma distinta en cada lenguaje (en Python y
Java son objetos separados en memoria). Con una lista plana los cuatro lenguajes guardan los datos
de la misma forma y la comparación mide el lenguaje, no la estructura de datos.

---

## 4. La multiplicación naive i-j-k (lo central)

```cpp
for (int i = 0; i < n; ++i)             // cada fila de A
    for (int j = 0; j < n; ++j) {       // cada columna de B
        double suma = 0.0;
        for (int k = 0; k < n; ++k)     // recorre la fila i de A y la columna j de B
            suma += a[i * n + k] * b[k * n + j];   // A[i][k] * B[k][j]
        c[i * n + j] = suma;            // C[i][j]
    }
```

Es la definición de los libros: **C[i][j] = Σₖ A[i][k] · B[k][j]**.

- `suma` es un acumulador local: suma los N productos y escribe en C una sola vez.
- Son tres ciclos anidados de N vueltas, es decir **N³ multiplicaciones**:
  - N = 500 → 125 millones
  - N = 1500 → 3375 millones (27 veces más)

  Por eso pasar de 500 a 1500 multiplica el tiempo por unas 27 a 70 veces.
- **"Naive"** significa que no se usan optimizaciones (bloques, paralelismo, bibliotecas como
  NumPy o BLAS). La actividad lo exige así para comparar los lenguajes con el mismo algoritmo.

---

## 5. Medir el tiempo (solo la multiplicación)

```cpp
for (int r = 1; r <= repeticiones; ++r) {
    const auto inicio = std::chrono::steady_clock::now();
    multiplicar(n, a, b, c);
    const auto fin = std::chrono::steady_clock::now();
    const double segundos = std::chrono::duration<double>(fin - inicio).count();
```

- El cronómetro rodea **solo** `multiplicar()`. Generar las matrices, escribir el CSV y calcular
  el checksum quedan **fuera** del tiempo medido, porque la actividad compara la multiplicación.
- Se usa un **reloj monotónico**, que nunca retrocede aunque cambie la hora del sistema:

  | Lenguaje | Reloj |
  |---|---|
  | C++ | `steady_clock` |
  | Go | `time.Now()` / `time.Since()` |
  | Java | `System.nanoTime()` |
  | Python | `time.perf_counter_ns()` |

- A, B y C se crean **una vez por N**, antes de las repeticiones. Cada repetición reutiliza las
  mismas matrices y no mide el tiempo de reservar memoria.
- Las 10 repeticiones dan la variabilidad que necesita el ANOVA de la semana 4.

---

## 6. Escribir el CSV

```cpp
csv << "language,N,repetition,time_seconds\n";      // encabezado, una sola vez
...
csv << "cpp," << n << "," << r << "," << std::fixed << std::setprecision(9) << segundos << "\n";
csv.flush();
```

- Cada repetición escribe una línea, por ejemplo `cpp,500,1,0.080312345`.
- Se usan **9 decimales**, es decir nanosegundos.
- `flush()` obliga a escribir la línea en el disco de inmediato. Si la ejecución se corta (Python
  tarda más de una hora), las líneas ya medidas no se pierden.
- En Java, `Locale.ROOT` asegura que el decimal sea un **punto**. En un computador configurado en
  español, Java escribiría `0,08`, que rompería el CSV.

---

## 7. Checksum: comprobar que los cuatro calculan lo mismo

```cpp
static double checksum(const std::vector<double>& c) {
    double s = 0.0;
    for (double x : c) s += x;   // suma de todos los elementos de C
    return s;
}
```

Si los cuatro lenguajes calculan bien la misma multiplicación, la suma de C, el primer elemento y
el último deben ser **iguales**. Se escriben con 17 dígitos (`setprecision(17)`), suficientes para
comparar bit a bit. Esta es la evidencia de que la comparación es justa (criterio *consistent* de
ACM).

**Por qué aparecen `-ffp-contract=off` (C++) y `float64(...)` (Go):** algunos procesadores pueden
fusionar `suma + a*b` en una sola instrucción (FMA), que redondea una vez en lugar de dos. El
resultado cambia en el último dígito y el checksum dejaría de coincidir. Esas dos marcas impiden
la fusión, de modo que los cuatro lenguajes hacen exactamente las mismas operaciones. Java y
Python nunca fusionan, así que no necesitan nada.

El checksum es **opcional** (quinto argumento). Si no se indica, el programa solo escribe los
tiempos.

---

## 8. El mensaje en pantalla

```
[cpp] N=500 rep=1 t=0.080312 s checksum=62513...
```

Va a la **salida de errores** (`stderr`), no al CSV. Sirve para seguir el avance mientras corre y
no mezcla texto con los datos.

---

## 9. Qué NO se debe cambiar (para no romper la equivalencia)

| No cambiar | Porque |
|---|---|
| El algoritmo i-j-k y el acumulador `suma` | La actividad pide el algoritmo naive igual en los 4 |
| `SplitMix64`, el orden A→B y la semilla 42 | Las matrices dejarían de ser idénticas |
| Lo que queda dentro del cronómetro | Se mediría algo distinto en cada lenguaje |
| El encabezado del CSV | Snakemake y el análisis esperan exactamente esas columnas |
| `-O2 -ffp-contract=off` en C++ y `float64()` en Go | El checksum dejaría de coincidir |

**Se puede cambiar libremente desde el comando:** N, el número de repeticiones y el archivo de
salida (ver [LEEME.md](../LEEME.md)).
