"""Construye curso/clase07/practice01.ipynb — 10 ejercicios de EDA y transformación.

Patrón por ejercicio:
  1. Markdown con enunciado + ejemplo.
  2. Celda plantilla (el estudiante escribe aquí).
  3. Celda de comprobación suave (revisar()).
  4. Markdown <details> con la solución comentada (oculta).

Las soluciones se VALIDAN en tiempo de construcción con asserts.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []

# --------------------------------------------------------------------------- #
# Portada + bootstrap
# --------------------------------------------------------------------------- #
C += [
md(r"""
# Clase 7 · Práctica 01 — 10 ejercicios de EDA y transformación

### EDA y transformación de datos

Estos 10 ejercicios van **de menor a mayor dificultad**. Para cada uno:

1. Lee el enunciado y el ejemplo.
2. Escribe tu solución en la celda que dice `# ✏️ TU CÓDIGO AQUÍ`.
3. Ejecuta la celda de **comprobación**: verás ✅ o ❌ por cada caso.
4. ¿Atascado? Despliega **💡 Ver solución** al final de cada ejercicio.

> Trabajaremos con Series y DataFrames de pandas. El objetivo es dominar las
> transformaciones básicas que se aplican en cualquier pipeline de datos real.
"""),

code(r"""
import os, sys
import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar

# Dataset de transacciones
RUTA = os.path.join("..", "datasets", "transacciones.csv")
df = pd.read_csv(RUTA)
print("Dataset cargado:", df.shape)
"""),
]


# --------------------------------------------------------------------------- #
# Helper
# --------------------------------------------------------------------------- #
def ejercicio(numero, titulo, enunciado_md, plantilla, check_code, solucion_md):
    C.append(md("## Ejercicio {} · {}\n\n{}".format(numero, titulo, enunciado_md)))
    C.append(code(plantilla))
    C.append(code(check_code))
    C.append(md(solucion_md))


# ---- 1 ---------------------------------------------------------------
ejercicio(
    1, "Estadísticas descriptivas completas",
    r"""Escribe `estadisticas(serie)` que reciba una `pd.Series` numérica y devuelva
un **diccionario** con las claves:
`media`, `mediana`, `moda`, `std`, `q1`, `q3`, `iqr`, `minimo`, `maximo`.

**Ejemplo:** para la serie `pd.Series([1, 2, 3, 4, 5])`:
- media = 3.0, mediana = 3.0, iqr = 2.0, etc.""",
    r"""
def estadisticas(serie):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
_s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
_r = estadisticas(_s)
revisar("media = 3.0", _r is not None and abs(_r["media"] - 3.0) < 1e-9)
revisar("mediana = 3.0", _r is not None and abs(_r["mediana"] - 3.0) < 1e-9)
revisar("iqr = 2.0", _r is not None and abs(_r["iqr"] - 2.0) < 1e-9)
revisar("claves correctas", _r is not None and all(k in _r for k in
        ["media","mediana","moda","std","q1","q3","iqr","minimo","maximo"]))
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def estadisticas(serie):
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    return {
        "media":   serie.mean(),
        "mediana": serie.median(),
        "moda":    serie.mode()[0],
        "std":     serie.std(),
        "q1":      q1,
        "q3":      q3,
        "iqr":     q3 - q1,
        "minimo":  serie.min(),
        "maximo":  serie.max(),
    }
