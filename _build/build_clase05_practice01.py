"""Construye curso/clase05/practice01.ipynb — 10 ejercicios graduales de NumPy.

Patrón por ejercicio:
  1. Markdown con enunciado + ejemplo.
  2. Celda plantilla (el estudiante escribe aquí).
  3. Celda de comprobación suave (revisar()).
  4. Markdown <details> con solución comentada (oculta).

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
# Clase 5 · Práctica 01 — 10 ejercicios de NumPy

### Arrays numéricos de alto rendimiento

Estos 10 ejercicios van **de menor a mayor dificultad**. Para cada uno:

1. Lee el enunciado y el ejemplo.
2. Escribe tu solución en la celda que dice `# ✏️ TU CÓDIGO AQUÍ`.
3. Ejecuta la celda de **comprobación**: verás ✅ o ❌ por cada caso.
4. ¿Atascado? Despliega **💡 Ver solución** al final de cada ejercicio.

> 🧠 **Antes de teclear**, escribe qué operación NumPy resuelve el problema.
> El objetivo no es solo pasar la comprobación, sino escribir código vectorizado
> (sin bucles `for`).

> ⚙️ Las comprobaciones son *suaves*: si tu función aún no está lista,
> el notebook sigue ejecutándose.
"""),

code(r"""
import os, sys
sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar
import numpy as np
print("Listo. NumPy version:", np.__version__)
"""),
]


# --------------------------------------------------------------------------- #
# Helper para construir ejercicios
# --------------------------------------------------------------------------- #
def ejercicio(numero, titulo, enunciado_md, plantilla, check_code, solucion_md):
    C.append(md("## Ejercicio {} · {}\n\n{}".format(numero, titulo, enunciado_md)))
    C.append(code(plantilla))
    C.append(code(check_code))
    C.append(md(solucion_md))


# ---- 1 --------------------------------------------------------------------
ejercicio(
    1, "Estadísticas de un array de precios",
    r"""Escribe `estadisticas(precios)` que reciba un array NumPy de precios y
devuelva una tupla `(media, std, minimo, maximo)`, **en ese orden**, usando
funciones NumPy (sin bucles).

**Ejemplo:**
```python
p = np.array([100, 200, 300, 400, 500])
estadisticas(p)  # → (300.0, 141.42..., 100, 500)
```""",
    r"""
import numpy as np

def estadisticas(precios):
    # ✏️ TU CÓDIGO AQUÍ — usa np.mean, np.std, np.min, np.max
    return None
""",
    r"""
import numpy as np
p = np.array([100, 200, 300, 400, 500])
res = estadisticas(p)
revisar("es tupla de 4", res is not None and len(res) == 4)
revisar("media == 300", abs(res[0] - 300.0) < 1e-9)
revisar("min == 100", res[2] == 100)
revisar("max == 500", res[3] == 500)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def estadisticas(precios):
    return (np.mean(precios), np.std(precios), np.min(precios), np.max(precios))
```
Una sola línea: devolvemos la tupla directamente con las cuatro ufuncs de reducción.
`np.std` calcula la desviación estándar poblacional por defecto (ddof=0).
</details>
""",
)

# ---- 2 --------------------------------------------------------------------
ejercicio(
    2, "Filtrar ventas por encima del promedio",
    r"""Escribe `ventas_sobre_promedio(ventas)` que reciba un array de montos y
devuelva **solo los montos que superen el promedio**, usando indexing booleano
(sin bucles).

**Ejemplo:**
```python
v = np.array([50, 200, 80, 350, 120])
ventas_sobre_promedio(v)  # → array([200, 350])  (promedio = 160)
```""",
    r"""
import numpy as np

def ventas_sobre_promedio(ventas):
    # ✏️ TU CÓDIGO AQUÍ — calcula la media y usa indexing booleano
    return None
""",
    r"""
import numpy as np
v = np.array([50, 200, 80, 350, 120])
res = ventas_sobre_promedio(v)
revisar("tipo ndarray", isinstance(res, np.ndarray))
revisar("valores correctos", set(res.tolist()) == {200, 350})
revisar("todos > promedio", (res > v.mean()).all())
revisar("array vacio si todos iguales",
        len(ventas_sobre_promedio(np.array([5, 5, 5]))) == 0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def ventas_sobre_promedio(ventas):
    return ventas[ventas > ventas.mean()]
```
`ventas.mean()` calcula el promedio; la comparación produce una máscara booleana;
el indexing filtra el array. Todo en una línea.
</details>
""",
)

