"""Construye curso/clase06/practice01.ipynb — 10 ejercicios graduales de pandas.

Patrón por ejercicio:
  1. Markdown con enunciado + ejemplo.
  2. Celda plantilla (el estudiante escribe aquí).
  3. Celda de comprobación SUAVE (revisar()).
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
# Clase 6 · Práctica 01 — 10 ejercicios graduales de pandas

### Series, DataFrames, filtrado, groupby y más

Estos 10 ejercicios van **de menor a mayor dificultad**. Para cada uno:

1. Lee el enunciado y el ejemplo.
2. Escribe tu solución en la celda que dice `# ✏️ TU CÓDIGO AQUÍ`.
3. Ejecuta la celda de **comprobación**: verás ✅ o ❌ por cada caso.
4. ¿Atascado? Despliega **💡 Ver solución** al final de cada ejercicio.

> 🗂️ Todos los ejercicios usan el dataset `transacciones.csv` con columnas:
> `id`, `fecha`, `ciudad`, `categoria`, `metodo_pago`, `monto`.

> ⚙️ Las comprobaciones son *suaves*: si tu función aún no está lista, verás ❌
> pero el notebook seguirá ejecutándose sin romperse.
"""),

code(r"""
import os, sys
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar

# Cargar el dataset una sola vez para todos los ejercicios
ruta = os.path.join("..", "datasets", "transacciones.csv")
df = pd.read_csv(ruta, parse_dates=["fecha"])
print("Dataset cargado:", df.shape, "| columnas:", df.columns.tolist())
print(df.head(3))
"""),
]


# --------------------------------------------------------------------------- #
# Helper para definir cada ejercicio
# --------------------------------------------------------------------------- #
def ejercicio(numero, titulo, enunciado_md, plantilla, check_code, solucion_md):
    C.append(md("## Ejercicio {0} · {1}\n\n{2}".format(numero, titulo, enunciado_md)))
    C.append(code(plantilla))
    C.append(code(check_code))
    C.append(md(solucion_md))


# ---- 1 -------------------------------------------------------------------- #
ejercicio(
    1, "Estadísticas básicas del dataset",
    r"""Escribe `estadisticas_basicas(df)` que devuelva un **diccionario** con:
- `"n_filas"`: número de filas
- `"n_columnas"`: número de columnas
- `"monto_total"`: suma total de la columna `monto`
- `"monto_promedio"`: promedio de `monto` (redondeado a 2 decimales)

**Ejemplo:** el resultado será un dict con 4 claves.""",
    r"""
def estadisticas_basicas(df):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
result = estadisticas_basicas(df)
revisar("tiene 4 claves", isinstance(result, dict) and len(result) == 4)
revisar("n_filas == 120", result is not None and result.get("n_filas") == 120)
revisar("n_columnas == 6", result is not None and result.get("n_columnas") == 6)
revisar("monto_total > 0", result is not None and result.get("monto_total", 0) > 0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def estadisticas_basicas(df):
    return {
        "n_filas": df.shape[0],
        "n_columnas": df.shape[1],
        "monto_total": df["monto"].sum(),
        "monto_promedio": round(df["monto"].mean(), 2),
    }
```
`df.shape` devuelve `(filas, columnas)`. `df["monto"].sum()` suma toda la columna.
</details>
""",
)

# ---- 2 -------------------------------------------------------------------- #
ejercicio(
    2, "Filtrar transacciones de una ciudad",
    r"""Escribe `filtrar_ciudad(df, ciudad)` que devuelva un **DataFrame** con
solo las filas donde `ciudad` coincide con el parámetro dado.

**Ejemplo:** `filtrar_ciudad(df, "Bogota")` devuelve todas las filas de Bogota.""",
    r"""
def filtrar_ciudad(df, ciudad):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
bta = filtrar_ciudad(df, "Bogota")
med = filtrar_ciudad(df, "Medellin")
revisar("devuelve DataFrame", bta is not None and hasattr(bta, 'shape'))
revisar("solo Bogota", bta is not None and (bta["ciudad"] == "Bogota").all())
revisar("solo Medellin", med is not None and (med["ciudad"] == "Medellin").all())
revisar("Bogota > 0 filas", bta is not None and len(bta) > 0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def filtrar_ciudad(df, ciudad):
    return df[df["ciudad"] == ciudad]
```
Creamos una máscara booleana `df["ciudad"] == ciudad` y la aplicamos como índice.
</details>
""",
)

