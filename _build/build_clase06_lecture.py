"""Construye curso/clase06/lecture.ipynb — Pandas: Series, DataFrames y análisis."""
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
# Clase 6 · Pandas: Series, DataFrames y análisis de datos

### Fundamentos de Programación para Ciencia de Datos

> *"Los datos son el nuevo petróleo, pero sin refinería no sirven de nada."*

---

**Duración:** 3 horas · **Modalidad:** notebook interactivo

En las clases anteriores aprendimos a manejar listas, diccionarios y NumPy.
Pero la realidad de los datos es heterogénea: una tabla de ventas mezcla fechas,
textos (ciudad, categoría) y números (monto). NumPy no está diseñado para eso.

**Pandas** es la herramienta que cubre ese hueco. Es la librería más usada en
ciencia de datos en Python: prácticamente cualquier proyecto de análisis de datos
comienza con `import pandas as pd`.

Hoy aprenderemos a:

- Crear y manipular **Series** y **DataFrames**.
- **Leer** datos desde CSV.
- **Seleccionar y filtrar** filas y columnas.
- **Transformar** columnas con `apply` y funciones.
- Manejar **nulos** (`isna`, `fillna`, `dropna`).
- **Agrupar** con `groupby` y agregar con `agg`.
- **Combinar** DataFrames con `merge` y `concat`.
- Reconocer los **errores comunes** y cómo evitarlos.
"""),

md(r"""
## Mapa de la clase

| Bloque | Tiempo | Qué haremos |
|---|---|---|
| 1. Motivación | 15 min | Por qué pandas, qué resuelve que NumPy no |
| 2. Series | 25 min | Creación, índice, dtype, operaciones |
| 3. DataFrame | 25 min | Concepto, columnas, relación con dicts |
| 4. Leer CSV | 15 min | `pd.read_csv`, dtypes automáticos |
| 5. Inspección | 15 min | `head`, `info`, `describe`, `shape` |
| 6. Selección: `loc` / `iloc` | 25 min | Etiquetas vs posiciones |
| 7. Filtrado booleano | 20 min | `&`, `|`, condiciones compuestas |
| 8. Crear columnas y `apply` | 20 min | Transformar datos |
| 9. Nulos | 15 min | `isna`, `fillna`, `dropna` |
| 10. `groupby` y `agg` | 25 min | Split-apply-combine |
| 11. `sort_values`, `rename`, `reset_index` | 10 min | Ordenar y renombrar |
| 12. `merge` y `concat` | 20 min | Combinar DataFrames |
| 13. Errores comunes | 10 min | SettingWithCopyWarning, `loc` vs `iloc` |
| 14. Resumen, quiz y retos | 15 min | Cierre |

> 🧭 **Cómo usar este notebook:** lee cada celda de texto *antes* de ejecutar
> la celda de código que le sigue. Detente en los bloques **🤔 ¿Qué pasaría si...?**
> e intenta responder mentalmente antes de continuar.
"""),
]


# ===================================================================== #
# 1. MOTIVACIÓN
# ===================================================================== #
C += [
md(r"""
## 1. Motivación: ¿qué resuelve pandas que NumPy no?

Imagina que recibes una tabla de ventas de una cadena de tiendas:

| id | fecha | ciudad | categoria | metodo_pago | monto |
|---|---|---|---|---|---|
| 1004 | 2024-01-01 | Medellin | papeleria | tarjeta | 73078 |
| 1079 | 2024-01-01 | Cali | tecnologia | efectivo | 110323 |
| 1067 | 2024-01-05 | Barranquilla | aseo | efectivo | 205064 |

Con NumPy podrías guardar la columna `monto` (números) y calcular estadísticas.
Pero NumPy no maneja bien:

- Columnas de **tipos distintos** (enteros, texto, fechas en la misma tabla).
- **Etiquetas** para filas y columnas (en vez de solo índices numéricos).
- Operaciones de **agrupación**: "total de ventas por ciudad".
- **Valores faltantes** (NaN) de forma natural.
- Lectura directa de **CSV, Excel, SQL**.

Pandas nació exactamente para cubrir estas necesidades. Internamente usa NumPy
para los cálculos numéricos, pero agrega toda la capa de etiquetas y
heterogeneidad que los datos reales exigen.
"""),

md(r"""
### La analogía: Excel en Python — pero programable

Si sabes usar Excel (tablas, filtros, tablas dinámicas), ya tienes la intuición.
Pandas hace lo mismo, pero:

- Con **código reproducible**: cada transformación queda documentada.
- A **escala**: funciona igual con 100 filas que con 100 millones.
- Integrado con **todo el ecosistema** de Python (visualización, machine learning, etc.).

El tradeoff: hay una curva inicial para aprender la API. Eso es exactamente lo
que haremos hoy.

```
        NumPy                   Pandas
   ┌────────────────┐      ┌─────────────────────┐
   │ ndarray homog. │      │ Series / DataFrame  │
   │ solo números   │      │ tipos mixtos        │
   │ índice 0,1,2…  │      │ índice con etiquetas│
   │ sin nombres    │ ───▶ │ columnas nombradas  │
   │ NaN manual     │      │ NaN nativo          │
   │ CSV con np.genfromtxt│ │ pd.read_csv() directo│
   └────────────────┘      └─────────────────────┘
```

> 💡 Pandas **no reemplaza** NumPy: lo usa internamente y ambas se complementan.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Intentaras guardar la tabla completa (id, fecha, ciudad, monto) en un array de
NumPy de un solo tipo. ¿Qué tipo elegiría NumPy? ¿Podrías hacer `monto.mean()`?
Guarda tu respuesta: la responderemos en la siguiente celda.
"""),

code(r"""
import numpy as np

# NumPy convierte todo al tipo 'más general' — que aquí sería str.
tabla = np.array([
    [1004, "2024-01-01", "Medellin", "papeleria", "tarjeta", 73078],
    [1079, "2024-01-01", "Cali",     "tecnologia","efectivo",110323],
])
print("dtype:", tabla.dtype)         # <U21 — texto Unicode
print("columna monto:", tabla[:, 5]) # aún es str

# Intentar mean() falla porque son strings:
try:
    print(tabla[:, 5].astype(float).mean())  # hay que convertir manualmente
except Exception as e:
    print("Error:", e)

# Con pandas, esto se maneja automáticamente.
"""),
]


# ===================================================================== #
# 2. SERIES
# ===================================================================== #
C += [
md(r"""
## 2. Series: el bloque fundamental de pandas

Una **Series** es una columna de datos con un **índice**. Es como un array de
NumPy, pero con etiquetas. Piénsala como un diccionario ordenado donde:

- las **claves** son el índice (pueden ser enteros, texto, fechas...),
- los **valores** son los datos,
- todos los valores tienen un **dtype** (tipo de dato).

```
índice   valor
──────   ─────
  0      73078    ← monto de la transacción 0
  1     110323
  2     205064
  3      66135
  dtype: int64
```
"""),

code(r"""
import pandas as pd

# Crear una Series desde una lista
montos = pd.Series([73078, 110323, 205064, 66135])
print(montos)
print()
print("dtype :", montos.dtype)
print("índice:", montos.index.tolist())
"""),

md(r"""
### Series con índice personalizado

