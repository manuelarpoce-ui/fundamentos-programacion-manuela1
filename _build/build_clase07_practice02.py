"""Construye curso/clase07/practice02.ipynb — EDA completo del dataset de transacciones.

Caso aplicado: EDA sistemático sobre transacciones.csv respondiendo preguntas
de negocio con evidencia visual y transformación de datos.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []

C += [
md(r"""
# Clase 7 · Práctica 02 — EDA completo: analizando transacciones

### EDA y transformación de datos aplicados a un caso real

En esta práctica aplicamos el pipeline EDA completo sobre el dataset de
transacciones de una cadena comercial con presencia en cinco ciudades de Colombia.

**Preguntas de negocio que responderemos:**

1. ¿Cuál es el perfil general del dataset? (nulos, tipos, cardinalidad)
2. ¿Cómo se distribuyen los montos? ¿Hay sesgo? ¿Outliers?
3. ¿Qué ciudad y categoría tienen mayor ticket promedio?
4. ¿Los montos difieren significativamente entre métodos de pago?
5. ¿Qué variables están correlacionadas con el monto?

Al final aplicarás tres transformaciones y responderás 3 preguntas propias.
"""),

code(r"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams["figure.figsize"] = (10, 4)
matplotlib.rcParams["axes.spines.top"] = False
matplotlib.rcParams["axes.spines.right"] = False

sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar

RUTA = os.path.join("..", "datasets", "transacciones.csv")
df = pd.read_csv(RUTA)
df["fecha"] = pd.to_datetime(df["fecha"])
print("Dataset cargado:", df.shape)
df.head(3)
"""),

md(r"""
## Paso 1: Perfilado del dataset

Antes de cualquier análisis, diagnosticamos el estado del dataset.
"""),

code(r"""
print("=== PERFIL DEL DATASET ===")
print("Forma:", df.shape)
print("\nTipos de datos:")
print(df.dtypes)
print("\nNulos por columna:")
print(df.isnull().sum())
print("\nFilas duplicadas:", df.duplicated().sum())
print("\nValores únicos por columna:")
print(df.nunique())
"""),

code(r"""
print("=== ESTADÍSTICAS NUMÉRICAS ===")
print(df.describe().round(0))
"""),

md(r"""
### Hallazgos del perfilado

Anota aquí lo que observas. Algunos puntos para reflexionar:
- ¿El rango de montos (min y max) tiene sentido para transacciones comerciales?
- ¿La desviación estándar es alta relativa a la media? ¿Qué indica?
- ¿Cuántas ciudades y categorías únicas hay?

---

## Paso 2: Distribución del monto (variable target)
"""),

code(r"""
monto = df["monto"]

print("=== ESTADÍSTICAS DE MONTO ===")
print("Media:    {:>12,.0f}".format(monto.mean()))
print("Mediana:  {:>12,.0f}".format(monto.median()))
print("Std:      {:>12,.0f}".format(monto.std()))
print("Skewness: {:>12.4f}".format(monto.skew()))
q1 = monto.quantile(0.25)
q3 = monto.quantile(0.75)
iqr = q3 - q1
print("IQR:      {:>12,.0f}".format(iqr))
print("Lim sup IQR: {:>10,.0f}".format(q3 + 1.5 * iqr))
print("\nDiferencia media/mediana: {:,.0f}".format(abs(monto.mean() - monto.median())))
print("Sesgo positivo => cola larga a la derecha (outliers altos)")
"""),

code(r"""
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Histograma
axes[0].hist(monto, bins=25, color="#4C72B0", edgecolor="white", alpha=0.85)
axes[0].axvline(monto.mean(), color="red", linestyle="--", label="Media")
axes[0].axvline(monto.median(), color="green", linestyle="--", label="Mediana")
axes[0].set_title("Distribución de montos")
axes[0].set_xlabel("Monto ($)")
axes[0].legend()

# Boxplot
axes[1].boxplot(monto, patch_artist=True,
                boxprops=dict(facecolor="#4C72B0", alpha=0.5),
                medianprops=dict(color="red", linewidth=2))
axes[1].set_title("Boxplot de montos")
axes[1].set_ylabel("Monto ($)")

# Log-transformado
axes[2].hist(np.log1p(monto), bins=25, color="#55A868", edgecolor="white", alpha=0.85)
axes[2].set_title("log(1 + Monto) — mas simetrico")
axes[2].set_xlabel("log(1 + Monto)")

for ax in axes:
    ax.set_ylabel("Frecuencia")

plt.suptitle("Distribución univariada del monto", fontsize=11)
plt.tight_layout()
plt.show()
"""),

