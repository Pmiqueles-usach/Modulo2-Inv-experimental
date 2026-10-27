# Reproduce el experimento completo en Windows con un solo comando (PowerShell + Docker Desktop).
#
#   1) verifica Docker y Python   2) construye MANUALMENTE las 5 imagenes desde los Dockerfile
#   3) instala Snakemake en .venv 4) ejecuta el pipeline       5) verifica el contenido del artifact
#
# Uso (PowerShell, desde la raiz del repositorio):
#   powershell -ExecutionPolicy Bypass -File scripts\reproducir.ps1 -Rapido   # prueba (~3 min) -> results_smoke
#   powershell -ExecutionPolicy Bypass -File scripts\reproducir.ps1           # experimento completo (~2,5 h) -> results_repro
#
# Opciones: -Engine podman   -Results <directorio>   -SinConstruir (si las imagenes ya existen)
param(
    [switch]$Rapido,
    [switch]$SinConstruir,
    [string]$Engine = "docker",
    [string]$Results = ""
)
Set-Location (Join-Path $PSScriptRoot "..")

function Paso([string]$texto) { Write-Host "`n== $texto ==" -ForegroundColor Cyan }
function Fallar([string]$texto) { Write-Host "ERROR: $texto" -ForegroundColor Red; exit 1 }

Paso "1/5 Verificando herramientas"
if (-not (Get-Command $Engine -ErrorAction SilentlyContinue)) {
    Fallar "No se encontro '$Engine'. Instale Docker Desktop: https://www.docker.com/products/docker-desktop/"
}
$null = & $Engine info 2>&1
if ($LASTEXITCODE -ne 0) {
    Fallar "'$Engine' no responde. Abra Docker Desktop y espere a que indique 'Engine running'."
}
Write-Host "  [ OK ] $(& $Engine --version)"

if (Get-Command py -ErrorAction SilentlyContinue) { $py = "py"; $pyArgs = @("-3") }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $py = "python"; $pyArgs = @() }
else { Fallar "No se encontro Python. Instale Python 3.11 o superior: https://www.python.org/downloads/" }
& $py @pyArgs -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"
if ($LASTEXITCODE -ne 0) { Fallar "Se requiere Python 3.11 o superior." }
Write-Host "  [ OK ] $(& $py @pyArgs --version)"

Paso "2/5 Construyendo las imagenes (manualmente, desde los Dockerfile)"
if ($SinConstruir) {
    Write-Host "  (omitido por -SinConstruir)"
} else {
    & (Join-Path $PSScriptRoot "build_images.ps1") -Engine $Engine
    if ($LASTEXITCODE -ne 0) { Fallar "No se pudieron construir las imagenes." }
}

Paso "3/5 Instalando Snakemake en .venv"
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    & $py @pyArgs -m venv .venv
    if ($LASTEXITCODE -ne 0) { Fallar "No se pudo crear el entorno virtual .venv" }
}
& .venv\Scripts\python.exe -m pip install --quiet -r requirements-host.txt
if ($LASTEXITCODE -ne 0) { Fallar "No se pudo instalar Snakemake." }
Write-Host "  [ OK ] snakemake $(& .venv\Scripts\snakemake.exe --version)"

Paso "4/5 Ejecutando el pipeline Snakemake"
if ($Rapido) { $dir = "results_smoke"; $extra = @("sizes=[50,100]", "repetitions=3") }
else { $dir = "results_repro"; $extra = @() }
if ($Results) { $dir = $Results }
Write-Host "  Resultados en: $dir"
& .venv\Scripts\snakemake.exe --config "engine=$Engine" "results_dir=$dir" @extra
if ($LASTEXITCODE -ne 0) { Fallar "El pipeline termino con errores (ver mensajes anteriores y $dir\logs\)." }

Paso "5/5 Verificando el artifact generado"
& .venv\Scripts\python.exe scripts\check_artifact.py $dir
$fallas = $LASTEXITCODE

Write-Host "`nRazon de tiempos respecto de C++ (esta ejecucion):" -ForegroundColor Cyan
Get-Content "$dir\analysis\tables\speedup.md"
Write-Host "`nResultados publicados (results\): results\analysis\tables\speedup.md y results\analysis\reporte_estadistico.md"
Write-Host "Reporte de esta ejecucion:         $dir\analysis\reporte_estadistico.md"
exit $fallas
