"""Construye curso/clase05/practice02.ipynb — análisis numérico de transacciones con NumPy.

Caso aplicado: cargar montos como array, calcular estadísticas descriptivas,
detectar outliers con z-score, agrupar con máscaras booleanas.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []

# --------------------------------------------------------------------------- #
# Portada
# --------------------------------------------------------------------------- #
C += [
md(r"""
# Clase 5 · Práctica 02 — Análisis numérico de transacciones con NumPy

### De listas Python a arrays de alto rendimiento

En la Práctica 02 de la Clase 1 analizamos este mismo dataset con listas y
bucles Python. Hoy hacemos exactamente el mismo análisis, pero con **NumPy**:
sin un solo bucle explícito.

Al final compararás cuánto código necesitas en cada enfoque.

**Dataset:** `transacciones.csv` — 120 transacciones de tiendas en Colombia.
Columnas: `id, fecha, ciudad, categoria, metodo_pago, monto`.

**Preguntas de negocio:**
1. ¿Cuáles son las estadísticas descriptivas del monto?
2. ¿Hay transacciones outliers? Detección por **z-score**.
3. ¿Qué ciudades tienen montos por encima de la media general?
4. ¿Cómo se distribuyen los montos por categoria?
5. ¿Cuál es la correlación entre el rango del monto y la ciudad?

> 🎯 **Objetivo:** escribir código vectorizado, sin `for`, para responder estas
> preguntas. Si te sale un bucle, hay una forma NumPy de hacerlo sin él.
"""),

code(r"""
import csv, os, sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar

ruta = os.path.join("..", "datasets", "transacciones.csv")
with open(ruta, encoding="utf-8") as f:
    filas = list(csv.DictReader(f))

# Extraemos los montos como array NumPy
montos = np.array([int(fila["monto"]) for fila in filas])
ciudades_raw = np.array([fila["ciudad"] for fila in filas])
categorias_raw = np.array([fila["categoria"] for fila in filas])
metodos_raw = np.array([fila["metodo_pago"] for fila in filas])

print("Transacciones cargadas:", len(montos))
print("Tipo de 'montos':", type(montos), "| dtype:", montos.dtype)
print("Primeros 5 montos:", montos[:5])
"""),
]

# --------------------------------------------------------------------------- #
# PASO 1: Estadísticas descriptivas
# --------------------------------------------------------------------------- #
C += [
md(r"""
## Paso 1 · Estadísticas descriptivas en una pasada

Con NumPy, las estadísticas sobre un array son funciones de una línea.
No hay bucles, no hay acumuladores manuales.
"""),

code(r"""
# Estadísticas descriptivas de los montos
n     = len(montos)
media = np.mean(montos)
std   = np.std(montos)
mediana = np.median(montos)
p25   = np.percentile(montos, 25)
p75   = np.percentile(montos, 75)
minv  = np.min(montos)
maxv  = np.max(montos)

print("=== Estadísticas descriptivas de 'monto' ===")
print("  N:        {:>10,}".format(n))
print("  Media:    {:>10,.0f}".format(media))
print("  Mediana:  {:>10,.0f}".format(mediana))
print("  Std:      {:>10,.0f}".format(std))
print("  Min:      {:>10,.0f}".format(minv))
print("  P25:      {:>10,.0f}".format(p25))
print("  P75:      {:>10,.0f}".format(p75))
print("  Max:      {:>10,.0f}".format(maxv))

# Coeficiente de variación: qué tan dispersos están los datos
cv = std / media * 100
print("  CV:       {:>9.1f}%".format(cv))
"""),

md(r"""
### Interpretación

- La **media** es mayor que la **mediana**: hay transacciones de montos muy altos
  que "jalan" la media hacia arriba. Distribución sesgada a la derecha.
- Un **coeficiente de variación** alto (>50%) indica mucha dispersión: las
  transacciones van desde compras pequeñas hasta compras muy grandes.
- El **rango intercuartil** (P75 - P25) es una medida de dispersión más robusta
  que el rango completo porque no la afectan los extremos.
"""),
]

# --------------------------------------------------------------------------- #
# PASO 2: Detección de outliers con z-score
# --------------------------------------------------------------------------- #
C += [
md(r"""
## Paso 2 · Detección de outliers con z-score

El **z-score** mide cuántas desviaciones estándar se aleja cada valor de la media:

```
z[i] = (monto[i] - media) / std
```

Convención: un |z| > 3 se considera un outlier (poco probable bajo distribución normal).
"""),

code(r"""
# Calcular z-scores de forma vectorizada
z_scores = (montos - media) / std

# Identificar outliers
mask_outlier = np.abs(z_scores) > 3.0
n_outliers = mask_outlier.sum()

print("Outliers (|z| > 3): {} transacciones".format(n_outliers))
print("\nMontos outliers:")
for m, z, c in zip(montos[mask_outlier], z_scores[mask_outlier], ciudades_raw[mask_outlier]):
    print("  ${:>12,.0f}  z={:.2f}  ciudad={}".format(m, z, c))
