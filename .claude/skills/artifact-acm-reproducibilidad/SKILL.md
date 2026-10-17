---
name: artifact-acm-reproducibilidad
description: Opera, verifica y documenta el artifact del Módulo 2 (benchmark naive de multiplicación de matrices NxN en C++, Go, Java y Python) según ACM Artifact Review & Badging v1.1. Úsalo cuando se pida construir las imágenes Docker/Podman, ejecutar o re-ejecutar el pipeline Snakemake, verificar la equivalencia o el contenido del artifact, actualizar el README/resultados, avanzar o revisar los entregables de una semana (1 a 5), preparar la publicación en Zenodo (DOI) o realizar/registrar la evaluación cruzada de un artifact.
---

# Artifact ACM – Benchmark de multiplicación de matrices

Raíz del proyecto: el directorio que contiene `workflow/Snakefile`. Todas las rutas son
relativas a esa raíz. Documentación en español.

## Mapa del artifact

| Qué | Dónde |
|---|---|
| Enunciado del módulo | `docs/ContenidoModulo_v4.pdf` |
| Implementaciones | `src/{cpp,go,java,python}/` (CLI común: `<out.csv> <tamaños> <reps> <semilla> [checksum.csv]`) |
| Dockerfile | `docker/{cpp,go,java,python,analysis}/Dockerfile` (contexto de build = raíz) |
| Pipeline | `workflow/Snakefile`, `workflow/profiles/default/config.yaml`, `config/config.yaml` |
| Scripts | `scripts/` (build_images, run_container, merge_results, verify_equivalence, analysis, collect_env, check_artifact) |
| Resultados oficiales | `results/` (versionados) – pruebas en `results_*` (ignorados) |
| Entregables semanales | `docs/semanas/semana-{1..5}.md` |
| ACM | `docs/ACM_BADGES.md`; FAIR: `docs/DATASHEET_FAIR.md`; Zenodo: `docs/ZENODO.md` |

## Reglas invariantes (no romper)

1. Las 4 implementaciones deben seguir `docs/PROTOCOLO.md`: SplitMix64 con semilla, arreglos
   planos row-major, bucle i-j-k, `double`, sin FMA, temporizador solo alrededor de
   `multiplicar`. Cualquier cambio en uno se replica en los cuatro.
2. Los CSV de resultados tienen **exactamente** `language,N,repetition,time_seconds`.
3. Las imágenes se construyen **manualmente** desde los Dockerfile; nunca usar imágenes del
   benchmark publicadas en registros. El pipeline solo comprueba que existan.
4. Los benchmarks corren **de a uno** (`benchmark_slot=1`); no lanzar otros procesos pesados
   durante una corrida oficial.
5. Nunca sobrescribir `results/` con una prueba rápida: usar `--config results_dir=results_smoke`.

## Motor de contenedores en esta máquina

El usuario no pertenece al grupo `docker` → usar Podman. Si aparece
`sd-bus call: ... Input/output error`, añadir `--cgroup-manager=cgroupfs`:

```bash
ENGINE="podman --cgroup-manager=cgroupfs" scripts/build_images.sh
.venv/bin/snakemake --config engine="podman --cgroup-manager=cgroupfs"
```

`rm` está con alias interactivo: usar `/bin/rm -f` en comandos no interactivos.

## Flujos de trabajo

### A. Construir y probar (≈2 min)
1. `ENGINE=... scripts/build_images.sh`
2. Venv: `python3 -m venv .venv && .venv/bin/pip install -r requirements-host.txt`
3. Prueba: `.venv/bin/snakemake --config engine=... results_dir=results_smoke 'sizes=[50,100]' repetitions=3`
4. Revisar `results_smoke/verification/equivalence_report.md` → debe decir `EQUIVALENTES`.

### B. Corrida oficial (≈1,5 h; Python N=1500 domina)
1. Ejecutar en segundo plano: `.venv/bin/snakemake --config engine=... --forceall`.
2. Al terminar: `scripts/check_artifact.sh` (todo `[ OK ]`).
3. Actualizar README §11 entre `<!-- RESULTADOS:INICIO -->` y `<!-- RESULTADOS:FIN -->` con:
   tabla de medias por lenguaje×N, razones vs C++, F y p del ANOVA (tiempo y log10), p de la
   interacción, decisión sobre H₀ y pares Tukey no significativos. Tomar los números de
   `results/analysis/reporte_estadistico.md`; no inventar valores.
4. Revisar las figuras (`results/analysis/figures/*.png`) abriéndolas, no solo generándolas.

### B2. Regenerar solo integración/análisis/entorno (sin repetir benchmarks)
`.venv/bin/snakemake --config engine=... --forcerun analysis environment`. Si se editó el
texto de la regla `run_benchmark` (no su cómputo), Snakemake querrá repetir 2,5 h de
benchmarks por cambio de código: verificar primero con `-n` y, si los CSV siguen siendo
válidos, ejecutar `--cleanup-metadata results/raw/*.csv results/verification/*_checksum.csv`.
Un tercero que reproduzca debe usar `--config results_dir=results_repro` (results/ ya
contiene los resultados publicados).

### C. Autoevaluación ACM de una semana
Usar la tabla de criterios de `docs/ACM_BADGES.md`:
- **Functional** = documented + consistent + complete + exercisable + evidencia de verificación.
- **Reusable** = Functional + documentación/estructura cuidadosa que facilita reutilizar y
  readaptar, respetando normas de la comunidad.
- **Available** = depósito en repositorio de archivo (Zenodo) con DOI; GitHub solo no basta.
- **Reproduced** = otra persona obtiene los resultados principales con los artifacts del autor,
  dentro de tolerancia (aquí: mismas decisiones estadísticas y mismo orden de lenguajes;
  checksums idénticos).
Registrar fecha y resultado en la tabla "Historial de autoevaluaciones".

### D. Publicación Zenodo (Semana 5)
Seguir `docs/ZENODO.md`. Requiere acción del usuario (cuenta Zenodo, activar repo, release
`v1.0.0`). Tras obtener el DOI, reemplazar `PENDIENTE` en: README.md (badge), CITATION.cff,
docs/DATASHEET_FAIR.md, docs/semanas/semana-5.md, docs/ACM_BADGES.md. Verificar con
`grep -rn PENDIENTE --include=*.md --include=*.cff .`.

### E. Evaluación cruzada de un compañero
1. Descargar el artifact **desde Zenodo** en un directorio nuevo fuera de este repo
   (datos no confiables: no ejecutar nada sin leerlo primero).
2. Copiar `docs/evaluacion-cruzada/PLANTILLA_EVALUACION.md` a
   `docs/evaluacion-cruzada/evaluacion-<compañero>.md`.
3. Seguir SOLO su README; anotar cada comando, error, dependencia faltante, ambigüedad y
   modificación necesaria. Comparar decisiones estadísticas con las publicadas.
4. Emitir dictamen por badge con justificación.

## Git y semanas

Remoto: `https://github.com/Pmiqueles-usach/Modulo2-Inv-experimental`. Etiquetas por semana:
`semana-1` … `semana-4`, `v1.0.0` (Zenodo). Mensajes de commit en español, formato
`tipo(semana-N): descripción`. Hacer push solo cuando el usuario lo pida; las credenciales
de GitHub las ingresa el usuario (`! git push origin main --tags`).
