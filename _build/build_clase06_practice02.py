"""Construye curso/clase06/practice02.ipynb — análisis completo del dataset de transacciones.

Caso aplicado de ciencia de datos: limpieza de tipos, análisis por dimensión
(ciudad, categoría, método), y visualización con matplotlib.
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
# Clase 6 · Práctica 02 — Análisis completo de transacciones con pandas

### De los datos crudos al informe ejecutivo

En esta práctica realizaremos un análisis exploratorio completo del dataset de
transacciones, aplicando todo lo aprendido en la clase:

1. Carga e inspección inicial.
2. Limpieza y conversión de tipos.
3. Análisis por ciudad, categoría y método de pago.
4. Análisis temporal.
5. Visualización con matplotlib.
6. Tres **"Tu turno"** para que practiques por tu cuenta.

> 🎯 Al terminar habrás producido el tipo de análisis que los científicos de datos
> hacen para responder preguntas de negocio reales.
"""),

code(r"""
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar

# Cargar dataset
ruta = os.path.join("..", "datasets", "transacciones.csv")
df = pd.read_csv(ruta, parse_dates=["fecha"])

print("Dataset cargado: {} filas x {} columnas".format(df.shape[0], df.shape[1]))
print("Columnas:", df.columns.tolist())
"""),
]


# --------------------------------------------------------------------------- #
# SECCIÓN 1: Inspección
# --------------------------------------------------------------------------- #
C += [
md(r"""
## Paso 1 · Inspección inicial

Antes de cualquier análisis, conocemos la estructura y calidad de los datos.
"""),

code(r"""
# Vista general
print("=== head(5) ===")
print(df.head(5))
"""),

code(r"""
# Tipos y nulos
print("=== info() ===")
df.info()
"""),

code(r"""
# Estadísticas numéricas
print("=== describe() ===")
print(df.describe())
"""),

code(r"""
# Distribución de valores categóricos
for col in ["ciudad", "categoria", "metodo_pago"]:
    print("--- {} ---".format(col))
    print(df[col].value_counts())
    print()
"""),

md(r"""
**Hallazgos de la inspección:**

- El dataset tiene 120 transacciones sin valores nulos.
- La columna `fecha` fue reconocida como `datetime64` gracias a `parse_dates`.
- El `monto` varía ampliamente (verifícalo con `describe()`).
- Las ciudades y categorías tienen distribución aproximadamente uniforme.
"""),
]


# --------------------------------------------------------------------------- #
# SECCIÓN 2: Análisis por ciudad
# --------------------------------------------------------------------------- #
C += [
md(r"""
## Paso 2 · Análisis por ciudad

Respondemos: ¿Qué ciudad genera más ingresos? ¿Cuál tiene el ticket más alto?
"""),

code(r"""
# Resumen completo por ciudad
resumen_ciudad = (
    df.groupby("ciudad")["monto"]
      .agg(
          total="sum",
          promedio="mean",
          maximo="max",
          n="count"
      )
      .round({"promedio": 0, "maximo": 0})
      .reset_index()
      .sort_values("total", ascending=False)
      .reset_index(drop=True)
)
print("Resumen por ciudad:")
print(resumen_ciudad.to_string(index=False))
"""),

code(r"""
# Calcular % de participación
total_global = df["monto"].sum()
resumen_ciudad["pct_total"] = (resumen_ciudad["total"] / total_global * 100).round(1)
print("\nParticipación porcentual por ciudad:")
print(resumen_ciudad[["ciudad", "total", "pct_total"]].to_string(index=False))
"""),

code(r"""
# Gráfico de barras horizontales
fig, axes = plt.subplots(1, 2, figsize=(13, 4))

# Barras de total
resumen_ciudad.sort_values("total").plot(
    kind="barh", x="ciudad", y="total", ax=axes[0],
    color="steelblue", title="Ventas totales por ciudad", legend=False
)
axes[0].set_xlabel("Monto (COP)")

# Barras de promedio
resumen_ciudad.sort_values("promedio").plot(
    kind="barh", x="ciudad", y="promedio", ax=axes[1],
    color="coral", title="Ticket promedio por ciudad", legend=False
)
axes[1].set_xlabel("Monto promedio (COP)")

plt.tight_layout()
plt.show()
"""),
]


# --------------------------------------------------------------------------- #
# SECCIÓN 3: Análisis por categoría
# --------------------------------------------------------------------------- #
C += [
md(r"""
## Paso 3 · Análisis por categoría

¿Qué categoría mueve más dinero? ¿Cuál tiene mayor variabilidad de precios?
"""),

code(r"""
# Estadísticas completas por categoría
resumen_cat = (
    df.groupby("categoria")["monto"]
      .agg(
          total="sum",
          promedio="mean",
          mediana=lambda x: x.median(),
          variabilidad="std",
          n="count"
      )
      .round(0)
      .reset_index()
      .sort_values("total", ascending=False)
      .reset_index(drop=True)
)
print("Resumen por categoría:")
print(resumen_cat.to_string(index=False))
"""),

code(r"""
# ¿Qué categoría tiene mayor variabilidad?
cat_max_var = resumen_cat.loc[resumen_cat["variabilidad"].idxmax(), "categoria"]
print("Categoría con mayor variabilidad de precios:", cat_max_var)
print("Std:", resumen_cat.loc[resumen_cat["variabilidad"].idxmax(), "variabilidad"])
"""),

code(r"""
# Boxplot de montos por categoría
fig, ax = plt.subplots(figsize=(10, 5))
categorias = df["categoria"].unique()
datos_box = [df[df["categoria"] == c]["monto"].values for c in sorted(categorias)]
ax.boxplot(datos_box, labels=sorted(categorias), vert=True)
ax.set_title("Distribución de montos por categoría")
ax.set_ylabel("Monto (COP)")
ax.set_xlabel("Categoría")
plt.tight_layout()
plt.show()
"""),
]


