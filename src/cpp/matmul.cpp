// Multiplicación naive de matrices NxN (C++).
//
// Uso: matmul <salida.csv> <tamaños: 500,1000,1500> <repeticiones> <semilla> [checksum.csv]
//
// Protocolo común a las cuatro implementaciones (ver docs/PROTOCOLO.md):
//   - Matrices double, almacenamiento plano row-major (vector de N*N).
//   - Generación determinista con SplitMix64 (A primero, luego B), estado reiniciado por cada N.
//   - Algoritmo naive i-j-k con acumulador local.
//   - El temporizador mide SOLO la multiplicación (matrices ya creadas y C ya reservada).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

// Generador SplitMix64: idéntico en C++, Go, Java y Python.
struct SplitMix64 {
    uint64_t state;
    explicit SplitMix64(uint64_t seed) : state(seed) {}
    uint64_t next() {
        state += 0x9E3779B97F4A7C15ULL;
        uint64_t z = state;
        z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
        z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
        return z ^ (z >> 31);
    }
    // Real uniforme en [0, 1) con 53 bits de precisión.
    double next_double() { return static_cast<double>(next() >> 11) * 0x1.0p-53; }
};

// Genera A y B (en ese orden) a partir de la semilla.
static void generar_matrices(int n, uint64_t semilla, std::vector<double>& a, std::vector<double>& b) {
    SplitMix64 rng(semilla);
    a.resize(static_cast<size_t>(n) * n);
    b.resize(static_cast<size_t>(n) * n);
    for (auto& x : a) x = rng.next_double();
    for (auto& x : b) x = rng.next_double();
}

// Algoritmo naive i-j-k: C = A x B.
static void multiplicar(int n, const std::vector<double>& a, const std::vector<double>& b, std::vector<double>& c) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            double suma = 0.0;
            for (int k = 0; k < n; ++k) {
                suma += a[i * n + k] * b[k * n + j];
            }
            c[i * n + j] = suma;
        }
    }
}

static double checksum(const std::vector<double>& c) {
    double s = 0.0;
    for (double x : c) s += x;
    return s;
}

static std::vector<int> parsear_tamanos(const std::string& texto) {
    std::vector<int> tamanos;
    std::stringstream ss(texto);
    std::string item;
    while (std::getline(ss, item, ',')) tamanos.push_back(std::stoi(item));
    return tamanos;
}

int main(int argc, char** argv) {
    if (argc < 5) {
        std::cerr << "Uso: " << argv[0] << " <salida.csv> <tamaños> <repeticiones> <semilla> [checksum.csv]\n";
        return 1;
    }
    const std::string salida = argv[1];
    const std::vector<int> tamanos = parsear_tamanos(argv[2]);
    const int repeticiones = std::stoi(argv[3]);
    const uint64_t semilla = std::stoull(argv[4]);
    const std::string salida_checksum = argc > 5 ? argv[5] : "";

    std::ofstream csv(salida);
    csv << "language,N,repetition,time_seconds\n";
    std::ofstream chk;
    if (!salida_checksum.empty()) {
        chk.open(salida_checksum);
        chk << "language,N,repetition,checksum,c_first,c_last\n";
    }

    for (int n : tamanos) {
        std::vector<double> a, b;
        generar_matrices(n, semilla, a, b);
        std::vector<double> c(static_cast<size_t>(n) * n, 0.0);
        for (int r = 1; r <= repeticiones; ++r) {
            const auto inicio = std::chrono::steady_clock::now();
            multiplicar(n, a, b, c);
            const auto fin = std::chrono::steady_clock::now();
            const double segundos = std::chrono::duration<double>(fin - inicio).count();

            csv << "cpp," << n << "," << r << "," << std::fixed << std::setprecision(9) << segundos << "\n";
            csv.flush();
            const double s = checksum(c);
            if (chk.is_open()) {
                chk << "cpp," << n << "," << r << "," << std::setprecision(17) << std::defaultfloat << s << ","
                    << c.front() << "," << c.back() << "\n";
                chk.flush();
            }
            std::cerr << "[cpp] N=" << n << " rep=" << r << " t=" << std::fixed << std::setprecision(6) << segundos
                      << " s checksum=" << std::setprecision(6) << s << std::defaultfloat << "\n";
        }
    }
    return 0;
}