El índice no tiene que ser numérico. Puede ser cualquier etiqueta significativa:
"""),

code(r"""
# Índice con IDs de transacción
montos_id = pd.Series(
    [73078, 110323, 205064, 66135],
    index=[1004, 1079, 1067, 1063]
)
print(montos_id)
print()
# Acceder por etiqueta (igual que un diccionario)
print("Monto de la transacción 1067:", montos_id[1067])
"""),

md(r"""
### Crear una Series desde un diccionario

Cuando ya tienes un diccionario, convertirlo a Series es directo. Las claves
se convierten en el índice:
"""),

code(r"""
ventas_ciudad = pd.Series({
    "Bogota":        5_240_000,
    "Medellin":      4_180_000,
    "Cali":          3_610_000,
    "Barranquilla":  2_950_000,
    "Bucaramanga":   2_100_000,
})
print(ventas_ciudad)
print()
print("Total ventas:", ventas_ciudad.sum())
print("Ciudad top: ", ventas_ciudad.idxmax())
"""),

md(r"""
### Operaciones vectorizadas en Series

Como en NumPy, las operaciones matemáticas se aplican **elemento a elemento**,
sin necesidad de bucles:
"""),

code(r"""
# Convertir montos de COP a USD (tasa: 1 USD = 4100 COP)
tasa = 4100
montos_usd = montos / tasa
print("Montos en USD:")
print(montos_usd.round(2))
print()

# Filtrado: montos mayores a $100.000
grandes = montos[montos > 100_000]
print("Transacciones > $100.000:")
print(grandes)
"""),

md(r"""
### Comparación Series vs lista vs diccionario

```
                lista        diccionario      Series
─────────────────────────────────────────────────────
acceder         [i]           [key]           [label] o .loc[label]
iterar          for x in      for k,v in      for x in (valores)
filtrar         lista[cond]   manual           serie[serie > x]
estadísticas    manual        manual           .mean(), .std(), .value_counts()
dtype           mixto         mixto            homogéneo (optimizado)
alineación      por posición  por clave        por etiqueta del índice
```

La alineación **por etiqueta** es la superpotencia de pandas: dos Series se
alinean automáticamente por su índice, no por posición.
"""),

code(r"""
# Alineación automática: las sumas se hacen por etiqueta, no por posición
enero = pd.Series({"Bogota": 500, "Cali": 300, "Medellin": 400})
febrero = pd.Series({"Medellin": 350, "Bogota": 550, "Barranquilla": 200})

print("Enero + Febrero (alineado por ciudad):")
print(enero + febrero)
# NaN donde no coinciden: pandas no inventa valores
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

¿Qué valor aparecería en `enero + febrero` para la ciudad `"Cali"`?
¿Y para `"Barranquilla"`? ¿Por qué aparece `NaN` en lugar de un error?

Esta es una decisión de diseño de pandas: cuando no puede hacer la operación
(falta un valor en uno de los operandos), produce `NaN` (*Not a Number*) para
señalar "dato faltante". Lo veremos en detalle en la sección de nulos.
"""),
]


# ===================================================================== #
# 3. DATAFRAME
# ===================================================================== #
C += [
md(r"""
## 3. DataFrame: la tabla de pandas

Un **DataFrame** es una tabla bidimensional: filas × columnas. Puedes pensarlo
como:

- Una colección de **Series** que comparten el mismo índice (una por columna).
- Una hoja de cálculo con superpoderes.
- Una tabla de base de datos en memoria.

```
         id      fecha        ciudad    categoria  metodo_pago   monto
       ──────────────────────────────────────────────────────────────
  0     1004  2024-01-01    Medellin    papeleria     tarjeta    73078
  1     1079  2024-01-01        Cali   tecnologia    efectivo   110323
  2     1067  2024-01-05  Barranquilla       aseo    efectivo   205064
       ↑                                                          ↑
    índice de fila                                           columna numérica
```

Cada columna es una **Series**. Todas las columnas comparten el mismo índice de
fila (0, 1, 2, …).
"""),

code(r"""
import pandas as pd

# Crear un DataFrame desde una lista de diccionarios
datos = [
    {"ciudad": "Bogota",    "categoria": "tecnologia", "monto": 320000},
    {"ciudad": "Medellin",  "categoria": "hogar",      "monto": 85000},
    {"ciudad": "Cali",      "categoria": "tecnologia", "monto": 150000},
    {"ciudad": "Bogota",    "categoria": "alimentos",  "monto": 45000},
    {"ciudad": "Medellin",  "categoria": "tecnologia", "monto": 210000},
]
df = pd.DataFrame(datos)
print(df)
"""),

code(r"""
# Propiedades básicas del DataFrame
print("Shape (filas, columnas):", df.shape)
print("Columnas:", df.columns.tolist())
print("Índice:", df.index.tolist())
print()
print("Tipos de datos:")
print(df.dtypes)
"""),

md(r"""
### Crear DataFrame desde un diccionario de listas

Es otra forma muy común: las claves son los nombres de columna,
los valores son listas (del mismo largo):
"""),

code(r"""
# Formato columnar: cada clave es una columna
df2 = pd.DataFrame({
    "ciudad":   ["Bogota", "Medellin", "Cali"],
    "monto":    [320000,   85000,      150000],
    "metodo":   ["tarjeta","efectivo", "transferencia"],
})
print(df2)
print()
# Acceder a una columna: devuelve una Series
print("Columna 'monto':")
print(df2["monto"])
"""),

md(r"""
### La relación entre DataFrame y Series

Cada columna de un DataFrame **es una Series**:

```
df["monto"]  →  Series con índice 0, 1, 2, ...
df["ciudad"] →  Series con índice 0, 1, 2, ...
```

Y un DataFrame es, conceptualmente, un diccionario de Series que comparten el
mismo índice de fila. Por eso, todas las operaciones que aprendiste para Series
funcionan sobre las columnas de un DataFrame.
"""),

code(r"""
# Demostración: la columna 'monto' es una Series
col = df["monto"]
print(type(col))
print(col.mean())    # promedio
print(col.max())     # máximo
print(col.std())     # desviación estándar
"""),
]


# ===================================================================== #
# 4. LEER CSV CON pd.read_csv
# ===================================================================== #
C += [
md(r"""
## 4. Leer CSV con `pd.read_csv`

En la práctica, los datos vienen de archivos. `pd.read_csv` es la función más
usada para cargar datos en pandas. Con una sola línea obtienes un DataFrame listo:
"""),

code(r"""
import os
import pandas as pd

# Ruta al dataset de transacciones del curso
ruta = os.path.join("..", "datasets", "transacciones.csv")
df = pd.read_csv(ruta)

print("Shape:", df.shape)
print()
print(df.head())   # primeras 5 filas
"""),

md(r"""
### Parámetros clave de `pd.read_csv`

```python
pd.read_csv(
    filepath,           # ruta o URL
    sep=",",            # separador (por defecto coma)
    index_col=None,     # columna que usará como índice (o None)
    usecols=["a","b"],  # solo leer ciertas columnas
    dtype={"monto": int},  # forzar tipos
    parse_dates=["fecha"],  # convertir columnas a datetime
    encoding="utf-8",   # codificación de caracteres
    nrows=100,          # leer solo las primeras N filas (útil para pruebas)
)
```