md(r"""
**Interpretación:**
- El histograma muestra sesgo a la derecha: la mayoría de transacciones son
  de montos bajos/medios, pero hay algunas muy altas que alargan la cola.
- La media es mayor que la mediana por esa misma razón.
- `log(1 + monto)` produce una distribución más simétrica, útil para modelos
  que asumen normalidad.

---

## Paso 3: Outliers
"""),

code(r"""
# Método IQR
q1, q3 = monto.quantile(0.25), monto.quantile(0.75)
iqr = q3 - q1
lim_sup = q3 + 1.5 * iqr
lim_inf = q1 - 1.5 * iqr

outliers = df[(monto < lim_inf) | (monto > lim_sup)]
print("Outliers por IQR: {}  ({:.1f}% del total)".format(
    len(outliers), 100 * len(outliers) / len(df)))
print("\nTop 5 outliers por monto:")
print(outliers.sort_values("monto", ascending=False)
      [["id", "ciudad", "categoria", "metodo_pago", "monto"]].head(5).to_string(index=False))

# Z-score
z = (monto - monto.mean()).abs() / monto.std()
print("\nOutliers por z-score (|z|>3): {}".format((z > 3).sum()))
"""),

md(r"""
### ¿Qué hacer con los outliers?

En este dataset, un monto de $2.3M puede ser una compra corporativa legítima.
**No se eliminan automáticamente.** Las opciones son:
1. Dejarlos y usar modelos robustos.
2. Transformar (`log`) para reducir su impacto.
3. Tratarlos por separado (segmento mayorista vs. minorista).

---

## Paso 4: Análisis por variables categóricas

### Pregunta 3: ¿Qué ciudad y categoría tienen mayor ticket promedio?
"""),

code(r"""
fig, axes = plt.subplots(2, 2, figsize=(13, 9))

# Mediana de monto por ciudad
gr_ciudad = df.groupby("ciudad")["monto"].median().sort_values(ascending=True)
axes[0, 0].barh(gr_ciudad.index, gr_ciudad.values, color="#4C72B0", edgecolor="white")
axes[0, 0].set_title("Mediana de monto por ciudad")
axes[0, 0].set_xlabel("Mediana del monto ($)")

# Mediana de monto por categoría
gr_cat = df.groupby("categoria")["monto"].median().sort_values(ascending=True)
axes[0, 1].barh(gr_cat.index, gr_cat.values, color="#55A868", edgecolor="white")
axes[0, 1].set_title("Mediana de monto por categoria")

# Frecuencia por metodo_pago
vc_metodo = df["metodo_pago"].value_counts()
axes[1, 0].bar(vc_metodo.index, vc_metodo.values, color="#C44E52", edgecolor="white")
axes[1, 0].set_title("Frecuencia por metodo de pago")
axes[1, 0].set_ylabel("N transacciones")

# Monto por metodo_pago (boxplot)
metodos = sorted(df["metodo_pago"].unique())
data_metodos = [df[df["metodo_pago"] == m]["monto"].values for m in metodos]
axes[1, 1].boxplot(data_metodos, labels=metodos, patch_artist=True)
axes[1, 1].set_title("Distribucion de monto por metodo de pago")
axes[1, 1].set_ylabel("Monto ($)")

plt.suptitle("Analisis por variables categoricas", fontsize=12)
plt.tight_layout()
plt.show()
"""),

code(r"""
print("=== TABLA: mediana y n por ciudad ===")
print(df.groupby("ciudad")["monto"].agg(["median","mean","count"]).round(0)
      .sort_values("median", ascending=False).to_string())

print("\n=== TABLA: mediana y n por categoría ===")
print(df.groupby("categoria")["monto"].agg(["median","mean","count"]).round(0)
      .sort_values("median", ascending=False).to_string())
"""),

md(r"""
### Pregunta 4: ¿Los montos difieren entre métodos de pago?
"""),

code(r"""
print("=== MONTO POR MÉTODO DE PAGO ===")
print(df.groupby("metodo_pago")["monto"].agg(["mean","median","std","count"]).round(0))
"""),

md(r"""
---

## Paso 5: Correlaciones

### Pregunta 5: ¿Qué variables numéricas correlacionan con el monto?
"""),

