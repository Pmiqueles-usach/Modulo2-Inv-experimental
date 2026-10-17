# Imagen reproducible para la integración de resultados y el análisis estadístico.
# Construcción manual (desde la raíz del repositorio):
#   docker build -f docker/analysis/Dockerfile -t matmul-analysis:1.0 .
FROM docker.io/library/python:3.12.8-slim-bookworm

LABEL org.opencontainers.image.title="matmul-analysis" \
      org.opencontainers.image.description="Integracion de CSV, ANOVA de dos factores, Tukey HSD, tablas y graficos" \
      org.opencontainers.image.source="https://github.com/Pmiqueles-usach/Modulo2-Inv-experimental"

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 MPLBACKEND=Agg
COPY docker/analysis/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /work