El parámetro más importante que *no* se suele poner es `dtype`:
pandas **infiere automáticamente** los tipos de cada columna, y casi siempre lo
hace bien. Pero conviene verificar con `df.dtypes`.
"""),

code(r"""
# Leemos con parse_dates para que 'fecha' sea datetime, no texto
df = pd.read_csv(ruta, parse_dates=["fecha"])

print("Tipos de datos tras read_csv:")
print(df.dtypes)
print()
print("Primera fila:")
print(df.iloc[0])
"""),

md(r"""
### ¿Qué hace `pd.read_csv` por dentro?

En la Clase 1 leímos el mismo CSV con `csv.DictReader` y cada fila era un
diccionario de strings. Teníamos que convertir los tipos a mano.

`pd.read_csv` hace todo eso automáticamente:
1. Lee línea por línea.
2. Infiere el tipo de cada columna (int, float, str, datetime).
3. Convierte los valores al tipo correcto.
4. Construye el DataFrame completo.

Lo que tardaba 10 líneas en Python puro ahora es 1 línea. Y además es más
rápido porque la lectura está implementada en C.
"""),
]


# ===================================================================== #
# 5. INSPECCIÓN DEL DATAFRAME
# ===================================================================== #
C += [
md(r"""
## 5. Inspección: conocer los datos antes de analizarlos

Antes de filtrar, agrupar o modelar, siempre hay que **conocer** los datos.
Pandas tiene un toolkit de inspección muy completo:
"""),

code(r"""
# head() y tail(): primeras / últimas filas
print("=== head(3) ===")
print(df.head(3))
print()
print("=== tail(3) ===")
print(df.tail(3))
"""),

code(r"""
# info(): resumen estructural — tipos, nulos, memoria
print("=== info() ===")
df.info()
"""),

code(r"""
# describe(): estadísticas descriptivas de columnas numéricas
print("=== describe() ===")
print(df.describe())
"""),

code(r"""
# shape, columns, dtypes: metadatos esenciales
print("Dimensiones:", df.shape)
print("Filas:", df.shape[0], "| Columnas:", df.shape[1])
print()
print("Nombres de columnas:", df.columns.tolist())
print()
print("Tipos de datos:")
print(df.dtypes)
"""),

code(r"""
# value_counts(): frecuencia de valores en columnas categóricas
print("Distribución por ciudad:")
print(df["ciudad"].value_counts())
print()
print("Distribución por método de pago:")
print(df["metodo_pago"].value_counts())
"""),

md(r"""
### Diagrama del flujo de inspección

```
  pd.read_csv(ruta)
        │
        ▼
  df.shape          ← ¿cuántas filas y columnas?
        │
        ▼
  df.dtypes         ← ¿qué tipo es cada columna?
        │
        ▼
  df.head()         ← ¿cómo se ven los datos?
        │
        ▼
  df.info()         ← ¿hay nulos? ¿cuánta memoria?
        │
        ▼
  df.describe()     ← ¿cuál es el rango, media, cuartiles?
        │
        ▼
  df["col"].value_counts()  ← ¿qué categorías hay?
```

Este flujo debería ser un **reflejo automático** cada vez que abras un dataset
nuevo. Nunca analices datos que no has inspeccionado primero.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

`df.describe()` muestra solo columnas numéricas por defecto. ¿Cómo podrías
incluir también las columnas de texto? Pista: `df.describe(include="all")`.
¿Qué información adicional aparece para la columna `"ciudad"`?
"""),
]


# ===================================================================== #
# 6. SELECCIÓN: loc E iloc
# ===================================================================== #
C += [
md(r"""
## 6. Selección: `df["col"]`, `loc` e `iloc`

Hay varias formas de "recortar" un DataFrame para quedarte con lo que necesitas.
Dominar la diferencia entre **etiquetas** (`.loc`) y **posiciones** (`.iloc`) es
esencial — y es fuente de confusión frecuente.

```
SELECCIÓN POR COLUMNA
─────────────────────
df["col"]           una columna (devuelve Series)
df[["col1","col2"]] varias columnas (devuelve DataFrame)

SELECCIÓN POR FILA + COLUMNA
─────────────────────────────
df.loc[etiq_fila, etiq_col]   por ETIQUETA (label-based)
df.iloc[pos_fila, pos_col]    por POSICIÓN entera (integer-based)
```
"""),

code(r"""
# Seleccionar una columna → Series
montos = df["monto"]
print(type(montos))
print(montos.head())
"""),

code(r"""
# Seleccionar varias columnas → DataFrame
sub = df[["ciudad", "monto"]]
print(sub.head())
"""),

code(r"""
# .loc — por ETIQUETA de fila y columna
# El índice de df es 0, 1, 2, ..., así que etiqueta == posición aquí.
print("fila 2, columna 'ciudad':", df.loc[2, "ciudad"])
print()
print("filas 0-3, columnas ciudad y monto:")
print(df.loc[0:3, ["ciudad", "monto"]])
"""),

code(r"""
# .iloc — por POSICIÓN entera (como slicing de listas)
print("fila en posición 2, columna en posición 2:")
print(df.iloc[2, 2])
print()
print("primeras 3 filas, primeras 2 columnas:")
print(df.iloc[:3, :2])
"""),

md(r"""
### Trazado de la diferencia loc vs iloc

Supón que tienes un DataFrame cuyo índice no empieza en 0:

```python
df_filtrado = df[df["ciudad"] == "Bogota"].reset_index(drop=True)
# los índices son ahora 0, 1, 2, ...  → loc y iloc coinciden

df_sin_reset = df[df["ciudad"] == "Bogota"]
# los índices son los ORIGINALES (ej. 4, 11, 23, ...)
# df.loc[4]  →  la fila con etiqueta 4
# df.iloc[0] →  la PRIMERA fila del resultado (etiqueta 4)
# ¡No son lo mismo!
```

| Operación | ¿Qué usa para navegar? | Ejemplo con índice 4, 11, 23 |
|---|---|---|
| `.loc[0]` | etiqueta | KeyError: 0 no existe |
| `.iloc[0]` | posición | devuelve la fila con etiqueta 4 |
| `.loc[4]` | etiqueta | devuelve la fila con etiqueta 4 |
| `.iloc[4]` | posición | devuelve la 5ª fila (etiqueta 23 si hay 5) |
"""),

code(r"""
# Demostración con índices no consecutivos
df_bta = df[df["ciudad"] == "Bogota"]  # índices originales del df completo
print("Índice de df_bta:", df_bta.index.tolist())
print()
primera_etiqueta = df_bta.index[0]
print("Primera etiqueta:", primera_etiqueta)
print("df_bta.loc[primera_etiqueta, 'monto']:", df_bta.loc[primera_etiqueta, "monto"])
print("df_bta.iloc[0, df.columns.get_loc('monto')]:", df_bta.iloc[0, df.columns.get_loc("monto")])
# Ambos dan el mismo monto — pero por caminos distintos
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Ejecutas `df.loc[5, "monto"]` después de haber filtrado el DataFrame por ciudad
y el índice 5 no existe en el resultado. ¿Obtendrías un error o un `NaN`?

