"""Construye curso/clase07/lecture.ipynb — EDA y transformación de datos."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []  # lista de celdas


# ===================================================================== #
# 0. PORTADA Y AGENDA
# ===================================================================== #
C += [
md(r"""
# Clase 7 · EDA y transformación de datos

### Fundamentos de Programación para Ciencia de Datos

> *"Los datos en bruto no son información. Explorarlos es el primer paso para convertirlos en conocimiento."*

---

**Duración:** 3 horas · **Modalidad:** notebook interactivo

Antes de entrenar un modelo, antes de responder una pregunta de negocio, antes de
hacer cualquier análisis serio, necesitas **entender tus datos**. El Análisis
Exploratorio de Datos (EDA, por sus siglas en inglés) es ese paso indispensable.

Hoy aprenderemos a:
- **Perfilar** un dataset: qué tiene, qué falta, qué tipos son.
- **Visualizar** distribuciones: histogramas, boxplots, scatter plots, heatmaps.
- **Detectar** valores atípicos con métodos sistemáticos.
- **Transformar** variables: normalizar, estandarizar, hacer binning, encoding.
- **Imputar** valores faltantes de forma inteligente.
- Construir un **pipeline EDA completo** sobre datos reales.
"""),

md(r"""
## Mapa de la clase

| Bloque | Tiempo | Qué haremos |
|---|---|---|
| 1. Motivación y perfilado | 25 min | Por qué EDA, shape, dtypes, nulos, cardinalidad |
| 2. Distribuciones univariadas | 25 min | Histogramas, boxplot, estadísticas descriptivas |
| 3. Distribuciones bivariadas | 20 min | Scatter, correlación, heatmap |
| 4. Variables categóricas | 15 min | value_counts, frecuencias, bar chart |
| 5. Detección de outliers | 20 min | Z-score, método IQR |
| 6. Transformaciones numéricas | 25 min | Normalización, estandarización, binning |
| 7. Encoding categórico | 20 min | Label encoding, one-hot (pd.get_dummies) |
| 8. Missing values | 15 min | Estrategias de imputación |
| 9. Pipeline EDA completo | 20 min | Todo junto sobre transacciones |
| 10. Errores, quiz y retos | 15 min | Cierre |

> **Cómo usar este notebook:** lee cada celda de texto *antes* de ejecutar la
> que le sigue. Detente en cada bloque **¿Qué pasaría si...?** e intenta
> responder antes de continuar.
"""),

md(r"""
## Antes de empezar: importaciones globales

Aquí configuramos las librerías que usaremos a lo largo de toda la clase.
"""),

code(r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os, sys

matplotlib.rcParams["figure.figsize"] = (9, 4)
matplotlib.rcParams["axes.spines.top"] = False
matplotlib.rcParams["axes.spines.right"] = False

# Dataset de transacciones (relativo a la carpeta clase07)
RUTA_CSV = os.path.join("..", "datasets", "transacciones.csv")
df = pd.read_csv(RUTA_CSV)
print("Dataset cargado:", df.shape)
df.head(3)
"""),
]


# ===================================================================== #
# 1. MOTIVACIÓN Y PERFILADO
# ===================================================================== #
C += [
md(r"""
## 1. ¿Por qué el EDA es el primer paso?

Imagina que recibes un dataset de transacciones de una cadena de tiendas.
Tu jefe te pide "entrenar un modelo que prediga si una venta es fraudulenta".
¿Cuál es el primer error que comete un analista principiante?

**Saltar directo al modelo.**

Resultado: el modelo aprende a predecir basura con basura. Los datos pueden
tener valores negativos en montos (imposible), fechas en el futuro, ciudades
mal escritas, columnas casi completamente nulas, variables correlacionadas al
100%... Un EDA sistemático expone todo esto antes de que cause problemas.

### El EDA responde tres grandes preguntas:

```
  1. ¿QUÉ TENGO?       Shape, tipos, cardinalidad, primeras filas
         │
         ▼
  2. ¿QUÉ ESTÁ MAL?    Nulos, outliers, inconsistencias, duplicados
         │
         ▼
  3. ¿QUÉ HAY AQUÍ?    Distribuciones, correlaciones, patrones, relaciones
```

Solo después de responder estas tres preguntas tiene sentido pensar en modelos.
"""),

md(r"""
## 1.1 Perfilado básico de un dataset

El **perfilado** es un diagnóstico rápido. En minutos debes poder responder:

| Pregunta | Método pandas |
|---|---|
| ¿Cuántas filas y columnas? | `df.shape` |
| ¿Qué tipo tiene cada columna? | `df.dtypes` |
| ¿Cuántos valores nulos? | `df.isnull().sum()` |
| ¿Cuántos valores únicos (categóricas)? | `df.nunique()` |
| Estadísticas básicas (numéricas) | `df.describe()` |
| ¿Hay filas duplicadas? | `df.duplicated().sum()` |
"""),

code(r"""
print("=== FORMA DEL DATASET ===")
print("Filas:", df.shape[0], "| Columnas:", df.shape[1])

print("\n=== TIPOS DE DATOS ===")
print(df.dtypes)

print("\n=== VALORES NULOS POR COLUMNA ===")
nulos = df.isnull().sum()
pct = (nulos / len(df) * 100).round(1)
resumen_nulos = pd.DataFrame({"nulos": nulos, "pct_%": pct})
print(resumen_nulos[resumen_nulos["nulos"] > 0] if nulos.sum() > 0 else "Sin nulos.")

print("\n=== FILAS DUPLICADAS ===", df.duplicated().sum())
"""),

code(r"""
print("=== CARDINALIDAD (valores únicos por columna) ===")
print(df.nunique().to_string())

print("\n=== ESTADÍSTICAS DESCRIPTIVAS (numéricas) ===")
df.describe().round(0)
"""),

md(r"""
### ¿Qué nos dice el perfilado?

- `fecha` llega como texto (`object`) — hay que convertirla.
- `monto` es numérico — bien.
- `ciudad`, `categoria`, `metodo_pago` son categóricas con cardinalidad baja (pocas categorías únicas).
- El monto mínimo y máximo nos dan la primera pista sobre outliers.

> **Regla de oro del perfilado:** nunca asumas el tipo de un dato. Verifica siempre.

### 🤔 ¿Qué pasaría si...?

- ¿...`nunique()` sobre `monto` diera el mismo número que las filas? Significaría
  que cada transacción tiene un monto diferente — posible, pero extraño.
- ¿...el 80% de una columna fuera nulo? Habría que decidir si vale la pena usarla.
"""),
]


