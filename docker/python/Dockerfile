# Imagen reproducible para la implementación Python (CPython puro, sin NumPy).
# Construcción manual (desde la raíz del repositorio):
#   docker build -f docker/python/Dockerfile -t matmul-python:1.0 .
FROM docker.io/library/python:3.12.8-slim-bookworm

LABEL org.opencontainers.image.title="matmul-python" \
      org.opencontainers.image.description="Benchmark naive NxN - Python (CPython 3.12, sin librerias optimizadas)" \
      org.opencontainers.image.source="https://github.com/Pmiqueles-usach/Modulo2-Inv-experimental"

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONHASHSEED=0
WORKDIR /opt/matmul
COPY src/python/matmul.py .

ENTRYPOINT ["python", "/opt/matmul/matmul.py"]
CMD ["/results/raw/python.csv", "500,1000,1500", "10", "42", "/results/verification/python_checksum.csv"]
