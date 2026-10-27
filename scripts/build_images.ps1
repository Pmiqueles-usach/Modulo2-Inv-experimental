# Construye MANUALMENTE las cinco imagenes a partir de los Dockerfile del artifact (Windows).
# No descarga imagenes del benchmark desde registros: solo las imagenes base oficiales.
#
# Uso (PowerShell, desde la raiz del repositorio):
#   powershell -ExecutionPolicy Bypass -File scripts\build_images.ps1
#   powershell -ExecutionPolicy Bypass -File scripts\build_images.ps1 -Engine podman -Tag 1.0
param(
    [string]$Engine = "docker",
    [string]$Tag = "1.0"
)
Set-Location (Join-Path $PSScriptRoot "..")

foreach ($lang in "cpp", "go", "java", "python", "analysis") {
    Write-Host ">> Construyendo matmul-${lang}:$Tag" -ForegroundColor Yellow
    & $Engine build -f "docker/$lang/Dockerfile" -t "matmul-${lang}:$Tag" .
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: fallo la construccion de matmul-${lang}:$Tag" -ForegroundColor Red
        exit 1
    }
}
& $Engine images --filter "reference=matmul-*"