# ===================================================================== #
# 2. DISTRIBUCIÓN UNIVARIADA
# ===================================================================== #
C += [
md(r"""
## 2. Distribución univariada

Analizar una variable a la vez nos dice **cómo se distribuyen sus valores**.

### Las estadísticas clave:

| Estadístico | Qué mide | Código |
|---|---|---|
| **Media** | promedio, sensible a outliers | `serie.mean()` |
| **Mediana** | valor central, robusta a outliers | `serie.median()` |
| **Moda** | valor más frecuente | `serie.mode()[0]` |
| **Std** | dispersión promedio alrededor de la media | `serie.std()` |
| **IQR** | rango del 50% central (Q3 - Q1), robusto | `serie.quantile(0.75) - serie.quantile(0.25)` |
| **Min / Max** | rango completo | `serie.min()`, `serie.max()` |

> Cuando media y mediana difieren mucho, la distribución está **sesgada**
> (hay valores extremos que jalan la media hacia un lado).
"""),

code(r"""
monto = df["monto"]

print("=== ESTADÍSTICAS DE MONTO ===")
print("Media:   {:,.0f}".format(monto.mean()))
print("Mediana: {:,.0f}".format(monto.median()))
print("Moda:    {:,.0f}".format(monto.mode()[0]))
print("Std:     {:,.0f}".format(monto.std()))
q1 = monto.quantile(0.25)
q3 = monto.quantile(0.75)
iqr = q3 - q1
print("Q1:      {:,.0f}".format(q1))
print("Q3:      {:,.0f}".format(q3))
print("IQR:     {:,.0f}".format(iqr))
print("Min:     {:,.0f}".format(monto.min()))
print("Max:     {:,.0f}".format(monto.max()))
print("\nSkewness (asimetría): {:.3f}".format(monto.skew()))
print("(> 0 = sesgo a la derecha, valores altos arrastran la media)")
"""),

code(r"""
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Histograma
axes[0].hist(df["monto"], bins=30, color="#4C72B0", edgecolor="white", alpha=0.85)
axes[0].axvline(df["monto"].mean(), color="red", linestyle="--", label="Media")
axes[0].axvline(df["monto"].median(), color="green", linestyle="--", label="Mediana")
axes[0].set_title("Distribución de montos")
axes[0].set_xlabel("Monto ($)")
axes[0].set_ylabel("Frecuencia")
axes[0].legend()

# Boxplot
axes[1].boxplot(df["monto"], vert=True, patch_artist=True,
                boxprops=dict(facecolor="#4C72B0", alpha=0.6),
                medianprops=dict(color="red", linewidth=2))
axes[1].set_title("Boxplot de montos")
axes[1].set_ylabel("Monto ($)")

plt.tight_layout()
plt.show()

print("Tip: en el boxplot, los puntos fuera de los 'bigotes' son outliers candidatos.")
"""),

md(r"""
### Lectura del boxplot

```
        ┌─────────────────────────────────────────┐
        │                                         │
  ──────┤  Q1          MEDIANA          Q3  ├──────  ← bigotes = 1.5 × IQR
        │                                         │
        └─────────────────────────────────────────┘
   *                                                   *
  puntos fuera de los bigotes = outliers candidatos
```

Los bigotes llegan hasta `Q1 - 1.5×IQR` y `Q3 + 1.5×IQR`. Todo lo que quede
fuera es marcado como outlier por la convención de Tukey.

### 🤔 ¿Qué pasaría si...?

- ¿...la media y la mediana fueran iguales? Señal de distribución **simétrica** (sin sesgo).
- ¿...el histograma tuviera dos "jorobas"? Se llama distribución **bimodal** y
  puede indicar que hay dos poblaciones mezcladas (ej: compras minoristas y mayoristas).
"""),
]


# ===================================================================== #
# 3. DISTRIBUCIÓN BIVARIADA
# ===================================================================== #
C += [
md(r"""
## 3. Distribución bivariada: relaciones entre variables

Analizar dos variables a la vez nos dice si **se mueven juntas** (correlación).

### Correlación de Pearson

Mide la **relación lineal** entre dos variables numéricas.

- **+1**: perfecto relación directa (cuando una sube, la otra sube).
- **0**: sin relación lineal.
- **-1**: perfecta relación inversa.

```
     r ≈ +1                r ≈ 0               r ≈ -1
  ↗ puntos suben juntos   · puntos dispersos   ↘ cuando una sube, la otra baja
```

> **Advertencia de oro:** correlación no implica causalidad. Que dos variables
> estén correlacionadas no significa que una cause a la otra.
"""),

code(r"""
# Para comparar monto vs una variable numérica sintética: monto vs id (solo como demo)
# En la práctica compararías monto vs otra columna numérica real.

# Creamos una variable numérica extra: hora simulada a partir del id
np.random.seed(42)
df["monto_log"] = np.log1p(df["monto"])  # log(1 + monto), transformación útil

print("Correlación de Pearson entre monto y monto_log: {:.4f}".format(
    df["monto"].corr(df["monto_log"])
))
print("(alta correlacion porque monto_log es una transformacion de monto)")
"""),

code(r"""
# Scatter plot: monto vs monto_log
fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(df["monto"], df["monto_log"], alpha=0.5, color="#4C72B0", s=25)
ax.set_xlabel("Monto ($)")
ax.set_ylabel("log(1 + Monto)")
ax.set_title("Scatter: Monto vs log(Monto)\n(tipica transformación para reducir sesgo)")
plt.tight_layout()
plt.show()
"""),

code(r"""
# Heatmap de correlaciones entre todas las numéricas
numericas = df.select_dtypes(include="number")
corr = numericas.corr()

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(corr, vmin=-1, vmax=1, cmap="coolwarm")
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
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- ¿...dos columnas tuvieran correlación = 1.0? Serían **perfectamente colineales**:
  una es una combinación lineal de la otra. En modelos lineales, esto causa
  problemas (multicolinealidad). Habría que eliminar una.
- ¿...encontraras correlación alta entre cantidad de incendios y consumo de helado?
  Ambas suben en verano. La causa es la **temperatura**, no que uno cause el otro.
"""),
]


# ===================================================================== #
# 4. ANÁLISIS DE VARIABLES CATEGÓRICAS
# ===================================================================== #
C += [
md(r"""
## 4. Análisis de variables categóricas

Las variables categóricas no tienen media ni desviación estándar, pero sí tienen
**frecuencias**. Las preguntas clave son:

- ¿Cuántas categorías hay?
- ¿Están balanceadas o hay una que domina?
- ¿Alguna categoría tiene muy pocas observaciones?

Una categoría muy rara puede ser problemática en modelos o indicar un error de datos.
"""),

code(r"""
print("=== FRECUENCIAS ABSOLUTAS: ciudad ===")
print(df["ciudad"].value_counts())

print("\n=== FRECUENCIAS RELATIVAS: ciudad ===")
print(df["ciudad"].value_counts(normalize=True).round(3))
"""),

code(r"""
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

for ax, col in zip(axes, ["ciudad", "categoria", "metodo_pago"]):
    vc = df[col].value_counts()
    ax.bar(vc.index, vc.values, color="#4C72B0", edgecolor="white", alpha=0.85)
    ax.set_title("Frecuencia: " + col)
    ax.set_ylabel("Conteo")
    ax.tick_params(axis="x", rotation=30)

plt.tight_layout()
plt.show()
"""),

code(r"""
# Monto promedio por categoría: combinando groupby con EDA
print("=== MONTO PROMEDIO POR CATEGORIA ===")
resumen_cat = df.groupby("categoria")["monto"].agg(["mean", "median", "std", "count"])
resumen_cat.columns = ["media", "mediana", "std", "n"]
print(resumen_cat.sort_values("media", ascending=False).round(0))
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- ¿...una categoría tuviera solo 1 observación? En modelos de ML, esa clase
  es difícil de aprender. Podría agruparse con "otras" o eliminarse.
- ¿...el gráfico de barras mostrara que el 95% de las ventas son de una sola ciudad?
  El modelo entrenado podría ser inútil para las otras ciudades (sesgo de datos).
"""),
]


