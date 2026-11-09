# Evaluación cruzada – Semana 5

El 2026-11-09 Pier Miqueles evaluó los cuatro artifacts que el profesor envió.
Cada evaluación sigue [PLANTILLA_EVALUACION.md](PLANTILLA_EVALUACION.md) y usa solo el depósito
de Zenodo, su README y sus archivos de configuración y automatización.

## Resumen de dictámenes

| Autor | DOI | Pipeline | Tiempo | Available | Functional | Reusable | Reproduced | Evaluación |
|---|---|---|---:|:-:|:-:|:-:|:-:|---|
| Joel Fuertes | [10.5281/zenodo.23988249](https://doi.org/10.5281/zenodo.23988249) | 4/4 pasos ✔ | 113 min | ✔ | ✔ | ✔ | ✔ | [evaluacion-fuertes.md](evaluacion-fuertes.md) |
| Jorge Fornes | [10.5281/zenodo.23987654](https://doi.org/10.5281/zenodo.23987654) | 19/19 pasos ✔ | 95 min | ✔ | ✔ (con reservas) | ✘ | ✔ (conclusiones generales) | [evaluacion-fornes.md](evaluacion-fornes.md) |
| Alejandro Pirez | [10.5281/zenodo.23954875](https://doi.org/10.5281/zenodo.23954875) | 19/19 pasos ✔ | 66 min | ✔ | ✔ | ✔ | ✔ | [evaluacion-pirez.md](evaluacion-pirez.md) |
| Jonathan Valenzuela | [10.5281/zenodo.23891451](https://doi.org/10.5281/zenodo.23891451) | 8/8 pasos ✔ | 102 min | ✔ | ✔ | ✔ | ✔ | [evaluacion-valenzuela.md](evaluacion-valenzuela.md) |

En los cuatro artifacts se verificó lo mismo:

- los 4 contenedores se construyen a mano desde sus Dockerfile y se ejecutan;
- se generan `cpp.csv`, `go.csv`, `java.csv` y `python.csv`, que se integran automáticamente en un `benchmark.csv` de 120 filas;
- se ejecutan el ANOVA y las tablas y gráficos.

En los cuatro casos se rechaza H₀ y Python es 1 a 2 órdenes de magnitud más lento que el lenguaje más rápido.

## Hallazgos transversales

1. **Los segundos no se reproducen; las decisiones sí.** En las cuatro reproducciones se mantienen las mismas decisiones del ANOVA del autor. Los tiempos absolutos y el orden entre C++, Go y Java cambian con el hardware: con las mismas imágenes, C++ con N=1500 tardó 11,6 s en el equipo de Fuertes y 3,7 s en el del evaluador.
2. **La verificación de equivalencia numérica separa a los artifacts.** Fuertes valida contra matrices de control y Valenzuela compara checksums automáticamente (idénticos a los publicados). Fornes solo imprime el checksum y Pirez no lo calcula.
3. **Fijar versiones fue lo que más facilitó la reproducción.** Ayudaron los digests de las imágenes base (Fuertes) y los lockfiles de Python (Fuertes, Valenzuela, Pirez). Fornes no fija versiones y ni siquiera lista Snakemake.
4. **La documentación quedó desfasada en el depósito.** Solo el README archivado de Pirez contiene su DOI. Valenzuela y Fornes dicen "DOI pendiente" y Fuertes no lo menciona. Además, Fornes manda a clonar GitHub en vez de usar el zip de Zenodo. (El enunciado pide el DOI en el README de GitHub; aquí se evaluó solo el depósito).
5. **Validez interna.** Fornes compila C++ con `-O0` y Go/Java optimizados; por eso C++ aparece más lento que Go y Java. Es una decisión documentada, pero compara configuraciones de compilación además de lenguajes.

## Entorno y adaptaciones del evaluador (comunes a las cuatro)

| Elemento | Valor |
|---|---|
| Equipo | Intel Core Ultra 7 165H (22 hilos), 30,8 GB RAM, Fedora 42, kernel 6.18.8 |
| Motor de contenedores | Podman 5.8.2 rootless: el usuario no pertenece al grupo `docker` |
| Python del host | 3.13.13, con un venv por artifact y sus propios requisitos (Snakemake 9.27.1 en los cuatro) |

Las adaptaciones están **fuera** de los artifacts; no se modificó ningún archivo de los compañeros:

- Un ejecutable `docker` en el `PATH` que delega en `podman --cgroup-manager=cgroupfs "$@"`. Responde `linux` solo a `docker info --format {{.OSType}}`, un campo que Podman no tiene y que usa Fuertes.
- `CONTAINERS_REGISTRIES_CONF` con `unqualified-search-registries = ["docker.io"]`, para que Podman resuelva `gcc:…`, `eclipse-temurin:…` y los `FROM` con solo digest.

**Limitación:** para presentar el mismo día, los cuatro pipelines se ejecutaron **en paralelo**
(10:25–12:18). Dentro de cada pipeline los contenedores corrieron de a uno (`--cores 1`), y el
equipo tiene 22 hilos para 4 procesos de un hilo, pero la frecuencia turbo compartida puede
inflar los segundos absolutos. Por eso se comparan decisiones estadísticas, orden y razones,
no segundos.

## Procedimiento y reproducción de esta evaluación

```bash
# 1. Descargar cada artifact desde Zenodo (verifica MD5, no ejecuta nada)
python3 scripts/descargar_zenodo.py <DOI> ../eval-cruzada/<autor>
# 2. Leer su README y seguirlo (builds manuales + snakemake), registrando cada paso
# 3. Comparar publicado vs reproducido con el mismo análisis para ambos
#    (requiere pandas, numpy y statsmodels)
python scripts/comparar_evaluacion.py <publicado/benchmark.csv> <reproducido/benchmark.csv> salida.md
```

Las salidas del paso 3 están en [comparaciones/](comparaciones/). El análisis del evaluador
(ANOVA tipo II en segundos y en log10, y Tukey log10 por N) se aplica igual a todos, pero
**no reemplaza** el análisis de cada autor: el dictamen *Reproduced* se basa en las
conclusiones que el propio autor declara.