Pruébalo: cambia `primera_etiqueta` por un número que sabes que no está en el
índice del DataFrame filtrado y observa el mensaje de error.
"""),
]


# ===================================================================== #
# 7. FILTRADO BOOLEANO
# ===================================================================== #
C += [
md(r"""
## 7. Filtrado booleano

El filtrado en pandas sigue el mismo patrón que en NumPy: crear una **máscara
booleana** (una Series de True/False) y usarla como índice del DataFrame.

```
  df["monto"] > 100_000
  ┌──────────────────────────┐
  │ 0   False                │
  │ 1    True                │
  │ 2    True                │
  │ ...                      │
  │ dtype: bool              │
  └──────────────────────────┘
         ↓
  df[ df["monto"] > 100_000 ]  → solo las filas donde es True
```
"""),

code(r"""
# Filtrar transacciones grandes
grandes = df[df["monto"] > 100_000]
print("Transacciones > $100.000:", len(grandes))
print(grandes.head())
"""),

code(r"""
# Filtrar por ciudad específica
bogota = df[df["ciudad"] == "Bogota"]
print("Transacciones en Bogota:", len(bogota))
print(bogota.head())
"""),

md(r"""
### Combinar condiciones con `&` y `|`

Para combinar condiciones, pandas usa `&` (Y) y `|` (O), **no** `and` / `or`.
Cada condición debe ir entre paréntesis:

```python
# CORRECTO:
df[(df["ciudad"] == "Bogota") & (df["monto"] > 100_000)]

# INCORRECTO — da error:
df[df["ciudad"] == "Bogota" and df["monto"] > 100_000]
```

¿Por qué? `and` de Python opera sobre un único valor True/False, pero aquí
tenemos una **Series** de booleans. `&` opera elemento a elemento.
"""),

code(r"""
# Ventas grandes en Bogota (Y lógico)
bta_grandes = df[(df["ciudad"] == "Bogota") & (df["monto"] > 100_000)]
print("Bogota y monto > 100k:", len(bta_grandes))

# Ventas en Bogota O en Medellin (O lógico)
bta_o_med = df[(df["ciudad"] == "Bogota") | (df["ciudad"] == "Medellin")]
print("Bogota o Medellin:", len(bta_o_med))
"""),

code(r"""
# isin(): forma elegante de "cualquiera de estos valores"
norte = df[df["ciudad"].isin(["Barranquilla", "Bucaramanga"])]
print("Ciudades del norte:", len(norte))
print(norte["ciudad"].value_counts())
"""),

code(r"""
# Negación: ~(tilde) invierte la máscara
no_efectivo = df[~(df["metodo_pago"] == "efectivo")]
print("Sin efectivo:", len(no_efectivo))
# Equivalente más legible:
no_efectivo2 = df[df["metodo_pago"] != "efectivo"]
print("Misma cuenta:", len(no_efectivo2))
"""),

md(r"""
### Trazado de filtrado combinado

Apliquemos el patrón metodología: queremos las transacciones de tecnología
con monto superior a $200.000.

**Pseudocódigo:**
```
mascara_cat   = df["categoria"] == "tecnologia"
mascara_monto = df["monto"] > 200_000
resultado     = df[ mascara_cat & mascara_monto ]
```

**Análisis:** Cada máscara tiene `len(df)` valores booleanos. La operación `&`
compara posición a posición (O(n)). El resultado es un DataFrame nuevo con solo
las filas donde ambas condiciones son True.
"""),

code(r"""
mascara_cat   = df["categoria"] == "tecnologia"
mascara_monto = df["monto"] > 200_000

print("filas que son tecnologia:", mascara_cat.sum())
print("filas con monto > 200k:", mascara_monto.sum())
print("filas con ambas condiciones:", (mascara_cat & mascara_monto).sum())

resultado = df[mascara_cat & mascara_monto]
print()
print(resultado[["id", "ciudad", "monto"]])
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

¿Cuántas filas devolvería `df[(df["monto"] > 500_000) | (df["categoria"] == "hogar")]`?
Antes de ejecutarlo, estima cuántas filas de cada condición hay por separado y
razona si el total será la suma, menos que la suma, o más.
"""),
]


# ===================================================================== #
# 8. CREAR Y TRANSFORMAR COLUMNAS
# ===================================================================== #
C += [
md(r"""
## 8. Crear y transformar columnas: asignación y `apply`

Una vez que tienes el DataFrame cargado, con frecuencia necesitas **crear nuevas
columnas** a partir de las existentes.

### Asignación directa (vectorizada)

La forma más eficiente: operar sobre columnas enteras, igual que con NumPy:
"""),

code(r"""
# Crear columna 'monto_usd' (tasa 1 USD = 4100 COP)
df["monto_usd"] = df["monto"] / 4100
print(df[["monto", "monto_usd"]].head())
"""),

code(r"""
# Crear columna booleana
df["es_grande"] = df["monto"] > 200_000
print(df[["monto", "es_grande"]].head())
print()
print("Transacciones grandes:", df["es_grande"].sum())
"""),

md(r"""
### `apply`: aplicar una función personalizada

Cuando la transformación no es una simple operación matemática, usamos `apply`.
Recibe una función y la aplica a cada elemento (con `axis=0`, a cada fila;
con ningún eje, a cada valor de la columna):
"""),

code(r"""
# Clasificar monto con una función
def clasificar_monto(m):
    if m < 50_000:
        return "bajo"
    elif m < 200_000:
        return "medio"
    else:
        return "alto"

df["segmento"] = df["monto"].apply(clasificar_monto)
print(df[["monto", "segmento"]].head(8))
print()
print("Distribución por segmento:")
print(df["segmento"].value_counts())
"""),

code(r"""
# Lambda: para funciones simples de una sola expresión
df["monto_miles"] = df["monto"].apply(lambda x: round(x / 1000, 1))
print(df[["monto", "monto_miles"]].head())
"""),

md(r"""
### `apply` con `axis=1`: operar sobre filas completas

Con `axis=1`, la función recibe cada **fila** como una Series. Útil cuando
la nueva columna depende de varias columnas:
"""),

code(r"""
def etiqueta_fila(fila):
    # 'fila' es una Series con todos los campos de esa fila
    if fila["ciudad"] == "Bogota" and fila["monto"] > 100_000:
        return "vip_bogota"
    elif fila["metodo_pago"] == "efectivo":
        return "efectivo"
    else:
        return "estandar"

df["tipo_cliente"] = df.apply(etiqueta_fila, axis=1)
print(df[["ciudad", "monto", "metodo_pago", "tipo_cliente"]].head(8))
"""),

md(r"""
### Nota de eficiencia: `apply` vs operaciones vectorizadas

```
velocidad  ◄──────────────────────────────────►  lentitud
  df["col"] * 2   >   np.where(...)   >   df["col"].apply(f)
  (vectorizado)      (semivectorizado)   (bucle en Python)
```