# ===================================================================== #
# 5. DETECCIÓN DE OUTLIERS
# ===================================================================== #
C += [
md(r"""
## 5. Detección de outliers

Un **outlier** (valor atípico) es una observación que difiere marcadamente del
resto. Pueden ser:

- **Errores de datos:** un monto negativo en ventas, una edad de 999 años.
- **Casos extremos reales:** una compra corporativa legítima de $2 millones.
- **Fraudes:** transacciones anómalas que el modelo debe aprender.

La detección de outliers es previa a decidir qué hacer con ellos. No siempre
se eliminan: a veces son justamente lo más interesante.

### Método 1: Z-score

El **z-score** mide cuántas desviaciones estándar está un valor de la media.

```
        valor - media
z  =  ─────────────────
            std
```

Convención: `|z| > 3` suele considerarse outlier (cubre el 99.7% de una normal).
"""),

code(r"""
from scipy import stats as scipy_stats

monto = df["monto"]
z_scores = np.abs((monto - monto.mean()) / monto.std())

umbral_z = 3.0
outliers_z = df[z_scores > umbral_z]

print("Outliers por z-score (|z| > {:.1f}): {:d}".format(umbral_z, len(outliers_z)))
if len(outliers_z) > 0:
    print(outliers_z[["id", "ciudad", "categoria", "monto"]].to_string(index=False))
"""),

md(r"""
### Método 2: Método IQR (Tukey)

Más robusto que el z-score porque no asume distribución normal.

```
  límite inferior = Q1 - 1.5 × IQR
  límite superior = Q3 + 1.5 × IQR
```

Todo lo que cae fuera de estos límites es un outlier candidato.

```
   ──────────[ Q1 ──────── Q2 ──────── Q3 ]──────────
   ↑                                              ↑
   Q1 - 1.5·IQR                          Q3 + 1.5·IQR
   (bigote inferior)                   (bigote superior)
        *  puntos aquí = outliers  *
```
"""),

code(r"""
q1 = monto.quantile(0.25)
q3 = monto.quantile(0.75)
iqr = q3 - q1
limite_inf = q1 - 1.5 * iqr
limite_sup = q3 + 1.5 * iqr

outliers_iqr = df[(monto < limite_inf) | (monto > limite_sup)]

print("Q1: {:,.0f}  Q3: {:,.0f}  IQR: {:,.0f}".format(q1, q3, iqr))
print("Límite inferior: {:,.0f}".format(limite_inf))
print("Límite superior: {:,.0f}".format(limite_sup))
print("Outliers por IQR: {:d}".format(len(outliers_iqr)))
if len(outliers_iqr) > 0:
    print(outliers_iqr[["id", "ciudad", "categoria", "monto"]].to_string(index=False))
"""),

code(r"""
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Z-scores visualizados
axes[0].scatter(range(len(z_scores)), z_scores, alpha=0.5, s=20, color="#4C72B0")
axes[0].axhline(umbral_z, color="red", linestyle="--", label="Umbral z=3")
axes[0].set_title("Z-scores del monto")
axes[0].set_xlabel("Indice de transaccion")
axes[0].set_ylabel("|z-score|")
axes[0].legend()

# IQR visualizado como boxplot anotado
axes[1].boxplot(monto, vert=True, patch_artist=True,
                boxprops=dict(facecolor="#4C72B0", alpha=0.5),
                medianprops=dict(color="red"))
axes[1].axhline(limite_sup, color="orange", linestyle="--", label="Lim sup IQR")
axes[1].axhline(limite_inf, color="green", linestyle="--", label="Lim inf IQR")
axes[1].set_title("Boxplot con limites IQR")
axes[1].legend()

plt.tight_layout()
plt.show()
"""),

md(r"""
### ¿Z-score o IQR?

| Característica | Z-score | IQR (Tukey) |
|---|---|---|
| Supuesto de distribución | normal | ninguno |
| Robusto a outliers existentes | no | sí |
| Fácil de interpretar | sí | sí |
| Cuando usarlo | datos aprox. normales | siempre que haya sesgo |

### 🤔 ¿Qué pasaría si...?

- ¿...elimináramos todos los outliers antes de entrenar un modelo de detección
  de fraudes? Eliminaríamos los casos de fraude, que son exactamente los que
  queremos detectar. **Conocer el contexto decide qué hacer con los outliers.**
"""),
]


# ===================================================================== #
# 6. TRANSFORMACIONES NUMÉRICAS
# ===================================================================== #
C += [
md(r"""
## 6. Transformaciones numéricas

Muchos algoritmos de ML (regresión logística, K-means, SVM, redes neuronales)
son sensibles a la **escala** de los datos. Una columna de salarios (millones)
y una de edad (decenas) harían que el algoritmo "ignore" la edad por tener
números más pequeños.

La solución: **escalar o transformar** las variables numéricas.

### 6.1 Normalización Min-Max

Mapea todos los valores al rango `[0, 1]`:

```
        valor - min
x' = ─────────────────
         max - min
```

- **Ventaja:** escala conocida y acotada.
- **Desventaja:** muy sensible a outliers (un valor extremo comprime todo lo demás).
"""),

code(r"""
monto = df["monto"]

# Normalización min-max manual
monto_min = monto.min()
monto_max = monto.max()
monto_norm = (monto - monto_min) / (monto_max - monto_min)

print("=== NORMALIZACIÓN MIN-MAX ===")
print("Original  -> min: {:,.0f}  max: {:,.0f}".format(monto_min, monto_max))
print("Normalizado -> min: {:.4f}  max: {:.4f}".format(monto_norm.min(), monto_norm.max()))
print("\nPrimeros 5 valores originales:", monto.head().tolist())
print("Primeros 5 valores normalizados:", monto_norm.head().round(4).tolist())
"""),

md(r"""
### 6.2 Estandarización Z-score

Centra los datos en 0 con desviación estándar 1:

```
        valor - media
x' = ─────────────────
            std
```

- **Ventaja:** robusta a diferentes escalas; los outliers no comprimen el resto tanto.
- **Desventaja:** no acota a un rango fijo; un outlier puede tener z = 10.
- **Cuando usarla:** algoritmos que asumen distribución normal (regresión logística, SVM).
"""),

code(r"""
media = monto.mean()
std = monto.std()
monto_std = (monto - media) / std

print("=== ESTANDARIZACIÓN Z-SCORE ===")
print("Original  -> media: {:,.1f}  std: {:,.1f}".format(media, std))
print("Estandarizado -> media: {:.4f}  std: {:.4f}".format(monto_std.mean(), monto_std.std()))
print("\nPrimeros 5 estandarizados:", monto_std.head().round(3).tolist())
"""),

code(r"""
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

axes[0].hist(monto, bins=25, color="#4C72B0", edgecolor="white", alpha=0.8)
axes[0].set_title("Original")
axes[0].set_xlabel("Monto ($)")

axes[1].hist(monto_norm, bins=25, color="#55A868", edgecolor="white", alpha=0.8)
axes[1].set_title("Normalizado [0, 1]")
axes[1].set_xlabel("Monto normalizado")

axes[2].hist(monto_std, bins=25, color="#C44E52", edgecolor="white", alpha=0.8)
axes[2].axvline(0, color="black", linestyle="--", alpha=0.5)
axes[2].set_title("Estandarizado (z-score)")
axes[2].set_xlabel("z-score")

for ax in axes:
    ax.set_ylabel("Frecuencia")

plt.suptitle("Efecto de las transformaciones de escala", fontsize=11, y=1.02)
plt.tight_layout()
plt.show()

print("Nota: la FORMA de la distribucion no cambia, solo la escala del eje X.")
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- ¿...normalizaras con el min/max del conjunto de entrenamiento y luego aplicaras
  esa escala al conjunto de prueba? Correcto. Lo incorrecto es calcular min/max
  sobre el conjunto completo (incluye el test): eso es **data leakage** — el modelo
  "ve" información del futuro.
"""),
]


