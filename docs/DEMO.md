# Demostración en consola para la clase

Script: `scripts/demo.sh`. Recorre la actividad semana a semana mostrando cada comando antes de
ejecutarlo y espera **Enter** entre pasos. Usa matrices pequeñas (N = 200, 400; 3 repeticiones)
y escribe en `results_demo/`, sin tocar los resultados oficiales de `results/`.

## Antes de la clase (una sola vez)

```bash
cd ~/Documentos/000-DOCTORADO-2DOsem/Inv-Experimental_Modulo2
ENGINE="podman --cgroup-manager=cgroupfs" scripts/build_images.sh   # si las imágenes no existen
SIN_PAUSA=1 scripts/demo.sh > /dev/null                              # ensayo (≈1,5 min)
```

## En la clase

```bash
scripts/demo.sh          # todas las semanas (≈3 min con pausas)
scripts/demo.sh 2        # solo una semana: 1, 2, 3, 4 o 5
```

| Semana | Qué muestra | Mensaje clave |
|---|---|---|
| 1 | `git log` con etiquetas, pregunta, hipótesis, variables y diseño del README | El repositorio es el artifact |
| 2 | Función `multiplicar` en los 4 lenguajes y ubicación del temporizador | Mismo algoritmo, datos y medición |
| 3 | Dockerfile, imágenes construidas manualmente, `run` de los 4 contenedores, 4 CSV y checksums | **Functional**: ejecutable y verificado (resultado idéntico bit a bit) |
| 4 | Plan de Snakemake y ejecución completa con un comando; decisión estadística | **Reusable**: automatizado y parametrizable |
| 5 | `check_artifact.sh`, tabla de razones vs C++, decisión sobre H₀ y figura de interacción | Listo para Zenodo (**Available**) |

## Opciones

| Variable | Efecto |
|---|---|
| `DEMO_SIZES=300,600 DEMO_REPS=5` | Cambia el tamaño de la demo (Python con N=600 tarda ~35 s por repetición) |
| `SIN_PAUSA=1` | Ejecuta todo seguido |
| `ENGINE=docker` | Fuerza Docker (por defecto: Docker si está disponible; si no, Podman) |

## Si algo falla en vivo

- `permission denied ... docker.sock` → el script usa Podman automáticamente; o `ENGINE="podman --cgroup-manager=cgroupfs"`.
- `falta la imagen matmul-<x>:1.0` → `ENGINE="podman --cgroup-manager=cgroupfs" scripts/build_images.sh`.
- Sin tiempo → mostrar directamente `results/analysis/reporte_estadistico.md` y las figuras de `results/analysis/figures/`.
