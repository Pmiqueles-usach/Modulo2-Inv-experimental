"""Análisis estadístico del benchmark de multiplicación de matrices.

Uso: python scripts/analysis.py <benchmark.csv> <directorio_salida> [alpha]

Genera en <directorio_salida>:
  tables/descriptivos.csv|md      estadística descriptiva por lenguaje x N
  tables/speedup.csv|md           razón de tiempos respecto de C++
  tables/anova_tiempo.csv|md      ANOVA de dos factores con interacción (tiempo en s)
  tables/anova_log.csv|md         ANOVA de dos factores con interacción (log10 del tiempo)
  tables/supuestos.md             normalidad de residuos y homogeneidad de varianzas
  tables/tukey_*.csv|md           comparaciones post-hoc Tukey HSD
  tables/kruskal.csv|md           contraste no paramétrico de robustez por N
  figures/*.png                   gráficos
  reporte_estadistico.md          reporte integrado con la decisión sobre H0
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Orden fijo de categorías y colores (paleta categórica validada, slots 1-4).
ORDEN = ["cpp", "go", "java", "python"]
ETIQUETAS = {"cpp": "C++", "go": "Go", "java": "Java", "python": "Python"}
COLORES = {"cpp": "#2a78d6", "go": "#eb6834", "java": "#1baf7a", "python": "#eda100"}
TINTA = "#0b0b0b"
TINTA_SECUNDARIA = "#52514e"
GRILLA = "#e4e3df"


def configurar_estilo() -> None:
    plt.rcParams.update({
        "figure.dpi": 150,
        "savefig.bbox": "tight",
        "font.size": 10,
        "axes.edgecolor": TINTA_SECUNDARIA,
        "axes.labelcolor": TINTA,
        "axes.titlesize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": GRILLA,
        "grid.linewidth": 0.8,
        "xtick.color": TINTA_SECUNDARIA,
        "ytick.color": TINTA_SECUNDARIA,
        "legend.frameon": False,
    })


def guardar_tabla(df: pd.DataFrame, ruta_base: str, indice: bool = False) -> None:
    """Guarda una tabla en CSV y Markdown."""
    df.to_csv(ruta_base + ".csv", index=indice)
    with open(ruta_base + ".md", "w", encoding="utf-8") as f:
        f.write(df.to_markdown(index=indice, floatfmt=".6g"))
        f.write("\n")


def descriptivos(df: pd.DataFrame) -> pd.DataFrame:
    """Media, desviación, mediana, extremos, CV e IC 95 % por lenguaje x N."""
    filas = []
    for (lang, n), g in df.groupby(["language", "N"]):
        t = g["time_seconds"]
        media, de, k = t.mean(), t.std(ddof=1), len(t)
        margen = stats.t.ppf(0.975, k - 1) * de / np.sqrt(k)
        filas.append({
            "language": lang, "N": n, "n": k, "media_s": media, "de_s": de,
            "mediana_s": t.median(), "min_s": t.min(), "max_s": t.max(),
            "cv_pct": 100 * de / media, "ic95_inf_s": media - margen, "ic95_sup_s": media + margen,
        })
    return pd.DataFrame(filas)


def speedup(desc: pd.DataFrame) -> pd.DataFrame:
    """Razón media(lenguaje) / media(C++) por N."""
    piv = desc.pivot(index="N", columns="language", values="media_s")
    return piv.div(piv["cpp"], axis=0).reset_index().rename_axis(None, axis=1)


def anova_dos_factores(df: pd.DataFrame, respuesta: str) -> tuple[pd.DataFrame, object]:
    """ANOVA tipo II con interacción y eta² parcial."""
    modelo = smf.ols(f"{respuesta} ~ C(language) * C(N)", data=df).fit()
    tabla = anova_lm(modelo, typ=2)
    ss_res = tabla.loc["Residual", "sum_sq"]
    tabla["eta2_parcial"] = tabla["sum_sq"] / (tabla["sum_sq"] + ss_res)
    tabla.loc["Residual", "eta2_parcial"] = np.nan
    tabla.index = tabla.index.str.replace("C(language)", "Lenguaje", regex=False) \
                             .str.replace("C(N)", "N", regex=False)
    return tabla, modelo


def supuestos(df: pd.DataFrame, modelo, respuesta: str) -> dict:
    residuos = modelo.resid
    sw = stats.shapiro(residuos)
    grupos = [g[respuesta].values for _, g in df.groupby(["language", "N"])]
    lev = stats.levene(*grupos, center="median")
    return {"shapiro_W": sw.statistic, "shapiro_p": sw.pvalue,
            "levene_W": lev.statistic, "levene_p": lev.pvalue}


def tukey(df: pd.DataFrame, respuesta: str, grupo: str, alpha: float) -> pd.DataFrame:
    res = pairwise_tukeyhsd(df[respuesta], df[grupo], alpha=alpha)
    tabla = pd.DataFrame(res._results_table.data[1:], columns=res._results_table.data[0])
    return tabla


def figura_boxplot(df: pd.DataFrame, ruta: str) -> None:
    tamanos = sorted(df["N"].unique())
    fig, ejes = plt.subplots(1, len(tamanos), figsize=(4 * len(tamanos), 4), sharey=True)
    for eje, n in zip(np.atleast_1d(ejes), tamanos):
        datos = [df[(df["language"] == l) & (df["N"] == n)]["time_seconds"] for l in ORDEN]
        cajas = eje.boxplot(datos, patch_artist=True, widths=0.55,
                            medianprops={"color": TINTA, "linewidth": 1.5})
        for caja, l in zip(cajas["boxes"], ORDEN):
            caja.set_facecolor(COLORES[l])
            caja.set_edgecolor(TINTA_SECUNDARIA)
        eje.set_xticks(range(1, len(ORDEN) + 1), [ETIQUETAS[l] for l in ORDEN])
        eje.set_yscale("log")
        eje.set_title(f"N = {n}")
    np.atleast_1d(ejes)[0].set_ylabel("Tiempo de multiplicación [s] (escala log)")
    fig.suptitle("Distribución del tiempo de ejecución por lenguaje y tamaño (10 repeticiones)")
    fig.savefig(ruta)
    plt.close(fig)


def figura_interaccion(desc: pd.DataFrame, ruta: str) -> None:
    fig, eje = plt.subplots(figsize=(6.5, 4.5))
    for l in ORDEN:
        d = desc[desc["language"] == l].sort_values("N")
        eje.errorbar(d["N"], d["media_s"], yerr=[d["media_s"] - d["ic95_inf_s"], d["ic95_sup_s"] - d["media_s"]],
                     color=COLORES[l], marker="o", markersize=6, linewidth=2, capsize=3, label=ETIQUETAS[l])
    eje.set_yscale("log")
    eje.set_xticks(sorted(desc["N"].unique()))
    eje.set_xlabel("Tamaño de la matriz N")
    eje.set_ylabel("Tiempo medio [s] (escala log, IC 95 %)")
    eje.set_title("Gráfico de interacción lenguaje x N")
    eje.legend(loc="upper left")
    fig.savefig(ruta)
    plt.close(fig)


def figura_speedup(sp: pd.DataFrame, ruta: str) -> None:
    tamanos = sp["N"].tolist()
    x = np.arange(len(tamanos))
    ancho = 0.2
    fig, eje = plt.subplots(figsize=(7, 4.5))
    for i, l in enumerate(ORDEN):
        barras = eje.bar(x + (i - 1.5) * ancho, sp[l], ancho * 0.9, color=COLORES[l], label=ETIQUETAS[l])
        eje.bar_label(barras, fmt="%.1f×", fontsize=8, color=TINTA_SECUNDARIA, padding=2)
    eje.set_yscale("log")
    eje.set_xticks(x, [f"N = {n}" for n in tamanos])
    eje.set_ylabel("Tiempo relativo a C++ (escala log)")
    eje.set_title("Razón de tiempos respecto de C++ (C++ = 1)")
    eje.legend(ncols=4, loc="upper left")
    fig.savefig(ruta)
    plt.close(fig)


def figura_repeticiones(df: pd.DataFrame, ruta: str) -> None:
    """Evolución del tiempo por repetición (detecta calentamiento, p.ej. JIT de Java)."""
    tamanos = sorted(df["N"].unique())
    fig, ejes = plt.subplots(1, len(tamanos), figsize=(4 * len(tamanos), 3.8), sharey=True)
    for eje, n in zip(np.atleast_1d(ejes), tamanos):
        for l in ORDEN:
            d = df[(df["language"] == l) & (df["N"] == n)].sort_values("repetition")
            eje.plot(d["repetition"], d["time_seconds"], color=COLORES[l], marker="o",
                     markersize=4, linewidth=2, label=ETIQUETAS[l])
        eje.set_yscale("log")
        eje.set_xlabel("Repetición")
        eje.set_title(f"N = {n}")
    np.atleast_1d(ejes)[0].set_ylabel("Tiempo [s] (escala log)")
    np.atleast_1d(ejes)[-1].legend(loc="center right")
    fig.suptitle("Tiempo por repetición (estabilidad y efecto de calentamiento)")
    fig.savefig(ruta)
    plt.close(fig)


def figura_qq(modelo, ruta: str, titulo: str) -> None:
    fig, eje = plt.subplots(figsize=(4.5, 4.5))
    (teo, obs), (pend, inter, _) = stats.probplot(modelo.resid, dist="norm")
    eje.plot(teo, obs, "o", color=COLORES["cpp"], markersize=4)
    eje.plot(teo, pend * np.asarray(teo) + inter, color=TINTA_SECUNDARIA, linewidth=1.5)
    eje.set_xlabel("Cuantiles teóricos N(0,1)")
    eje.set_ylabel("Residuos ordenados")
    eje.set_title(titulo)
    fig.savefig(ruta)
    plt.close(fig)


def interpretar_interaccion(p_tiempo: float, p_log: float, alpha: float) -> str:
    """Interpreta la interacción; el modelo log10 es el principal (varianza más estable)."""
    if p_tiempo < alpha and p_log < alpha:
        return "La diferencia entre lenguajes **depende del tamaño de la matriz** (ambos modelos)."
    if p_log < alpha:
        return "La razón de tiempos entre lenguajes **depende del tamaño de la matriz** (modelo log10)."
    if p_tiempo < alpha:
        return ("La interacción es significativa solo en la escala original: las diferencias "
                "**absolutas** crecen con N, pero las **razones** entre lenguajes se mantienen "
                "aproximadamente constantes (interacción no significativa en log10).")
    return "No hay evidencia de que la diferencia entre lenguajes dependa del tamaño."


def decision(p: float, alpha: float) -> str:
    return "se rechaza H₀" if p < alpha else "no se rechaza H₀"


def main() -> int:
    entrada, salida = sys.argv[1], sys.argv[2]
    alpha = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05
    dir_tablas = os.path.join(salida, "tables")
    dir_figuras = os.path.join(salida, "figures")
    os.makedirs(dir_tablas, exist_ok=True)
    os.makedirs(dir_figuras, exist_ok=True)
    configurar_estilo()

    df = pd.read_csv(entrada)
    df["log_time"] = np.log10(df["time_seconds"])
    df["grupo"] = df["language"] + "_N" + df["N"].astype(str)

    desc = descriptivos(df)
    guardar_tabla(desc, os.path.join(dir_tablas, "descriptivos"))
    sp = speedup(desc)
    guardar_tabla(sp, os.path.join(dir_tablas, "speedup"))

    anova_t, modelo_t = anova_dos_factores(df, "time_seconds")
    anova_l, modelo_l = anova_dos_factores(df, "log_time")
    guardar_tabla(anova_t, os.path.join(dir_tablas, "anova_tiempo"), indice=True)
    guardar_tabla(anova_l, os.path.join(dir_tablas, "anova_log"), indice=True)

    sup_t = supuestos(df, modelo_t, "time_seconds")
    sup_l = supuestos(df, modelo_l, "log_time")
    tabla_sup = pd.DataFrame([{"respuesta": "time_seconds", **sup_t}, {"respuesta": "log10(time)", **sup_l}])
    guardar_tabla(tabla_sup, os.path.join(dir_tablas, "supuestos"))

    # Post-hoc: lenguaje (global), lenguaje dentro de cada N y combinación completa.
    tk_lang = tukey(df, "log_time", "language", alpha)
    guardar_tabla(tk_lang, os.path.join(dir_tablas, "tukey_lenguaje_log"))
    tk_por_n = []
    for n, g in df.groupby("N"):
        t = tukey(g, "log_time", "language", alpha)
        t.insert(0, "N", n)
        tk_por_n.append(t)
    tk_por_n = pd.concat(tk_por_n, ignore_index=True)
    guardar_tabla(tk_por_n, os.path.join(dir_tablas, "tukey_lenguaje_por_N_log"))
    tk_por_n_t = []
    for n, g in df.groupby("N"):
        t = tukey(g, "time_seconds", "language", alpha)
        t.insert(0, "N", n)
        tk_por_n_t.append(t)
    tk_por_n_t = pd.concat(tk_por_n_t, ignore_index=True)
    guardar_tabla(tk_por_n_t, os.path.join(dir_tablas, "tukey_lenguaje_por_N_tiempo"))
    tk_grupo = tukey(df, "log_time", "grupo", alpha)
    guardar_tabla(tk_grupo, os.path.join(dir_tablas, "tukey_lenguaje_x_N_log"))

    # Robustez no paramétrica: Kruskal-Wallis entre lenguajes para cada N.
    kw = []
    for n, g in df.groupby("N"):
        h = stats.kruskal(*[g[g["language"] == l]["time_seconds"] for l in ORDEN if l in set(g["language"])])
        kw.append({"N": n, "H": h.statistic, "p_valor": h.pvalue})
    kw = pd.DataFrame(kw)
    guardar_tabla(kw, os.path.join(dir_tablas, "kruskal"))

    figura_boxplot(df, os.path.join(dir_figuras, "boxplot_tiempos.png"))
    figura_interaccion(desc, os.path.join(dir_figuras, "interaccion_lenguaje_N.png"))
    figura_speedup(sp, os.path.join(dir_figuras, "speedup_vs_cpp.png"))
    figura_repeticiones(df, os.path.join(dir_figuras, "tiempo_por_repeticion.png"))
    figura_qq(modelo_t, os.path.join(dir_figuras, "qq_residuos_tiempo.png"), "Q-Q residuos (tiempo)")
    figura_qq(modelo_l, os.path.join(dir_figuras, "qq_residuos_log.png"), "Q-Q residuos (log10 tiempo)")

    # Reporte integrado.
    p_lang_t = anova_t.loc["Lenguaje", "PR(>F)"]
    p_lang_l = anova_l.loc["Lenguaje", "PR(>F)"]
    p_int_t = anova_t.loc["Lenguaje:N", "PR(>F)"]
    p_int_l = anova_l.loc["Lenguaje:N", "PR(>F)"]
    no_signif = tk_por_n[~tk_por_n["reject"].astype(bool)]
    r = [
        "# Reporte estadístico del benchmark",
        "",
        f"- Observaciones: **{len(df)}** ({df['language'].nunique()} lenguajes × "
        f"{df['N'].nunique()} tamaños × {df.groupby(['language', 'N']).size().min()} repeticiones)",
        f"- Nivel de significancia: α = {alpha}",
        "- Modelo: ANOVA de dos factores con interacción, `y ~ Lenguaje + N + Lenguaje:N` (suma de cuadrados tipo II).",
        "- Se reporta sobre el tiempo en segundos (especificación del módulo) y sobre log10(tiempo), "
        "transformación que estabiliza la varianza cuando los tiempos difieren en órdenes de magnitud.",
        "",
        "## 1. Estadística descriptiva",
        "",
        desc.to_markdown(index=False, floatfmt=".4g"),
        "",
        "## 2. Razón de tiempos respecto de C++",
        "",
        sp.astype({"N": str}).to_markdown(index=False, floatfmt=".3g"),
        "",
        "## 3. ANOVA de dos factores (tiempo en segundos)",
        "",
        anova_t.to_markdown(floatfmt=".4g"),
        "",
        "## 4. ANOVA de dos factores (log10 del tiempo)",
        "",
        anova_l.to_markdown(floatfmt=".4g"),
        "",
        "## 5. Supuestos del ANOVA",
        "",
        tabla_sup.to_markdown(index=False, floatfmt=".4g"),
        "",
        "Shapiro-Wilk evalúa la normalidad de los residuos; Levene (centrado en la mediana) la homogeneidad "
        "de varianzas entre las 12 celdas. Con n = 10 por celda el ANOVA es razonablemente robusto a "
        "desviaciones moderadas de normalidad, pero no a heterocedasticidad severa: por ello la inferencia "
        "principal se apoya en el modelo log10 y se contrasta con Kruskal-Wallis.",
        "",
        "## 6. Tukey HSD: lenguajes dentro de cada N (log10 del tiempo)",
        "",
        tk_por_n.to_markdown(index=False, floatfmt=".4g"),
        "",
        "Pares **no** significativos: "
        + ("ninguno." if no_signif.empty else
           "; ".join(f"N={f.N}: {f.group1} vs {f.group2} (p={f._5:.3g})" for f in no_signif.itertuples())),
        "",
        "## 7. Robustez: Kruskal-Wallis por N",
        "",
        kw.to_markdown(index=False, floatfmt=".4g"),
        "",
        "## 8. Decisión sobre las hipótesis",
        "",
        f"- Efecto principal del lenguaje (tiempo): F = {anova_t.loc['Lenguaje', 'F']:.4g}, "
        f"p = {p_lang_t:.3g} → **{decision(p_lang_t, alpha)}**.",
        f"- Efecto principal del lenguaje (log10): F = {anova_l.loc['Lenguaje', 'F']:.4g}, "
        f"p = {p_lang_l:.3g} → **{decision(p_lang_l, alpha)}**.",
        f"- Interacción lenguaje × N (tiempo): p = {p_int_t:.3g}; (log10): p = {p_int_l:.3g}. "
        + interpretar_interaccion(p_int_t, p_int_l, alpha),
        "",
        "## 9. Figuras",
        "",
        "![Boxplot](figures/boxplot_tiempos.png)",
        "",
        "![Interacción](figures/interaccion_lenguaje_N.png)",
        "",
        "![Speedup](figures/speedup_vs_cpp.png)",
        "",
        "![Repeticiones](figures/tiempo_por_repeticion.png)",
        "",
        "![QQ tiempo](figures/qq_residuos_tiempo.png) ![QQ log](figures/qq_residuos_log.png)",
        "",
    ]
    with open(os.path.join(salida, "reporte_estadistico.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(r))
    print(f"Análisis completo en {salida}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
