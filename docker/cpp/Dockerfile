# Imagen reproducible para la implementación C++.
# Construcción manual (desde la raíz del repositorio):
#   docker build -f docker/cpp/Dockerfile -t matmul-cpp:1.0 .
FROM docker.io/library/gcc:14.2.0

LABEL org.opencontainers.image.title="matmul-cpp" \
      org.opencontainers.image.description="Benchmark naive NxN - C++ (g++ -O2)" \
      org.opencontainers.image.source="https://github.com/Pmiqueles-usach/Modulo2-Inv-experimental"

WORKDIR /opt/matmul
COPY src/cpp/matmul.cpp .
# -O2: optimización estándar; -ffp-contract=off: sin FMA, para resultados bit a bit idénticos a los demás lenguajes.
RUN g++ -O2 -std=c++17 -ffp-contract=off -o matmul matmul.cpp

ENTRYPOINT ["/opt/matmul/matmul"]
CMD ["/results/raw/cpp.csv", "500,1000,1500", "10", "42", "/results/verification/cpp_checksum.csv"]
