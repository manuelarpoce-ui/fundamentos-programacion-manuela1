"""Construye curso/clase08/practice01.ipynb — 10 ejercicios del proyecto integrador.

Cada ejercicio sigue el patrón:
  1. Markdown con enunciado + ejemplo.
  2. Celda plantilla (el estudiante escribe aquí).
  3. Celda de comprobación suave (revisar()).
  4. Markdown <details> con solución comentada.

Las soluciones se validan en tiempo de construcción con _validar().
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
# Clase 8 · Práctica 01 — 10 ejercicios del proyecto integrador

### Proyecto integrador de ciencia de datos

Estos 10 ejercicios construyen un pipeline completo sobre el dataset de
transacciones. Para cada uno:

1. Lee el enunciado y el ejemplo.
2. Implementa la función en la celda `# ✏️ TU CÓDIGO AQUÍ`.
3. Ejecuta la comprobación: verás ✅ o ❌.
4. ¿Atascado? Despliega **💡 Ver solución**.

> 🎯 El objetivo no es solo "pasar los tests" sino construir funciones reutilizables
> que, encadenadas, forman un mini-pipeline de análisis.
"""),

code(r"""
# Bootstrap: cargamos el dataset y la utilidad de comprobación.
import os, sys
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar

ruta = os.path.join("..", "datasets", "transacciones.csv")
df_raw = pd.read_csv(ruta)
print("Dataset cargado:", df_raw.shape)
print(df_raw.head(3).to_string(index=False))
"""),
]


# --------------------------------------------------------------------------- #
# Helper para construir las celdas de cada ejercicio
# --------------------------------------------------------------------------- #
def ejercicio(numero, titulo, enunciado_md, plantilla, check_code, solucion_md):
    C.append(md("## Ejercicio {} · {}\n\n{}".format(numero, titulo, enunciado_md)))
    C.append(code(plantilla))
    C.append(code(check_code))
    C.append(md(solucion_md))


# ---- 1 --------------------------------------------------------------------
ejercicio(
    1, "Pipeline carga_limpia(ruta_csv)",
    r"""Implementa `carga_limpia(ruta_csv)` que:
1. Cargue el CSV con `pd.read_csv`.
2. Convierta `fecha` a `datetime`.
3. Elimine filas con valores nulos en cualquier columna.
4. Elimine filas con `monto <= 0`.
5. Devuelva el DataFrame limpio.

**Ejemplo:** `carga_limpia("../datasets/transacciones.csv")` → DataFrame con columna
`fecha` de tipo `datetime64`.
""",
    r"""
def carga_limpia(ruta_csv):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
df_limpio = carga_limpia("../datasets/transacciones.csv")
revisar("devuelve DataFrame", isinstance(df_limpio, pd.DataFrame))
revisar("fecha es datetime", pd.api.types.is_datetime64_any_dtype(df_limpio["fecha"]))
revisar("sin nulos", df_limpio.isnull().sum().sum() == 0)
revisar("monto > 0", (df_limpio["monto"] > 0).all())
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def carga_limpia(ruta_csv):
    df = pd.read_csv(ruta_csv)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.dropna()
    df = df[df["monto"] > 0]
    return df.reset_index(drop=True)
```
</details>
""",
)

# ---- 2 --------------------------------------------------------------------
ejercicio(
    2, "resumen_ejecutivo(df)",
    r"""Implementa `resumen_ejecutivo(df)` que devuelva un **diccionario** con:

- `"total_ventas"`: suma de todos los montos.
- `"ticket_promedio"`: media de los montos.
- `"ticket_mediano"`: mediana de los montos.
- `"n_transacciones"`: número de filas.
- `"ciudad_lider"`: ciudad con mayor suma de montos.

**Ejemplo:** el dict debe incluir la clave `"ciudad_lider"` con el nombre de la
ciudad de mayor volumen.
""",
    r"""
def resumen_ejecutivo(df):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
df_limpio = carga_limpia("../datasets/transacciones.csv")
res = resumen_ejecutivo(df_limpio)
revisar("es dict", isinstance(res, dict))
revisar("tiene total_ventas", "total_ventas" in res)
revisar("total_ventas > 0", res.get("total_ventas", 0) > 0)
revisar("tiene ciudad_lider", "ciudad_lider" in res)
revisar("n_transacciones correcto", res.get("n_transacciones") == len(df_limpio))
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def resumen_ejecutivo(df):
    return {
        "total_ventas":    df["monto"].sum(),
        "ticket_promedio": df["monto"].mean(),
        "ticket_mediano":  df["monto"].median(),
        "n_transacciones": len(df),
        "ciudad_lider":    df.groupby("ciudad")["monto"].sum().idxmax(),
    }
```
</details>
""",
)

