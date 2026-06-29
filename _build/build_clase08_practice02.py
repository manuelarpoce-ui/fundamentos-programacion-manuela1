"""Construye curso/clase08/practice02.ipynb — pipeline integrador completo.

Caso aplicado: pipeline de ciencia de datos de extremo a extremo sobre
transacciones.csv — carga, limpieza, análisis NumPy/Pandas, visualización
y conclusiones de negocio.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []

C += [
md(r"""
# Clase 8 · Práctica 02 — Pipeline integrador de ciencia de datos

### Proyecto integrador · caso real sobre transacciones

Esta práctica te lleva, paso a paso, a través del pipeline completo de un
proyecto de ciencia de datos:

```
CSV
 │
 ▼
[1. Carga y exploración]
 │
 ▼
[2. Limpieza y validación]
 │
 ▼
[3. Ingeniería de features]
 │
 ▼
[4. Análisis NumPy]
 │
 ▼
[5. Análisis Pandas]
 │
 ▼
[6. Visualización]
 │
 ▼
[7. Conclusiones de negocio]
```

Al finalizar habrás respondido **6 preguntas de negocio** con evidencia cuantitativa.

> 🎯 **Objetivo:** No solo ejecutar código — **interpretar** cada resultado y
> traducirlo a lenguaje de negocio.
"""),

code(r"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath("__file__")), "..", "shared"))

RUTA_CSV = os.path.join(
    os.path.dirname(os.path.abspath("__file__")), "..", "datasets", "transacciones.csv"
)
print("Dataset:", RUTA_CSV)
print("Dependencias cargadas ✔")
"""),

]

# ============================================================ #
# FASE 1: CARGA Y EXPLORACIÓN
# ============================================================ #
C += [
md(r"""
---
## Fase 1 · Carga y exploración inicial

Antes de analizar cualquier dato necesitamos responder:

| Pregunta | Por qué importa |
|---|---|
| ¿Cuántas filas/columnas? | Dimensión del problema |
| ¿Qué tipos de datos? | Detectar columnas mal tipadas |
| ¿Hay nulos? | Decidir estrategia de limpieza |
| ¿Cuál es el rango temporal? | Contexto del análisis |

### Pseudocódigo
```
cargar CSV
mostrar dimensiones, tipos, primeras filas
contar nulos por columna
mostrar estadísticas descriptivas
```
"""),

code(r"""
df_raw = pd.read_csv(RUTA_CSV)

print("=" * 55)
print(f"  Dimensiones : {df_raw.shape[0]} filas x {df_raw.shape[1]} columnas")
print("=" * 55)
print("\nTipos de datos:")
print(df_raw.dtypes.to_string())
print("\nPrimeras 3 filas:")
df_raw.head(3)
"""),

code(r"""
nulos = df_raw.isnull().sum()
print("Valores nulos por columna:")
print(nulos[nulos > 0] if nulos.any() else "  (ningún nulo)")

print("\nEstadísticas descriptivas — columnas numéricas:")
df_raw.describe().round(2)
"""),

md(r"""
### 🔍 Observaciones de exploración

Después de cargar, siempre documenta:

- **Filas duplicadas:** `df.duplicated().sum()` — si hay, ¿son errores o reintentos?
- **Cardinalidad de categorías:** `df["columna"].value_counts()` — ¿cuántos valores únicos?
- **Rango temporal:** `df["fecha"].min()` y `df["fecha"].max()`.

> 🤔 **¿Qué pasaría si...?**
> El CSV tuviera una fila completamente vacía al final.
> `pd.read_csv` la incluiría como NaN en todas las columnas.
> Por eso siempre revisamos nulos ANTES de calcular estadísticas.
"""),

code(r"""
print(f"Filas duplicadas: {df_raw.duplicated().sum()}")

print("\nValores únicos por columna categórica:")
for col in ["categoria", "metodo_pago", "ciudad"]:
    vals = df_raw[col].value_counts()
    print(f"\n  {col}:")
    for v, n in vals.items():
        print(f"    {v:20s}: {n:4d} ({n/len(df_raw)*100:.1f}%)")
"""),

]

