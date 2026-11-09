"""Compara un benchmark.csv publicado con uno reproducido usando el mismo análisis para todos.

Uso: python scripts/comparar_evaluacion.py <publicado.csv> <reproducido.csv> <salida.md>

Para cada CSV calcula: filas por celda, medias por lenguaje×N, orden de lenguajes por N,
razones vs C++, ANOVA tipo II de dos factores con interacción en segundos y en log10,
y Tukey HSD (log10) de lenguajes dentro de cada N. Así ambos lados se comparan con
exactamente el mismo procedimiento, independiente del script de análisis del autor.
"""
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def cargar(ruta):
    df = pd.read_csv(ruta)
    df.columns = [c.strip().lstrip("﻿") for c in df.columns]
    df["language"] = df["language"].str.strip().str.lower().replace({"c++": "cpp"})
    df["N"] = df["N"].astype(int)
    df["log_t"] = np.log10(df["time_seconds"])
    return df


def resumen(df):
    r = {"filas": len(df), "columnas": list(df.columns[:4])}
    r["celdas"] = df.groupby(["language", "N"]).size().to_dict()
    medias = df.groupby(["N", "language"])["time_seconds"].mean().unstack()
    r["medias"] = medias
    r["orden"] = {n: " < ".join(medias.loc[n].sort_values().index) for n in medias.index}
    r["razones"] = medias.div(medias["cpp"], axis=0)
    for col, nombre in (("time_seconds", "seg"), ("log_t", "log10")):
        m = smf.ols(f"{col} ~ C(language) * C(N)", data=df).fit()
        a = anova_lm(m, typ=2)
        r[f"anova_{nombre}"] = a
    tk = {}
    for n, g in df.groupby("N"):
        t = pairwise_tukeyhsd(g["log_t"], g["language"], alpha=0.05)
        tab = pd.DataFrame(t._results_table.data[1:], columns=t._results_table.data[0])
        tk[n] = tab
    r["tukey"] = tk
    return r


def no_signif(r):
    salida = []
    for n, tab in r["tukey"].items():
        ns = tab[~tab["reject"].astype(bool)]
        salida.append(f"N={n}: " + (", ".join(f"{a}–{b}" for a, b in zip(ns.group1, ns.group2)) or "ninguno"))
    return "; ".join(salida)


def main():
    pub, rep = resumen(cargar(sys.argv[1])), resumen(cargar(sys.argv[2]))
    L = ["# Comparación publicado vs reproducido (análisis uniforme del evaluador)\n"]
    L.append(f"- Filas: publicado {pub['filas']} · reproducido {rep['filas']}")
    L.append(f"- Columnas reproducido: `{','.join(rep['columnas'])}`")
    celdas_ok = all(v == 10 for v in rep["celdas"].values()) and len(rep["celdas"]) == 12
    L.append(f"- 12 celdas × 10 repeticiones en reproducido: {'sí' if celdas_ok else 'NO'}\n")
    L.append("## Medias (s) y razón vs C++\n")
    L.append("| N | Lenguaje | Media publicada | Media reproducida | Razón/C++ publ. | Razón/C++ repr. |")
    L.append("|---|---|---:|---:|---:|---:|")
    for n in pub["medias"].index:
        for l in ["cpp", "go", "java", "python"]:
            L.append(f"| {n} | {l} | {pub['medias'].loc[n, l]:.4f} | {rep['medias'].loc[n, l]:.4f} | "
                     f"{pub['razones'].loc[n, l]:.2f} | {rep['razones'].loc[n, l]:.2f} |")
    L.append("\n## Orden de lenguajes (más rápido primero)\n")
    L.append("| N | Publicado | Reproducido | ¿Igual? |\n|---|---|---|---|")
    for n in pub["orden"]:
        L.append(f"| {n} | {pub['orden'][n]} | {rep['orden'][n]} | {'sí' if pub['orden'][n] == rep['orden'][n] else 'no'} |")
    L.append("\n## ANOVA tipo II (p-valores)\n")
    L.append("| Escala | Efecto | p publicado | p reproducido | Decisión igual (α=0,05) |\n|---|---|---:|---:|---|")
    for esc in ("seg", "log10"):
        for ef in ("C(language)", "C(N)", "C(language):C(N)"):
            pp, pr = pub[f"anova_{esc}"].loc[ef, "PR(>F)"], rep[f"anova_{esc}"].loc[ef, "PR(>F)"]
            L.append(f"| {esc} | {ef} | {pp:.3g} | {pr:.3g} | {'sí' if (pp < .05) == (pr < .05) else 'NO'} |")
    L.append("\n## Tukey HSD log10, pares de lenguajes NO significativos dentro de cada N\n")
    L.append(f"- Publicado: {no_signif(pub)}")
    L.append(f"- Reproducido: {no_signif(rep)}")
    open(sys.argv[3], "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
