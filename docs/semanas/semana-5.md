# Semana 5 – Publicación del artifact y evaluación cruzada

**Etiqueta git:** `v1.0.0` · **Objetivo ACM:** *Artifacts Available* (+ *Results Reproduced* vía revisión cruzada)

## Lo que pide el módulo

- Publicar una versión estable en **Zenodo** con DOI e incorporarlo al README.
- Contenido mínimo: código de los 4 lenguajes, README, Dockerfile, Snakefile, los 4 CSV,
  `benchmark.csv`, análisis estadístico, tablas y gráficos, licencia y mini datasheet FAIR.
- Evaluar el artifact de un compañero usando solo su artifact publicado (construir imágenes,
  ejecutar Snakemake, verificar CSV y `benchmark.csv`), registrando dificultades,
  dependencias faltantes, ambigüedades, modificaciones y diferencias de resultados.
- Presentación final: resultados, artifact en Zenodo y experiencia de evaluación cruzada.

## Entregables

| Entregable | Ubicación | Estado |
|---|---|---|
| Metadatos Zenodo | [.zenodo.json](../../.zenodo.json), [CITATION.cff](../../CITATION.cff) | ✅ |
| Procedimiento de publicación | [ZENODO.md](../ZENODO.md) | ✅ |
| Verificación de contenido mínimo | `scripts/check_artifact.sh` | ✅ |
| Licencias | [LICENSE](../../LICENSE) (MIT), [LICENSE-DATA](../../LICENSE-DATA) (CC BY 4.0) | ✅ |
| Mini datasheet FAIR | [DATASHEET_FAIR.md](../DATASHEET_FAIR.md) | ✅ |
| Release `v1.0.0` y DOI | Zenodo | ⏳ requiere acción del autor |
| DOI en README | README línea 3 | ⏳ |
| Plantilla de evaluación cruzada | [PLANTILLA_EVALUACION.md](../evaluacion-cruzada/PLANTILLA_EVALUACION.md) | ✅ |
| Evaluación del artifact de un compañero | `docs/evaluacion-cruzada/evaluacion-<compañero>.md` | ⏳ |
| Respuesta a la evaluación recibida | `docs/evaluacion-cruzada/respuesta-evaluacion.md` | ⏳ |

**DOI:** PENDIENTE

## Pasos

1. `scripts/check_artifact.sh` → todo `[ OK ]`.
2. Seguir [ZENODO.md](../ZENODO.md) (release `v1.0.0` → DOI).
3. Actualizar DOI en README, CITATION.cff, DATASHEET y este documento; commit y push.
4. Entregar el DOI al compañero evaluador.
5. Evaluar el artifact del compañero con la plantilla (en una carpeta aparte, descargando
   **desde Zenodo**, no desde GitHub).
6. Registrar la experiencia y preparar la presentación final.

## Guion de presentación final

| Bloque | Contenido |
|---|---|
| Resultados | ANOVA, interacción, Tukey; figura de interacción y speedup |
| Artifact | Página de Zenodo, DOI, contenido, licencias, datasheet |
| Evaluación cruzada (como evaluador) | Qué funcionó, qué falló, cuánto tiempo, dictamen ACM |
| Evaluación cruzada (como evaluado) | Problemas reportados y correcciones (nueva versión si aplica) |
| Lecciones | Repeatability vs reproducibility; qué se reproduce en un benchmark de tiempos |