# ============================================================ #
# FASE 2: LIMPIEZA
# ============================================================ #
C += [
md(r"""
---
## Fase 2 · Limpieza y validación

La limpieza no es eliminar datos incómodos — es garantizar que cada
operación posterior trabaja con datos **correctos y coherentes**.

### Checklist de limpieza

- [ ] Convertir `fecha` de texto a `datetime`
- [ ] Filtrar montos ≤ 0 (transacciones inválidas)
- [ ] Eliminar filas con nulos en columnas clave
- [ ] Verificar que categorías y métodos de pago tengan valores esperados
"""),

code(r"""
df = df_raw.copy()

# Paso 1: convertir fecha
df["fecha"] = pd.to_datetime(df["fecha"])

# Paso 2: filtrar montos inválidos
n_antes = len(df)
df = df[df["monto"] > 0].copy()
print(f"Filas eliminadas por monto <= 0: {n_antes - len(df)}")

# Paso 3: eliminar nulos en columnas clave
df = df.dropna(subset=["monto", "categoria", "ciudad"]).reset_index(drop=True)
print(f"Filas finales: {len(df)}")

# Paso 4: verificar valores esperados
cats_esperadas  = {"alimentos", "electronica", "ropa", "hogar", "deportes"}
metodos_esperados = {"efectivo", "tarjeta", "transferencia"}

cats_reales    = set(df["categoria"].unique())
metodos_reales = set(df["metodo_pago"].unique())

print(f"\nCategorías inesperadas:    {cats_reales - cats_esperadas}")
print(f"Métodos de pago inesperados: {metodos_reales - metodos_esperados}")
"""),

]

# ============================================================ #
# FASE 3: INGENIERÍA DE FEATURES
# ============================================================ #
C += [
md(r"""
---
## Fase 3 · Ingeniería de features

Transformamos las columnas brutas en **variables derivadas** que son más
útiles para el análisis:

| Feature nuevo | Origen | Utilidad |
|---|---|---|
| `anio`, `mes`, `dia_semana` | `fecha` | Análisis temporal |
| `monto_log` | `monto` | Reducir sesgo derecho |
| `es_fin_semana` | `dia_semana` | Detección de patrones semanales |
| `monto_zscore` | `monto` | Detección de outliers |
"""),

code(r"""
# Features temporales
df["anio"]        = df["fecha"].dt.year
df["mes"]         = df["fecha"].dt.month
df["dia_semana"]  = df["fecha"].dt.dayofweek   # 0=lunes, 6=domingo
df["es_fin_semana"] = df["dia_semana"].isin([5, 6]).astype(int)

# Transformación logarítmica para reducir asimetría
df["monto_log"] = np.log1p(df["monto"])

# Z-score por ciudad (outliers locales)
def zscore_grupo(serie):
    mu, sigma = serie.mean(), serie.std()
    return (serie - mu) / sigma if sigma > 0 else serie * 0

df["monto_zscore"] = df.groupby("ciudad")["monto"].transform(zscore_grupo)
df["es_outlier"]   = (df["monto_zscore"].abs() > 3).astype(int)

print(f"Features nuevos: {['anio','mes','dia_semana','es_fin_semana','monto_log','monto_zscore','es_outlier']}")
print(f"\nOutliers detectados: {df['es_outlier'].sum()} ({df['es_outlier'].mean()*100:.1f}%)")
print("\nPrimeras 3 filas con nuevos features:")
df[["fecha","monto","monto_log","monto_zscore","es_outlier"]].head(3)
"""),

]

# ============================================================ #
# FASE 4: ANÁLISIS NUMPY
# ============================================================ #
C += [
md(r"""
---
## Fase 4 · Análisis con NumPy

Usamos NumPy para cómputo matricial eficiente: estadísticas, correlaciones
y simulaciones que requieren vectorización.

### Pregunta 1: ¿Qué tan correlacionados están el método de pago y el monto?

Codificamos los métodos de pago como enteros y calculamos la correlación de
Pearson. Una correlación alta indicaría que el método *predice* el monto.
"""),

code(r"""
# Codificación numérica de método de pago
mapa_metodo = {"efectivo": 0, "tarjeta": 1, "transferencia": 2}
metodo_cod  = df["metodo_pago"].map(mapa_metodo).to_numpy()
montos      = df["monto"].to_numpy()

# Correlación de Pearson con NumPy
r = np.corrcoef(metodo_cod, montos)[0, 1]
print(f"Correlación método de pago ↔ monto:  r = {r:.4f}")

if abs(r) < 0.1:
    interpretacion = "Sin correlación práctica"
elif abs(r) < 0.3:
    interpretacion = "Correlación débil"
elif abs(r) < 0.5:
    interpretacion = "Correlación moderada"
else:
    interpretacion = "Correlación fuerte"

print(f"Interpretación: {interpretacion}")
"""),

md(r"""
### Pregunta 2: ¿Cómo se distribuyen los montos? ¿Hay asimetría?

La **asimetría** (*skewness*) mide si la distribución tiene cola más larga
a la derecha (positiva) o a la izquierda (negativa).

- Skewness > 1: muy sesgada a la derecha → la media exagera el monto "típico"
- Skewness ~0: distribución simétrica
"""),

code(r"""
# Estadísticas de distribución
montos_arr = df["monto"].to_numpy()

media   = np.mean(montos_arr)
mediana = np.median(montos_arr)
std     = np.std(montos_arr)
# Skewness de Fisher: E[(x-mu)^3] / sigma^3
skewness = np.mean(((montos_arr - media) / std) ** 3)

print("Distribución de montos:")
print(f"  Media:    {media:>12,.0f}")
print(f"  Mediana:  {mediana:>12,.0f}")
print(f"  Std:      {std:>12,.0f}")
print(f"  Skewness: {skewness:>12.3f}")

print("\nConclusion:")
if skewness > 1:
    print("  Distribución muy sesgada a la derecha.")
    print("  La mediana es mejor indicador del monto 'típico' que la media.")
elif skewness > 0.5:
    print("  Sesgo moderado a la derecha.")
else:
    print("  Distribución aproximadamente simétrica.")
"""),

]

