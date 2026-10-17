// Multiplicación naive de matrices NxN (Java).
//
// Uso: java MatMul <salida.csv> <tamaños: 500,1000,1500> <repeticiones> <semilla> [checksum.csv]
//
// Protocolo común a las cuatro implementaciones (ver docs/PROTOCOLO.md):
//   - Matrices double, almacenamiento plano row-major (double[N*N]).
//   - Generación determinista con SplitMix64 (A primero, luego B), estado reiniciado por cada N.
//   - Algoritmo naive i-j-k con acumulador local.
//   - El temporizador mide SOLO la multiplicación (matrices ya creadas y C ya reservada).

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Locale;

public class MatMul {

    /** Generador SplitMix64: idéntico en C++, Go, Java y Python. */
    static final class SplitMix64 {
        private long state;

        SplitMix64(long seed) {
            this.state = seed;
        }

        long next() {
            state += 0x9E3779B97F4A7C15L;
            long z = state;
            z = (z ^ (z >>> 30)) * 0xBF58476D1CE4E5B9L;
            z = (z ^ (z >>> 27)) * 0x94D049BB133111EBL;
            return z ^ (z >>> 31);
        }

        /** Real uniforme en [0, 1) con 53 bits de precisión. */
        double nextDouble() {
            return (next() >>> 11) * 0x1.0p-53;
        }
    }

    /** Genera A y B (en ese orden) a partir de la semilla. */
    static double[][] generarMatrices(int n, long semilla) {
        SplitMix64 rng = new SplitMix64(semilla);
        double[] a = new double[n * n];
        double[] b = new double[n * n];
        for (int i = 0; i < a.length; i++) a[i] = rng.nextDouble();
        for (int i = 0; i < b.length; i++) b[i] = rng.nextDouble();
        return new double[][] {a, b};
    }

    /** Algoritmo naive i-j-k: C = A x B. */
    static void multiplicar(int n, double[] a, double[] b, double[] c) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                double suma = 0.0;
                for (int k = 0; k < n; k++) {
                    suma += a[i * n + k] * b[k * n + j];
                }
                c[i * n + j] = suma;
            }
        }
    }

    static double checksum(double[] c) {
        double s = 0.0;
        for (double x : c) s += x;
        return s;
    }

    /** Formato con 17 dígitos significativos (equivalente a %.17g de C). */
    static String g17(double x) {
        return new java.math.BigDecimal(x).round(new java.math.MathContext(17)).stripTrailingZeros().toString();
    }

    public static void main(String[] args) throws IOException {
        if (args.length < 4) {
            System.err.println("Uso: java MatMul <salida.csv> <tamaños> <repeticiones> <semilla> [checksum.csv]");
            System.exit(1);
        }
        String salida = args[0];
        String[] partes = args[1].split(",");
        int repeticiones = Integer.parseInt(args[2]);
        long semilla = Long.parseUnsignedLong(args[3]);

        try (PrintWriter csv = new PrintWriter(new FileWriter(salida));
             PrintWriter chk = args.length > 4 ? new PrintWriter(new FileWriter(args[4])) : null) {
            csv.println("language,N,repetition,time_seconds");
            if (chk != null) chk.println("language,N,repetition,checksum,c_first,c_last");

            for (String p : partes) {
                int n = Integer.parseInt(p.trim());
                double[][] ab = generarMatrices(n, semilla);
                double[] a = ab[0];
                double[] b = ab[1];
                double[] c = new double[n * n];
                for (int r = 1; r <= repeticiones; r++) {
                    long inicio = System.nanoTime();
                    multiplicar(n, a, b, c);
                    long fin = System.nanoTime();
                    double segundos = (fin - inicio) / 1e9;

                    csv.println(String.format(Locale.ROOT, "java,%d,%d,%.9f", n, r, segundos));
                    csv.flush();
                    double s = checksum(c);
                    if (chk != null) {
                        chk.println("java," + n + "," + r + "," + g17(s) + "," + g17(c[0]) + "," + g17(c[c.length - 1]));
                        chk.flush();
                    }
                    System.err.println(String.format(Locale.ROOT, "[java] N=%d rep=%d t=%.6f s checksum=%.6f", n, r, segundos, s));
                }
            }
        }
    }
}