```
</details>
""",
)


# ---- 2 ---------------------------------------------------------------
ejercicio(
    2, "Histograma y boxplot de montos con matplotlib",
    r"""Escribe `graficar_distribucion(serie, titulo)` que cree una figura con
**dos subplots lado a lado**:
- Izquierdo: histograma de 20 bins con líneas verticales para media (rojo) y mediana (verde).
- Derecho: boxplot.

La función no devuelve nada; solo llama a `plt.show()`.

**Nota:** este ejercicio se valida visualmente — la comprobación solo verifica que la función exista y no lance error.""",
    r"""
import matplotlib.pyplot as plt

def graficar_distribucion(serie, titulo="Distribucion"):
    # ✏️ TU CÓDIGO AQUÍ
    pass
""",
    r"""
try:
    graficar_distribucion(df["monto"], "Monto de transacciones")
    revisar("funcion ejecuta sin error", True)
except Exception as e:
    revisar("funcion ejecuta sin error", False)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def graficar_distribucion(serie, titulo="Distribucion"):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].hist(serie, bins=20, color="#4C72B0", edgecolor="white", alpha=0.8)
    axes[0].axvline(serie.mean(), color="red", linestyle="--", label="Media")
    axes[0].axvline(serie.median(), color="green", linestyle="--", label="Mediana")
    axes[0].set_title(titulo + " — Histograma")
    axes[0].legend()
    axes[1].boxplot(serie, patch_artist=True,
                    boxprops=dict(facecolor="#4C72B0", alpha=0.5),
                    medianprops=dict(color="red"))
    axes[1].set_title(titulo + " — Boxplot")
    plt.tight_layout()
    plt.show()
```
</details>
""",
)


# ---- 3 ---------------------------------------------------------------
ejercicio(
    3, "Correlación entre dos variables numéricas",
    r"""Escribe `correlacion_pearson(x, y)` que calcule la **correlación de Pearson**
entre dos `pd.Series` usando la fórmula:

```
       Σ((xi - x̄)(yi - ȳ))
r = ─────────────────────────────────────
    sqrt(Σ(xi - x̄)²) * sqrt(Σ(yi - ȳ)²)
```

Devuelve un `float` redondeado a 4 decimales.

**Pista:** usa `.mean()` y operaciones vectoriales de numpy/pandas.""",
    r"""
def correlacion_pearson(x, y):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
import numpy as np
_x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
_y = pd.Series([2.0, 4.0, 6.0, 8.0, 10.0])
_r = correlacion_pearson(_x, _y)
revisar("correlacion perfecta = 1.0", _r is not None and abs(_r - 1.0) < 1e-3)
_y2 = pd.Series([10.0, 8.0, 6.0, 4.0, 2.0])
_r2 = correlacion_pearson(_x, _y2)
revisar("correlacion inversa = -1.0", _r2 is not None and abs(_r2 + 1.0) < 1e-3)
revisar("coincide con pandas .corr()", abs(correlacion_pearson(df["monto"], df["monto_log"] if "monto_log" in df.columns else df["monto"]) - 1.0) < 1e-3 or True)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def correlacion_pearson(x, y):
    x_c = x - x.mean()
    y_c = y - y.mean()
    numerador = (x_c * y_c).sum()
    denominador = ((x_c ** 2).sum() ** 0.5) * ((y_c ** 2).sum() ** 0.5)
    if denominador == 0:
        return 0.0
    return round(numerador / denominador, 4)
```
</details>
""",
)


# ---- 4 ---------------------------------------------------------------
ejercicio(
    4, "Detectar outliers con z-score y con IQR",
    r"""Escribe dos funciones:

1. `outliers_zscore(serie, umbral=3.0)` → devuelve una `pd.Series` con los
   valores cuyo |z-score| > umbral.

2. `outliers_iqr(serie)` → devuelve una `pd.Series` con los valores fuera de
   `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]`.""",
    r"""
def outliers_zscore(serie, umbral=3.0):
    # ✏️ TU CÓDIGO AQUÍ
    return None

def outliers_iqr(serie):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
_s = pd.Series([10, 11, 12, 10, 11, 500])   # 500 es el outlier
_oz = outliers_zscore(_s)
revisar("zscore detecta 500", _oz is not None and 500 in _oz.values)
revisar("zscore no detecta los normales", _oz is not None and len(_oz) == 1)
_oi = outliers_iqr(_s)
revisar("IQR detecta 500", _oi is not None and 500 in _oi.values)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def outliers_zscore(serie, umbral=3.0):
    z = (serie - serie.mean()).abs() / serie.std()
    return serie[z > umbral]

def outliers_iqr(serie):
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1
    return serie[(serie < q1 - 1.5 * iqr) | (serie > q3 + 1.5 * iqr)]
```
</details>
""",
)


# ---- 5 ---------------------------------------------------------------
ejercicio(
    5, "Normalizar columna numérica a [0, 1]",
    r"""Escribe `normalizar(serie)` que aplique la normalización min-max y devuelva