# ---- 3 --------------------------------------------------------------------
ejercicio(
    3, "Pipeline de transformación: normalizar y segmentar",
    r"""Implementa `transformar(df)` que agregue al DataFrame estas columnas:

- `"monto_norm"`: normalización min-max del monto → rango [0, 1].
- `"segmento"`: `"bajo"` si monto < 100 000, `"medio"` si < 300 000, `"alto"` si >= 300 000.
- `"mes"`: mes numérico extraído de `fecha`.

Devuelve el DataFrame enriquecido (puede modificar o copiar, lo que prefieras).

**Ejemplo:** `transformar(df).columns` debe contener `"monto_norm"`, `"segmento"` y `"mes"`.
""",
    r"""
def transformar(df):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
df_limpio = carga_limpia("../datasets/transacciones.csv")
df_t = transformar(df_limpio)
revisar("tiene monto_norm", "monto_norm" in df_t.columns)
revisar("monto_norm en [0,1]", df_t["monto_norm"].between(0, 1).all())
revisar("tiene segmento", "segmento" in df_t.columns)
revisar("segmento valores validos", df_t["segmento"].isin(["bajo","medio","alto"]).all())
revisar("tiene mes", "mes" in df_t.columns)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def transformar(df):
    df = df.copy()
    m_min, m_max = df["monto"].min(), df["monto"].max()
    df["monto_norm"] = (df["monto"] - m_min) / (m_max - m_min)

    def segmentar(m):
        if m < 100_000:
            return "bajo"
        elif m < 300_000:
            return "medio"
        else:
            return "alto"

    df["segmento"] = df["monto"].apply(segmentar)
    df["mes"] = pd.to_datetime(df["fecha"]).dt.month
    return df
```
</details>
""",
)

# ---- 4 --------------------------------------------------------------------
ejercicio(
    4, "Análisis de cohortes: métricas por mes",
    r"""Implementa `cohortes_mensuales(df)` que devuelva un DataFrame con índice `mes`
y columnas:

- `"n"`: número de transacciones en ese mes.
- `"total"`: suma de montos.
- `"promedio"`: media de montos.

Ordena el resultado por mes ascendente.

**Ejemplo:** el resultado debe tener tantas filas como meses distintos hay en el dataset.
""",
    r"""
def cohortes_mensuales(df):
    # ✏️ TU CÓDIGO AQUÍ (pista: groupby + agg, asegúrate de que 'mes' exista)
    return None
""",
    r"""
df_limpio = carga_limpia("../datasets/transacciones.csv")
df_t = transformar(df_limpio)
coh = cohortes_mensuales(df_t)
revisar("es DataFrame", isinstance(coh, pd.DataFrame))
revisar("tiene columna 'n'", "n" in coh.columns)
revisar("tiene columna 'total'", "total" in coh.columns)
revisar("tiene columna 'promedio'", "promedio" in coh.columns)
revisar("ordenado por mes", coh.index.is_monotonic_increasing)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def cohortes_mensuales(df):
    return (
        df.groupby("mes")["monto"]
        .agg(n="count", total="sum", promedio="mean")
        .sort_index()
    )
```
Si el DataFrame no tiene columna `mes`, agrégala primero:
```python
df["mes"] = pd.to_datetime(df["fecha"]).dt.month
```
</details>
""",
)

