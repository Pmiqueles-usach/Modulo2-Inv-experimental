# Semana 3 – Entorno reproducible y evaluación funcional del artifact

**Etiqueta git:** `semana-3` · **Objetivo ACM:** *Artifacts Evaluated – Functional*

## Lo que pide el módulo

- Cuatro imágenes Docker (C++, Go, Python, Java) con lo necesario para compilar/ejecutar,
  construidas manualmente.
- README con instrucciones para que un tercero ejecute el experimento hasta este punto.
- Cada ejecución genera su CSV independiente con la estructura común.
- Revisar el artifact con los criterios ACM para alcanzar *Functional*.
- Demostración en clase con los contenedores y la documentación actualizada.

## Entregables

| Entregable | Ubicación | Estado |
|---|---|---|
| Dockerfile C++ (`gcc:14.2.0`) | [docker/cpp/Dockerfile](../../docker/cpp/Dockerfile) | ✅ |
| Dockerfile Go (`golang:1.23.4-bookworm`) | [docker/go/Dockerfile](../../docker/go/Dockerfile) | ✅ |
| Dockerfile Java (`eclipse-temurin:21.0.5_11-jdk`) | [docker/java/Dockerfile](../../docker/java/Dockerfile) | ✅ |
| Dockerfile Python (`python:3.12.8-slim-bookworm`) | [docker/python/Dockerfile](../../docker/python/Dockerfile) | ✅ |
| Instrucciones de construcción y ejecución manual | README §8–9 | ✅ |
| Script de ejecución manual por lenguaje | [scripts/run_container.sh](../../scripts/run_container.sh) | ✅ |
| Autoevaluación *Functional* | [ACM_BADGES.md §2.1](../ACM_BADGES.md) | ✅ |

## Decisiones de diseño de los contenedores

- **Versiones exactas** de imagen base (no `latest`).
- La imagen **compila el código dentro del build**: el binario se genera siempre igual a
  partir del código fuente versionado.
- `ENTRYPOINT` = programa; `CMD` = parámetros del experimento oficial → `docker run imagen`
  ejecuta el experimento completo sin argumentos.
- Resultados vía volumen `-v $PWD/results:/results:z` (`:z` para SELinux en Fedora/RHEL).
- `--user $(id -u):$(id -g)` (Docker) o `--userns=keep-id` (Podman) para que los CSV queden a
  nombre del usuario.
- `--network none`: el experimento no requiere red.

## Demostración (guion)

```bash
docker build -f docker/cpp/Dockerfile -t matmul-cpp:1.0 .      # (y go, java, python)
docker images | grep matmul
scripts/run_container.sh cpp 500 2 42 results_demo             # demostración corta
head results_demo/raw/cpp.csv
```

## Autoevaluación Functional

| Criterio | Cumple | Evidencia |
|---|---|---|
| Documented | ✅ | Inventario (README §6) e instrucciones (§8–9) |
| Consistent | ✅ | Todo componente produce o analiza los resultados |
| Complete | ✅ | Sin dependencias externas no incluidas, salvo imágenes base oficiales |
| Exercisable | ✅ | 4 contenedores ejecutados; 4 CSV generados |
| Verificación | ✅ | Checksums idénticos entre lenguajes |