# ---- 3 -------------------------------------------------------------------- #
ejercicio(
    3, "Total e ingreso promedio por ciudad (groupby)",
    r"""Escribe `resumen_por_ciudad(df)` que devuelva un **DataFrame** con:
- columna `"ciudad"` (como columna, no como índice)
- columna `"total"`: suma de montos por ciudad
- columna `"promedio"`: promedio de montos por ciudad (redondeado a 2 decimales)
- ordenado de mayor a menor `"total"`

**Ejemplo:** la primera fila será la ciudad con más ventas totales.""",
    r"""
def resumen_por_ciudad(df):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
res = resumen_por_ciudad(df)
revisar("es DataFrame", res is not None and hasattr(res, 'columns'))
revisar("tiene col ciudad", res is not None and "ciudad" in res.columns)
revisar("tiene col total", res is not None and "total" in res.columns)
revisar("tiene col promedio", res is not None and "promedio" in res.columns)
revisar("5 ciudades", res is not None and len(res) == 5)
revisar("ordenado desc", res is not None and res.iloc[0]["total"] >= res.iloc[-1]["total"])
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def resumen_por_ciudad(df):
    return (
        df.groupby("ciudad")["monto"]
          .agg(total="sum", promedio="mean")
          .round({"promedio": 2})
          .reset_index()
          .sort_values("total", ascending=False)
          .reset_index(drop=True)
    )
```
`agg` calcula ambas métricas en un solo groupby. `reset_index()` convierte
ciudad de índice a columna. El segundo `reset_index(drop=True)` limpia el índice
tras el sort.
</details>
""",
)

# ---- 4 -------------------------------------------------------------------- #
ejercicio(
    4, "Crear columna monto_usd con conversión de tasa",
    r"""Escribe `agregar_monto_usd(df, tasa)` que devuelva una **copia** del
DataFrame con una nueva columna `"monto_usd"` = `monto / tasa`, redondeada
a 2 decimales. El DataFrame original no debe modificarse.

**Ejemplo:** `agregar_monto_usd(df, 4100)` agrega la columna en dólares.""",
    r"""
def agregar_monto_usd(df, tasa):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
df_usd = agregar_monto_usd(df, 4100)
revisar("devuelve DataFrame", df_usd is not None and hasattr(df_usd, 'columns'))
revisar("tiene monto_usd", df_usd is not None and "monto_usd" in df_usd.columns)
revisar("original sin monto_usd", "monto_usd" not in df.columns)
revisar("primera fila correcta", df_usd is not None and abs(df_usd.iloc[0]["monto_usd"] - round(df.iloc[0]["monto"] / 4100, 2)) < 0.01)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def agregar_monto_usd(df, tasa):
    copia = df.copy()
    copia["monto_usd"] = (copia["monto"] / tasa).round(2)
    return copia
```
Usamos `.copy()` para no modificar el DataFrame original (evita SettingWithCopyWarning).
La división vectorizada opera sobre toda la columna a la vez.
</details>
""",
)