Usa `apply` cuando la lógica es compleja. Para operaciones matemáticas simples,
las operaciones vectorizadas son **5-100 veces más rápidas** en datasets grandes.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Intentas crear una columna con `df["nueva"] = df["monto"].apply(lambda x: x * 2)`
después de haber creado `df_bta = df[df["ciudad"] == "Bogota"]`, y luego haces
`df_bta["nueva"] = ...`. ¿Qué advertencia verías? (Es el famoso
`SettingWithCopyWarning` — lo veremos en la sección de errores comunes.)
"""),
]


# ===================================================================== #
# 9. MANEJO DE NULOS
# ===================================================================== #
C += [
md(r"""
## 9. Manejo de nulos: `isna`, `fillna`, `dropna`

En la vida real, los datos tienen valores faltantes. Pandas los representa con
`NaN` (Not a Number, de NumPy) o `pd.NaT` para fechas. Ignorarlos causa
resultados incorrectos; por eso hay que detectarlos y decidir qué hacer.

```
  Opciones ante un nulo
  ─────────────────────
  1. Ignorar (algunas operaciones como mean() ya lo hacen)
  2. Eliminar la fila/columna con dropna()
  3. Reemplazar con un valor fijo con fillna()
  4. Imputar (usar la media, la moda, interpolación, etc.)
```
"""),

code(r"""
import pandas as pd
import numpy as np

# Creamos un DataFrame con nulos artificiales para practicar
df_con_nulos = pd.DataFrame({
    "id":       [1, 2, 3, 4, 5],
    "ciudad":   ["Bogota", "Medellin", None, "Cali", "Bogota"],
    "monto":    [120000, np.nan, 85000, np.nan, 210000],
    "categoria":["tecnologia", "hogar", "hogar", "alimentos", None],
})
print(df_con_nulos)
"""),

code(r"""
# isna(): máscara de nulos (True = nulo)
print("Máscara de nulos:")
print(df_con_nulos.isna())
print()
# Contar nulos por columna
print("Nulos por columna:")
print(df_con_nulos.isna().sum())
"""),

code(r"""
# dropna(): eliminar filas con AL MENOS un nulo
df_limpio = df_con_nulos.dropna()
print("Tras dropna():", df_limpio.shape)
print(df_limpio)
print()
# dropna(subset=): solo si cierta columna tiene nulo
df_sin_monto_nulo = df_con_nulos.dropna(subset=["monto"])
print("Eliminando filas solo si 'monto' es nulo:", df_sin_monto_nulo.shape)
"""),

code(r"""
# fillna(): reemplazar nulos
df_relleno = df_con_nulos.copy()
df_relleno["monto"] = df_relleno["monto"].fillna(df_relleno["monto"].mean())
df_relleno["ciudad"] = df_relleno["ciudad"].fillna("Desconocida")
df_relleno["categoria"] = df_relleno["categoria"].fillna("otra")
print("Tras fillna:")
print(df_relleno)
"""),

md(r"""
### Nulos en el dataset real

Nuestro dataset `transacciones.csv` no tiene nulos (lo verificamos con `df.info()`).
Pero en proyectos reales es raro tener datos perfectos. El flujo siempre es:

```
1. df.isna().sum()          → detectar
2. ¿cuántos y en qué cols?  → decidir estrategia
3. dropna() o fillna()      → ejecutar
4. df.isna().sum() again    → verificar que quedó limpio
```

> ⚠️ Nunca elimines nulos sin entender **por qué** están ahí. A veces el nulo
> es la señal: "este campo no aplica para esta fila". Borrarlo puede distorsionar
> el análisis.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Calculas `df_con_nulos["monto"].mean()` con los nulos presentes. ¿Pandas lanza
un error o ignora los NaN automáticamente? Pruébalo. ¿Y si usas `.sum()`?
¿Y si lo conviertes a lista y llamas `sum(lista)`?
"""),

code(r"""
print("mean() con NaN:", df_con_nulos["monto"].mean())   # ignora NaN
print("sum()  con NaN:", df_con_nulos["monto"].sum())    # ignora NaN
# Python nativo:
lista = df_con_nulos["monto"].tolist()
try:
    print("sum() Python nativo:", sum(lista))
except TypeError as e:
    print("Error con sum() nativo:", e)
"""),
]


# ===================================================================== #
# 10. GROUPBY
# ===================================================================== #
C += [
md(r"""
## 10. `groupby`: split-apply-combine

`groupby` es la operación más poderosa de pandas para análisis. Implementa el
patrón **split-apply-combine**:

```
SPLIT     ─────────────────────────────────────────────────────
          df agrupa filas por el valor de una columna (p.ej. ciudad)

          Bogota   | Medellin | Cali | ...
          ──────   | ──────── | ──── |

APPLY     ─────────────────────────────────────────────────────
          A cada grupo, le aplica una función (sum, mean, count, ...)

          sum(monto)  sum(monto)  sum(monto)

COMBINE   ─────────────────────────────────────────────────────
          Los resultados se combinan en un nuevo DataFrame/Series

          ciudad        monto
          Bogota         X
          Medellin       Y
          Cali           Z
```

En pandas esto es, literalmente, una línea:
"""),

code(r"""
import os
import pandas as pd

ruta = os.path.join("..", "datasets", "transacciones.csv")
df = pd.read_csv(ruta)

# Total de ventas por ciudad
ventas_ciudad = df.groupby("ciudad")["monto"].sum()
print("Total de ventas por ciudad:")
print(ventas_ciudad.sort_values(ascending=False))
"""),

code(r"""
# Número de transacciones por ciudad
n_ciudad = df.groupby("ciudad")["monto"].count()
print("Transacciones por ciudad:")
print(n_ciudad.sort_values(ascending=False))
"""),

code(r"""
# Ticket promedio por categoría
ticket_cat = df.groupby("categoria")["monto"].mean().round(0)
print("Ticket promedio por categoría:")
print(ticket_cat.sort_values(ascending=False))
"""),

md(r"""
### `agg`: múltiples agregaciones a la vez

Con `agg` puedes calcular varias métricas en una sola pasada:
"""),

code(r"""
# Múltiples métricas por ciudad
resumen_ciudad = df.groupby("ciudad")["monto"].agg(
    total="sum",
    promedio="mean",
    maximo="max",
    n_transacciones="count"
).round(0)
print("Resumen por ciudad:")
print(resumen_ciudad)
"""),

code(r"""
# Agrupar por dos columnas
por_ciudad_metodo = df.groupby(["ciudad", "metodo_pago"])["monto"].sum().reset_index()
print("Ventas por ciudad y método de pago:")
print(por_ciudad_metodo.head(10))
"""),

md(r"""
### Trazado del split-apply-combine

Hagamos el análisis paso a paso para "total de ventas por categoría":

| Paso | Qué ocurre |
|---|---|
| `df.groupby("categoria")` | Split: agrupa las 120 filas en grupos por categoría |
| `["monto"]` | Selecciona la columna monto dentro de cada grupo |
| `.sum()` | Apply: suma los montos de cada grupo |
| (implícito) | Combine: produce una Series con índice = categorías |
"""),

code(r"""
# Paso a paso visible
grupos = df.groupby("categoria")

print("Número de grupos:", grupos.ngroups)
print("Tamaño de cada grupo:")
print(grupos.size())
print()