code(r"""
# Creamos variables numéricas para el heatmap
df_num = df.copy()
df_num["monto_log"] = np.log1p(df_num["monto"])
df_num["es_tecnologia"] = (df_num["categoria"] == "tecnologia").astype(int)
df_num["es_transferencia"] = (df_num["metodo_pago"] == "transferencia").astype(int)

cols_num = ["monto", "monto_log", "es_tecnologia", "es_transferencia"]
corr = df_num[cols_num].corr()

fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
fig.colorbar(im, ax=ax)
ax.set_xticks(range(len(cols_num)))
ax.set_yticks(range(len(cols_num)))
ax.set_xticklabels(cols_num, rotation=35, ha="right")
ax.set_yticklabels(cols_num)
for i in range(len(cols_num)):
    for j in range(len(cols_num)):
        ax.text(j, i, "{:.2f}".format(corr.iloc[i, j]),
                ha="center", va="center", fontsize=10)
ax.set_title("Heatmap de correlaciones")
plt.tight_layout()
plt.show()
"""),

md(r"""
---

## Paso 6: Transformaciones para modelado

Antes de pasar al modelado, aplicamos las transformaciones estándar.
"""),

code(r"""
# Normalización, estandarización, encoding y binning en un paso
df_model = df.copy()

# Normalización min-max del monto
mn, mx = df_model["monto"].min(), df_model["monto"].max()
df_model["monto_norm"] = (df_model["monto"] - mn) / (mx - mn)

# Estandarización z-score del monto
mu, sigma = df_model["monto"].mean(), df_model["monto"].std()
df_model["monto_std"] = (df_model["monto"] - mu) / sigma

# Binning en 4 cuartiles
df_model["monto_qbin"] = pd.qcut(df_model["monto"], q=4,
                                   labels=["Q1","Q2","Q3","Q4"])

# One-hot encoding
df_model = pd.concat([
    df_model,
    pd.get_dummies(df_model["metodo_pago"], prefix="pago"),
    pd.get_dummies(df_model["ciudad"], prefix="ciudad"),
    pd.get_dummies(df_model["categoria"], prefix="cat"),
], axis=1)

print("Shape final para modelado:", df_model.shape)
print("\nNuevas columnas numéricas:")
print([c for c in df_model.columns if c.startswith(("pago_","ciudad_","cat_","monto_"))])
"""),
]