# --------------------------------------------------------------------------- #
# SECCIÓN 4: Análisis por método de pago
# --------------------------------------------------------------------------- #
C += [
md(r"""
## Paso 4 · Análisis por método de pago

¿Cómo se comparan los métodos en volumen e importe?
"""),

code(r"""
# Número de transacciones y total por método
metodo_res = (
    df.groupby("metodo_pago")["monto"]
      .agg(n="count", total="sum", promedio="mean")
      .round({"promedio": 0})
      .reset_index()
      .sort_values("total", ascending=False)
)
print("Análisis por método de pago:")
print(metodo_res.to_string(index=False))
"""),

code(r"""
# Pivot: ciudad × método de pago (para ver qué combina más)
pivot_metodo = pd.pivot_table(
    df,
    values="monto",
    index="ciudad",
    columns="metodo_pago",
    aggfunc="sum",
    fill_value=0,
)
print("Ventas por ciudad y método de pago (COP):")
print(pivot_metodo)
"""),
]


# --------------------------------------------------------------------------- #
# SECCIÓN 5: Análisis temporal
# --------------------------------------------------------------------------- #
C += [
md(r"""
## Paso 5 · Análisis temporal

Vemos cómo evolucionan las ventas a lo largo del tiempo.
"""),

code(r"""
# Extraer mes y agrupar
df["mes"] = df["fecha"].dt.month
df["mes_str"] = df["fecha"].dt.to_period("M").astype(str)

ventas_mes = (
    df.groupby("mes_str")["monto"]
      .agg(total="sum", n="count")
      .reset_index()
      .sort_values("mes_str")
)
print("Ventas por mes:")
print(ventas_mes.to_string(index=False))
"""),

code(r"""
# Ventas acumuladas en el tiempo
df_sorted = df.sort_values("fecha").reset_index(drop=True)
df_sorted["acumulado"] = df_sorted["monto"].cumsum()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df_sorted.index, df_sorted["acumulado"], color="darkgreen", linewidth=1.5)
ax.fill_between(df_sorted.index, df_sorted["acumulado"], alpha=0.1, color="darkgreen")
ax.set_title("Ventas acumuladas en el tiempo")
ax.set_xlabel("Número de transacción (ordenada por fecha)")
ax.set_ylabel("Monto acumulado (COP)")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: "{:,.0f}".format(x)))
plt.tight_layout()
plt.show()
"""),
]