# ===================================================================== #
# 7. BINNING
# ===================================================================== #
C += [
md(r"""
## 7. Binning: convertir numérico en categorías

A veces queremos **discretizar** una variable continua. Por ejemplo:
- Agrupar edades en "joven", "adulto", "senior".
- Agrupar montos en rangos para análisis de negocio.
- Reducir el impacto de outliers en ciertos modelos de árbol.

### pd.cut — intervalos de igual ancho

Divide el rango `[min, max]` en `n` bins del mismo tamaño.
"""),

code(r"""
# Binning de monto en 5 categorías de igual ancho
df["monto_bin5"] = pd.cut(df["monto"], bins=5,
                           labels=["muy_bajo", "bajo", "medio", "alto", "muy_alto"])

print("=== pd.cut (igual ancho) ===")
print(df["monto_bin5"].value_counts().sort_index())
print("\nIntervales generados:")
print(pd.cut(df["monto"], bins=5).value_counts().sort_index())
"""),

md(r"""
### pd.qcut — cuantiles (igual frecuencia)

Divide en `n` bins de modo que **cada bin tenga el mismo número de observaciones**.
Útil cuando la distribución está sesgada (pd.cut dejaría bins casi vacíos).
"""),

code(r"""
# Binning por cuartiles (4 grupos de igual tamaño)
df["monto_qbin4"] = pd.qcut(df["monto"], q=4,
                              labels=["Q1_bajo", "Q2_medio_bajo",
                                      "Q3_medio_alto", "Q4_alto"])

print("=== pd.qcut (igual frecuencia) ===")
print(df["monto_qbin4"].value_counts().sort_index())
print("\nDistribucion equitativa (cada bin tiene aprox. el mismo numero de obs).")
"""),

code(r"""
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

vc5 = df["monto_bin5"].value_counts().sort_index()
axes[0].bar(range(len(vc5)), vc5.values, color="#4C72B0", edgecolor="white")
axes[0].set_xticks(range(len(vc5)))
axes[0].set_xticklabels(vc5.index, rotation=20)
axes[0].set_title("pd.cut: igual ancho (puede haber bins vacios)")
axes[0].set_ylabel("Frecuencia")

vc4 = df["monto_qbin4"].value_counts().sort_index()
axes[1].bar(range(len(vc4)), vc4.values, color="#55A868", edgecolor="white")
axes[1].set_xticks(range(len(vc4)))
axes[1].set_xticklabels(vc4.index, rotation=20)
axes[1].set_title("pd.qcut: igual frecuencia (balanceado)")
axes[1].set_ylabel("Frecuencia")

plt.tight_layout()
plt.show()
"""),

md(r"""
### ¿pd.cut o pd.qcut?

| Situación | Usar |
|---|---|
| Rangos tienen significado de negocio (0-50k, 50k-100k…) | `pd.cut` |
| Quieres grupos balanceados para un modelo | `pd.qcut` |
| Distribución sesgada y necesitas bins representativos | `pd.qcut` |

### 🤔 ¿Qué pasaría si...?

- ¿...usaras `pd.cut` con una distribución muy sesgada? La mayoría de los datos
  caería en un solo bin y el resto estarían casi vacíos. `pd.qcut` resuelve esto.
"""),
]


# ===================================================================== #
# 8. ENCODING DE VARIABLES CATEGÓRICAS
# ===================================================================== #
C += [
md(r"""
## 8. Encoding de variables categóricas

Los algoritmos de ML trabajan con **números**, no con texto. Hay que convertir
las categorías a representaciones numéricas. Las dos técnicas fundamentales:

### 8.1 Label Encoding

Asigna un entero a cada categoría: `efectivo=0`, `tarjeta=1`, `transferencia=2`.

**Problema:** crea un orden artificial (`transferencia > tarjeta > efectivo`) que
no existe en la realidad. Solo es válido para variables **ordinales** (donde el
orden sí tiene sentido: bajo < medio < alto).
"""),

code(r"""
# Label encoding manual
metodos = df["metodo_pago"].unique()
label_map = {m: i for i, m in enumerate(sorted(metodos))}
df["metodo_pago_label"] = df["metodo_pago"].map(label_map)

print("=== LABEL ENCODING: metodo_pago ===")
print("Mapping:", label_map)
print(df[["metodo_pago", "metodo_pago_label"]].drop_duplicates().sort_values("metodo_pago_label"))
"""),

md(r"""
### 8.2 One-Hot Encoding (pd.get_dummies)

Crea una columna binaria (0/1) por cada categoría. Sin orden artificial.

```
  metodo_pago     efectivo   tarjeta   transferencia
  efectivo    →      1          0           0
  tarjeta     →      0          1           0
  transferencia→     0          0           1
```

**Ventaja:** no asume orden. **Cuidado:** con muchas categorías crea muchas columnas
(explosión de dimensionalidad).
"""),

code(r"""
# One-hot encoding con pd.get_dummies
dummies = pd.get_dummies(df["metodo_pago"], prefix="pago")
print("=== ONE-HOT ENCODING: metodo_pago ===")
print(dummies.head(8))
print("\nTipos:", dummies.dtypes.to_dict())

# Unir al dataframe original
df_encoded = pd.concat([df, dummies], axis=1)
print("\nForma final del dataframe:", df_encoded.shape)
"""),

code(r"""
# También podemos encodear todas las categóricas a la vez
df_ohe = pd.get_dummies(df[["ciudad", "categoria", "metodo_pago"]])
print("=== OHE de todas las categoricas ===")
print("Columnas generadas:", df_ohe.columns.tolist())
print("Shape:", df_ohe.shape)
"""),

md(r"""
### ¿Label o One-Hot?

| Variable | Tipo | Usar |
|---|---|---|
| talla: S, M, L, XL | ordinal (tiene orden) | Label Encoding |
| ciudad: Bogotá, Medellín, Cali | nominal (sin orden) | One-Hot Encoding |
| clasificación: bajo, medio, alto | ordinal | Label Encoding con orden correcto |
| metodo_pago | nominal | One-Hot Encoding |

### 🤔 ¿Qué pasaría si...?

- ¿...aplicaras Label Encoding a `metodo_pago`? Un modelo lineal podría aprender
  que `transferencia (2)` es el doble de `efectivo (1)`, lo cual no tiene sentido.
"""),
]