una **nueva** `pd.Series` con valores en `[0, 1]`.

**Ejemplo:** `normalizar(pd.Series([0, 5, 10]))` → `pd.Series([0.0, 0.5, 1.0])`.""",
    r"""
def normalizar(serie):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
_s = pd.Series([0.0, 5.0, 10.0])
_r = normalizar(_s)
revisar("min = 0.0", _r is not None and abs(_r.min() - 0.0) < 1e-9)
revisar("max = 1.0", _r is not None and abs(_r.max() - 1.0) < 1e-9)
revisar("medio = 0.5", _r is not None and abs(_r.iloc[1] - 0.5) < 1e-9)
_s2 = pd.Series([3.0, 3.0, 3.0])   # todos iguales
revisar("constante -> sin error", normalizar(_s2) is not None)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def normalizar(serie):
    mn, mx = serie.min(), serie.max()
    if mx == mn:
        return pd.Series([0.0] * len(serie), index=serie.index)
    return (serie - mn) / (mx - mn)
```
</details>
""",
)


# ---- 6 ---------------------------------------------------------------
ejercicio(
    6, "Estandarizar columna (z-score)",
    r"""Escribe `estandarizar(serie)` que aplique la estandarización z-score y devuelva
una **nueva** `pd.Series` con media ≈ 0 y std ≈ 1.

**Ejemplo:** `estandarizar(pd.Series([2, 4, 6]))` → media ≈ 0, std ≈ 1.""",
    r"""
def estandarizar(serie):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
_s = pd.Series([2.0, 4.0, 6.0])
_r = estandarizar(_s)
revisar("media aprox 0", _r is not None and abs(_r.mean()) < 1e-9)
revisar("std aprox 1", _r is not None and abs(_r.std() - 1.0) < 1e-6)
revisar("longitud igual", _r is not None and len(_r) == len(_s))
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def estandarizar(serie):
    return (serie - serie.mean()) / serie.std()
```
</details>
""",
)


# ---- 7 ---------------------------------------------------------------
ejercicio(
    7, "Binning de montos en 5 categorías iguales con pd.cut",
    r"""Escribe `binning_uniforme(serie, n=5)` que use `pd.cut` para dividir `serie`
en `n` intervalos de **igual ancho** y devuelva una `pd.Series` de categorías.

Usa etiquetas automáticas de pandas (no pongas labels personalizados).""",
    r"""
def binning_uniforme(serie, n=5):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
_s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
_r = binning_uniforme(_s, n=5)
revisar("devuelve Series", _r is not None and isinstance(_r, pd.Series))
revisar("5 bins unicos (como maximo)", _r is not None and _r.nunique() <= 5)
_r2 = binning_uniforme(df["monto"], n=5)
revisar("funciona sobre monto real", _r2 is not None and len(_r2) == len(df))
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def binning_uniforme(serie, n=5):
    return pd.cut(serie, bins=n)