# ============================================================ #
# FASE 5: ANÁLISIS PANDAS
# ============================================================ #
C += [
md(r"""
---
## Fase 5 · Análisis con Pandas

Ahora respondemos preguntas de negocio usando agrupaciones y pivotes.

### Pregunta 3: ¿Qué ciudad y categoría tienen mayor volumen de ventas?
"""),

code(r"""
# Volumen por ciudad
volumen_ciudad = (
    df.groupby("ciudad")["monto"]
    .agg(total="sum", n_transacciones="count", ticket_medio="mean")
    .sort_values("total", ascending=False)
    .round(0)
)
print("Volumen por ciudad:")
print(volumen_ciudad.to_string())
"""),

code(r"""
# Volumen por categoría
volumen_cat = (
    df.groupby("categoria")["monto"]
    .agg(total="sum", n_transacciones="count", ticket_medio="mean")
    .sort_values("total", ascending=False)
    .round(0)
)
print("Volumen por categoría:")
print(volumen_cat.to_string())
"""),

md(r"""
### Pregunta 4: ¿Cuál es el ticket promedio por método de pago?

Una diferencia grande indicaría que ciertos métodos se usan para
compras de mayor valor.
"""),

code(r"""
ticket_metodo = (
    df.groupby("metodo_pago")["monto"]
    .agg(promedio="mean", mediana="median", total="sum", n="count")
    .round(1)
    .sort_values("promedio", ascending=False)
)
print("Ticket por método de pago:")
print(ticket_metodo.to_string())
"""),

md(r"""
### Pregunta 5: ¿Hay concentración de ventas en pocos clientes?

Usaremos la participación acumulada (análisis ABC / curva de Pareto).
"""),

code(r"""
# Análisis de Pareto: ¿el 20% de las transacciones explica el 80% del monto?
montos_ord = df["monto"].sort_values(ascending=False).reset_index(drop=True)
total      = montos_ord.sum()
pct_acum   = (montos_ord.cumsum() / total * 100).round(1)

# ¿Con qué % de transacciones llegamos al 80% del monto?
idx_80 = (pct_acum >= 80).idxmax()
pct_tx_para_80 = (idx_80 + 1) / len(montos_ord) * 100

print(f"Para llegar al 80% del monto total se necesitan el {pct_tx_para_80:.1f}% de las transacciones.")
print(f"\nRegla 80/20 (Pareto): {'confirmada' if pct_tx_para_80 < 25 else 'NO confirmada en este dataset'}")
"""),

]

# ============================================================ #
# FASE 6: VISUALIZACIÓN
# ============================================================ #
C += [
md(r"""
---
## Fase 6 · Visualización

Generamos 3 gráficos que sintetizan el análisis:

1. **Histograma de montos** (con y sin log) — compara distribuciones
2. **Barras de volumen por ciudad** — responde pregunta 3
3. **Box plot por método de pago** — responde pregunta 4
"""),

code(r"""
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Gráfico 1: Histograma de montos
axes[0].hist(df["monto"], bins=30, color="steelblue", edgecolor="white")
axes[0].set_title("Distribución de montos")
axes[0].set_xlabel("Monto")
axes[0].set_ylabel("Frecuencia")

# Gráfico 2: Volumen por ciudad
vc = df.groupby("ciudad")["monto"].sum().sort_values(ascending=False)
axes[1].bar(vc.index, vc.values / 1e6, color="teal", edgecolor="white")
axes[1].set_title("Ventas totales por ciudad (M)")
axes[1].set_xlabel("Ciudad")
axes[1].set_ylabel("Monto total (millones)")
axes[1].tick_params(axis="x", rotation=30)

# Gráfico 3: Box plot por método de pago
grupos = [df[df["metodo_pago"] == m]["monto"].values
          for m in ["efectivo", "tarjeta", "transferencia"]]
axes[2].boxplot(grupos, labels=["Efectivo", "Tarjeta", "Transferencia"])
axes[2].set_title("Monto por método de pago")
axes[2].set_ylabel("Monto")

plt.tight_layout()
plt.savefig("/tmp/clase08_analisis.png", dpi=90, bbox_inches="tight")
plt.close()
print("Gráficos generados ✔  (guardados en /tmp/clase08_analisis.png)")
"""),

]

