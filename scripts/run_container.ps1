# Ejecuta manualmente (sin Snakemake) el benchmark de un lenguaje dentro de su contenedor (Windows).
# Equivalente a scripts/run_container.sh.
#
# Uso (PowerShell, desde la raiz del repositorio):
#   powershell -ExecutionPolicy Bypass -File scripts\run_container.ps1 <cpp|go|java|python> [tamanos] [reps] [semilla] [dir]
#   powershell -ExecutionPolicy Bypass -File scripts\run_container.ps1 cpp 200,400 3 42 results_demo
#
# Resultado: <dir>\raw\<lang>.csv y <dir>\verification\<lang>_checksum.csv
param(
    [Parameter(Mandatory = $true)][ValidateSet("cpp", "go", "java", "python")][string]$Lang,
    [string[]]$Sizes = @("500", "1000", "1500"),
    [int]$Reps = 10,
    [int]$Seed = 42,
    [string]$Results = "results",
    [string]$Engine = "docker",
    [string]$Tag = "1.0"
)
Set-Location (Join-Path $PSScriptRoot "..")

# "200,400" sin comillas llega como arreglo: se une con comas.
$tamanos = ($Sizes -join ",") -replace "\s", ""

foreach ($d in "raw", "verification", "logs") {
    New-Item -ItemType Directory -Force -Path (Join-Path $Results $d) | Out-Null
}
$absoluto = (Resolve-Path $Results).Path

Write-Host ">> matmul-${Lang}:$Tag  N=$tamanos  repeticiones=$Reps  semilla=$Seed  -> $absoluto" -ForegroundColor Yellow
& $Engine run --rm --network none -v "${absoluto}:/results" "matmul-${Lang}:$Tag" `
    "/results/raw/$Lang.csv" $tamanos $Reps $Seed "/results/verification/${Lang}_checksum.csv"
exit $LASTEXITCODE
