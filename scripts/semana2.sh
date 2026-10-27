#!/usr/bin/env bash
# Semana 2 – Compila y ejecuta en vivo las cuatro implementaciones, sin contenedores.
#
# Uso:   scripts/semana2.sh [tamaños] [repeticiones] [semilla]
#        scripts/semana2.sh                 # por defecto: 200,400  3  42
#        scripts/semana2.sh 500,1000,1500 10 42   # experimento completo (~1,5 h por Python)
#
# Requisitos en el host: g++, go, java (JDK 11+; si no hay javac se usa el modo
# "archivo fuente" de java) y python3. Si falta alguno, use Docker: README §5.
# Variable opcional: SIN_PAUSA=1 (no esperar Enter entre lenguajes).
set -euo pipefail
cd "$(dirname "$0")/.."

TAMANOS="${1:-200,400}"
REPS="${2:-3}"
SEMILLA="${3:-42}"
SALIDA="results_semana2"
BIN="$SALIDA/bin"

NEGRITA=$'\e[1m'; AZUL=$'\e[34m'; VERDE=$'\e[32m'; ROJO=$'\e[31m'; GRIS=$'\e[90m'; FIN=$'\e[0m'
titulo()   { printf '\n%s%s══ %s ══%s\n' "$NEGRITA" "$AZUL" "$*" "$FIN"; }
ejecutar() { printf '%s$ %s%s\n' "$NEGRITA" "$*" "$FIN"; "$@"; }
pausa()    { [ -n "${SIN_PAUSA:-}" ] || read -rp "${GRIS}[Enter para continuar]${FIN} " _; }
falta()    { printf '%s✘ No se encontró %s en el host. Use Docker (README §5).%s\n' "$ROJO" "$1" "$FIN"; exit 1; }

/bin/rm -rf "$SALIDA"
mkdir -p "$BIN" "$SALIDA/raw" "$SALIDA/verification"
printf '%sParámetros:%s N = %s · repeticiones = %s · semilla = %s · salida = %s/\n' \
    "$NEGRITA" "$FIN" "$TAMANOS" "$REPS" "$SEMILLA" "$SALIDA"

# Argumentos comunes de los cuatro programas.
args() { echo "$SALIDA/raw/$1.csv $TAMANOS $REPS $SEMILLA $SALIDA/verification/$1_checksum.csv"; }

titulo "C++  ·  compilar con g++ -O2 (sin FMA)"
command -v g++ > /dev/null || falta g++
g++ --version | head -n1
ejecutar g++ -O2 -std=c++17 -ffp-contract=off -o "$BIN/matmul_cpp" src/cpp/matmul.cpp
# shellcheck disable=SC2046
ejecutar "$BIN/matmul_cpp" $(args cpp)
pausa

titulo "Go  ·  compilar con go build"
command -v go > /dev/null || falta go
go version
ejecutar env CGO_ENABLED=0 go -C src/go build -o "$PWD/$BIN/matmul_go" .
# shellcheck disable=SC2046
ejecutar "$BIN/matmul_go" $(args go)
pausa

titulo "Java  ·  compilar con javac y ejecutar en la JVM"
command -v java > /dev/null || falta java
java --version | head -n1
if command -v javac > /dev/null; then
    ejecutar javac -encoding UTF-8 -d "$BIN" src/java/MatMul.java
    # shellcheck disable=SC2046
    ejecutar java -Xms1g -Xmx1g -cp "$BIN" MatMul $(args java)
else
    printf '%s(sin javac: modo archivo fuente, la JVM compila en memoria)%s\n' "$GRIS" "$FIN"
    # shellcheck disable=SC2046
    ejecutar java -Xms1g -Xmx1g src/java/MatMul.java $(args java)
fi
pausa

titulo "Python  ·  interpretado (CPython, sin NumPy)"
command -v python3 > /dev/null || falta python3
python3 --version
# shellcheck disable=SC2046
ejecutar python3 src/python/matmul.py $(args python)
pausa

titulo "Resultados: cuatro CSV con la misma estructura"
for lang in cpp go java python; do
    printf '%s%s%s\n' "$GRIS" "$SALIDA/raw/$lang.csv" "$FIN"
    column -s, -t < "$SALIDA/raw/$lang.csv"
done
pausa

titulo "Tiempo medio por lenguaje y N [s]"
awk -F, 'FNR > 1 { s[$1","$2] += $4; n[$1","$2]++ }
         END { for (k in s) { split(k, p, ","); printf "%-7s N=%-5s %12.6f\n", p[1], p[2], s[k] / n[k] } }' \
    "$SALIDA"/raw/*.csv | sort -k2,2V -k1,1

titulo "Equivalencia: checksum de C (repetición 1) en cada lenguaje"
awk -F, 'FNR > 1 && $3 == 1 { printf "%-7s N=%-5s suma(C)=%s\n", $1, $2, $4
                             if (!($2 in ref)) ref[$2] = $4; else if (ref[$2] != $4) distinto = 1 }
         END { exit distinto }' "$SALIDA"/verification/*_checksum.csv \
    && printf '%s✔ Las cuatro implementaciones producen la MISMA matriz (bit a bit).%s\n' "$VERDE" "$FIN" \
    || printf '%s✘ Diferencias entre implementaciones.%s\n' "$ROJO" "$FIN"