# --------------------------------------------------------------------------- #
# SECCIÓN 6: TU TURNO
# --------------------------------------------------------------------------- #
C += [
md(r"""
---
## Tu turno

Ahora resuelve tú estas tres tareas usando pandas.
"""),

md(r"""
### Tarea A · Top 3 categorías por ciudad

Completa `top_categorias_ciudad(df, ciudad, n=3)` que devuelva un DataFrame
con las `n` categorías con mayor suma de monto en la ciudad indicada.
El resultado debe tener columnas `"categoria"` y `"total"`, ordenado de mayor a menor.
"""),

code(r"""
def top_categorias_ciudad(df, ciudad, n=3):
    # ✏️ TU CÓDIGO AQUÍ
    return None

# Comprobación
res_bta = top_categorias_ciudad(df, "Bogota", 3)
revisar("devuelve DataFrame", res_bta is not None and hasattr(res_bta, 'columns'))
revisar("3 filas", res_bta is not None and len(res_bta) == 3)
revisar("tiene col categoria", res_bta is not None and "categoria" in res_bta.columns)
revisar("tiene col total", res_bta is not None and "total" in res_bta.columns)
revisar("ordenado desc", res_bta is not None and res_bta.iloc[0]["total"] >= res_bta.iloc[-1]["total"])
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def top_categorias_ciudad(df, ciudad, n=3):
    return (
        df[df["ciudad"] == ciudad]
          .groupby("categoria")["monto"]
          .sum()
          .reset_index()
          .rename(columns={"monto": "total"})
          .sort_values("total", ascending=False)
          .head(n)
          .reset_index(drop=True)
    )
```
Primero filtramos por ciudad, luego groupby por categoría, luego ordenamos y
tomamos los top n.
</details>
"""),

md(r"""
### Tarea B · Mediana por método de pago

Completa `medianas_metodo(df)` que devuelva una Series con la mediana de monto
para cada método de pago, ordenada de mayor a menor.
"""),

code(r"""
def medianas_metodo(df):
    # ✏️ TU CÓDIGO AQUÍ
    return None

medianas = medianas_metodo(df)
revisar("es Series", medianas is not None and hasattr(medianas, 'index'))
revisar("3 valores", medianas is not None and len(medianas) == 3)
revisar("ordenado desc", medianas is not None and medianas.iloc[0] >= medianas.iloc[-1])
revisar("valores positivos", medianas is not None and (medianas > 0).all())
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def medianas_metodo(df):
    return (
        df.groupby("metodo_pago")["monto"]
          .median()
          .sort_values(ascending=False)
    )
```
`median()` calcula la mediana (valor central) para cada grupo.
</details>
"""),

md(r"""
### Tarea C · Exportar resumen a CSV

Completa `exportar_resumen(df, ruta_salida)` que:
1. Calcule el resumen por ciudad: total, promedio, n_transacciones.
2. Exporte el resultado a `ruta_salida` como CSV (sin índice).
3. Devuelva el número de filas escritas.
"""),

code(r"""
def exportar_resumen(df, ruta_salida):
    # ✏️ TU CÓDIGO AQUÍ
    return None

import tempfile, os
with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
    ruta_tmp = f.name

n = exportar_resumen(df, ruta_tmp)
revisar("devuelve 5 (5 ciudades)", n == 5)
# Verificar que el archivo fue creado y tiene contenido
df_leido = pd.read_csv(ruta_tmp)
revisar("archivo tiene 5 filas", len(df_leido) == 5)
revisar("tiene columna ciudad", "ciudad" in df_leido.columns)
os.unlink(ruta_tmp)  # limpiar archivo temporal
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def exportar_resumen(df, ruta_salida):
    resumen = (
        df.groupby("ciudad")["monto"]
          .agg(total="sum", promedio="mean", n_transacciones="count")
          .reset_index()
    )
    resumen.to_csv(ruta_salida, index=False)
    return len(resumen)
```
`to_csv(index=False)` exporta sin la columna de índice. Devolvemos `len(resumen)`
que coincide con el número de filas (una por ciudad).
</details>
"""),
]


C += [
md(r"""
---
## Reflexión final

En esta práctica aplicamos el flujo completo de análisis de datos con pandas:

```
1. Carga (pd.read_csv)
       │
       ▼
2. Inspección (head, info, describe, value_counts)
       │
       ▼
3. Análisis por dimensión (groupby + agg)
       │
       ▼
4. Análisis temporal (dt.month, cumsum)
       │
       ▼
5. Visualización (matplotlib)
       │
       ▼
6. Exportar (to_csv)
```

Este es el flujo que usarás en prácticamente cualquier proyecto de ciencia de
datos. Lo que cambia es la profundidad de cada paso.

Compara con la Clase 1, donde hicimos algo similar con Python puro y bucles.
¿Cuánto código ahorramos? ¿Cuánto más rápido es pandas para datasets grandes?

Continúa con **homework01.ipynb** para ejercicios con autocalificación.
"""),
]


# ===================================================================== #
# VALIDACIÓN EN TIEMPO DE CONSTRUCCIÓN
# ===================================================================== #
def _validar():
    import pandas as pd
    import numpy as np

    ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "datasets", "transacciones.csv")
    df = pd.read_csv(os.path.abspath(ruta), parse_dates=["fecha"])

    def top_categorias_ciudad(df, ciudad, n=3):
        return (
            df[df["ciudad"] == ciudad]
              .groupby("categoria")["monto"]
              .sum()
              .reset_index()
              .rename(columns={"monto": "total"})
              .sort_values("total", ascending=False)
              .head(n)
              .reset_index(drop=True)
        )
    res_bta = top_categorias_ciudad(df, "Bogota", 3)
    assert len(res_bta) == 3
    assert "categoria" in res_bta.columns
    assert "total" in res_bta.columns
    assert res_bta.iloc[0]["total"] >= res_bta.iloc[-1]["total"]

    def medianas_metodo(df):
        return df.groupby("metodo_pago")["monto"].median().sort_values(ascending=False)
    medianas = medianas_metodo(df)
    assert len(medianas) == 3
    assert medianas.iloc[0] >= medianas.iloc[-1]
    assert (medianas > 0).all()

    def exportar_resumen(df, ruta_salida):
        resumen = (
            df.groupby("ciudad")["monto"]
              .agg(total="sum", promedio="mean", n_transacciones="count")
              .reset_index()
        )
        resumen.to_csv(ruta_salida, index=False)
        return len(resumen)

    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        ruta_tmp = f.name
    n = exportar_resumen(df, ruta_tmp)
    assert n == 5
    df_leido = pd.read_csv(ruta_tmp)
    assert len(df_leido) == 5
    assert "ciudad" in df_leido.columns
    os.unlink(ruta_tmp)

    print("Todas las soluciones de referencia de practice02 pasan sus pruebas.")

_validar()


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase06", "practice02.ipynb")
build(os.path.abspath(ruta), C)