"""),

code(r"""
# Histograma ASCII: distribución de montos en rangos
bins = np.array([0, 50_000, 100_000, 200_000, 500_000, np.inf])
etiquetas = ["0-50k", "50k-100k", "100k-200k", "200k-500k", ">500k"]

print("Distribución de montos:")
for i in range(len(etiquetas)):
    mask = (montos >= bins[i]) & (montos < bins[i+1])
    conteo = mask.sum()
    barra = "#" * conteo
    print("  {:>12}: {:>3} | {}".format(etiquetas[i], conteo, barra))
"""),
]

# --------------------------------------------------------------------------- #
# PASO 3: Agrupación por ciudad con máscaras booleanas
# --------------------------------------------------------------------------- #
C += [
md(r"""
## Paso 3 · Agrupar por ciudad con máscaras booleanas

En lugar de bucles o diccionarios, usamos una máscara booleana por ciudad.
Es el patrón más directo en NumPy para "GROUP BY":
"""),

code(r"""
ciudades_unicas = np.unique(ciudades_raw)
print("Ciudad            |  N  |    Media    |  Std     |  Max")
print("-" * 65)

for ciudad in ciudades_unicas:
    mask_c = (ciudades_raw == ciudad)
    m_c = montos[mask_c]
    print("  {:15} | {:>3} | {:>10,.0f} | {:>8,.0f} | {:>10,.0f}".format(
        ciudad, len(m_c), m_c.mean(), m_c.std(), m_c.max()
    ))
"""),

code(r"""
# Ciudades cuya media supera la media general
media_general = montos.mean()
print("Media general: ${:,.0f}".format(media_general))
print("\nCiudades con media > media general:")

for ciudad in ciudades_unicas:
    mask_c = (ciudades_raw == ciudad)
    media_c = montos[mask_c].mean()
    if media_c > media_general:
        print("  {:15} ${:,.0f} (diferencia: +${:,.0f})".format(
            ciudad, media_c, media_c - media_general
        ))
"""),
]

# --------------------------------------------------------------------------- #
# PASO 4: Agrupación por categoría
# --------------------------------------------------------------------------- #
C += [
md(r"""
## Paso 4 · Estadísticas por categoría

El mismo patrón: una máscara por categoría, luego reducción sobre los montos
filtrados.
"""),

code(r"""
categorias_unicas = np.unique(categorias_raw)

totales  = np.array([montos[categorias_raw == c].sum() for c in categorias_unicas])
medias   = np.array([montos[categorias_raw == c].mean() for c in categorias_unicas])
conteos  = np.array([(categorias_raw == c).sum() for c in categorias_unicas])

# Ordenar por total descendente usando argsort
orden = np.argsort(totales)[::-1]

print("Categoría        |  N  |    Total     |   Media")
print("-" * 60)
for idx in orden:
    print("  {:15} | {:>3} | {:>12,.0f} | {:>10,.0f}".format(
        categorias_unicas[idx], conteos[idx], totales[idx], medias[idx]
    ))
"""),
]

# --------------------------------------------------------------------------- #
# PASO 5: Análisis de método de pago
# --------------------------------------------------------------------------- #
C += [
md(r"""
## Paso 5 · Distribución por método de pago

Calculamos el porcentaje del total que representa cada método de pago:
"""),

code(r"""
metodos_unicos = np.unique(metodos_raw)
total_global = montos.sum()

print("Metodo de pago | Transacciones | Total        | % del total")
print("-" * 65)

for metodo in metodos_unicos:
    mask_m = (metodos_raw == metodo)
    n_m    = mask_m.sum()
    total_m = montos[mask_m].sum()
    pct = total_m / total_global * 100
    print("  {:14} | {:>13} | {:>12,.0f} | {:>10.1f}%".format(
        metodo, n_m, total_m, pct
    ))
"""),
]

# --------------------------------------------------------------------------- #
# TU TURNO: 3 tareas con comprobación
# --------------------------------------------------------------------------- #
C += [
md(r"""
---
## Tu turno

Ahora aplica lo aprendido. Completa cada función y ejecuta la comprobación.
"""),

md(r"""
### Tarea A · Normalizar los montos a [0, 1]

Completa `normalizar_montos(montos)` que aplique la normalización min-max
**de forma vectorizada** y devuelva el array normalizado.

```
resultado[i] = (montos[i] - min) / (max - min)
```
"""),

code(r"""
def normalizar_montos(montos):
    # ✏️ TU CÓDIGO AQUÍ — vectorizado, sin bucles
    return None

# Comprobación
import numpy as np
_norm = normalizar_montos(montos)
revisar("array numpy", isinstance(_norm, np.ndarray))
revisar("min == 0", abs(_norm.min() - 0.0) < 1e-9)
revisar("max == 1", abs(_norm.max() - 1.0) < 1e-9)
revisar("mismo shape", _norm.shape == montos.shape)
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def normalizar_montos(montos):
    return (montos - montos.min()) / (montos.max() - montos.min())