# --------------------------------------------------------------------------- #
# Tu turno: 3 mini-tareas
# --------------------------------------------------------------------------- #
C += [
md(r"""
---
## Tu turno

Ahora resuelve tú. Completa cada función y ejecuta su comprobación.
"""),

md(r"""
### Tarea A · Detectar columnas con más del X% de nulos

Completa `columnas_con_nulos(df, umbral_pct=20)`: devuelve una **lista** con los
nombres de las columnas que tienen más del `umbral_pct`% de valores nulos.

**Ejemplo:** si `monto` tiene 30% de nulos y el umbral es 20, debe aparecer en la lista.
"""),

code(r"""
def columnas_con_nulos(df, umbral_pct=20):
    # ✏️ TU CÓDIGO AQUÍ (usa df.isnull().mean() * 100)
    return None

# Prueba con un DataFrame artificial que tiene nulos controlados
import numpy as np
_df_test = pd.DataFrame({
    "a": [1.0, np.nan, np.nan, 4.0],       # 50% nulos
    "b": [1.0, 2.0, 3.0, np.nan],           # 25% nulos
    "c": [1.0, 2.0, 3.0, 4.0],             # 0% nulos
})
_r = columnas_con_nulos(_df_test, umbral_pct=20)
revisar("detecta columnas con >20% nulos", _r is not None and set(_r) == {"a", "b"})
revisar("no incluye columna sin nulos", _r is not None and "c" not in _r)
revisar("funciona sobre dataset real (esperamos lista vacía)", columnas_con_nulos(df) is not None)
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def columnas_con_nulos(df, umbral_pct=20):
    pct_nulos = df.isnull().mean() * 100
    return pct_nulos[pct_nulos > umbral_pct].index.tolist()
```
</details>
"""),

md(r"""
### Tarea B · Tabla de frecuencias relativas de una categórica

Completa `frecuencias_relativas(df, columna)`: devuelve una `pd.Series` con las
frecuencias relativas (como porcentaje entre 0 y 100, redondeado a 1 decimal),
ordenada de mayor a menor.

**Ejemplo:** para `metodo_pago` devuelve algo como:
```
efectivo       40.0
tarjeta        33.3
transferencia  26.7
```
"""),

code(r"""
def frecuencias_relativas(df, columna):
    # ✏️ TU CÓDIGO AQUÍ
    return None

_r = frecuencias_relativas(df, "metodo_pago")
revisar("devuelve Serie", _r is not None and isinstance(_r, pd.Series))
revisar("suma 100%", _r is not None and abs(_r.sum() - 100.0) < 0.5)
revisar("ordenada de mayor a menor", _r is not None and _r.iloc[0] >= _r.iloc[-1])
revisar("valores son porcentajes (>1)", _r is not None and _r.max() > 1.0)
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def frecuencias_relativas(df, columna):
    return (df[columna].value_counts(normalize=True) * 100).round(1)
```
</details>
"""),

md(r"""
### Tarea C · Normalizar todas las columnas numéricas de un DataFrame

Completa `normalizar_numericas(df)`: devuelve un **nuevo DataFrame** donde todas
las columnas numéricas han sido normalizadas a `[0, 1]` (min-max).
Las columnas no numéricas deben mantenerse sin cambios.

**Importante:** no modifiques el DataFrame original.
"""),

code(r"""
def normalizar_numericas(df):
    # ✏️ TU CÓDIGO AQUÍ
    return None

_df_test = pd.DataFrame({
    "ciudad": ["Bogota", "Cali", "Bogota"],
    "monto":  [100.0, 200.0, 150.0],
    "id":     [1, 2, 3],
})
_r = normalizar_numericas(_df_test)
revisar("devuelve DataFrame", _r is not None and isinstance(_r, pd.DataFrame))
revisar("monto normalizado a [0,1]", _r is not None and abs(_r["monto"].min() - 0.0) < 1e-9 and abs(_r["monto"].max() - 1.0) < 1e-9)
revisar("ciudad sin cambios", _r is not None and list(_r["ciudad"]) == ["Bogota", "Cali", "Bogota"])
revisar("original intacto", _df_test["monto"].max() == 200.0)
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def normalizar_numericas(df):
    df_out = df.copy()
    cols_num = df_out.select_dtypes(include="number").columns
    for col in cols_num:
        mn, mx = df_out[col].min(), df_out[col].max()
        if mx != mn:
            df_out[col] = (df_out[col] - mn) / (mx - mn)
        else:
            df_out[col] = 0.0
    return df_out
```
</details>
"""),

md(r"""
---
## Reflexión final

Este notebook demostró el flujo completo de un EDA real:

1. **Perfilar** → sabemos qué tenemos y qué está mal.
2. **Distribución univariada** → detectamos sesgo y outliers en el monto.
3. **Análisis categórico** → identificamos diferencias entre ciudades y categorías.
4. **Correlaciones** → entendemos qué variables se mueven juntas.
5. **Transformaciones** → preparamos los datos para modelado.

En la Clase 8 usaremos estos datos ya preparados para entrenar nuestros primeros modelos.

Continúa con **homework01.ipynb** y **homework02.ipynb**.
"""),
]


# ===================================================================== #
# VALIDACIÓN en construcción
# ===================================================================== #
def _validar():
    import csv
    import numpy as np
    import pandas as pd

    ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "datasets", "transacciones.csv")
    df = pd.read_csv(os.path.abspath(ruta))

    def columnas_con_nulos(df, umbral_pct=20):
        pct_nulos = df.isnull().mean() * 100
        return pct_nulos[pct_nulos > umbral_pct].index.tolist()

    df_test = pd.DataFrame({
        "a": [1.0, np.nan, np.nan, 4.0],
        "b": [1.0, 2.0, 3.0, np.nan],
        "c": [1.0, 2.0, 3.0, 4.0],
    })
    assert set(columnas_con_nulos(df_test, 20)) == {"a", "b"}
    assert columnas_con_nulos(df) == []

    def frecuencias_relativas(df, columna):
        return (df[columna].value_counts(normalize=True) * 100).round(1)

    fr = frecuencias_relativas(df, "metodo_pago")
    assert isinstance(fr, pd.Series)
    assert abs(fr.sum() - 100.0) < 0.5

    def normalizar_numericas(df):
        df_out = df.copy()
        cols_num = df_out.select_dtypes(include="number").columns
        for col in cols_num:
            mn, mx = df_out[col].min(), df_out[col].max()
            if mx != mn:
                df_out[col] = (df_out[col] - mn) / (mx - mn)
            else:
                df_out[col] = 0.0
        return df_out

    df_n = normalizar_numericas(df)
    assert abs(df_n["monto"].min() - 0.0) < 1e-9
    assert abs(df_n["monto"].max() - 1.0) < 1e-9

    print("✔ Las soluciones de referencia de practice02 pasan sus pruebas.")


_validar()

# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase07", "practice02.ipynb")
build(os.path.abspath(ruta), C)