# ===================================================================== #
# 9. MISSING VALUES
# ===================================================================== #
C += [
md(r"""
## 9. Valores faltantes (missing values)

Los datos reales casi siempre tienen nulos. Las estrategias para manejarlos:

### 9.1 Eliminar filas o columnas

Simple pero costoso: perdes información. Solo si la columna tiene >50-70% de nulos
o si los nulos son poquísimos y aleatorios.

### 9.2 Imputar con estadístico

Rellenar el nulo con un valor representativo:

| Estrategia | Cuándo usarla |
|---|---|
| **Media** | distribución aproximadamente normal, sin outliers extremos |
| **Mediana** | distribución sesgada o con outliers |
| **Moda** | variables categóricas |
| **Forward-fill** | series de tiempo (el valor previo es el mejor estimado) |
| **Modelo predictivo** | cuando los nulos tienen un patrón (MNAR) |

> Nunca imputar con la media/mediana calculada sobre todos los datos si vas a
> separar train/test después. Calcula la estadística solo sobre **train** y
> aplícala a ambos conjuntos — de lo contrario tienes **data leakage**.
"""),

code(r"""
# Creamos nulos artificiales para demostrar imputación
df_nulos = df.copy()
np.random.seed(7)
idx_nulos = np.random.choice(df_nulos.index, size=15, replace=False)
df_nulos.loc[idx_nulos, "monto"] = np.nan

print("Nulos introducidos en 'monto':", df_nulos["monto"].isnull().sum())
print("Valores originales en esas posiciones (primeros 5):")
print(df.loc[idx_nulos[:5], "monto"].tolist())
"""),

code(r"""
# Estrategia 1: imputar con la media
media_train = df_nulos["monto"].mean()   # calculada solo sobre los no-nulos
df_imp_media = df_nulos.copy()
df_imp_media["monto"] = df_imp_media["monto"].fillna(media_train)

# Estrategia 2: imputar con la mediana
mediana_train = df_nulos["monto"].median()
df_imp_mediana = df_nulos.copy()
df_imp_mediana["monto"] = df_imp_mediana["monto"].fillna(mediana_train)

print("Media usada para imputar:   {:,.1f}".format(media_train))
print("Mediana usada para imputar: {:,.1f}".format(mediana_train))
print("\nDiferencia media vs mediana: {:,.1f}".format(abs(media_train - mediana_train)))
print("(Si hay outliers, la mediana es mas robusta)")

# Comprobar que no quedan nulos
print("\nNulos tras imputar con media:   ", df_imp_media["monto"].isnull().sum())
print("Nulos tras imputar con mediana:", df_imp_mediana["monto"].isnull().sum())
"""),

code(r"""
# Forward-fill: útil para series de tiempo (precio de una acción, etc.)
df_ts = pd.DataFrame({
    "dia": range(10),
    "precio": [100, 102, np.nan, np.nan, 107, np.nan, 110, 111, np.nan, 115]
})
df_ts["precio_ffill"] = df_ts["precio"].ffill()
df_ts["precio_media"] = df_ts["precio"].fillna(df_ts["precio"].mean())

print("=== FORWARD-FILL vs MEDIA en serie de tiempo ===")
print(df_ts.to_string(index=False))
print("\nForward-fill preserva la tendencia; la media puede ser muy diferente.")
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- ¿...imputaras la media antes de separar train/test? El conjunto de test
  "contamina" el cálculo de la media. El modelo aprende sobre información que
  en producción no tendría. Eso es **data leakage**.
- ¿...no imputaras y dejaras los nulos? pandas y sklearn en su mayoría lanzan
  error con NaN. Siempre hay que decidir qué hacer con ellos.
"""),
]