# ============================================================ #
# FASE 7: CONCLUSIONES
# ============================================================ #
C += [
md(r"""
---
## Fase 7 · Conclusiones y recomendaciones de negocio

### Síntesis del pipeline

| Fase | Herramienta | Pregunta respondida |
|---|---|---|
| Carga | `pd.read_csv` | ¿Qué datos tenemos? |
| Limpieza | Pandas + validación | ¿Cuáles son confiables? |
| Features | NumPy + Pandas | ¿Qué información derivada es útil? |
| Distribución | NumPy (skewness) | ¿Cómo se comportan los montos? |
| Volumen | Pandas groupby | ¿Qué ciudad/categoría lidera? |
| Concentración | Pandas cumsum | ¿Hay concentración Pareto? |
| Visualización | Matplotlib | ¿Cómo comunicamos los hallazgos? |

### Template de conclusión de negocio

Una buena conclusión siempre sigue esta estructura:

```
HALLAZGO + EVIDENCIA + IMPLICACIÓN
```

Ejemplo:
> "La ciudad [X] concentra el [Y]% del volumen total (evidencia: tabla de
> volumen por ciudad). Esto sugiere priorizar campañas de fidelización en
> esa plaza antes de expandirse a otras ciudades."
"""),

code(r"""
print("=== RESUMEN EJECUTIVO ===\n")

ciudad_top = df.groupby("ciudad")["monto"].sum().idxmax()
cat_top    = df.groupby("categoria")["monto"].sum().idxmax()
metodo_top = df.groupby("metodo_pago")["monto"].sum().idxmax()
pct_outliers = df["es_outlier"].mean() * 100

print(f"Ciudad con mayor volumen:    {ciudad_top}")
print(f"Categoría líder:             {cat_top}")
print(f"Método de pago dominante:    {metodo_top}")
print(f"Outliers detectados:         {pct_outliers:.1f}% de las transacciones")
print(f"\nSkewness de montos:          {skewness:.3f}")
print(f"  → Usar mediana como referencia del ticket 'típico'.")
"""),

md(r"""
---
## Tus preguntas propias

Ahora que tienes el pipeline completo, plantea y responde **3 preguntas adicionales**
usando las herramientas que aprendiste en el curso.

**Ejemplos de preguntas posibles:**
- ¿Los outliers se concentran en alguna categoría o ciudad en particular?
- ¿Las transacciones de fin de semana tienen un ticket diferente?
- ¿Hay algún mes con caída de ventas?

> 💡 Documenta cada hallazgo con el formato: **HALLAZGO + EVIDENCIA + IMPLICACIÓN**.
"""),

code(r"""
# Pregunta 1: (escribe tu pregunta aquí)
# ────────────────────────────────────────
# Tu análisis aquí

# Pregunta 2: (escribe tu pregunta aquí)
# ────────────────────────────────────────
# Tu análisis aquí

# Pregunta 3: (escribe tu pregunta aquí)
# ────────────────────────────────────────
# Tu análisis aquí
"""),

md(r"""
---
## Recapitulación

En esta práctica ejecutaste el pipeline completo de ciencia de datos:

1. **Carga** — `pd.read_csv`, inspección de tipos y nulos
2. **Limpieza** — filtros, conversión de tipos, validación de valores
3. **Ingeniería de features** — variables temporales, log, z-score
4. **Análisis NumPy** — correlación, skewness, vectorización
5. **Análisis Pandas** — groupby, agg, cumsum (Pareto)
6. **Visualización** — histograma, barras, boxplot
7. **Conclusiones** — HALLAZGO + EVIDENCIA + IMPLICACIÓN

### ¿Qué sigue?
- **Machine learning:** usar los features para predecir el monto de la próxima transacción.
- **Series de tiempo:** modelar la tendencia mensual con regresión.
- **Dashboards:** exponer el resumen ejecutivo en una interfaz interactiva (Streamlit, Dash).

> ✅ Completaste el curso de Fundamentos de Programación para Ciencia de Datos.
> Tienes las bases para aprender cualquier herramienta adicional — porque ahora
> entiendes el *por qué* detrás de cada operación.
"""),

]

# ============================================================ #
# BUILD
# ============================================================ #
dest = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "curso", "clase08", "practice02.ipynb",
)
build(os.path.abspath(dest), C)
print(f"✔  Generado: {dest}")