# ---- 5 --------------------------------------------------------------------
ejercicio(
    5, "Detectar anomalías: outliers por IQR",
    r"""Implementa `detectar_anomalias(df, columna="monto")` que devuelva un DataFrame
con **solo las filas anómalas**, usando la regla de Tukey:

```
Q1 = percentil 25
Q3 = percentil 75
limite_sup = Q3 + 1.5 * IQR
limite_inf = Q1 - 1.5 * IQR
Anomalía: valor < limite_inf  OR  valor > limite_sup
```

**Ejemplo:** `len(detectar_anomalias(df))` debería ser mayor que 0 en nuestro dataset.
""",
    r"""
def detectar_anomalias(df, columna="monto"):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
df_limpio = carga_limpia("../datasets/transacciones.csv")
anomalias = detectar_anomalias(df_limpio)
revisar("es DataFrame", isinstance(anomalias, pd.DataFrame))
revisar("hay anomalias", len(anomalias) > 0)
revisar("anomalias son subset del df", anomalias.index.isin(df_limpio.index).all())
# Verificar que todos los valores detectados realmente son outliers por IQR
Q1 = df_limpio["monto"].quantile(0.25)
Q3 = df_limpio["monto"].quantile(0.75)
IQR = Q3 - Q1
lim_sup = Q3 + 1.5 * IQR
lim_inf = Q1 - 1.5 * IQR
mask = (df_limpio["monto"] > lim_sup) | (df_limpio["monto"] < lim_inf)
revisar("detecta exactamente los outliers IQR", len(anomalias) == mask.sum())
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def detectar_anomalias(df, columna="monto"):
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1
    lim_sup = Q3 + 1.5 * IQR
    lim_inf = Q1 - 1.5 * IQR
    mask = (df[columna] > lim_sup) | (df[columna] < lim_inf)
    return df[mask].copy()
```
</details>
""",
)

# ---- 6 --------------------------------------------------------------------
ejercicio(
    6, "Valor de vida del cliente aproximado (LTV por ciudad)",
    r"""Implementa `ltv_por_ciudad(df)` que devuelva una Series de pandas con índice
`ciudad` y valores igual al **promedio de monto** por ciudad, ordenada de mayor a menor.

En este contexto simplificado, el LTV (Lifetime Value) aproximado por ciudad es
el ticket promedio: cuánto vale en promedio cada transacción en esa zona.

**Ejemplo:** `ltv_por_ciudad(df).idxmax()` debe devolver la ciudad con mayor ticket promedio.
""",
    r"""
def ltv_por_ciudad(df):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
df_limpio = carga_limpia("../datasets/transacciones.csv")
ltv = ltv_por_ciudad(df_limpio)
revisar("es Series", isinstance(ltv, pd.Series))
revisar("indice son ciudades", set(ltv.index) == set(df_limpio["ciudad"].unique()))
revisar("ordenada desc", ltv.is_monotonic_decreasing)
revisar("valores positivos", (ltv > 0).all())
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def ltv_por_ciudad(df):
    return df.groupby("ciudad")["monto"].mean().sort_values(ascending=False)
```
</details>
""",
)

