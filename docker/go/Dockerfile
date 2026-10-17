# Imagen reproducible para la implementación Go.
# Construcción manual (desde la raíz del repositorio):
#   docker build -f docker/go/Dockerfile -t matmul-go:1.0 .
FROM docker.io/library/golang:1.23.4-bookworm

LABEL org.opencontainers.image.title="matmul-go" \
      org.opencontainers.image.description="Benchmark naive NxN - Go (gc)" \
      org.opencontainers.image.source="https://github.com/Pmiqueles-usach/Modulo2-Inv-experimental"

WORKDIR /opt/matmul
COPY src/go/go.mod src/go/matmul.go ./
# Compilación por defecto de gc (optimizaciones activas), sin cgo.
ENV CGO_ENABLED=0 GOFLAGS=-trimpath
RUN go build -o matmul .

ENTRYPOINT ["/opt/matmul/matmul"]
CMD ["/results/raw/go.csv", "500,1000,1500", "10", "42", "/results/verification/go_checksum.csv"]