# ---- 5 -------------------------------------------------------------------- #
ejercicio(
    5, "Top N transacciones más grandes",
    r"""Escribe `top_transacciones(df, n)` que devuelva un **DataFrame** con
las `n` filas con mayor `monto`, ordenadas de mayor a menor.

**Ejemplo:** `top_transacciones(df, 5)` devuelve las 5 transacciones más grandes.""",
    r"""
def top_transacciones(df, n):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
top5 = top_transacciones(df, 5)
top1 = top_transacciones(df, 1)
revisar("devuelve 5 filas", top5 is not None and len(top5) == 5)
revisar("devuelve 1 fila", top1 is not None and len(top1) == 1)
revisar("ordenado desc", top5 is not None and top5.iloc[0]["monto"] >= top5.iloc[-1]["monto"])
revisar("primera fila es el max", top1 is not None and top1.iloc[0]["monto"] == df["monto"].max())
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def top_transacciones(df, n):
    return df.sort_values("monto", ascending=False).head(n).reset_index(drop=True)
```
`sort_values` ordena de mayor a menor. `head(n)` toma las primeras n filas.
`reset_index(drop=True)` limpia el índice para que empiece en 0.
</details>
""",
)

# ---- 6 -------------------------------------------------------------------- #
ejercicio(
    6, "Contar transacciones por método de pago",
    r"""Escribe `conteo_metodo_pago(df)` que devuelva un **diccionario**
`{metodo: cantidad}` con el número de transacciones por cada método de pago.

**Ejemplo:** `{"efectivo": N1, "tarjeta": N2, "transferencia": N3}`.""",
    r"""
def conteo_metodo_pago(df):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
conteo = conteo_metodo_pago(df)
revisar("es dict", isinstance(conteo, dict))
revisar("3 métodos", conteo is not None and len(conteo) == 3)
revisar("tiene efectivo", conteo is not None and "efectivo" in conteo)
revisar("total == 120", conteo is not None and sum(conteo.values()) == 120)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def conteo_metodo_pago(df):
    return df["metodo_pago"].value_counts().to_dict()
```
`value_counts()` cuenta frecuencias. `.to_dict()` convierte la Series a dict.
También se puede usar: `df.groupby("metodo_pago").size().to_dict()`
</details>
""",
)

# ---- 7 -------------------------------------------------------------------- #
ejercicio(
    7, "Ticket promedio por categoría",
    r"""Escribe `ticket_promedio_categoria(df)` que devuelva una **Series** con
el ticket promedio (media de monto) por categoría, redondeado a 2 decimales,
ordenado de mayor a menor.

**Ejemplo:** la categoría con mayor ticket aparece primero.""",
    r"""
def ticket_promedio_categoria(df):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
ticket = ticket_promedio_categoria(df)
revisar("es Series", ticket is not None and hasattr(ticket, 'index'))
revisar("5 categorias", ticket is not None and len(ticket) == 5)
revisar("ordenado desc", ticket is not None and ticket.iloc[0] >= ticket.iloc[-1])
# verificar que el valor es razonable
revisar("valores positivos", ticket is not None and (ticket > 0).all())
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def ticket_promedio_categoria(df):
    return (
        df.groupby("categoria")["monto"]
          .mean()
          .round(2)
          .sort_values(ascending=False)
    )
```
`groupby` + `mean()` calcula el promedio por categoría. `sort_values(ascending=False)`
ordena de mayor a menor.
</details>
""",
)

# ---- 8 -------------------------------------------------------------------- #
ejercicio(
    8, "Detectar y contar filas con nulos",
    r"""Escribe `contar_nulos(df)` que devuelva un **diccionario** `{columna: n_nulos}`
con el conteo de nulos por columna. Solo incluye las columnas que tienen al menos
un nulo. Si no hay nulos, devuelve `{}`.

**Nota:** el dataset real no tiene nulos, así que crearemos un df de prueba en
la comprobación.""",
    r"""
def contar_nulos(df):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
import numpy as np
df_test = pd.DataFrame({
    "a": [1, None, 3],
    "b": [4, 5, 6],
    "c": [None, None, 9],
})
result = contar_nulos(df_test)
revisar("es dict", isinstance(result, dict))
revisar("no incluye b (sin nulos)", result is not None and "b" not in result)
revisar("a tiene 1 nulo", result is not None and result.get("a") == 1)
revisar("c tiene 2 nulos", result is not None and result.get("c") == 2)
revisar("sin nulos devuelve {}", contar_nulos(df) == {})
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def contar_nulos(df):
    nulos = df.isna().sum()
    return nulos[nulos > 0].to_dict()
```
`df.isna().sum()` cuenta nulos por columna. Filtramos los que son > 0 y
convertimos a dict.
</details>
""",
)