# ---- 7 --------------------------------------------------------------------
ejercicio(
    7, "Segmentación ABC de categorías",
    r"""Implementa `segmentacion_abc(df)` que devuelva un DataFrame con columnas:

- `"categoria"`: nombre de la categoría.
- `"total"`: ventas totales.
- `"pct_acumulado"`: porcentaje acumulado de ventas (de mayor a menor categoría).
- `"segmento_abc"`: `"A"` si pct_acumulado <= 60, `"B"` si <= 90, `"C"` el resto.

Ordenado de mayor a menor `total`.

**Ejemplo:** la categoría con más ventas debería tener `segmento_abc == "A"`.
""",
    r"""
def segmentacion_abc(df):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
df_limpio = carga_limpia("../datasets/transacciones.csv")
abc = segmentacion_abc(df_limpio)
revisar("es DataFrame", isinstance(abc, pd.DataFrame))
revisar("tiene columnas correctas", {"categoria","total","pct_acumulado","segmento_abc"}.issubset(abc.columns))
revisar("ordenado desc por total", abc["total"].is_monotonic_decreasing)
revisar("segmentos solo A B C", set(abc["segmento_abc"].unique()).issubset({"A","B","C"}))
revisar("primer segmento es A", abc["segmento_abc"].iloc[0] == "A")
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def segmentacion_abc(df):
    tot = df.groupby("categoria")["monto"].sum().sort_values(ascending=False).reset_index()
    tot.columns = ["categoria", "total"]
    gran_total = tot["total"].sum()
    tot["pct_acumulado"] = (tot["total"].cumsum() / gran_total * 100)

    def seg(p):
        if p <= 60:
            return "A"
        elif p <= 90:
            return "B"
        else:
            return "C"

    tot["segmento_abc"] = tot["pct_acumulado"].apply(seg)
    return tot
```
</details>
""",
)

# ---- 8 --------------------------------------------------------------------
ejercicio(
    8, "Visualización comparativa de dos variables",
    r"""Implementa `visualizar_scatter(df, ciudad1, ciudad2)` que genere un scatter plot
comparando el monto de transacciones de `ciudad1` vs `ciudad2`.

El scatter plot debe:
- Mostrar los puntos de `ciudad1` en azul y `ciudad2` en naranja.
- Tener etiquetas de ejes y título.
- Llamar a `plt.show()` al final.

La función puede retornar `None`.

**Nota:** esta función se evalúa por ejecución sin error, no por el contenido visual.
""",
    r"""
def visualizar_scatter(df, ciudad1, ciudad2):
    # ✏️ TU CÓDIGO AQUÍ
    import matplotlib.pyplot as plt
    pass
""",
    r"""
import matplotlib
matplotlib.use("Agg")  # sin ventana para el test
df_limpio = carga_limpia("../datasets/transacciones.csv")
try:
    visualizar_scatter(df_limpio, "Bogota", "Medellin")
    revisar("ejecuta sin error", True)
except Exception as e:
    revisar("ejecuta sin error", False)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def visualizar_scatter(df, ciudad1, ciudad2):
    import matplotlib.pyplot as plt
    d1 = df[df["ciudad"] == ciudad1]["monto"].reset_index(drop=True)
    d2 = df[df["ciudad"] == ciudad2]["monto"].reset_index(drop=True)
    plt.figure(figsize=(8, 5))
    plt.scatter(range(len(d1)), d1, color="steelblue", label=ciudad1, alpha=0.6)
    plt.scatter(range(len(d2)), d2, color="orange",    label=ciudad2, alpha=0.6)
    plt.xlabel("Indice de transaccion")
    plt.ylabel("Monto ($)")
    plt.title("Comparacion de montos: {} vs {}".format(ciudad1, ciudad2))
    plt.legend()
    plt.tight_layout()
    plt.show()
```
</details>
""",
)

# ---- 9 --------------------------------------------------------------------
ejercicio(
    9, "Correlación entre método de pago y monto promedio",
    r"""Implementa `correlacion_pago_monto(df)` que devuelva el coeficiente de
correlación de Pearson entre el método de pago (codificado como entero:
efectivo=0, tarjeta=1, transferencia=2) y el monto.

Devuelve un `float` entre -1 y 1.

**Ejemplo:** `isinstance(correlacion_pago_monto(df), float)` → `True`.
""",
    r"""
def correlacion_pago_monto(df):
    # ✏️ TU CÓDIGO AQUÍ (pista: .map() para codificar, np.corrcoef para correlacion)
    return None
""",
    r"""
df_limpio = carga_limpia("../datasets/transacciones.csv")
r = correlacion_pago_monto(df_limpio)
revisar("es float", isinstance(r, float))
revisar("en rango [-1, 1]", -1.0 <= r <= 1.0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def correlacion_pago_monto(df):
    import numpy as np
    mapa = {"efectivo": 0, "tarjeta": 1, "transferencia": 2}
    pago_cod = df["metodo_pago"].map(mapa).to_numpy()
    montos   = df["monto"].to_numpy()
    r = np.corrcoef(pago_cod, montos)[0, 1]
    return float(r)
```
</details>
""",
)