# ===================================================================== #
# 10. PIPELINE EDA COMPLETO
# ===================================================================== #
C += [
md(r"""
## 10. Pipeline EDA completo

Ahora integramos todo en un flujo sistemático aplicado al dataset de transacciones.
Este es el orden recomendado para cualquier dataset nuevo:

```
  PASO 1: Cargar y perfilar (shape, dtypes, nulos, duplicados)
      │
  PASO 2: Limpiar (tipos, nulos, duplicados)
      │
  PASO 3: Distribuciones univariadas (histogramas, boxplots, estadísticas)
      │
  PASO 4: Distribuciones bivariadas y correlaciones
      │
  PASO 5: Análisis categórico (frecuencias, groupby)
      │
  PASO 6: Detección de outliers
      │
  PASO 7: Transformaciones (normalizar, estandarizar, encoding, binning)
      │
  PASO 8: Documentar hallazgos y decisiones
```
"""),

code(r"""
# Pipeline EDA completo en una función reutilizable
def pipeline_eda(df, col_target="monto"):
    print("=" * 55)
    print("PIPELINE EDA - Dataset de Transacciones")
    print("=" * 55)

    # Paso 1: Perfil
    print("\n--- PASO 1: Perfil ---")
    print("Forma:", df.shape)
    print("Nulos:\n", df.isnull().sum()[df.isnull().sum() > 0] if df.isnull().sum().sum() > 0 else "  Ninguno")
    print("Duplicados:", df.duplicated().sum())

    # Paso 2: Estadísticas
    print("\n--- PASO 2: Estadísticas de '{0}' ---".format(col_target))
    s = df[col_target]
    print("  Media:   {:>12,.1f}".format(s.mean()))
    print("  Mediana: {:>12,.1f}".format(s.median()))
    print("  Std:     {:>12,.1f}".format(s.std()))
    print("  Skew:    {:>12.3f}".format(s.skew()))

    # Paso 3: Outliers
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr_val = q3 - q1
    out_iqr = ((s < q1 - 1.5 * iqr_val) | (s > q3 + 1.5 * iqr_val)).sum()
    z = (s - s.mean()).abs() / s.std()
    out_z = (z > 3).sum()
    print("\n--- PASO 3: Outliers ---")
    print("  Por IQR: {0}  |  Por z-score: {1}".format(out_iqr, out_z))

    # Paso 4: Resumen por categorías
    print("\n--- PASO 4: Mediana de '{0}' por categorica ---".format(col_target))
    for col_cat in ["ciudad", "categoria", "metodo_pago"]:
        gr = df.groupby(col_cat)[col_target].median().round(0)
        mejor = gr.idxmax()
        print("  {0}: max en '{1}' ({2:,.0f})".format(col_cat, mejor, gr[mejor]))

    print("\nPipeline EDA completado.")

pipeline_eda(df)
"""),

code(r"""
# Dashboard visual compacto
fig, axes = plt.subplots(2, 3, figsize=(15, 8))

# 1. Histograma de monto
axes[0, 0].hist(df["monto"], bins=25, color="#4C72B0", edgecolor="white", alpha=0.8)
axes[0, 0].set_title("Distribucion de Montos")
axes[0, 0].set_xlabel("Monto ($)")

# 2. Boxplot
axes[0, 1].boxplot(df["monto"], patch_artist=True,
                   boxprops=dict(facecolor="#4C72B0", alpha=0.6),
                   medianprops=dict(color="red"))
axes[0, 1].set_title("Boxplot de Montos")

# 3. Frecuencia de categorias
vc_cat = df["categoria"].value_counts()
axes[0, 2].barh(vc_cat.index, vc_cat.values, color="#55A868", edgecolor="white")
axes[0, 2].set_title("Categorias")

# 4. Monto mediano por ciudad
gr_ciudad = df.groupby("ciudad")["monto"].median().sort_values()
axes[1, 0].barh(gr_ciudad.index, gr_ciudad.values, color="#C44E52", edgecolor="white")
axes[1, 0].set_title("Mediana de monto por ciudad")

# 5. Distribución por método de pago
vc_metodo = df["metodo_pago"].value_counts()
axes[1, 1].pie(vc_metodo.values, labels=vc_metodo.index, autopct="%1.1f%%",
               colors=["#4C72B0", "#55A868", "#C44E52"])
axes[1, 1].set_title("Metodo de pago")

# 6. Monto normalizado
monto_n = (df["monto"] - df["monto"].min()) / (df["monto"].max() - df["monto"].min())
axes[1, 2].hist(monto_n, bins=25, color="#8172B2", edgecolor="white", alpha=0.8)
axes[1, 2].set_title("Monto normalizado [0,1]")
axes[1, 2].set_xlabel("Monto norm.")

plt.suptitle("Dashboard EDA - Transacciones", fontsize=13, y=1.01)
plt.tight_layout()
plt.show()
"""),
]


# ===================================================================== #
# 11. ERRORES COMUNES
# ===================================================================== #
C += [
md(r"""
## 11. Errores comunes en EDA y transformación

### Error 1: Data leakage al normalizar

El error más peligroso y más común en la industria:

```python
# MAL: calculas min/max sobre TODOS los datos (incluye test)
scaler_fit = df["monto"].min(), df["monto"].max()
df["monto_norm"] = (df["monto"] - scaler_fit[0]) / (scaler_fit[1] - scaler_fit[0])

# BIEN: calculas min/max solo sobre TRAIN
train_min = df_train["monto"].min()
train_max = df_train["monto"].max()
df_train["monto_norm"] = (df_train["monto"] - train_min) / (train_max - train_min)
df_test["monto_norm"]  = (df_test["monto"]  - train_min) / (train_max - train_min)
```

El conjunto de test simula "datos futuros". Si calculamos estadísticas sobre él,
le estamos pasando información del futuro al modelo.

### Error 2: Correlación ≠ Causalidad

```
  Correlacion alta entre:         NO significa que:
  helados vendidos y ahogados  →  comer helado cause ahogarse
  zapatos y educación          →  los zapatos eduquen
  (ambas son causadas por una tercera variable: temperatura / riqueza)
```

### Error 3: Imputar antes de explorar

Si rellenas los nulos antes de ver cuántos hay y dónde están, puedes:
- Enmascarar un problema de calidad de datos grave.
- Imponer una distribución artificial.
- Introducir sesgo si los nulos no son aleatorios (MNAR).

**Regla:** explora primero, imputa después.

### Error 4: Normalizar variables categóricas

`pd.get_dummies` ya produce valores `0/1`. Normalizarlas no tiene sentido
y puede corromper la representación binaria.

### Error 5: Olvidar el contexto de negocio

Un outlier estadístico puede ser completamente válido desde el negocio
(una compra corporativa de $2M es real). Siempre valida los outliers
con quien conoce los datos.
"""),
]