# ---- 3 --------------------------------------------------------------------
ejercicio(
    3, "Precio con IVA (operación vectorizada)",
    r"""Escribe `aplicar_iva(precios, tasa)` que reciba un array de precios y
una tasa (p.ej. `0.19` para 19 %) y devuelva un array con los precios
**incluyendo IVA**, sin usar bucles.

**Ejemplo:**
```python
p = np.array([100_000, 50_000, 200_000])
aplicar_iva(p, 0.19)  # → array([119000., 59500., 238000.])
```""",
    r"""
import numpy as np

def aplicar_iva(precios, tasa):
    # ✏️ TU CÓDIGO AQUÍ — operación escalar sobre el array
    return None
""",
    r"""
import numpy as np
p = np.array([100_000, 50_000, 200_000])
res = aplicar_iva(p, 0.19)
revisar("tipo ndarray", isinstance(res, np.ndarray))
revisar("primer precio", abs(res[0] - 119_000.0) < 0.01)
revisar("tasa cero = sin cambio", np.allclose(aplicar_iva(p, 0.0), p))
revisar("tasa 0.5", abs(aplicar_iva(np.array([100.0]), 0.5)[0] - 150.0) < 0.01)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def aplicar_iva(precios, tasa):
    return precios * (1 + tasa)
```
El broadcasting escalar aplica `(1 + tasa)` a todos los elementos simultáneamente.
</details>
""",
)

# ---- 4 --------------------------------------------------------------------
ejercicio(
    4, "Suma por filas y columnas (axis=0, axis=1)",
    r"""Escribe `resumen_ventas(matriz)` que reciba una matriz 2-D de ventas
(filas=ciudades, columnas=meses) y devuelva una tupla
`(suma_por_ciudad, suma_por_mes)`, donde:
- `suma_por_ciudad`: array con el total de cada ciudad (axis=1).
- `suma_por_mes`: array con el total de cada mes (axis=0).

**Ejemplo:**
```python
m = np.array([[10, 20], [30, 40], [50, 60]])
r = resumen_ventas(m)
# r[0] → array([ 30,  70, 110])   ciudad 0: 10+20, etc.
# r[1] → array([ 90, 120])        mes 0: 10+30+50, mes 1: 20+40+60
```""",
    r"""
import numpy as np

def resumen_ventas(matriz):
    # ✏️ TU CÓDIGO AQUÍ — usa np.sum con axis=
    return None
""",
    r"""
import numpy as np
m = np.array([[10, 20], [30, 40], [50, 60]])
r = resumen_ventas(m)
revisar("tipo tupla", isinstance(r, tuple) and len(r) == 2)
revisar("suma por ciudad", np.array_equal(r[0], np.array([30, 70, 110])))
revisar("suma por mes", np.array_equal(r[1], np.array([90, 120])))
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def resumen_ventas(matriz):
    suma_por_ciudad = np.sum(matriz, axis=1)  # colapsa columnas → 1 valor por fila
    suma_por_mes    = np.sum(matriz, axis=0)  # colapsa filas → 1 valor por columna
    return (suma_por_ciudad, suma_por_mes)
```
`axis=1` "viaja" a lo largo de las columnas (suma todos los meses de cada ciudad);
`axis=0` "viaja" a lo largo de las filas (suma todas las ciudades de cada mes).
</details>
""",
)

# ---- 5 --------------------------------------------------------------------
ejercicio(
    5, "Normalizar un array a [0, 1]",
    r"""Escribe `normalizar(arr)` que aplique la normalización min-max:

```
resultado[i] = (arr[i] - min(arr)) / (max(arr) - min(arr))
```

De forma vectorizada. Si todos los valores son iguales (max == min),
devuelve un array de ceros del mismo shape.

**Ejemplo:**
```python
a = np.array([0.0, 5.0, 10.0])
normalizar(a)  # → array([0.0, 0.5, 1.0])
```""",
    r"""
import numpy as np

def normalizar(arr):
    # ✏️ TU CÓDIGO AQUÍ — operaciones vectorizadas; maneja max == min
    return None
""",
    r"""
import numpy as np
a = np.array([0.0, 5.0, 10.0])
res = normalizar(a)
revisar("primer == 0", abs(res[0] - 0.0) < 1e-9)
revisar("ultimo == 1", abs(res[-1] - 1.0) < 1e-9)
revisar("medio == 0.5", abs(res[1] - 0.5) < 1e-9)
revisar("todos iguales -> ceros", np.array_equal(normalizar(np.array([3.0, 3.0, 3.0])),
                                                  np.zeros(3)))
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def normalizar(arr):
    minv = arr.min()
    maxv = arr.max()
    if maxv == minv:
        return np.zeros_like(arr, dtype=float)
    return (arr - minv) / (maxv - minv)
```
`np.zeros_like(arr)` crea un array de ceros con el mismo shape y dtype.
La resta y división son vectorizadas: se aplican a todos los elementos.
</details>
""",
)