resultado = grupos["monto"].sum()
print("Total por categoría:")
print(resultado.sort_values(ascending=False))
"""),

md(r"""
### `reset_index()`: cuando el resultado tiene índice "raro"

Después de un `groupby`, la columna por la que agrupaste se convierte en índice.
A veces conviene volver a tenerla como columna normal:
"""),

code(r"""
# Sin reset_index: ciudad ES el índice
resultado_sin = df.groupby("ciudad")["monto"].sum()
print("Tipo:", type(resultado_sin))
print("Índice:", resultado_sin.index.tolist())
print(resultado_sin.head())
print()

# Con reset_index: ciudad vuelve a ser una columna
resultado_con = df.groupby("ciudad")["monto"].sum().reset_index()
print("Con reset_index:")
print(resultado_con)
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

`df.groupby("ciudad")["monto"].mean()` y
`df.groupby(["ciudad", "metodo_pago"])["monto"].mean()` producen resultados con
índices de **distinto nivel** (simple vs. multi-índice). ¿Cómo accederías al
valor de Bogota/efectivo en el segundo caso?
"""),
]


# ===================================================================== #
# 11. SORT, RENAME, RESET_INDEX
# ===================================================================== #
C += [
md(r"""
## 11. `sort_values`, `rename` y `reset_index`

### `sort_values`: ordenar filas

```python
df.sort_values("col")                  # ascendente
df.sort_values("col", ascending=False) # descendente
df.sort_values(["col1", "col2"])       # varios criterios
```
"""),

code(r"""
# Top 5 transacciones más grandes
top5 = df.sort_values("monto", ascending=False).head(5)
print("Top 5 transacciones:")
print(top5[["id", "fecha", "ciudad", "categoria", "monto"]])
"""),

code(r"""
# Ordenar por ciudad (A-Z) y dentro de cada ciudad por monto (mayor primero)
df_ord = df.sort_values(["ciudad", "monto"], ascending=[True, False])
print("Primeras filas ordenadas por ciudad y monto:")
print(df_ord[["ciudad", "monto"]].head(10))
"""),

md(r"""
### `rename`: renombrar columnas o índices
"""),

code(r"""
# Renombrar columnas
df_renamed = df.rename(columns={
    "metodo_pago": "metodo",
    "monto": "importe_cop"
})
print("Columnas renombradas:", df_renamed.columns.tolist())
print(df_renamed.head(3))
"""),

md(r"""
### `reset_index`: recuperar el índice como columna

Es el complemento de `set_index`. Muy útil tras `groupby`:
"""),

code(r"""
# groupby produce índice = ciudad; reset_index lo convierte a columna
resumen = (
    df.groupby("ciudad")["monto"]
      .agg(["sum", "mean", "count"])
      .rename(columns={"sum": "total", "mean": "promedio", "count": "n"})
      .reset_index()
      .sort_values("total", ascending=False)
)
print(resumen)
"""),
]


# ===================================================================== #
# 12. MERGE Y CONCAT
# ===================================================================== #
C += [
md(r"""
## 12. `merge` y `concat`: combinar DataFrames

En el mundo real los datos vienen en varias tablas. Pandas permite combinarlas
de dos formas principales:

```
CONCAT: apilar DataFrames (filas o columnas)
──────────────────────────────────────────
 DF1          DF2         pd.concat([DF1, DF2])
 ────         ────        ─────────────────────
 A | B        A | B       A | B
 1 | x        3 | z       1 | x
 2 | y        4 | w       2 | y
                          3 | z
                          4 | w

MERGE: unir por columna clave (como JOIN en SQL)
────────────────────────────────────────────────
 DF_transac.  DF_regiones   merge(on="ciudad")
 ──────────   ──────────    ────────────────────
 ciudad|monto  ciudad|region  ciudad|monto|region
 Bogota|100   Bogota|Centro  Bogota|100|Centro
 Cali  |200   Cali  |Andina  Cali  |200|Andina
```
"""),

code(r"""
import pandas as pd

# Tabla de regiones
regiones = pd.DataFrame({
    "ciudad":  ["Bogota", "Medellin", "Cali", "Barranquilla", "Bucaramanga"],
    "region":  ["Centro", "Andina",   "Pacifica", "Caribe",   "Andina"],
    "poblacion_mm": [7.4, 2.6, 2.2, 1.2, 0.6],
})
print("Tabla de regiones:")
print(regiones)
"""),

code(r"""
# Merge (inner join por defecto): solo filas que coinciden en ambas tablas
df_enriquecido = df.merge(regiones, on="ciudad", how="left")
print("Shape antes:", df.shape)
print("Shape después:", df_enriquecido.shape)
print()
print(df_enriquecido[["ciudad", "monto", "region", "poblacion_mm"]].head())
"""),

code(r"""
# Tipos de join
print("Tipos de join en pd.merge:")
print("  how='inner' (default) : solo filas que aparecen en AMBAS tablas")
print("  how='left'            : todas las filas de la tabla izquierda")
print("  how='right'           : todas las filas de la tabla derecha")
print("  how='outer'           : todas las filas de ambas tablas (rellena NaN)")
print()

# Ventas por región (posible solo tras el merge)
por_region = df_enriquecido.groupby("region")["monto"].sum().sort_values(ascending=False)
print("Ventas por región:")
print(por_region)
"""),

code(r"""
# pd.concat: apilar DataFrames de la misma estructura
df_enero = df[df["fecha"] < "2024-02-01"].copy()
df_febrero = df[(df["fecha"] >= "2024-02-01") & (df["fecha"] < "2024-03-01")].copy()

df_enero["mes"] = "enero"
df_febrero["mes"] = "febrero"

df_combinado = pd.concat([df_enero, df_febrero], ignore_index=True)
print("Enero:", len(df_enero), "filas | Febrero:", len(df_febrero), "filas")
print("Combinado:", len(df_combinado), "filas")
print()
print(df_combinado[["fecha", "mes", "ciudad", "monto"]].head(8))
"""),

md(r"""
### ¿Cuándo usar `merge` vs `concat`?

```
CONCAT                          MERGE
──────────────────────          ─────────────────────────────
Mismo esquema de columnas       Distintas columnas / tablas relacionadas
Apilado de períodos de tiempo   Enriquecer con datos de otra fuente
Unir resultados parciales       JOIN de tipo SQL (one-to-many, etc.)
```

En resumen: `concat` apila, `merge` une por clave.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Haces un `merge` con `how="inner"` y una ciudad del dataset de transacciones
no está en la tabla de regiones. ¿Esas filas aparecerían en el resultado?
¿Y si usas `how="left"`? ¿Qué valor tendría la columna `"region"` en ese caso?
"""),
]


# ===================================================================== #
# 13. ERRORES COMUNES
# ===================================================================== #
C += [
md(r"""
## 13. Errores comunes (y cómo evitarlos)

### Error 1: SettingWithCopyWarning

Este es el error más frecuente para los que empiezan con pandas. Ocurre cuando
intentas modificar un **subconjunto** del DataFrame.

**Mal:**
```python
df_bta = df[df["ciudad"] == "Bogota"]   # esto es una VISTA o copia (ambiguo)
df_bta["nueva_col"] = 0                  # ⚠️ SettingWithCopyWarning
```