# ===================================================================== #
# 12. RESUMEN + QUIZ + RETOS
# ===================================================================== #
C += [
md(r"""
## 12. Resumen de la clase

| Concepto | Herramienta clave | Nota |
|---|---|---|
| **Perfilado** | `df.shape`, `dtypes`, `isnull()`, `nunique()` | primer paso siempre |
| **Distribución univariada** | `hist`, `boxplot`, `mean/median/std/IQR` | detecta sesgo y outliers |
| **Correlación** | `.corr()`, `scatter`, heatmap | lineal, no causal |
| **Categóricas** | `value_counts()`, `groupby` | frecuencias y promedios |
| **Outliers** | z-score, método IQR | contexto decide qué hacer |
| **Normalización** | `(x - min) / (max - min)` | escala [0,1] |
| **Estandarización** | `(x - media) / std` | media=0, std=1 |
| **Binning** | `pd.cut`, `pd.qcut` | igual ancho vs. igual frecuencia |
| **Label Encoding** | `.map(dict)` | solo para ordinales |
| **One-Hot** | `pd.get_dummies` | para nominales |
| **Imputación** | `.fillna(media/mediana)`, `.ffill()` | calcular en train |

### Lo más importante:
> **EDA no es un paso opcional.** Es la diferencia entre un modelo que aprende
> de datos y uno que aprende de artefactos. Haz siempre el diagnóstico antes de
> cualquier transformación.
"""),

md(r"""
## 13. Glosario

| Término | Definición |
|---|---|
| **EDA** | Análisis Exploratorio de Datos: diagnóstico y comprensión de un dataset |
| **Perfilado** | resumen rápido: tipos, nulos, cardinalidad, estadísticas básicas |
| **Distribución** | cómo se distribuyen los valores de una variable |
| **Sesgo (skewness)** | asimetría de la distribución; sesgo > 0 = cola a la derecha |
| **IQR** | Rango Intercuartílico = Q3 - Q1; mide dispersión del 50% central |
| **Outlier** | valor atípico que se aleja significativamente del resto |
| **Z-score** | número de desviaciones estándar que un valor está de la media |
| **Correlación** | medida de relación lineal entre dos variables (-1 a +1) |
| **Normalización** | escalar a [0,1] con min/max |
| **Estandarización** | centrar en media=0 con std=1 |
| **Binning** | discretizar una variable continua en intervalos |
| **Label Encoding** | asignar enteros a categorías; para variables ordinales |
| **One-Hot Encoding** | columna binaria por cada categoría; para nominales |
| **Imputación** | rellenar valores faltantes con un estadístico o modelo |
| **Data Leakage** | usar información del conjunto de test en el entrenamiento |
| **MNAR** | Missing Not At Random: los nulos tienen un patrón no aleatorio |
"""),

md(r"""
## 14. Quiz de autoevaluación

Responde mentalmente y luego ejecuta la celda para verificar.

1. ¿Cuál es la diferencia entre **normalización** y **estandarización**?
2. ¿Cuándo preferirías **mediana** sobre **media** para imputar nulos?
3. ¿Qué problema tiene aplicar **Label Encoding** a `metodo_pago` (efectivo, tarjeta, transferencia)?
4. ¿Por qué calcular `min/max` de normalización sobre el dataset completo (train+test) es un error?
5. ¿`pd.cut` o `pd.qcut`? Tienes una distribución muy sesgada y necesitas bins balanceados.
"""),

code(r"""
respuestas = {
    1: ("Normalización: mapea a [0,1] con (x-min)/(max-min). "
        "Estandarización: centra en 0 con (x-media)/std. "
        "Normalización acota el rango; estandarización no."),
    2: ("Cuando la distribución está sesgada o tiene outliers. "
        "La media es arrastrada por valores extremos; la mediana no."),
    3: ("Asigna orden implícito (efectivo=0 < tarjeta=1 < transferencia=2) "
        "que no existe en la realidad. Un modelo lineal lo interpretaría "
        "como si transferencia valiera el doble que efectivo."),
    4: ("Data leakage: el conjunto de test simula datos futuros. "
        "Si calculamos estadísticas sobre él, el modelo aprende información "
        "que en producción no estaría disponible."),
    5: ("pd.qcut: produce bins de igual frecuencia, ideal para distribuciones "
        "sesgadas donde pd.cut dejaría la mayoría de datos en un solo bin."),
}
for k, v in respuestas.items():
    print("{0}. {1}\n".format(k, v))
"""),

md(r"""
## 15. Retos para practicar

1. **Outliers bidimensionales:** un punto puede ser normal en X y normal en Y,
   pero extremo en su combinación. Busca "Mahalanobis distance" y explica cuándo usarla.

2. **Imputación avanzada:** investiga `KNNImputer` de scikit-learn. ¿Cuándo es
   mejor que imputar con la mediana?

3. **Sesgo de muestra:** imagina que el dataset de transacciones solo incluye
   ventas completadas. Las transacciones canceladas no aparecen. ¿Cómo afecta
   esto a un modelo que intenta predecir cancelaciones?

4. **Encoding de alta cardinalidad:** si `ciudad` tuviera 500 valores únicos,
   one-hot crearía 500 columnas. Investiga **Target Encoding** como alternativa.

5. **Pipeline con sklearn:** investiga `sklearn.pipeline.Pipeline` y
   `sklearn.preprocessing.StandardScaler`. ¿Cómo encapsulan las transformaciones
   para evitar data leakage automáticamente?

---

### Siguiente paso

- **practice01.ipynb** — 10 ejercicios graduales de EDA y transformación.
- **practice02.ipynb** — EDA completo del dataset de transacciones respondiendo preguntas de negocio.
- **homework01.ipynb** y **homework02.ipynb** — tareas autocalificables.
"""),
]


# ===================================================================== #
# CELDAS ADICIONALES — insertar_despues para alcanzar 80+ celdas
# ===================================================================== #

def insertar_despues(celdas, marcador_texto, nuevas):
    """Inserta 'nuevas' justo después de la primera celda cuyo source contiene 'marcador_texto'."""
    for i, c in enumerate(celdas):
        if marcador_texto in c.source:
            return celdas[: i + 1] + nuevas + celdas[i + 1 :]
    return celdas + nuevas


# --- Ampliación motivación: historia del EDA ---
EXTRA_EDA_HISTORIA = [
md(r"""
### Un poco de historia: John Tukey y el EDA

El término "Análisis Exploratorio de Datos" fue acuñado por **John Tukey** en su
libro de 1977. Tukey argumentaba que los estadísticos pasaban demasiado tiempo
confirmando hipótesis previas y muy poco tiempo **dejando que los datos hablen**.

Sus contribuciones incluyen:
- El **boxplot** (que vimos hoy).
- La **stem-and-leaf plot**.
- El concepto de datos **robustos** (resistentes a outliers).

> *"El análisis de datos, y la estadística, son ciencias incompletas. Cada vez
> que analizamos datos, necesitamos estar listos para ser sorprendidos."* — Tukey

Esta filosofía es el corazón del EDA: no llegues al dataset con conclusiones
pre-hechas. Llega con preguntas abiertas.
"""),
]

# --- Ampliación sobre tipos de nulos ---
EXTRA_TIPOS_NULOS = [
md(r"""
### Los tres tipos de valores faltantes

No todos los nulos son iguales. La teoría estadística distingue:

| Tipo | Nombre | Descripción | Implicación |
|---|---|---|---|
| **MCAR** | Missing Completely At Random | Los nulos no dependen de ninguna variable | Imputar con media/mediana es seguro |
| **MAR** | Missing At Random | Los nulos dependen de otras variables observadas | Imputar con modelo usando esas variables |
| **MNAR** | Missing Not At Random | Los nulos dependen del valor faltante mismo | Difícil de manejar; puede haber sesgo |

**Ejemplo MNAR:** en una encuesta de ingresos, las personas con ingresos más
altos tienden a no responder. Los nulos en "ingreso" no son aleatorios; están
correlacionados con el ingreso mismo. Imputar con la media subestimaría el
ingreso promedio real.

Diagnosticar el tipo de nulo requiere conocimiento del dominio y análisis de patrones.
"""),
]

# --- Ampliación: violin plot ---
EXTRA_VIOLIN = [
md(r"""
### Violinplot: más información que el boxplot

El **violinplot** combina un boxplot con una estimación de densidad (KDE).
Muestra no solo Q1, mediana y Q3, sino la forma completa de la distribución.
"""),
code(r"""
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Boxplot por categoría
categorias = df["categoria"].unique()
data_por_cat = [df[df["categoria"] == c]["monto"].values for c in sorted(categorias)]

axes[0].boxplot(data_por_cat, labels=sorted(categorias), patch_artist=True)
axes[0].set_title("Boxplot: monto por categoria")
axes[0].set_ylabel("Monto ($)")
axes[0].tick_params(axis="x", rotation=20)

# Violinplot manual con histogramas rotativos (matplotlib no tiene violinplot
# nativo tan bueno; mostramos densidad superpuesta)
for i, (cat, datos) in enumerate(zip(sorted(categorias), data_por_cat)):
    axes[1].hist(datos, bins=12, alpha=0.4, label=cat)

axes[1].set_title("Distribucion de monto por categoria")
axes[1].set_xlabel("Monto ($)")
axes[1].legend(fontsize=8)

plt.tight_layout()
plt.show()

print("Observa si alguna categoria tiene una distribucion bimodal o muy diferente.")
"""),
]

