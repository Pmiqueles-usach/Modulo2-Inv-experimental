"""Verifica la equivalencia funcional de las cuatro implementaciones.

Compara, para cada N y repetición, la suma de todos los elementos de C (checksum)
y los elementos C[0,0] y C[N-1,N-1] producidos por cada lenguaje. Como las
cuatro implementaciones usan el mismo generador, los mismos datos y el mismo
orden de operaciones (sin FMA), los valores deben ser idénticos bit a bit.

Uso: python scripts/verify_equivalence.py <reporte.md> <checksum_1.csv> ... <checksum_k.csv>
"""

import sys

import pandas as pd


def main() -> int:
    salida, entradas = sys.argv[1], sys.argv[2:]
    # round_trip: lectura exacta de los 17 dígitos significativos (sin redondeo del parser).
    df = pd.concat([pd.read_csv(r, float_precision="round_trip") for r in entradas], ignore_index=True)
    lineas = [
        "# Verificación de equivalencia funcional",
        "",
        "Se compara el resultado de la multiplicación en cada lenguaje (suma total de C, "
        "primer y último elemento). Criterio: igualdad exacta (bit a bit) entre lenguajes "
        "y entre repeticiones.",
        "",
        "| N | checksum | C[0,0] | C[N-1,N-1] | lenguajes | ¿idénticos? |",
        "|---|---|---|---|---|---|",
    ]
    todo_ok = True
    for n, grupo in df.groupby("N"):
        valores = grupo[["checksum", "c_first", "c_last"]].drop_duplicates()
        ok = len(valores) == 1
        todo_ok &= ok
        fila = valores.iloc[0]
        lenguajes = ", ".join(sorted(grupo["language"].unique()))
        lineas.append(
            f"| {n} | {float(fila['checksum'])!r} | {float(fila['c_first'])!r} | {float(fila['c_last'])!r} | "
            f"{lenguajes} | {'SÍ' if ok else 'NO'} |"
        )
    lineas += ["", f"**Resultado global:** {'EQUIVALENTES' if todo_ok else 'DIFERENCIAS DETECTADAS'}", ""]
    with open(salida, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))
    print("\n".join(lineas), file=sys.stderr)
    return 0 if todo_ok else 1


if __name__ == "__main__":
    sys.exit(main())
