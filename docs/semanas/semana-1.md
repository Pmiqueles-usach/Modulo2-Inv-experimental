# Semana 1 – Diseño experimental, GitHub y documentación del artifact

**Etiqueta git:** `semana-1` · **Presentación:** [../presentaciones/Presentacion_Semana_1_Experimentacion_Computacional_ACM.pptx](../presentaciones/Presentacion_Semana_1_Experimentacion_Computacional_ACM.pptx)

## Lo que pide el módulo

- Crear un repositorio GitHub como espacio de desarrollo, documentación y control de versiones.
- Versión inicial de `README.md` con objetivo, pregunta de investigación, H₀/H₁, variables
  independientes y dependientes, y diseño experimental.
- Presentar la propuesta (10 min) y comentar los principios ACM Artifact Review & Badging.

## Entregables

| Entregable | Ubicación | Estado |
|---|---|---|
| Repositorio GitHub | https://github.com/Pmiqueles-usach/Modulo2-Inv-experimental | ✅ |
| README.md inicial (objetivo, pregunta, hipótesis, variables, diseño) | [README.md](../../README.md) §1–6 | ✅ |
| Estructura inicial del artifact (`src/`, `docker/`, `results/`, `docs/`) | raíz del repositorio | ✅ |
| Comentarios sobre ACM | sección siguiente y [ACM_BADGES.md](../ACM_BADGES.md) | ✅ |
| Presentación de 10 minutos | `docs/presentaciones/` | ✅ |

## Diseño experimental (resumen)

- **Factores:** lenguaje (4 niveles) × tamaño N (3 niveles) → diseño factorial completo 4×3.
- **Respuesta:** `time_seconds`, solo la multiplicación.
- **Réplicas:** 10 por celda → 120 observaciones.
- **Controles:** mismo algoritmo naive, tipo `double`, mismas matrices (semilla), reloj
  monotónico, ejecución secuencial en contenedores.
- **Análisis previsto:** ANOVA de dos factores con interacción + Tukey HSD.

## Comentarios sobre ACM Artifact Review & Badging

1. **Terminología.** Desde la versión 1.1 ACM armonizó sus términos con NISO:
   *repeatability* (mismo equipo y montaje), *reproducibility* (otro equipo, artifacts del
   autor) y *replicability* (otro equipo, artifacts propios). La evaluación cruzada de la
   Semana 5 corresponde a **reproducibilidad**; reimplementar el benchmark desde cero sería
   **replicabilidad**.
2. **Badges independientes.** *Artifacts Evaluated* (Functional / Reusable), *Artifacts
   Available* y *Results Validated* (Reproduced / Replicated) pueden obtenerse por separado.
   El módulo los recorre en orden: Functional (S3) → Reusable (S4) → Available + Reproduced (S5).
3. **Functional** exige artifacts *documented, consistent, complete, exercisable* y evidencia de
   verificación. Por ello se diseñó desde el inicio un **checksum** de la matriz resultado que
   permite verificar que las 4 implementaciones calculan exactamente lo mismo.
4. **Available** exige un repositorio de **archivo** con plan de permanencia y DOI: GitHub no
   basta, de ahí Zenodo.
5. **Results Reproduced** no exige igualdad exacta sino concordancia dentro de una tolerancia
   que no cambie las conclusiones. En un benchmark de tiempos esto es clave: los segundos
   absolutos cambiarán con el hardware; lo que debe reproducirse son las decisiones
   estadísticas y el orden relativo de los lenguajes (criterios en ACM_BADGES.md §2.4).
6. **Crítica.** Los badges evalúan el artifact, no la validez del diseño experimental: un
   benchmark mal controlado podría ser perfectamente "Reusable". Por eso el protocolo
   (docs/PROTOCOLO.md) documenta además las amenazas a la validez.

## Guion de presentación (10 min)

| Tiempo | Contenido |
|---|---|
| 0–2 | Problema y objetivo |
| 2–4 | Pregunta e hipótesis H₀/H₁ |
| 4–6 | Variables, diseño 4×3×10, protocolo de medición |
| 6–8 | Repositorio GitHub y README.md |
| 8–10 | ACM: terminología, badges y cómo los abordará el módulo |