# --- Ampliación: scatter matrix ---
EXTRA_SCATTER_MATRIX = [
md(r"""
### Scatter matrix: todas las relaciones de un vistazo

Cuando tienes varias variables numéricas, la **scatter matrix** (o pair plot)
muestra todas las combinaciones de scatter plots de una vez. En la diagonal
suele mostrarse la distribución de cada variable.
"""),
code(r"""
# Versión manual de scatter matrix con matplotlib (sin seaborn)
cols_num = ["monto", "monto_log"]  # usamos las que hemos creado

n = len(cols_num)
fig, axes = plt.subplots(n, n, figsize=(8, 7))

colores = {"Bogota": "#4C72B0", "Medellin": "#55A868", "Cali": "#C44E52",
           "Barranquilla": "#8172B2", "Bucaramanga": "#CCB974"}

for i, col_y in enumerate(cols_num):
    for j, col_x in enumerate(cols_num):
        ax = axes[i, j]
        if i == j:
            ax.hist(df[col_x], bins=20, color="#4C72B0", alpha=0.7)
        else:
            for ciudad, grp in df.groupby("ciudad"):
                ax.scatter(grp[col_x], grp[col_y], alpha=0.4, s=10,
                           color=colores.get(ciudad, "gray"), label=ciudad)
        if i == n - 1:
            ax.set_xlabel(col_x, fontsize=8)
        if j == 0:
            ax.set_ylabel(col_y, fontsize=8)
        ax.tick_params(labelsize=7)

plt.suptitle("Scatter matrix (coloreado por ciudad)", fontsize=10)
plt.tight_layout()
plt.show()
"""),
]

# --- Ampliación: encoding avanzado ---
EXTRA_ENCODING_AVANZADO = [
md(r"""
### Encoding avanzado: frecuencia y target encoding

Cuando una variable categórica tiene alta cardinalidad (muchas categorías
únicas), one-hot encoding crea demasiadas columnas. Dos alternativas:

**Frequency Encoding:** reemplaza cada categoría por su frecuencia relativa.

```python
freq_map = df["ciudad"].value_counts(normalize=True).to_dict()
df["ciudad_freq"] = df["ciudad"].map(freq_map)
```

**Target Encoding:** reemplaza cada categoría por el promedio del target en
esa categoría. Muy efectivo pero propenso a data leakage si no se calcula
solo en train.

```python
# Calcular SOLO en train
target_map = df_train.groupby("ciudad")["monto"].mean().to_dict()
df_train["ciudad_target"] = df_train["ciudad"].map(target_map)
df_test["ciudad_target"]  = df_test["ciudad"].map(target_map)
```
"""),
code(r"""
# Frequency encoding en práctica
freq_map = df["ciudad"].value_counts(normalize=True).to_dict()
df["ciudad_freq"] = df["ciudad"].map(freq_map)

print("=== FREQUENCY ENCODING: ciudad ===")
muestra = df[["ciudad", "ciudad_freq"]].drop_duplicates().sort_values("ciudad_freq", ascending=False)
print(muestra.to_string(index=False))
print("\nLa ciudad mas frecuente tiene el valor mas alto.")
"""),
]

# --- Ampliación: transformación logarítmica ---
EXTRA_LOG = [
md(r"""
### Transformación logarítmica: domar el sesgo

Cuando una distribución tiene sesgo fuerte a la derecha (muchos valores
pequeños y pocos muy grandes), la **transformación logarítmica** la acerca
a una distribución normal.

```
  Original:  ████████▓▓▒░░         sesgado a la derecha
  log(x):    ▒▒▓▓████▓▓▒▒░         más simétrico
```

Usamos `log(1 + x)` en vez de `log(x)` para manejar ceros sin error.

Los algoritmos que asumen normalidad (regresión lineal, Gaussian NB) se
benefician enormemente de esta transformación.
"""),
code(r"""
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

axes[0].hist(df["monto"], bins=30, color="#4C72B0", edgecolor="white", alpha=0.8)
axes[0].set_title("Monto original (sesgado)")
axes[0].set_xlabel("Monto ($)")
axes[0].text(0.65, 0.85, "Skew: {:.2f}".format(df["monto"].skew()),
             transform=axes[0].transAxes, fontsize=10, color="red")

monto_log = np.log1p(df["monto"])
axes[1].hist(monto_log, bins=30, color="#55A868", edgecolor="white", alpha=0.8)
axes[1].set_title("log(1 + Monto) (mas simetrico)")
axes[1].set_xlabel("log(1 + Monto)")
axes[1].text(0.05, 0.85, "Skew: {:.2f}".format(monto_log.skew()),
             transform=axes[1].transAxes, fontsize=10, color="green")

for ax in axes:
    ax.set_ylabel("Frecuencia")

plt.tight_layout()
plt.show()
"""),
]

# --- Ampliación: análisis temporal básico ---
EXTRA_TEMPORAL = [
md(r"""
### Análisis temporal: la dimensión del tiempo

Muchos datasets tienen una columna de fecha. El tiempo es una variable especial
porque introduce **dependencia temporal**: lo que pasa hoy depende de lo que
pasó ayer. El EDA temporal responde:

- ¿Cómo evolucionan las ventas en el tiempo?
- ¿Hay estacionalidad (patrones que se repiten)?
- ¿Hay tendencia (creciente o decreciente)?
"""),
code(r"""
# Convertir fecha y analizar tendencia mensual
df["fecha"] = pd.to_datetime(df["fecha"])
df["mes"] = df["fecha"].dt.to_period("M").astype(str)

ventas_mes = df.groupby("mes")["monto"].agg(["sum", "count", "mean"]).reset_index()
ventas_mes.columns = ["mes", "total", "n_transacciones", "ticket_medio"]

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(range(len(ventas_mes)), ventas_mes["total"] / 1e6, color="#4C72B0",
       edgecolor="white", alpha=0.8)
ax.set_xticks(range(len(ventas_mes)))
ax.set_xticklabels(ventas_mes["mes"], rotation=40, ha="right", fontsize=8)
ax.set_ylabel("Ventas totales (millones $)")
ax.set_title("Ventas totales por mes")
plt.tight_layout()
plt.show()

print(ventas_mes.head(6).to_string(index=False))
"""),
]

# Insertar bloques en posiciones estratégicas
C = insertar_despues(C, "Haz siempre el diagnóstico antes de", EXTRA_EDA_HISTORIA)
C = insertar_despues(C, "Regla de oro del perfilado:", EXTRA_TIPOS_NULOS)
C = insertar_despues(C, "Observa si alguna categoria tiene", EXTRA_SCATTER_MATRIX)
C = insertar_despues(C, "muestra no solo Q1, mediana y Q3", EXTRA_VIOLIN)
C = insertar_despues(C, "escalar o transformar", EXTRA_LOG)
C = insertar_despues(C, "Frequency Encoding:", EXTRA_ENCODING_AVANZADO)
C = insertar_despues(C, "solo para nominales", EXTRA_TEMPORAL)


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase07", "lecture.ipynb")
build(os.path.abspath(ruta), C)