# ---- 9 -------------------------------------------------------------------- #
ejercicio(
    9, "Merge de transacciones con tabla de regiones",
    r"""Escribe `enriquecer_con_region(df, regiones)` que haga un **left join**
entre `df` y `regiones` (que tiene columnas `"ciudad"` y `"region"`) usando
la columna `"ciudad"` como clave. Devuelve el DataFrame enriquecido.

**Ejemplo:** el resultado tiene todas las columnas de `df` más la columna `"region"`.""",
    r"""
def enriquecer_con_region(df, regiones):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
regiones = pd.DataFrame({
    "ciudad":  ["Bogota", "Medellin", "Cali", "Barranquilla", "Bucaramanga"],
    "region":  ["Centro", "Andina",   "Pacifica", "Caribe",   "Andina"],
})
df_enrich = enriquecer_con_region(df, regiones)
revisar("devuelve DataFrame", df_enrich is not None and hasattr(df_enrich, 'columns'))
revisar("tiene columna region", df_enrich is not None and "region" in df_enrich.columns)
revisar("mismas filas que df", df_enrich is not None and len(df_enrich) == len(df))
revisar("Bogota=Centro", df_enrich is not None and (df_enrich[df_enrich["ciudad"]=="Bogota"]["region"] == "Centro").all())
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def enriquecer_con_region(df, regiones):
    return df.merge(regiones, on="ciudad", how="left")
```
`how="left"` garantiza que todas las filas de `df` se conservan aunque no tengan
correspondencia en `regiones` (en ese caso `region` sería NaN).
</details>
""",
)

# ---- 10 ------------------------------------------------------------------- #
ejercicio(
    10, "Pivot table: ciudad × metodo_pago con suma de monto",
    r"""Escribe `pivot_ciudad_metodo(df)` que devuelva una **pivot table** donde:
- Las filas son las ciudades.
- Las columnas son los métodos de pago.
- Los valores son la **suma de montos**.
- Los NaN se reemplazan por 0.

Usa `pd.pivot_table`.""",
    r"""
def pivot_ciudad_metodo(df):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
pivot = pivot_ciudad_metodo(df)
revisar("devuelve DataFrame", pivot is not None and hasattr(pivot, 'columns'))
revisar("3 columnas de metodo", pivot is not None and len(pivot.columns) == 3)
revisar("5 ciudades como filas", pivot is not None and len(pivot) == 5)
revisar("sin NaN", pivot is not None and not pivot.isna().any().any())
revisar("columna efectivo existe", pivot is not None and "efectivo" in pivot.columns)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def pivot_ciudad_metodo(df):
    return pd.pivot_table(
        df,
        values="monto",
        index="ciudad",
        columns="metodo_pago",
        aggfunc="sum",
        fill_value=0,
    )
```
`pd.pivot_table` hace un groupby bidimensional. `fill_value=0` reemplaza NaN
(combinaciones ciudad-método sin transacciones) con 0.
</details>
""",
)

C.append(md(r"""
---
## ¡Terminaste la práctica 01!

Si todas tus comprobaciones muestran ✅, dominas el toolkit esencial de pandas:

| Ejercicio | Concepto |
|---|---|
| 1 | Inspección: `shape`, `sum`, `mean` |
| 2 | Filtrado booleano |
| 3 | `groupby` + `agg` + `reset_index` |
| 4 | Crear columnas vectorizadas |
| 5 | `sort_values` + `head` |
| 6 | `value_counts` + `to_dict` |
| 7 | `groupby` + `mean` + `sort_values` |
| 8 | `isna()` + `sum()` |
| 9 | `merge` (left join) |
| 10 | `pd.pivot_table` |

Continúa con **practice02.ipynb** para un análisis completo del dataset.
"""))


