"""Integra los archivos de resultados por lenguaje en un único benchmark.csv.

Uso: python scripts/merge_results.py <salida benchmark.csv> <cpp.csv> <go.csv> <java.csv> <python.csv>

Valida que cada archivo tenga exactamente las columnas
language, N, repetition, time_seconds y que no existan filas duplicadas.
"""

import sys

import pandas as pd

COLUMNAS = ["language", "N", "repetition", "time_seconds"]


def cargar(ruta: str) -> pd.DataFrame:
    """Lee un CSV de resultados y valida su estructura."""
    df = pd.read_csv(ruta)
    if list(df.columns) != COLUMNAS:
        raise ValueError(f"{ruta}: columnas {list(df.columns)} != {COLUMNAS}")
    if df.empty:
        raise ValueError(f"{ruta}: archivo sin filas")
    if df["time_seconds"].le(0).any() or df["time_seconds"].isna().any():
        raise ValueError(f"{ruta}: tiempos no válidos")
    return df


def main() -> int:
    salida, entradas = sys.argv[1], sys.argv[2:]
    df = pd.concat([cargar(r) for r in entradas], ignore_index=True)
    duplicados = df.duplicated(subset=["language", "N", "repetition"])
    if duplicados.any():
        raise ValueError(f"Filas duplicadas:\n{df[duplicados]}")
    df = df.sort_values(["language", "N", "repetition"]).reset_index(drop=True)
    df.to_csv(salida, index=False, float_format="%.9f")
    resumen = df.groupby(["language", "N"]).size().unstack()
    print(f"benchmark.csv: {len(df)} filas\n{resumen}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
