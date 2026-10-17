# Imagen reproducible para la implementación Java.
# Construcción manual (desde la raíz del repositorio):
#   docker build -f docker/java/Dockerfile -t matmul-java:1.0 .
FROM docker.io/library/eclipse-temurin:21.0.5_11-jdk

LABEL org.opencontainers.image.title="matmul-java" \
      org.opencontainers.image.description="Benchmark naive NxN - Java (OpenJDK Temurin 21, HotSpot JIT)" \
      org.opencontainers.image.source="https://github.com/Pmiqueles-usach/Modulo2-Inv-experimental"

WORKDIR /opt/matmul
COPY src/java/MatMul.java .
RUN javac -encoding UTF-8 MatMul.java

# Heap fijo para que la JVM no dependa de la memoria del host.
ENTRYPOINT ["java", "-Xms1g", "-Xmx1g", "-cp", "/opt/matmul", "MatMul"]
CMD ["/results/raw/java.csv", "500,1000,1500", "10", "42", "/results/verification/java_checksum.csv"]
