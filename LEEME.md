# LEEME – Cómo ejecutar cada programa (versión simple)

Guía rápida para compilar y ejecutar a mano las cuatro implementaciones.
La documentación completa del experimento está en [README.md](README.md).

## Lo que se escribe después del programa (igual en los 4 lenguajes)

```
<programa>   resultado.csv   500,1000,1500   10   42
                  ①               ②          ③    ④
```

| | Qué es | Ejemplo |
|---|---|---|
| ① | **Archivo donde quedan los resultados** | `cpp.csv` |
| ② | **Tamaños N**, separados por coma y sin espacios | `500,1000,1500` o solo `200` |
| ③ | Repeticiones por cada N | `10` |
| ④ | Semilla para generar las matrices (dejar en 42) | `42` |

**Para cambiar N no se edita el código:** se cambia el valor ② en el comando.

Todos los comandos se ejecutan desde la carpeta del proyecto (la que contiene este archivo).

## 1. C++ (`src/cpp/matmul.cpp`)

Primero se compila y después se ejecuta:

```bash
g++ -O2 -o matmul_cpp src/cpp/matmul.cpp
./matmul_cpp cpp.csv 200 3 42
```

## 2. Go (`src/go/matmul.go`)

```bash
cd src/go
go build -o ../../matmul_go .
cd ../..
./matmul_go go.csv 200 3 42
```

## 3. Java (`src/java/MatMul.java`)

Con Java 11 o superior se compila y ejecuta en un solo paso:

```bash
java src/java/MatMul.java java.csv 200 3 42
```

Forma clásica, si tiene `javac`:

```bash
javac src/java/MatMul.java
java -cp src/java MatMul java.csv 200 3 42
```

## 4. Python (`src/python/matmul.py`)

No se compila:

```bash
python3 src/python/matmul.py python.csv 200 3 42
```

## Dónde quedan los resultados

En el archivo indicado en ①, dentro de la carpeta desde donde se ejecutó el comando
(por ejemplo `cpp.csv`). Para verlo:

```bash
cat cpp.csv
```

```
language,N,repetition,time_seconds
cpp,200,1,0.004794754
cpp,200,2,0.004691888
cpp,200,3,0.004651437
```

Mientras corre, el programa también muestra cada repetición en pantalla.

## Dónde lee el programa la N

En cada archivo hay una línea que toma el valor ② del comando:

| Lenguaje | Línea |
|---|---|
| C++ | `src/cpp/matmul.cpp`, línea 77 → `parsear_tamanos(argv[2])` |
| Go | `src/go/matmul.go`, línea 80 → `os.Args[2]` |
| Java | `src/java/MatMul.java`, línea 80 → `args[1].split(",")` |
| Python | `src/python/matmul.py`, línea 66 → `sys.argv[2].split(",")` |

Así N se cambia sin tocar el código y los 4 lenguajes usan los mismos tamaños.

## Tamaños recomendados

Python es unas 200 veces más lento que C++:

- **Para probar o mostrar en clase:** `200` o `200,400` (Python tarda menos de 10 s por repetición).
- **Experimento oficial:** `500,1000,1500 10 42`. Python tarda más de 1 hora; ya está ejecutado
  y sus resultados están en `results/raw/`.

## ¿Quiere entender el código?

Vea [docs/EXPLICACION_CODIGO.md](docs/EXPLICACION_CODIGO.md): explica cada parte en relación con lo que pide la actividad.

## Requisitos

`g++`, Go 1.20 o superior, Java 11 o superior y Python 3.9 o superior.
Sin estos compiladores se puede usar Docker: ver la sección 9b del [README.md](README.md).