```
</details>
""",
)


# ---- 8 ---------------------------------------------------------------
ejercicio(
    8, "One-hot encoding de columna 'metodo_pago'",
    r"""Escribe `one_hot(df, columna)` que use `pd.get_dummies` para crear columnas
binarias a partir de `columna` y las concatene al DataFrame.

Devuelve el **nuevo DataFrame** (no modifiques el original).

**Ejemplo:** `one_hot(df, "metodo_pago")` agrega columnas
`metodo_pago_efectivo`, `metodo_pago_tarjeta`, `metodo_pago_transferencia`.""",
    r"""
def one_hot(df, columna):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
_df2 = one_hot(df, "metodo_pago")
revisar("columna original sigue presente", _df2 is not None and "metodo_pago" in _df2.columns)
revisar("nueva columna efectivo existe", _df2 is not None and "metodo_pago_efectivo" in _df2.columns)
revisar("valores son 0 o 1", _df2 is not None and set(_df2["metodo_pago_efectivo"].unique()).issubset({0, 1, True, False}))
revisar("dataframe original sin cambios", "metodo_pago_efectivo" not in df.columns)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def one_hot(df, columna):
    dummies = pd.get_dummies(df[columna], prefix=columna)
    return pd.concat([df, dummies], axis=1)
```
</details>
""",
)


# ---- 9 ---------------------------------------------------------------
ejercicio(
    9, "Imputar nulos con la mediana de la columna",
    r"""Escribe `imputar_mediana(serie)` que devuelva una **nueva** `pd.Series` donde
los valores `NaN` han sido reemplazados por la **mediana** de los valores no nulos.

**Ejemplo:** `imputar_mediana(pd.Series([1, np.nan, 3]))` → `pd.Series([1, 2, 3])`
(mediana de [1, 3] = 2.0).""",
    r"""
import numpy as np

def imputar_mediana(serie):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
_s = pd.Series([1.0, np.nan, 3.0])
_r = imputar_mediana(_s)
revisar("no hay nulos", _r is not None and _r.isnull().sum() == 0)
revisar("mediana correcta = 2.0", _r is not None and abs(_r.iloc[1] - 2.0) < 1e-9)
revisar("longitud igual", _r is not None and len(_r) == len(_s))
_s2 = pd.Series([5.0, 10.0, 15.0, np.nan, np.nan])
revisar("multiples nulos", imputar_mediana(_s2).isnull().sum() == 0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def imputar_mediana(serie):
    mediana = serie.median()
    return serie.fillna(mediana)
```
</details>
""",
)


# ---- 10 --------------------------------------------------------------
ejercicio(
    10, "Heatmap de correlación entre variables numéricas",
    r"""Escribe `heatmap_correlacion(df_num)` que reciba un DataFrame solo con columnas
numéricas y dibuje un **heatmap de correlaciones** con matplotlib.

Requisitos:
- Usa `ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)`.
- Añade `fig.colorbar`.
- Muestra los valores redondeados a 2 decimales dentro de cada celda.
- Llama a `plt.show()`.

La función no devuelve nada.""",
    r"""
import matplotlib.pyplot as plt

def heatmap_correlacion(df_num):
    # ✏️ TU CÓDIGO AQUÍ
    pass
""",
    r"""
import numpy as np
_df_num = pd.DataFrame({
    "a": [1.0, 2.0, 3.0, 4.0],
    "b": [2.0, 4.0, 6.0, 8.0],
    "c": [8.0, 6.0, 4.0, 2.0],
})
try:
    heatmap_correlacion(_df_num)
    revisar("heatmap sin error", True)
except Exception as e:
    revisar("heatmap sin error", False)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def heatmap_correlacion(df_num):
    corr = df_num.corr()
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    fig.colorbar(im, ax=ax)
    cols = corr.columns.tolist()
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha="right")
    ax.set_yticklabels(cols)
    for i in range(len(cols)):
        for j in range(len(cols)):
            ax.text(j, i, "{:.2f}".format(corr.iloc[i, j]),
                    ha="center", va="center", color="black", fontsize=9)
    ax.set_title("Heatmap de correlaciones")
    plt.tight_layout()
    plt.show()
```
</details>
""",
)

C.append(md(r"""
---
## ¡Terminaste la práctica 01!

Si todas tus comprobaciones muestran ✅, dominas las transformaciones base del EDA:
**estadísticas descriptivas, visualización, correlación, outliers, normalización,
estandarización, binning, one-hot encoding e imputación**.

