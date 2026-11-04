# Publicación del artifact en Zenodo (Semana 5)

## Opción usada: API REST con DOI reservado (`scripts/zenodo_publicar.py`)

Permite escribir el DOI en el README **antes** de archivar, así la copia de Zenodo ya lo contiene.

1. Token personal en *Settings → Applications → Personal access tokens* (permisos
   `deposit:write`, `deposit:actions`). Guardarlo fuera del repositorio:
   `read -rs T && printf %s "$T" > ~/.zenodo_token && chmod 600 ~/.zenodo_token && unset T`.
2. `python3 scripts/zenodo_publicar.py reservar` → crea el borrador con `.zenodo.json` y
   muestra el DOI reservado (queda en `.zenodo_deposito.json`, ignorado por git).
3. Escribir el DOI reservado (README, CITATION.cff, DATASHEET_FAIR.md, ACM_BADGES.md),
   commit y `git tag -a v1.0.0`.
4. `git archive --format=zip --prefix=Modulo2-Inv-experimental-v1.0.0/ -o artifact-v1.0.0.zip v1.0.0`
   (excluye `docs/ContenidoModulo_v4.pdf`, material del curso, vía `export-ignore`).
5. `python3 scripts/zenodo_publicar.py subir artifact-v1.0.0.zip`, revisar con `estado` y en la
   web, y `python3 scripts/zenodo_publicar.py publicar` (irreversible).
6. `git push origin main --tags`.

Para ensayar sin publicar nada real: `ZENODO_URL=https://sandbox.zenodo.org` (requiere un token
de sandbox.zenodo.org).

## Opción A: integración GitHub → Zenodo

1. Iniciar sesión en https://zenodo.org con la cuenta de GitHub.
2. Ir a *Account → GitHub* y activar el interruptor del repositorio
   `Pmiqueles-usach/Modulo2-Inv-experimental`.
3. Verificar que `main` contiene los resultados finales (`results/`) y que todo está commiteado.
4. Crear una *release* en GitHub con la etiqueta `v1.0.0`:
   ```bash
   git tag -a v1.0.0 -m "Artifact v1.0.0 - publicación Zenodo"
   git push origin v1.0.0
   ```
   y luego *Releases → Draft a new release → v1.0.0 → Publish*.
5. Zenodo archiva automáticamente la release usando los metadatos de `.zenodo.json`
   y asigna un **DOI de versión** y un **concept DOI**.
6. Copiar el DOI en:
   - `README.md` (badge de la línea 3, §7.5 y §12),
   - `CITATION.cff` (campo `doi`),
   - `docs/DATASHEET_FAIR.md` (sección 1),
   - `docs/ACM_BADGES.md` (tabla 2.3).
7. Commit `docs: agrega DOI de Zenodo` y push (la versión archivada no cambia; el DOI queda en
   GitHub para quienes lleguen desde ahí).

## Opción B: carga manual

```bash
git archive --format=zip --prefix=Modulo2-Inv-experimental-v1.0.0/ -o artifact-v1.0.0.zip v1.0.0
```

Subir `artifact-v1.0.0.zip` en *New upload*, tipo **Software**, completar metadatos (copiar de
`.zenodo.json`), licencia MIT, publicar y reservar DOI.

## Checklist del contenido mínimo exigido por el módulo

| Elemento exigido | Ubicación en el artifact | ✓ |
|---|---|---|
| Código fuente C++, Go, Java y Python | `src/` | ✓ |
| README.md con instrucciones completas | `README.md` | ✓ |
| Dockerfile y archivos para construir entornos | `docker/`, `.dockerignore`, `scripts/build_images.sh` | ✓ |
| Pipeline Snakefile | `workflow/Snakefile`, `workflow/profiles/`, `config/` | ✓ |
| cpp.csv, go.csv, python.csv, java.csv | `results/raw/` | ✓ |
| benchmark.csv | `results/benchmark.csv` | ✓ |
| Resultados del análisis estadístico | `results/analysis/reporte_estadistico.md`, `tables/` | ✓ |
| Tablas y gráficos | `results/analysis/tables/`, `results/analysis/figures/` | ✓ |
| Licencia | `LICENSE` (MIT), `LICENSE-DATA` (CC BY 4.0) | ✓ |
| Mini datasheet FAIR | `docs/DATASHEET_FAIR.md` | ✓ |

Verificación automática del contenido: `python3 scripts/check_artifact.py` (Windows: `py scripts\check_artifact.py`).