# ---- 6 --------------------------------------------------------------------
ejercicio(
    6, "Percentil 90 de alturas aleatorias",
    r"""Escribe `percentil90_alturas(n, seed)` que:
1. Genere `n` alturas aleatorias con distribución `Normal(170, 10)` (media 170 cm,
   std 10 cm) usando `np.random.default_rng(seed)`.
2. Devuelva el **percentil 90** de esas alturas, redondeado a 2 decimales.

Usa `np.percentile`.

**Ejemplo:**
```python
percentil90_alturas(1000, seed=42)  # → un número cerca de 183 cm
```""",
    r"""
import numpy as np

def percentil90_alturas(n, seed=42):
    # ✏️ TU CÓDIGO AQUÍ — genera alturas y calcula el percentil 90
    return None
""",
    r"""
import numpy as np
res = percentil90_alturas(10_000, seed=42)
revisar("es flotante", isinstance(res, float))
revisar("entre 180 y 190 cm con seed=42", 180.0 < res < 192.0)
revisar("con seed fija, reproducible",
        percentil90_alturas(10_000, seed=42) == percentil90_alturas(10_000, seed=42))
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def percentil90_alturas(n, seed=42):
    rng = np.random.default_rng(seed)
    alturas = rng.normal(loc=170, scale=10, size=n)
    return round(float(np.percentile(alturas, 90)), 2)
```
`rng.normal(loc, scale, size)` genera la distribución normal;
`np.percentile(arr, 90)` devuelve el valor por debajo del cual cae el 90% de los datos.
`round(float(...), 2)` garantiza el tipo y precisión requeridos.
</details>
""",
)

# ---- 7 --------------------------------------------------------------------
ejercicio(
    7, "Ventas totales por ciudad (multiplicación matricial)",
    r"""Escribe `ingresos_por_ciudad(unidades, precios)` que calcule el ingreso
total por ciudad usando multiplicación matricial.

- `unidades`: matriz (n_ciudades, n_productos) — unidades vendidas.
- `precios`: vector (n_productos,) — precio unitario de cada producto.
- Devuelve: vector (n_ciudades,) — ingreso total por ciudad.

No uses bucles; usa `@` o `np.dot`.

**Ejemplo:**
```python
u = np.array([[10, 5], [3, 8]])    # 2 ciudades, 2 productos
p = np.array([100, 200])           # precios
ingresos_por_ciudad(u, p)          # → array([2000, 1900])
# Bogota: 10*100 + 5*200 = 2000
# Medellin: 3*100 + 8*200 = 1900
```""",
    r"""
import numpy as np

def ingresos_por_ciudad(unidades, precios):
    # ✏️ TU CÓDIGO AQUÍ — una sola operación matricial
    return None
""",
    r"""
import numpy as np
u = np.array([[10, 5], [3, 8]])
p = np.array([100, 200])
res = ingresos_por_ciudad(u, p)
revisar("tipo ndarray", isinstance(res, np.ndarray))
revisar("Bogota 2000", res[0] == 2000)
revisar("Medellin 1900", res[1] == 1900)
revisar("shape correcto", res.shape == (2,))
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def ingresos_por_ciudad(unidades, precios):
    return unidades @ precios
```
`(n_ciudades, n_productos) @ (n_productos,)` → `(n_ciudades,)`.
El operador `@` hace la suma de productos fila × columna, exactamente lo que queremos.
</details>
""",
)

# ---- 8 --------------------------------------------------------------------
ejercicio(
    8, "Reshape y transpose de una matriz 2D",
    r"""Escribe `reordenar(arr_1d, filas, columnas)` que:
1. Convierta `arr_1d` (array 1-D de `filas * columnas` elementos) en una
   matriz de shape `(filas, columnas)`.
2. Devuelva la **transpuesta** de esa matriz.

**Ejemplo:**
```python
a = np.arange(6)   # [0, 1, 2, 3, 4, 5]
reordenar(a, 2, 3)
# reshape → [[0,1,2],[3,4,5]]   shape (2,3)
# .T      → [[0,3],[1,4],[2,5]] shape (3,2)
```""",
    r"""
import numpy as np

def reordenar(arr_1d, filas, columnas):
    # ✏️ TU CÓDIGO AQUÍ — reshape luego .T
    return None
""",
    r"""
import numpy as np
a = np.arange(6)
res = reordenar(a, 2, 3)
revisar("shape (3,2)", res.shape == (3, 2))
revisar("esquina [0,0] == 0", res[0, 0] == 0)
revisar("esquina [0,1] == 3", res[0, 1] == 3)
revisar("shape (4,3) con 12 elems", reordenar(np.arange(12), 3, 4).shape == (4, 3))
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def reordenar(arr_1d, filas, columnas):
    return arr_1d.reshape(filas, columnas).T
```
`reshape` cambia la forma sin copiar datos;
`.T` transpone intercambiando los ejes (también sin copiar, solo cambia strides).
</details>
""",
)