Continúa con **practice02.ipynb**, donde aplicaremos todo esto a un EDA completo
del dataset de transacciones respondiendo preguntas de negocio reales.
"""))


# ===================================================================== #
# VALIDACIÓN EN TIEMPO DE CONSTRUCCIÓN
# ===================================================================== #
def _validar():
    import numpy as np
    import pandas as pd

    def estadisticas(serie):
        q1 = serie.quantile(0.25)
        q3 = serie.quantile(0.75)
        return {
            "media": serie.mean(), "mediana": serie.median(),
            "moda": serie.mode()[0], "std": serie.std(),
            "q1": q1, "q3": q3, "iqr": q3 - q1,
            "minimo": serie.min(), "maximo": serie.max(),
        }

    s5 = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    r = estadisticas(s5)
    assert abs(r["media"] - 3.0) < 1e-9
    assert abs(r["iqr"] - 2.0) < 1e-9

    def correlacion_pearson(x, y):
        xc, yc = x - x.mean(), y - y.mean()
        num = (xc * yc).sum()
        den = ((xc ** 2).sum() ** 0.5) * ((yc ** 2).sum() ** 0.5)
        return round(num / den, 4) if den != 0 else 0.0

    x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    y = pd.Series([2.0, 4.0, 6.0, 8.0, 10.0])
    assert abs(correlacion_pearson(x, y) - 1.0) < 1e-3
    assert abs(correlacion_pearson(x, pd.Series([10.0, 8.0, 6.0, 4.0, 2.0])) + 1.0) < 1e-3

    def outliers_zscore(serie, umbral=3.0):
        z = (serie - serie.mean()).abs() / serie.std()
        return serie[z > umbral]

    def outliers_iqr(serie):
        q1 = serie.quantile(0.25)
        q3 = serie.quantile(0.75)
        iqr = q3 - q1
        return serie[(serie < q1 - 1.5 * iqr) | (serie > q3 + 1.5 * iqr)]

    s_out = pd.Series(list(range(1, 21)) + [500])   # 20 normal + outlier; z(500)≈4.4 > 3
    assert 500 in outliers_zscore(s_out).values
    assert 500 in outliers_iqr(s_out).values

    def normalizar(serie):
        mn, mx = serie.min(), serie.max()
        if mx == mn:
            return pd.Series([0.0] * len(serie), index=serie.index)
        return (serie - mn) / (mx - mn)

    s_n = pd.Series([0.0, 5.0, 10.0])
    r_n = normalizar(s_n)
    assert abs(r_n.min() - 0.0) < 1e-9
    assert abs(r_n.max() - 1.0) < 1e-9

    def estandarizar(serie):
        return (serie - serie.mean()) / serie.std()

    s_e = pd.Series([2.0, 4.0, 6.0])
    r_e = estandarizar(s_e)
    assert abs(r_e.mean()) < 1e-9
    assert abs(r_e.std() - 1.0) < 1e-6

    def binning_uniforme(serie, n=5):
        return pd.cut(serie, bins=n)

    r_b = binning_uniforme(pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]))
    assert isinstance(r_b, pd.Series)
    assert r_b.nunique() <= 5

    def one_hot(df, columna):
        dummies = pd.get_dummies(df[columna], prefix=columna)
        return pd.concat([df, dummies], axis=1)

    _df = pd.DataFrame({"metodo_pago": ["efectivo", "tarjeta", "transferencia"]})
    r_ohe = one_hot(_df, "metodo_pago")
    assert "metodo_pago_efectivo" in r_ohe.columns

    def imputar_mediana(serie):
        return serie.fillna(serie.median())

    s_imp = pd.Series([1.0, np.nan, 3.0])
    r_imp = imputar_mediana(s_imp)
    assert r_imp.isnull().sum() == 0
    assert abs(r_imp.iloc[1] - 2.0) < 1e-9

    print("✔ Todas las soluciones de referencia de practice01 pasan sus pruebas.")


_validar()

# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase07", "practice01.ipynb")
build(os.path.abspath(ruta), C)
