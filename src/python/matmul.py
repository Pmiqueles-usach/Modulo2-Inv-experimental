"""Multiplicación naive de matrices NxN (Python puro, sin NumPy).

Uso: python matmul.py <salida.csv> <tamaños: 500,1000,1500> <repeticiones> <semilla> [checksum.csv]

Protocolo común a las cuatro implementaciones (ver docs/PROTOCOLO.md):
  - Matrices float (double IEEE-754), almacenamiento plano row-major (lista de N*N).
  - Generación determinista con SplitMix64 (A primero, luego B), estado reiniciado por cada N.
  - Algoritmo naive i-j-k con acumulador local.
  - El temporizador mide SOLO la multiplicación (matrices ya creadas y C ya reservada).
"""

import sys
import time

MASCARA_64 = 0xFFFFFFFFFFFFFFFF


class SplitMix64:
    """Generador SplitMix64: idéntico en C++, Go, Java y Python."""

    def __init__(self, semilla: int) -> None:
        self.state = semilla & MASCARA_64

    def next(self) -> int:
        self.state = (self.state + 0x9E3779B97F4A7C15) & MASCARA_64
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASCARA_64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASCARA_64
        return z ^ (z >> 31)

    def next_double(self) -> float:
        """Real uniforme en [0, 1) con 53 bits de precisión."""
        return (self.next() >> 11) * (1.0 / (1 << 53))


def generar_matrices(n: int, semilla: int) -> tuple[list[float], list[float]]:
    """Genera A y B (en ese orden) a partir de la semilla."""
    rng = SplitMix64(semilla)
    a = [rng.next_double() for _ in range(n * n)]
    b = [rng.next_double() for _ in range(n * n)]
    return a, b


def multiplicar(n: int, a: list[float], b: list[float], c: list[float]) -> None:
    """Algoritmo naive i-j-k: C = A x B."""
    for i in range(n):
        for j in range(n):
            suma = 0.0
            for k in range(n):
                suma += a[i * n + k] * b[k * n + j]
            c[i * n + j] = suma


def checksum(c: list[float]) -> float:
    s = 0.0
    for x in c:
        s += x
    return s


def main() -> int:
    if len(sys.argv) < 5:
        print(__doc__, file=sys.stderr)
        return 1
    salida = sys.argv[1]
    tamanos = [int(t) for t in sys.argv[2].split(",")]
    repeticiones = int(sys.argv[3])
    semilla = int(sys.argv[4])
    salida_checksum = sys.argv[5] if len(sys.argv) > 5 else None

    chk = open(salida_checksum, "w", encoding="utf-8") if salida_checksum else None
    with open(salida, "w", encoding="utf-8") as csv:
        csv.write("language,N,repetition,time_seconds\n")
        if chk:
            chk.write("language,N,repetition,checksum,c_first,c_last\n")
        for n in tamanos:
            a, b = generar_matrices(n, semilla)
            c = [0.0] * (n * n)
            for r in range(1, repeticiones + 1):
                inicio = time.perf_counter_ns()
                multiplicar(n, a, b, c)
                fin = time.perf_counter_ns()
                segundos = (fin - inicio) / 1e9

                csv.write(f"python,{n},{r},{segundos:.9f}\n")
                csv.flush()
                s = checksum(c)
                if chk:
                    chk.write(f"python,{n},{r},{s:.17g},{c[0]:.17g},{c[-1]:.17g}\n")
                    chk.flush()
                print(f"[python] N={n} rep={r} t={segundos:.6f} s checksum={s:.6f}", file=sys.stderr)
    if chk:
        chk.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