# ---- 9 --------------------------------------------------------------------
ejercicio(
    9, "Comparar tiempos: bucle vs np.sum",
    r"""Escribe `comparar_tiempos(n)` que:
1. Cree un array de `n` números aleatorios con `np.random.default_rng(0)`.
2. Mida el tiempo de sumar con un bucle Python y con `np.sum`.
3. Devuelva la tupla `(tiempo_bucle, tiempo_numpy)` en segundos.

Usa `time.perf_counter` para medir.

**Nota:** no hay valores correctos/incorrectos para los tiempos, pero
`tiempo_numpy` debe ser **menor** que `tiempo_bucle` para `n >= 100_000`.

**Ejemplo:**
```python
tb, tn = comparar_tiempos(500_000)
print(tb, tn)  # algo como (0.08, 0.0005)
```""",
    r"""
import numpy as np
import time

def comparar_tiempos(n):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
import numpy as np
res = comparar_tiempos(500_000)
revisar("devuelve 2 valores", res is not None and len(res) == 2)
revisar("numpy mas rapido", res[1] < res[0])
revisar("ambos positivos", res[0] > 0 and res[1] > 0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def comparar_tiempos(n):
    import time
    rng = np.random.default_rng(0)
    arr = rng.random(n)

    # Bucle Python
    t0 = time.perf_counter()
    total = 0.0
    for x in arr:
        total += x
    t1 = time.perf_counter()
    tiempo_bucle = t1 - t0

    # NumPy vectorizado
    t0 = time.perf_counter()
    _ = np.sum(arr)
    t1 = time.perf_counter()
    tiempo_numpy = t1 - t0

    return (tiempo_bucle, tiempo_numpy)
```
Con n=500.000, el bucle Python puede tardar ~100ms y `np.sum` ~1ms.
</details>
""",
)

# ---- 10 -------------------------------------------------------------------
ejercicio(
    10, "Indexing avanzado: filas que cumplen dos condiciones",
    r"""Escribe `transacciones_validas(matriz, min_monto, max_monto)` que:
- Reciba una matriz de shape (n, 3) donde la columna 0 es el monto,
  la columna 1 es la ciudad_id y la columna 2 es la categoria_id.
- Devuelva solo las **filas** donde el monto está en el rango
  `[min_monto, max_monto]` (inclusivo en ambos extremos).

Usa indexing booleano con dos condiciones combinadas con `&`.

**Ejemplo:**
```python
m = np.array([[50, 1, 0], [200, 2, 1], [75, 0, 2], [300, 1, 1]])
transacciones_validas(m, 60, 250)
# → array([[200,   2,   1],
#          [ 75,   0,   2]])
```""",
    r"""
import numpy as np

def transacciones_validas(matriz, min_monto, max_monto):
    # ✏️ TU CÓDIGO AQUÍ — dos máscaras booleanas combinadas con &
    return None
""",
    r"""
import numpy as np
m = np.array([[50, 1, 0], [200, 2, 1], [75, 0, 2], [300, 1, 1]])
res = transacciones_validas(m, 60, 250)
revisar("shape correcto", res.shape == (2, 3))
revisar("montos en rango", (res[:, 0] >= 60).all() and (res[:, 0] <= 250).all())
revisar("sin filas si nada cumple",
        transacciones_validas(m, 1000, 2000).shape[0] == 0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def transacciones_validas(matriz, min_monto, max_monto):
    montos = matriz[:, 0]                          # columna 0
    mask = (montos >= min_monto) & (montos <= max_monto)
    return matriz[mask]
```
`matriz[:, 0]` extrae la columna de montos.
La máscara combina dos condiciones con `&` (AND booleano de NumPy).
`matriz[mask]` selecciona las filas completas donde la máscara es True.
</details>
""",
)