# ===================================================================== #
# VALIDACIÓN EN TIEMPO DE CONSTRUCCIÓN
# ===================================================================== #
def _validar():
    import csv
    import pandas as pd
    import numpy as np

    ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "datasets", "transacciones.csv")
    df = pd.read_csv(os.path.abspath(ruta), parse_dates=["fecha"])

    def estadisticas_basicas(df):
        return {
            "n_filas": df.shape[0],
            "n_columnas": df.shape[1],
            "monto_total": df["monto"].sum(),
            "monto_promedio": round(df["monto"].mean(), 2),
        }
    r = estadisticas_basicas(df)
    assert r["n_filas"] == 120
    assert r["n_columnas"] == 6
    assert r["monto_total"] > 0

    def filtrar_ciudad(df, ciudad):
        return df[df["ciudad"] == ciudad]
    bta = filtrar_ciudad(df, "Bogota")
    assert (bta["ciudad"] == "Bogota").all()
    assert len(bta) > 0

    def resumen_por_ciudad(df):
        return (
            df.groupby("ciudad")["monto"]
              .agg(total="sum", promedio="mean")
              .round({"promedio": 2})
              .reset_index()
              .sort_values("total", ascending=False)
              .reset_index(drop=True)
        )
    res = resumen_por_ciudad(df)
    assert len(res) == 5
    assert "ciudad" in res.columns
    assert res.iloc[0]["total"] >= res.iloc[-1]["total"]

    def agregar_monto_usd(df, tasa):
        copia = df.copy()
        copia["monto_usd"] = (copia["monto"] / tasa).round(2)
        return copia
    df_usd = agregar_monto_usd(df, 4100)
    assert "monto_usd" in df_usd.columns
    assert "monto_usd" not in df.columns
    assert abs(df_usd.iloc[0]["monto_usd"] - round(df.iloc[0]["monto"] / 4100, 2)) < 0.01

    def top_transacciones(df, n):
        return df.sort_values("monto", ascending=False).head(n).reset_index(drop=True)
    top5 = top_transacciones(df, 5)
    assert len(top5) == 5
    assert top5.iloc[0]["monto"] == df["monto"].max()

    def conteo_metodo_pago(df):
        return df["metodo_pago"].value_counts().to_dict()
    conteo = conteo_metodo_pago(df)
    assert len(conteo) == 3
    assert sum(conteo.values()) == 120

    def ticket_promedio_categoria(df):
        return df.groupby("categoria")["monto"].mean().round(2).sort_values(ascending=False)
    ticket = ticket_promedio_categoria(df)
    assert len(ticket) == 5
    assert ticket.iloc[0] >= ticket.iloc[-1]

    def contar_nulos(df):
        nulos = df.isna().sum()
        return nulos[nulos > 0].to_dict()
    df_test = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, 6], "c": [None, None, 9]})
    result = contar_nulos(df_test)
    assert result.get("a") == 1
    assert result.get("c") == 2
    assert "b" not in result
    assert contar_nulos(df) == {}

    def enriquecer_con_region(df, regiones):
        return df.merge(regiones, on="ciudad", how="left")
    regiones = pd.DataFrame({
        "ciudad":  ["Bogota", "Medellin", "Cali", "Barranquilla", "Bucaramanga"],
        "region":  ["Centro", "Andina",   "Pacifica", "Caribe",   "Andina"],
    })
    df_enrich = enriquecer_con_region(df, regiones)
    assert "region" in df_enrich.columns
    assert len(df_enrich) == len(df)
    assert (df_enrich[df_enrich["ciudad"] == "Bogota"]["region"] == "Centro").all()

    def pivot_ciudad_metodo(df):
        return pd.pivot_table(df, values="monto", index="ciudad",
                              columns="metodo_pago", aggfunc="sum", fill_value=0)
    pivot = pivot_ciudad_metodo(df)
    assert len(pivot.columns) == 3
    assert len(pivot) == 5
    assert not pivot.isna().any().any()

    print("Todas las soluciones de referencia de practice01 pasan sus pruebas.")

_validar()


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase06", "practice01.ipynb")
build(os.path.abspath(ruta), C)