**Bien:**
```python
df_bta = df[df["ciudad"] == "Bogota"].copy()  # copia explícita
df_bta["nueva_col"] = 0                        # sin warning
```
"""),

code(r"""
import warnings

# Reproducir el warning
df_bta = df[df["ciudad"] == "Bogota"]  # sin .copy()
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    df_bta["prueba"] = 0
    if w:
        print("Warning capturado:", w[0].category.__name__)
        print(str(w[0].message)[:120])
    else:
        print("(no se produjo warning — depende de la versión de pandas)")

# Solución correcta
df_bta = df[df["ciudad"] == "Bogota"].copy()
df_bta["prueba"] = 0   # sin warning
print("Con .copy() no hay warning")
"""),

md(r"""
### Error 2: confundir `loc` e `iloc`

```python
# Si el índice del df filtrado es [4, 11, 23, ...]
df_filtrado.loc[0]    # KeyError — 0 no existe como etiqueta
df_filtrado.iloc[0]   # OK — primera fila (etiqueta 4)
```

Regla nemotécnica:
- **`loc`** → **L**abel → etiqueta (lo que ves en el índice)
- **`iloc`** → **i**nteger → posición entera (0, 1, 2, ...)
"""),

md(r"""
### Error 3: groupby olvidando `reset_index`

```python
resultado = df.groupby("ciudad")["monto"].sum()
# ¡ciudad es el ÍNDICE, no una columna!
resultado["ciudad"]   # KeyError — no hay columna ciudad

# Correcto:
resultado = df.groupby("ciudad")["monto"].sum().reset_index()
resultado["ciudad"]   # OK
```
"""),

md(r"""
### Error 4: `&` y `|` sin paréntesis

```python
# MALO — da resultados incorrectos por precedencia de operadores
df[df["ciudad"] == "Bogota" & df["monto"] > 100_000]

# BUENO — paréntesis alrededor de cada condición
df[(df["ciudad"] == "Bogota") & (df["monto"] > 100_000)]
```
"""),

md(r"""
### Error 5: modificar el DataFrame original por accidente

```python
df2 = df              # NO es una copia — ambas variables apuntan al mismo objeto
df2["monto"] = 0      # ¡también modifica df!

df2 = df.copy()       # Ahora sí es una copia independiente
df2["monto"] = 0      # solo afecta df2
```

En pandas (a diferencia de NumPy) `df.copy()` hace una **copia profunda** por
defecto. Úsala siempre que quieras trabajar con una versión modificada sin
tocar el original.
"""),

code(r"""
# Demostración del error 5
import pandas as pd

df_orig = pd.DataFrame({"x": [1, 2, 3]})
df_alias = df_orig          # alias, no copia
df_copia = df_orig.copy()   # copia real

df_alias["y"] = 99
print("df_orig tras modificar df_alias (sin .copy()):")
print(df_orig)   # también tiene la columna 'y' !

df_copia["y"] = 0
print()
print("df_orig tras modificar df_copia (con .copy()):")
print(df_orig)   # 'y' sigue siendo 99, no cambia a 0
"""),
]


# ===================================================================== #
# 14. RESUMEN, QUIZ Y RETOS
# ===================================================================== #
C += [
md(r"""
## 14. Resumen de la clase

| Concepto | Una frase |
|---|---|
| **Series** | array etiquetado con índice; base de las columnas de un DataFrame |
| **DataFrame** | tabla de datos heterogéneos; colección de Series con el mismo índice |
| **`pd.read_csv`** | lee un CSV y construye el DataFrame con tipos inferidos automáticamente |
| **Inspección** | `head`, `info`, `describe`, `value_counts` — siempre lo primero |
| **`loc` / `iloc`** | `loc` por etiqueta, `iloc` por posición entera |
| **Filtrado booleano** | máscara True/False; combinar con `&` y `|` entre paréntesis |
| **`apply`** | aplicar función elemento a elemento; menos eficiente que ops vectorizadas |
| **Nulos** | `isna()` detecta, `fillna()` rellena, `dropna()` elimina |
| **`groupby`** | split-apply-combine; siempre sigue de `.sum()`, `.mean()`, `.agg()`, etc. |
| **`reset_index`** | convierte el índice del resultado de groupby en columna |
| **`sort_values`** | ordenar filas por una o varias columnas |
| **`merge`** | unir DataFrames por columna clave (tipo JOIN de SQL) |
| **`concat`** | apilar DataFrames con la misma estructura de columnas |

### Lo más importante que te llevas

> **Pandas transforma filas en conocimiento.** El flujo es siempre:
> leer → inspeccionar → limpiar (nulos, tipos) → filtrar → transformar → agrupar → exportar.
"""),

md(r"""
## Quiz de autoevaluación

Responde mentalmente y luego ejecuta la celda para verificar.

1. ¿Cuál es la diferencia entre `df.loc[5]` y `df.iloc[5]`?
2. ¿Por qué necesitas paréntesis en `(df["a"] > 0) & (df["b"] < 10)`?
3. ¿Qué hace `df.groupby("ciudad")["monto"].sum().reset_index()`?
4. Si `df["monto"].isna().sum()` devuelve 3, ¿cuántos nulos hay en esa columna?
5. ¿Cuándo usarías `merge` y cuándo `concat`?
"""),

code(r"""
respuestas = {
    1: ("loc usa ETIQUETAS del índice; iloc usa POSICIONES enteras (0,1,2,...). "
        "Si el índice no es 0,1,2,..., dan resultados distintos."),
    2: ("& y | tienen menos precedencia que == y >, así que sin paréntesis "
        "Python evalúa la expresión en orden incorrecto y lanza un error."),
    3: ("Agrupa las filas por ciudad, suma los montos de cada grupo, "
        "y convierte ciudad de índice a columna normal."),
    4: "Exactamente 3 nulos en la columna monto.",
    5: ("concat: apilar DataFrames con la misma estructura (más filas o más columnas). "
        "merge: unir dos tablas que comparten una columna clave, como un JOIN de SQL."),
}
for k, v in respuestas.items():
    print("{0}. {1}\n".format(k, v))
"""),

md(r"""
## Retos para practicar

1. **Filtrado compuesto.** Encuentra las transacciones de la categoría `"tecnologia"`
   con monto superior a $200.000 y método de pago `"tarjeta"`. ¿Cuántas hay?

2. **Tabla dinámica.** Crea un pivot de ventas totales donde las filas sean ciudades,
   las columnas sean categorías y los valores sean la suma de montos.
   Pista: `pd.pivot_table(df, values="monto", index="ciudad", columns="categoria", aggfunc="sum")`.

3. **Exportar.** Tras construir el resumen por ciudad (`groupby` + `agg`), guárdalo
   en CSV con `resultado.to_csv("resumen_ventas.csv", index=False)`.

4. **Análisis libre.** ¿En qué ciudad el ticket promedio es más alto?
   ¿Qué método de pago acumula más dinero? Responde con código.

---

### Siguiente paso

- **practice01.ipynb** — 10 ejercicios graduales con pandas sobre el dataset.
- **practice02.ipynb** — análisis completo del dataset (limpieza, agrupación, visualización).
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