# ---- 10 -------------------------------------------------------------------
ejercicio(
    10, "Exportar reporte final a CSV",
    r"""Implementa `exportar_reporte(df, ruta_salida)` que:

1. Calcule, por ciudad, el total de ventas, la media, la mediana y el número de
   transacciones.
2. Guarde ese resumen como CSV en `ruta_salida`.
3. Devuelva el DataFrame de resumen.

**Ejemplo:** el CSV debe tener una fila por ciudad y columnas:
`ciudad`, `total`, `promedio`, `mediana`, `n_transacciones`.
""",
    r"""
def exportar_reporte(df, ruta_salida):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
import tempfile, os
df_limpio = carga_limpia("../datasets/transacciones.csv")
with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
    ruta_tmp = tmp.name
reporte = exportar_reporte(df_limpio, ruta_tmp)
revisar("devuelve DataFrame", isinstance(reporte, pd.DataFrame))
revisar("archivo existe", os.path.exists(ruta_tmp))
reporte_leido = pd.read_csv(ruta_tmp)
revisar("CSV tiene columna 'ciudad'", "ciudad" in reporte_leido.columns)
revisar("filas == ciudades unicas", len(reporte_leido) == df_limpio["ciudad"].nunique())
os.unlink(ruta_tmp)  # limpiar temp
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def exportar_reporte(df, ruta_salida):
    resumen = (
        df.groupby("ciudad")["monto"]
        .agg(total="sum", promedio="mean", mediana="median", n_transacciones="count")
        .reset_index()
    )
    resumen.to_csv(ruta_salida, index=False)
    return resumen
```
</details>
""",
)

C.append(md(r"""
---
## ¡Terminaste la práctica 01 de la Clase 8!

Si todas las comprobaciones muestran ✅, construiste las piezas fundamentales de
un pipeline de ciencia de datos:

| Ejercicio | Componente del pipeline |
|---|---|
| 1 carga_limpia | Extract + validación |
| 2 resumen_ejecutivo | KPIs de negocio |
| 3 transformar | Transform / feature engineering |
| 4 cohortes_mensuales | Análisis temporal |
| 5 detectar_anomalias | Control de calidad |
| 6 ltv_por_ciudad | Métrica de negocio |
| 7 segmentacion_abc | Priorización |
| 8 visualizar_scatter | Comunicación visual |
| 9 correlacion_pago_monto | Análisis estadístico |
| 10 exportar_reporte | Load / entrega |

➡️ Continúa con **practice02.ipynb** para el análisis end-to-end completo.
"""))