```
</details>
"""),

md(r"""
### Tarea B · Z-score por ciudad

Completa `zscore_ciudad(montos, ciudades_raw, ciudad)` que:
1. Filtre los montos de esa ciudad.
2. Calcule el z-score de cada monto de esa ciudad (media y std de esa ciudad).
3. Devuelva el array de z-scores.
"""),

code(r"""
def zscore_ciudad(montos, ciudades_raw, ciudad):
    # ✏️ TU CÓDIGO AQUÍ — filtra, calcula media/std, devuelve z-scores
    return None

# Comprobación
import numpy as np
_z = zscore_ciudad(montos, ciudades_raw, "Bogota")
revisar("array numpy", isinstance(_z, np.ndarray))
revisar("media aprox 0", abs(_z.mean()) < 0.001)
revisar("std aprox 1", abs(_z.std() - 1.0) < 0.001)
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def zscore_ciudad(montos, ciudades_raw, ciudad):
    mask = (ciudades_raw == ciudad)
    m_c = montos[mask].astype(float)
    media_c = m_c.mean()
    std_c = m_c.std()
    return (m_c - media_c) / std_c
```
El z-score se centra en la media y escala por la desviación de esa ciudad.
Usar `.astype(float)` evita problemas de división entera.
</details>
"""),

md(r"""
### Tarea C · Top-k montos más altos

Completa `top_k_montos(montos, k)` que devuelva los `k` montos más altos
en orden descendente. Usa `np.sort` o `np.argsort`.
"""),

code(r"""
def top_k_montos(montos, k):
    # ✏️ TU CÓDIGO AQUÍ — sin bucles
    return None

# Comprobación
import numpy as np
_top = top_k_montos(montos, 5)
revisar("longitud k", len(_top) == 5)
revisar("orden descendente", (_top[:-1] >= _top[1:]).all())
revisar("el mayor esta primero", _top[0] == montos.max())
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def top_k_montos(montos, k):
    return np.sort(montos)[::-1][:k]
```
`np.sort` ordena ascendente; `[::-1]` invierte (descendente); `[:k]` toma los primeros k.

Alternativa con argsort:
```python
def top_k_montos(montos, k):
    idx = np.argsort(montos)[::-1]
    return montos[idx[:k]]
```
</details>
"""),
]

# --------------------------------------------------------------------------- #
# Cierre
# --------------------------------------------------------------------------- #
C += [
md(r"""
---
## Reflexión: listas vs NumPy

Compara el código de esta práctica con el de la Clase 1 Práctica 02:

| Tarea | Con listas (Clase 1) | Con NumPy (Clase 5) |
|---|---|---|
| Media | `sum(montos)/len(montos)` | `montos.mean()` |
| Filtrar > media | bucle `for` con `if` | `montos[montos > media]` |
| Estadísticas | varios recorridos | `np.mean/std/min/max` |
| Ordenar | `sorted(...)` | `np.sort(montos)[::-1]` |
| Z-score | bucle manual | `(montos - media) / std` |

NumPy no solo es más conciso: para datasets de millones de filas la diferencia
de velocidad es de 10x a 100x.

> 💡 En la Clase 6, pandas usará NumPy internamente para hacer exactamente
> estos cálculos, pero con etiquetas de columnas y filas para mayor legibilidad.

➡️ Sigue con **homework01.ipynb** y **homework02.ipynb**.
"""),
]


# ===================================================================== #
# VALIDACIÓN en construcción
# ===================================================================== #
def _validar():
    import csv
    import numpy as np

    ruta = os.path.join(
        os.path.dirname(__file__), "..", "curso", "datasets", "transacciones.csv"
    )
    with open(os.path.abspath(ruta), encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    montos_v = np.array([int(fila["monto"]) for fila in filas])
    ciudades_v = np.array([fila["ciudad"] for fila in filas])

    def normalizar_montos(montos):
        return (montos - montos.min()) / (montos.max() - montos.min())

    n = normalizar_montos(montos_v)
    assert isinstance(n, np.ndarray)
    assert abs(n.min() - 0.0) < 1e-9
    assert abs(n.max() - 1.0) < 1e-9
    assert n.shape == montos_v.shape

    def zscore_ciudad(montos, ciudades_raw, ciudad):
        mask = (ciudades_raw == ciudad)
        m_c = montos[mask].astype(float)
        return (m_c - m_c.mean()) / m_c.std()

    z = zscore_ciudad(montos_v, ciudades_v, "Bogota")
    assert isinstance(z, np.ndarray)
    assert abs(z.mean()) < 0.001
    assert abs(z.std() - 1.0) < 0.001

    def top_k_montos(montos, k):
        return np.sort(montos)[::-1][:k]

    top = top_k_montos(montos_v, 5)
    assert len(top) == 5
    assert (top[:-1] >= top[1:]).all()
    assert top[0] == montos_v.max()

    print("✔ Las soluciones de referencia de practice02 (clase05) funcionan sobre el dataset.")


_validar()


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase05", "practice02.ipynb")
build(os.path.abspath(ruta), C)