# --- Extra: anatomía de una Series ---
EXTRA_SERIES_ANAT = [
md(r"""
### Anatomía de una Series: valores, índice y dtype

Una Series tiene tres componentes que vale la pena inspeccionar por separado:

```
pd.Series([73078, 110323, 205064], index=["A","B","C"])

  .values → array([73078, 110323, 205064], dtype=int64)
  .index  → Index(['A', 'B', 'C'], dtype='object')
  .dtype  → dtype('int64')
  .name   → None  (puede asignarse: serie.name = "monto")
```

El `dtype` determina cómo pandas almacena y opera los datos:
- `int64` / `float64` → numérico (rápido, vectorizable)
- `object` → texto o mixto (más lento)
- `bool` → booleano
- `datetime64[ns]` → fechas
"""),

code(r"""
import pandas as pd

s = pd.Series([73078, 110323, 205064], index=["A", "B", "C"], name="monto_cop")
print("values:", s.values)
print("index:", s.index.tolist())
print("dtype:", s.dtype)
print("name:", s.name)
print()
# Operaciones de resumen
print("sum:", s.sum())
print("mean:", s.mean())
print("std:", s.std().round(2))
print("min/max:", s.min(), "/", s.max())
"""),
]

# --- Extra: pivot_table ---
EXTRA_PIVOT = [
md(r"""
### Tabla dinámica con `pd.pivot_table`

Una **pivot table** es como un `groupby` bidimensional: filas de un lado,
columnas del otro, valores en el centro.

```
pd.pivot_table(df,
    values  = "monto",      # qué columna agregar
    index   = "ciudad",     # filas
    columns = "metodo_pago",# columnas
    aggfunc = "sum"         # cómo agregar
)
```

Produce una tabla como:

```
metodo_pago    efectivo  tarjeta  transferencia
ciudad
Barranquilla   XXX       XXX      XXX
Bogota         XXX       XXX      XXX
...
```
"""),

code(r"""
import os, pandas as pd

ruta = os.path.join("..", "datasets", "transacciones.csv")
df = pd.read_csv(ruta)

pivot = pd.pivot_table(
    df,
    values  = "monto",
    index   = "ciudad",
    columns = "metodo_pago",
    aggfunc = "sum",
    fill_value = 0,
)
print("Ventas por ciudad y método de pago:")
print(pivot)
print()
print("Ciudad con más ventas en tarjeta:", pivot["tarjeta"].idxmax())
"""),
]

# --- Extra: glosario ---
EXTRA_GLOSARIO = [
md(r"""
## Glosario de la Clase 6

| Término | Definición |
|---|---|
| **Series** | Estructura 1D de pandas: valores + índice etiquetado |
| **DataFrame** | Estructura 2D: tabla de filas × columnas heterogéneas |
| **índice** | Etiquetas de las filas (pueden ser números, texto, fechas) |
| **dtype** | Tipo de dato de una columna (int64, float64, object, bool…) |
| **`pd.read_csv`** | Lee un archivo CSV y devuelve un DataFrame |
| **`head/tail`** | Ver primeras/últimas N filas |
| **`info`** | Resumen estructural: tipos, nulos, memoria |
| **`describe`** | Estadísticas descriptivas (count, mean, std, cuartiles) |
| **`loc`** | Selección por **etiqueta** de fila y columna |
| **`iloc`** | Selección por **posición entera** |
| **máscara booleana** | Series de True/False usada para filtrar filas |
| **`apply`** | Aplica una función a cada elemento de una columna o fila |
| **NaN** | Not a Number — valor especial para representar datos faltantes |
| **`isna`** | Detecta nulos (devuelve máscara booleana) |
| **`fillna`** | Rellena nulos con un valor |
| **`dropna`** | Elimina filas (o columnas) con nulos |
| **`groupby`** | Agrupa filas por una columna; patrón split-apply-combine |
| **`agg`** | Aplica múltiples funciones de agregación en un groupby |
| **`reset_index`** | Convierte el índice en columna normal |
| **`sort_values`** | Ordena el DataFrame por una o más columnas |
| **`merge`** | Une dos DataFrames por columna clave (tipo SQL JOIN) |
| **`concat`** | Apila DataFrames (verticalmente o lateralmente) |
| **SettingWithCopyWarning** | Advertencia al modificar una copia sin `.copy()` |
"""),
]

# --- Extra: matplotlib con pandas ---
EXTRA_VIZ = [
md(r"""
### Visualización rápida con pandas y matplotlib

Pandas tiene integración directa con matplotlib. Para visualizaciones exploratorias
rápidas, `df.plot()` es suficiente:
"""),

code(r"""
import os
import pandas as pd
import matplotlib.pyplot as plt

ruta = os.path.join("..", "datasets", "transacciones.csv")
df = pd.read_csv(ruta)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Barras: total por ciudad
df.groupby("ciudad")["monto"].sum().sort_values().plot(
    kind="barh", ax=axes[0], title="Total ventas por ciudad", color="steelblue"
)
axes[0].set_xlabel("Monto (COP)")

# Histograma: distribución de montos
df["monto"].plot(
    kind="hist", bins=20, ax=axes[1], title="Distribución de montos", color="coral"
)
axes[1].set_xlabel("Monto (COP)")

plt.tight_layout()
plt.show()
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Ejecutas `df.groupby("categoria")["monto"].sum().plot(kind="pie")`. ¿Qué
información comunica ese gráfico? ¿Es la mejor forma de mostrarlo? ¿Cuándo
un gráfico de barras es superior a un pie chart?
"""),
]

# --- Extra: cumsum y análisis temporal ---
EXTRA_TEMPORAL = [
md(r"""
### Análisis temporal: ventas acumuladas en el tiempo

Cuando los datos tienen una columna de fecha, podemos hacer análisis temporal.
Un patrón útil es calcular ventas **acumuladas** con `cumsum()`:
"""),

code(r"""
import os
import pandas as pd

ruta = os.path.join("..", "datasets", "transacciones.csv")
df = pd.read_csv(ruta, parse_dates=["fecha"])

# Ordenar por fecha y calcular acumulado
df_sorted = df.sort_values("fecha").reset_index(drop=True)
df_sorted["monto_acumulado"] = df_sorted["monto"].cumsum()

print("Ventas acumuladas (primeras 10 filas):")
print(df_sorted[["fecha", "monto", "monto_acumulado"]].head(10))
print()
print("Total final:", df_sorted["monto_acumulado"].iloc[-1])
"""),
]

# Insertar bloques en puntos estratégicos
C = insertar_despues(C, "ambas se complementan.", EXTRA_SERIES_ANAT)
C = insertar_despues(C, "Esa decisión de diseño de pandas", EXTRA_TEMPORAL)
C = insertar_despues(C, "No analices datos que no has inspeccionado primero.", EXTRA_PIVOT)
C = insertar_despues(C, "siempre depende del contexto", EXTRA_VIZ)
C = insertar_despues(C, "Pruébalo. Y si lo conviertes", EXTRA_GLOSARIO)

# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase06", "lecture.ipynb")
build(os.path.abspath(ruta), C)