# ===================================================================== #
# VALIDACIÓN EN TIEMPO DE CONSTRUCCIÓN
# ===================================================================== #
def _validar():
    import csv
    import tempfile
    import pandas as pd
    import numpy as np

    ruta_csv = os.path.join(
        os.path.dirname(__file__), "..", "curso", "datasets", "transacciones.csv"
    )

    # Reimplementamos las soluciones de referencia
    def carga_limpia(ruta_csv):
        df = pd.read_csv(ruta_csv)
        df["fecha"] = pd.to_datetime(df["fecha"])
        df = df.dropna()
        df = df[df["monto"] > 0]
        return df.reset_index(drop=True)

    def resumen_ejecutivo(df):
        return {
            "total_ventas":    df["monto"].sum(),
            "ticket_promedio": df["monto"].mean(),
            "ticket_mediano":  df["monto"].median(),
            "n_transacciones": len(df),
            "ciudad_lider":    df.groupby("ciudad")["monto"].sum().idxmax(),
        }

    def transformar(df):
        df = df.copy()
        m_min, m_max = df["monto"].min(), df["monto"].max()
        df["monto_norm"] = (df["monto"] - m_min) / (m_max - m_min)
        def segmentar(m):
            if m < 100_000: return "bajo"
            elif m < 300_000: return "medio"
            else: return "alto"
        df["segmento"] = df["monto"].apply(segmentar)
        df["mes"] = pd.to_datetime(df["fecha"]).dt.month
        return df

    def cohortes_mensuales(df):
        return df.groupby("mes")["monto"].agg(n="count", total="sum", promedio="mean").sort_index()

    def detectar_anomalias(df, columna="monto"):
        Q1 = df[columna].quantile(0.25)
        Q3 = df[columna].quantile(0.75)
        IQR = Q3 - Q1
        lim_sup = Q3 + 1.5 * IQR
        lim_inf = Q1 - 1.5 * IQR
        mask = (df[columna] > lim_sup) | (df[columna] < lim_inf)
        return df[mask].copy()

    def ltv_por_ciudad(df):
        return df.groupby("ciudad")["monto"].mean().sort_values(ascending=False)

    def segmentacion_abc(df):
        tot = df.groupby("categoria")["monto"].sum().sort_values(ascending=False).reset_index()
        tot.columns = ["categoria", "total"]
        gran_total = tot["total"].sum()
        tot["pct_acumulado"] = (tot["total"].cumsum() / gran_total * 100)
        def seg(p):
            if p <= 60: return "A"
            elif p <= 90: return "B"
            else: return "C"
        tot["segmento_abc"] = tot["pct_acumulado"].apply(seg)
        return tot

    def correlacion_pago_monto(df):
        mapa = {"efectivo": 0, "tarjeta": 1, "transferencia": 2}
        pago_cod = df["metodo_pago"].map(mapa).to_numpy()
        montos   = df["monto"].to_numpy()
        r = np.corrcoef(pago_cod, montos)[0, 1]
        return float(r)

    def exportar_reporte(df, ruta_salida):
        resumen = (
            df.groupby("ciudad")["monto"]
            .agg(total="sum", promedio="mean", mediana="median", n_transacciones="count")
            .reset_index()
        )
        resumen.to_csv(ruta_salida, index=False)
        return resumen

    # Ejecutar validaciones
    df = carga_limpia(os.path.abspath(ruta_csv))
    assert isinstance(df, pd.DataFrame)
    assert pd.api.types.is_datetime64_any_dtype(df["fecha"])
    assert df.isnull().sum().sum() == 0
    assert (df["monto"] > 0).all()

    res = resumen_ejecutivo(df)
    assert "total_ventas" in res and res["total_ventas"] > 0
    assert "ciudad_lider" in res

    df_t = transformar(df)
    assert "monto_norm" in df_t.columns
    assert df_t["monto_norm"].between(0, 1).all()
    assert df_t["segmento"].isin(["bajo", "medio", "alto"]).all()

    coh = cohortes_mensuales(df_t)
    assert isinstance(coh, pd.DataFrame)
    assert "n" in coh.columns and "total" in coh.columns

    anom = detectar_anomalias(df)
    assert isinstance(anom, pd.DataFrame)
    assert len(anom) > 0

    ltv = ltv_por_ciudad(df)
    assert isinstance(ltv, pd.Series)
    assert ltv.is_monotonic_decreasing

    abc = segmentacion_abc(df)
    assert "segmento_abc" in abc.columns
    assert abc["segmento_abc"].iloc[0] == "A"

    r_corr = correlacion_pago_monto(df)
    assert isinstance(r_corr, float) and -1 <= r_corr <= 1

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        ruta_tmp = tmp.name
    reporte = exportar_reporte(df, ruta_tmp)
    assert isinstance(reporte, pd.DataFrame)
    import os as _os
    assert _os.path.exists(ruta_tmp)
    _os.unlink(ruta_tmp)

    print("✔ Todas las soluciones de referencia de practice01 (clase 8) pasan sus pruebas.")


_validar()


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase08", "practice01.ipynb")
build(os.path.abspath(ruta), C)