C.append(md(r"""
---
## ¡Terminaste la práctica 01!

Si todas las comprobaciones muestran ✅, dominas los fundamentos de NumPy:
**estadísticas, vectorización, broadcasting, indexing booleano y álgebra lineal**.

➡️ Continúa con **practice02.ipynb**, donde aplicaremos NumPy a un análisis
numérico real del dataset de transacciones.
"""))


# ===================================================================== #
# VALIDACIÓN EN TIEMPO DE CONSTRUCCIÓN
# ===================================================================== #
def _validar():
    import numpy as np

    def estadisticas(precios):
        return (np.mean(precios), np.std(precios), np.min(precios), np.max(precios))

    p = np.array([100, 200, 300, 400, 500])
    res = estadisticas(p)
    assert abs(res[0] - 300.0) < 1e-9
    assert res[2] == 100 and res[3] == 500

    def ventas_sobre_promedio(ventas):
        return ventas[ventas > ventas.mean()]

    v = np.array([50, 200, 80, 350, 120])
    res2 = ventas_sobre_promedio(v)
    assert set(res2.tolist()) == {200, 350}
    assert len(ventas_sobre_promedio(np.array([5, 5, 5]))) == 0

    def aplicar_iva(precios, tasa):
        return precios * (1 + tasa)

    p2 = np.array([100_000, 50_000, 200_000])
    assert abs(aplicar_iva(p2, 0.19)[0] - 119_000.0) < 0.01
    assert np.allclose(aplicar_iva(p2, 0.0), p2)

    def resumen_ventas(matriz):
        return (np.sum(matriz, axis=1), np.sum(matriz, axis=0))

    m = np.array([[10, 20], [30, 40], [50, 60]])
    r = resumen_ventas(m)
    assert np.array_equal(r[0], np.array([30, 70, 110]))
    assert np.array_equal(r[1], np.array([90, 120]))

    def normalizar(arr):
        minv = arr.min()
        maxv = arr.max()
        if maxv == minv:
            return np.zeros_like(arr, dtype=float)
        return (arr - minv) / (maxv - minv)

    a = np.array([0.0, 5.0, 10.0])
    res3 = normalizar(a)
    assert abs(res3[0] - 0.0) < 1e-9
    assert abs(res3[-1] - 1.0) < 1e-9
    assert np.array_equal(normalizar(np.array([3.0, 3.0, 3.0])), np.zeros(3))

    def percentil90_alturas(n, seed=42):
        rng = np.random.default_rng(seed)
        alturas = rng.normal(loc=170, scale=10, size=n)
        return round(float(np.percentile(alturas, 90)), 2)

    res4 = percentil90_alturas(10_000, seed=42)
    assert isinstance(res4, float)
    assert 180.0 < res4 < 192.0

    def ingresos_por_ciudad(unidades, precios):
        return unidades @ precios

    u = np.array([[10, 5], [3, 8]])
    p3 = np.array([100, 200])
    res5 = ingresos_por_ciudad(u, p3)
    assert res5[0] == 2000 and res5[1] == 1900

    def reordenar(arr_1d, filas, columnas):
        return arr_1d.reshape(filas, columnas).T

    a2 = np.arange(6)
    res6 = reordenar(a2, 2, 3)
    assert res6.shape == (3, 2)
    assert res6[0, 0] == 0 and res6[0, 1] == 3

    def comparar_tiempos(n):
        import time
        rng2 = np.random.default_rng(0)
        arr = rng2.random(n)
        t0 = time.perf_counter()
        total = 0.0
        for x in arr:
            total += x
        t1 = time.perf_counter()
        tiempo_bucle = t1 - t0
        t0 = time.perf_counter()
        _ = np.sum(arr)
        t1 = time.perf_counter()
        tiempo_numpy = t1 - t0
        return (tiempo_bucle, tiempo_numpy)

    tb, tn = comparar_tiempos(500_000)
    assert tb > 0 and tn > 0
    assert tn < tb

    def transacciones_validas(matriz, min_monto, max_monto):
        montos = matriz[:, 0]
        mask = (montos >= min_monto) & (montos <= max_monto)
        return matriz[mask]

    m2 = np.array([[50, 1, 0], [200, 2, 1], [75, 0, 2], [300, 1, 1]])
    res7 = transacciones_validas(m2, 60, 250)
    assert res7.shape == (2, 3)
    assert (res7[:, 0] >= 60).all() and (res7[:, 0] <= 250).all()
    assert transacciones_validas(m2, 1000, 2000).shape[0] == 0

    print("✔ Todas las soluciones de referencia de practice01 (clase05) pasan sus pruebas.")


_validar()


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase05", "practice01.ipynb")
build(os.path.abspath(ruta), C)
