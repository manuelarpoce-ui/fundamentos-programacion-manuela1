"""Construye curso/clase05/lecture.ipynb — NumPy: arrays, indexing, broadcasting y álgebra lineal."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []  # lista de celdas


# ===================================================================== #
# 0. PORTADA Y AGENDA  (15 min)
# ===================================================================== #
C += [
md(r"""
# Clase 5 · NumPy: arrays numéricos de alto rendimiento

### Fundamentos de Programación para Ciencia de Datos

> *"NumPy es el sustrato sobre el que reposa casi todo el ecosistema científico de Python."*
> — Jake VanderPlas, *Python Data Science Handbook*

---

**Duración:** 3 horas · **Modalidad:** notebook interactivo

Hasta ahora hemos usado listas de Python para guardar colecciones de datos.
Son flexibles, pero tienen un precio: son lentas para cálculos numéricos masivos.
**NumPy** resuelve exactamente ese problema. Es la librería que está por debajo
de pandas, scikit-learn, TensorFlow y casi toda la ciencia de datos en Python.

Hoy aprenderemos cómo funciona NumPy, por qué es rápido, y cómo aprovechar sus
herramientas para hacer cálculos vectorizados, filtrar datos y operar matrices
sin escribir un solo bucle.
"""),

md(r"""
## Mapa de la clase

| Bloque | Tiempo | Qué haremos |
|---|---|---|
| 1. Motivación: listas vs arrays | 20 min | Medir diferencia de velocidad |
| 2. El ndarray: shape, dtype, ndim | 25 min | La estructura central de NumPy |
| 3. Crear arrays | 20 min | zeros, ones, arange, linspace, random |
| 4. Indexing y slicing | 25 min | Multidimensional, vistas vs copias |
| 5. Operaciones vectorizadas | 20 min | Operar arrays sin bucles |
| 6. Broadcasting | 25 min | Reglas, casos comunes y trampas |
| 7. Funciones universales (ufuncs) | 15 min | sum, mean, std, axis= |
| 8. Indexing booleano | 15 min | Filtrar filas de una matriz |
| 9. Reshaping | 15 min | reshape, flatten, transpose |
| 10. Álgebra lineal básica | 15 min | dot, matmul, linalg.norm |
| 11. Números aleatorios reproducibles | 10 min | default_rng(seed) |
| 12. Errores comunes, resumen y quiz | 15 min | Trampas clásicas |

> 🧭 **Cómo usar este notebook:** lee cada celda de texto antes de ejecutar
> la celda de código. Detente en los bloques **🤔 ¿Qué pasaría si...?** e
> intenta responder mentalmente antes de ver la respuesta.
"""),
]


# ===================================================================== #
# 1. MOTIVACIÓN: LISTAS vs ARRAYS  (20 min)
# ===================================================================== #
C += [
md(r"""
## 1. Motivación: ¿por qué NumPy si ya tenemos listas?

Imagina que tienes los precios de un millón de productos y necesitas aplicar
un 19 % de IVA a cada uno. Con una lista Python:

```python
precios_con_iva = [p * 1.19 for p in precios]
```

Funciona. Pero Python tiene que:
1. Leer el precio (objeto Python de tipo `float`, 28 bytes en memoria).
2. Crear un objeto Python para `1.19`.
3. Hacer la multiplicación a nivel de objetos Python.
4. Crear un nuevo objeto para el resultado.
5. Guardarlo en la lista.

Repite eso un millón de veces. Con NumPy, **todo el array vive en un bloque
contiguo de memoria** como valores de 8 bytes (`float64`), y la multiplicación
se ejecuta en C puro sobre ese bloque. La diferencia es de 10x a 100x.
"""),

code(r"""
import numpy as np
import time

# Creamos un millón de precios entre $10.000 y $500.000
rng = np.random.default_rng(42)
precios_lista = list(rng.integers(10_000, 500_000, size=1_000_000))
precios_array = np.array(precios_lista)

# Versión lista (Python puro)
t0 = time.perf_counter()
iva_lista = [p * 1.19 for p in precios_lista]
t1 = time.perf_counter()
tiempo_lista = t1 - t0

# Versión NumPy (operación vectorizada)
t0 = time.perf_counter()
iva_array = precios_array * 1.19
t1 = time.perf_counter()
tiempo_numpy = t1 - t0

print("Tiempo con lista Python:  {:.4f} s".format(tiempo_lista))
print("Tiempo con NumPy:         {:.4f} s".format(tiempo_numpy))
print("NumPy es {:.0f}x más rapido".format(tiempo_lista / tiempo_numpy))
print("Resultados coinciden:", iva_lista[:3], list(iva_array[:3]))
"""),

md(r"""
### ¿Por qué es tan rápido NumPy?

```
Lista Python           Array NumPy
═══════════════════    ═══════════════════════════════════════
│PyObject│ → 28 B │    │ f64 │ f64 │ f64 │ f64 │ ... │ f64 │
│PyObject│ → 28 B │    └─────────────────────────────────────┘
│PyObject│ → 28 B │    Bloque contiguo, 8 bytes cada elemento
│  ...   │         │    ← operación en C sobre todo el bloque
═══════════════════
Punteros dispersos
en memoria
```

- **Tipo homogéneo:** todos los elementos son del mismo tipo (`dtype`), así no
  hay overhead de "averiguar qué tipo es este objeto".
- **Memoria contigua:** el procesador puede leer el bloque entero de un tirón,
  aprovechando la caché. Las listas Python saltan por toda la RAM.
- **Código nativo:** las operaciones (+, *, sin...) se ejecutan en C/Fortran
  compilado, no interpretado.

> 💡 En ciencia de datos, los conjuntos de datos tienen millones o miles de
> millones de filas. La diferencia entre una lista y un array NumPy puede ser
> la diferencia entre un análisis que tarda 5 segundos o 10 minutos.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- ¿...el array tuviera enteros en vez de flotantes? ¿Seguiría siendo rápido?
  (Sí: la clave es el tipo homogéneo, no si es `int` o `float`.)
- ¿...mezclaras un entero y una cadena en el mismo array NumPy? ¿Qué tipo
  tomaría? (Lo descubrimos en el bloque siguiente.)
"""),
]


# ===================================================================== #
# 2. EL NDARRAY: shape, dtype, ndim
# ===================================================================== #
C += [
md(r"""
## 2. El ndarray: shape, dtype, ndim

El objeto central de NumPy es el **ndarray** (*n-dimensional array*). Tres
atributos lo describen completamente:

| Atributo | Significado | Ejemplo |
|---|---|---|
| `shape` | tupla con el tamaño de cada dimensión | `(3, 4)` → 3 filas, 4 cols |
| `dtype` | tipo de dato de cada elemento | `float64`, `int32`, `bool` |
| `ndim`  | número de dimensiones | `1` (vector), `2` (matriz), `3` (tensor) |

El tipo homogéneo es la clave del rendimiento. Cuando creas un array,
NumPy elige automáticamente el `dtype` más conveniente — o tú puedes
especificarlo.
"""),

code(r"""
import numpy as np

# 1-D: vector (como una lista, pero numérico)
ventas = np.array([120_000, 89_000, 240_000, 310_000, 56_000])
print("ventas:", ventas)
print("  shape:", ventas.shape, "| dtype:", ventas.dtype, "| ndim:", ventas.ndim)

# 2-D: matriz (lista de listas)
matriz_ventas = np.array([
    [120_000, 89_000, 240_000],   # Bogotá: ene, feb, mar
    [310_000, 56_000, 190_000],   # Medellín: ene, feb, mar
    [ 75_000, 210_000, 88_000],   # Cali: ene, feb, mar
])
print("\nmatriz_ventas:\n", matriz_ventas)
print("  shape:", matriz_ventas.shape, "| ndim:", matriz_ventas.ndim)
"""),

md(r"""
### El dtype importa: coerción automática

Cuando mezclas tipos en un array, NumPy los **unifica** al tipo más general:
"""),

code(r"""
import numpy as np

a = np.array([1, 2, 3])           # solo enteros → int64
b = np.array([1, 2.5, 3])         # mezcla int/float → float64
c = np.array([1, 2, "tres"])      # mezcla int/str → U21 (Unicode)

print("a dtype:", a.dtype)   # int64
print("b dtype:", b.dtype)   # float64 (promoción automática)
print("c dtype:", c.dtype)   # <U21 (cadena Unicode)

# Si 'c' fuera un array de precios, las operaciones aritméticas fallarían.
# Por eso es crítico controlar el dtype al cargar datos.
try:
    c * 2
except TypeError as e:
    print("Error con array de strings:", e)
"""),

md(r"""
### Trazado de shape

Para entender una operación NumPy, escribe el shape de cada array:

```
ventas.shape      = (5,)       ← vector de 5 elementos
precios.shape     = (100,)     ← vector de 100 precios
matriz.shape      = (3, 4)     ← 3 filas, 4 columnas
tensor.shape      = (2, 3, 4)  ← 2 "tablas" de 3×4
```

Cuando veas un error como `operands could not be broadcast together`,
lo primero que debes hacer es imprimir `.shape` de cada operando.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- Tienes `np.array([1, 2, 3, 4])` con `dtype=int64`. Al multiplicarlo por `0.5`,
  ¿el resultado sería `int64` o `float64`? (NumPy promueve al tipo más general.)
- ¿Cuál sería el `ndim` de `np.array([[[1, 2], [3, 4]]])`?
  (Cuenta los niveles de corchetes: tres → `ndim=3`.)
"""),
]


# ===================================================================== #
# 3. CREAR ARRAYS
# ===================================================================== #
C += [
md(r"""
## 3. Crear arrays: el catálogo de constructores

NumPy ofrece muchas funciones para crear arrays sin tener que tipear todos
los valores a mano.

| Función | Qué crea | Uso típico |
|---|---|---|
| `np.array(lista)` | array desde una lista Python | cargar datos conocidos |
| `np.zeros(shape)` | array de ceros | inicializar acumuladores |
| `np.ones(shape)` | array de unos | pesos, matrices identidad |
| `np.arange(inicio, fin, paso)` | como `range()` | secuencias numéricas |
| `np.linspace(a, b, n)` | `n` puntos equidistantes en [a, b] | gráficas, simulaciones |
| `np.eye(n)` | matriz identidad n×n | álgebra lineal |
| `np.random.default_rng(seed)` | generador reproducible | simulaciones |
"""),

code(r"""
import numpy as np

# Ceros y unos: muy útiles para inicializar matrices de resultados
acumulador = np.zeros(5)           # [0. 0. 0. 0. 0.]
pesos = np.ones(4) / 4             # pesos uniformes: [0.25, 0.25, 0.25, 0.25]

# arange: como range() pero devuelve un array (acepta floats)
dias = np.arange(1, 8)             # [1, 2, 3, 4, 5, 6, 7]
paso = np.arange(0, 1.1, 0.25)    # [0.  0.25 0.5  0.75 1. ]

# linspace: útil cuando quieres exactamente n puntos
meses = np.linspace(0, 1, 5)       # [0.  0.25 0.5  0.75 1. ]

print("acumulador:", acumulador)
print("pesos:     ", pesos)
print("dias:      ", dias)
print("paso:      ", paso)
print("meses:     ", meses)
"""),

code(r"""
import numpy as np

# zeros/ones con forma 2D: inicializar matrices
tabla_ventas = np.zeros((3, 4))    # 3 ciudades, 4 trimestres
print("Tabla vacía:\n", tabla_ventas)

# eye: matriz identidad (álgebra lineal)
identidad = np.eye(3)
print("\nMatriz identidad 3x3:\n", identidad)

# Crear y llenar: un array de días laborables con precio de apertura ficticio
rng = np.random.default_rng(7)
precios_apertura = rng.uniform(10_000, 50_000, size=30)   # 30 días
print("\nPrimeros 5 precios de apertura:", precios_apertura[:5].round(0))
"""),

md(r"""
### La diferencia entre arange y linspace

```
np.arange(0, 1, 0.3)   →  [0.   0.3  0.6  0.9]     ← paso fijo, n variable
np.linspace(0, 1, 4)   →  [0.   0.333 0.667 1.]     ← n fijo, paso variable
```

Usa `arange` cuando el **paso** importa; usa `linspace` cuando el **número de
puntos** importa (muy común en gráficas donde quieres exactamente 100 o 1000
puntos).

> ⚠️ `np.arange` con paso flotante puede dar sorpresas por aritmética de punto
> flotante. Para rangos precisos, `linspace` es más seguro.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- `np.zeros(5)` crea flotantes. ¿Cómo crearías un array de 5 ceros **enteros**?
  (pista: `dtype=int`)
- ¿Cuántos elementos tiene `np.arange(2, 10, 3)`?
  (Traza: 2, 5, 8 → 3 elementos.)
"""),
]


# ===================================================================== #
# 4. INDEXING Y SLICING MULTIDIMENSIONAL
# ===================================================================== #
C += [
md(r"""
## 4. Indexing y slicing multidimensional

El indexing de NumPy extiende la sintaxis de listas Python a múltiples
dimensiones. En lugar de `[i][j]`, usas `[i, j]`.

```
         col 0    col 1    col 2
fila 0 │ 120000 │  89000 │ 240000 │
fila 1 │ 310000 │  56000 │ 190000 │
fila 2 │  75000 │ 210000 │  88000 │
```

- `m[1, 2]`   → elemento en fila 1, col 2 → `190000`
- `m[0, :]`   → toda la fila 0 (Bogotá)
- `m[:, 1]`   → toda la col 1 (febrero)
- `m[1:, :2]` → submatriz: filas 1 y 2, columnas 0 y 1
"""),

code(r"""
import numpy as np

m = np.array([
    [120_000,  89_000, 240_000],   # Bogota: ene, feb, mar
    [310_000,  56_000, 190_000],   # Medellin: ene, feb, mar
    [ 75_000, 210_000,  88_000],   # Cali: ene, feb, mar
])

print("Venta de Medellin en marzo (fila 1, col 2):", m[1, 2])
print("Ventas de Bogota (fila 0):                 ", m[0, :])
print("Ventas de febrero (col 1):                 ", m[:, 1])
print("Submatriz [1:, :2]:\n", m[1:, :2])
"""),

md(r"""
### ⚠️ Vista vs Copia: la trampa más común

El slicing de NumPy devuelve una **vista** (un "alias"), no una copia. Si
modificas la vista, modificas el array original:

```
lista Python:   lista[1:3]     → siempre copia nueva
NumPy:          arr[1:3]       → vista (alias), ¡modifica el original!
                arr[1:3].copy() → copia explícita (segura)
```

Esta decisión de diseño existe porque copiar arrays grandes costaría mucha
memoria. Pero si no la conoces, produce bugs sutiles y difíciles de detectar.
"""),

code(r"""
import numpy as np

original = np.array([10, 20, 30, 40, 50])

# Slicing → vista (alias del original)
vista = original[1:4]
vista[0] = 999          # <-- modificar la vista cambia el original

print("original tras modificar la vista:", original)  # 999 aparece en posición 1
print("vista:", vista)

# Para evitarlo: .copy()
copia = original[1:4].copy()
copia[0] = 0
print("\noriginal tras modificar la COPIA:", original)  # no cambia
"""),

code(r"""
import numpy as np

# Indexing multidimensional: ver todas las ventas de enero (columna 0)
# y filtrar las ciudades que vendieron más de 100.000 en enero

ventas = np.array([
    [120_000,  89_000, 240_000],
    [310_000,  56_000, 190_000],
    [ 75_000, 210_000,  88_000],
    [ 95_000, 180_000, 320_000],
])

enero = ventas[:, 0]          # todos los valores de la columna 0
print("Ventas de enero:", enero)

# Ciudades con ventas de enero > 100.000 (indexing booleano, lo veremos a fondo)
mask = enero > 100_000
print("Ciudades que superan 100k en enero:", ventas[mask])
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- Tienes `a = np.arange(12).reshape(3, 4)`. ¿Qué devuelve `a[1:, 2:]`?
  (Traza: filas 1 y 2, columnas 2 y 3 → submatriz 2×2.)
- Si haces `b = a[0]` y luego `b[0] = -1`, ¿cambia `a[0, 0]`?
  (Sí: `a[0]` es una vista de la primera fila.)
"""),
]


# ===================================================================== #
# 5. OPERACIONES VECTORIZADAS
# ===================================================================== #
C += [
md(r"""
## 5. Operaciones vectorizadas: adios a los bucles

Una **operación vectorizada** aplica una operación a todos los elementos de
un array de una vez, sin escribir un `for`. Internamente NumPy ejecuta el
bucle en C, que es órdenes de magnitud más rápido.

```
Python (bucle):             NumPy (vectorizado):
resultado = []              resultado = arr * 1.19
for x in arr:
    resultado.append(x * 1.19)
```

Las operaciones aritméticas básicas (`+`, `-`, `*`, `/`, `**`, `%`) entre
arrays del mismo shape, o entre un array y un escalar, operan elemento a
elemento:
"""),

code(r"""
import numpy as np

# Precios de artículos en pesos colombianos
precios = np.array([45_000, 120_000, 88_000, 210_000, 33_000])

# IVA del 19%: operación escalar-array
precios_con_iva = precios * 1.19
print("Precios con IVA:", precios_con_iva.astype(int))

# Descuento del 10%: todos los productos en oferta
descuentos = precios * 0.10
precios_oferta = precios - descuentos
print("Precios en oferta:", precios_oferta.astype(int))

# Comparar dos versiones de precios (array - array)
precios_2023 = np.array([42_000, 115_000, 85_000, 200_000, 30_000])
variacion = precios - precios_2023
print("Variacion respecto a 2023:", variacion)
print("Variacion %:", (variacion / precios_2023 * 100).round(1))
"""),

code(r"""
import numpy as np

# Operaciones entre matrices del mismo shape: elemento a elemento
ventas_q1 = np.array([[120_000, 89_000], [310_000, 56_000]])
ventas_q2 = np.array([[ 95_000, 105_000], [280_000, 70_000]])

total_semestral = ventas_q1 + ventas_q2
print("Total semestral:\n", total_semestral)

crecimiento = (ventas_q2 - ventas_q1) / ventas_q1 * 100
print("\nCrecimiento Q2 vs Q1 (%):\n", crecimiento.round(1))
"""),

md(r"""
### Por qué evitar los bucles explícitos en NumPy

```
Con bucle:  for i in range(n): resultado[i] = a[i] + b[i]   ← O(n) en Python
Vectorizado: resultado = a + b                               ← O(n) en C

Para n = 1 millón: el bucle puede tardar ~0.5 s, el vectorizado ~0.001 s.
```

> 🚩 **Regla de oro:** si te encuentras escribiendo `for i in range(len(arr)):`,
> pregúntate si NumPy tiene una forma vectorizada. Casi siempre la tiene.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- Tienes dos arrays de distinto tamaño, `np.array([1,2,3]) + np.array([1,2])`.
  ¿Qué lanza NumPy? (Un `ValueError`: shapes incompatibles. Más adelante veremos
  cuándo sí se pueden combinar arrays de distintos tamaños: broadcasting.)
- ¿Cuál es el resultado de `np.array([2, 4, 8]) ** np.array([1, 2, 3])`?
  (Elemento a elemento: [2¹, 4², 8³] = [2, 16, 512].)
"""),
]


# ===================================================================== #
# 6. BROADCASTING
# ===================================================================== #
C += [
md(r"""
## 6. Broadcasting: operar arrays de distintos shapes

**Broadcasting** es el mecanismo por el cual NumPy opera arrays de shapes
distintos. En vez de copiar datos, "expande" mentalmente el array más pequeño
para que encaje con el más grande.

### Las reglas (de atrás hacia adelante en el shape)

```
Regla 1: si dos shapes difieren en número de dimensiones,
          el de menos dims se rellena con 1 a la izquierda.

Regla 2: las dimensiones deben ser iguales O una de ellas debe ser 1.
          Si es 1, se "estira" hasta coincidir.

Regla 3: si ninguna condición se cumple → ValueError.
```

Ejemplo visual:

```
 A.shape = (3, 4)     cada fila tiene 4 elementos
 B.shape =    (4,)    ← se trata como (1, 4) y se repite 3 veces
─────────────────────
resultado.shape = (3, 4)
```
"""),

code(r"""
import numpy as np

# Caso 1: vector + escalar (caso trivial, siempre funciona)
precios = np.array([10_000, 25_000, 50_000])
con_iva = precios * 1.19
print("Vector + escalar:", con_iva.astype(int))

# Caso 2: matriz + vector → se suma el vector a CADA fila
costos = np.array([
    [100, 200, 300],   # producto A: costo materiales, mano de obra, logistica
    [150, 180, 250],   # producto B
    [ 80, 220, 400],   # producto C
])
gastos_fijos = np.array([50, 30, 80])   # gastos fijos por categoría

total = costos + gastos_fijos            # (3,3) + (3,) → broadcasting
print("\nCostos + gastos fijos:\n", total)
print("Shape costos:", costos.shape, "| Shape gastos_fijos:", gastos_fijos.shape)
"""),

code(r"""
import numpy as np

# Caso 3: columna + fila → tabla de combinaciones (broadcasting 2D real)
# Calcular precio total: base de ciudad x factor de categoría

base_ciudad = np.array([[100], [120], [90]])   # shape (3, 1): Bogota, Medellin, Cali
factor_cat  = np.array([1.0,  1.2,  0.8, 1.5]) # shape (4,):  tec, ropa, hogar, alim

tabla_precios = base_ciudad * factor_cat        # (3,1) x (4,) → (3,4)
print("Base ciudad shape:", base_ciudad.shape)
print("Factor cat shape: ", factor_cat.shape)
print("Tabla precios shape:", tabla_precios.shape)
print("Tabla de precios:\n", tabla_precios)
"""),

md(r"""
### Casos trampa del broadcasting

```
np.array([1,2,3]) + np.array([1,2])         → ERROR: shapes (3,) y (2,) incompatibles
np.array([[1],[2],[3]]) + np.array([1,2,3]) → OK: (3,1) + (3,) se expande a (3,3)

La trampa: confundir un array de shape (3,) con uno de shape (3,1).
Son distintos y producen resultados muy distintos al hacer broadcasting.
```

Siempre revisa los shapes antes de operar. Si el resultado no es el que
esperas, imprime `.shape` de cada operando.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- `A.shape = (4, 1)` y `B.shape = (1, 3)`. ¿Cuál sería el shape del resultado
  de `A + B`? (Broadcasting: 4 > 1 y 3 > 1 → resultado (4, 3).)
- ¿Qué pasa con `np.array([1,2,3,4]) + np.array([[1],[2]])`?
  (Shape (4,) + (2,1) → resultado (2,4): la fila se repite 2 veces.)
"""),
]


# ===================================================================== #
# 7. FUNCIONES UNIVERSALES (ufuncs)
# ===================================================================== #
C += [
md(r"""
## 7. Funciones universales (ufuncs) y reducciones

Las **ufuncs** (universal functions) son funciones que operan elemento a
elemento sobre arrays, y las **reducciones** colapsan una o más dimensiones.

### Ufuncs elemento a elemento

| Función | Significado |
|---|---|
| `np.abs(a)` | valor absoluto |
| `np.sqrt(a)` | raíz cuadrada |
| `np.exp(a)` | e^a |
| `np.log(a)` | logaritmo natural |
| `np.round(a, d)` | redondear a d decimales |
| `np.clip(a, min, max)` | recortar a un rango |

### Reducciones (colapsan el array)

| Función | Significado | Eje |
|---|---|---|
| `np.sum(a, axis=k)` | suma | `axis=0` colapsa filas, `axis=1` colapsa columnas |
| `np.mean(a, axis=k)` | promedio | igual |
| `np.std(a, axis=k)` | desviación estándar | igual |
| `np.min/max(a, axis=k)` | mínimo/máximo | igual |
| `np.argmin/argmax(a)` | índice del mínimo/máximo | |
"""),

code(r"""
import numpy as np

ventas = np.array([
    [120_000,  89_000, 240_000, 310_000],   # Bogota: Q1,Q2,Q3,Q4
    [ 56_000, 190_000,  75_000, 210_000],   # Medellin
    [ 88_000,  95_000, 180_000, 320_000],   # Cali
])

ciudades = ["Bogota", "Medellin", "Cali"]
trimestres = ["Q1", "Q2", "Q3", "Q4"]

# Reducir por trimestre: total de CADA trimestre (colapsar filas, eje 0)
total_trimestre = np.sum(ventas, axis=0)
print("Total por trimestre (axis=0):", total_trimestre)

# Reducir por ciudad: total de CADA ciudad (colapsar columnas, eje 1)
total_ciudad = np.sum(ventas, axis=1)
for c, t in zip(ciudades, total_ciudad):
    print("  {}: ${:,.0f}".format(c, t))

# Promedio general
print("\nPromedio de todas las ventas: ${:,.0f}".format(np.mean(ventas)))
print("Desviacion estandar:          ${:,.0f}".format(np.std(ventas)))
"""),

code(r"""
import numpy as np

ventas = np.array([
    [120_000,  89_000, 240_000, 310_000],
    [ 56_000, 190_000,  75_000, 210_000],
    [ 88_000,  95_000, 180_000, 320_000],
])

# argmax: ¿qué ciudad vendió más en Q3 (columna 2)?
mejor_q3 = np.argmax(ventas[:, 2])
ciudades = ["Bogota", "Medellin", "Cali"]
print("Mejor ciudad en Q3:", ciudades[mejor_q3])

# clip: limitar montos entre 100k y 250k (para análisis sin extremos)
ventas_clip = np.clip(ventas, 100_000, 250_000)
print("\nVentas recortadas [100k, 250k]:\n", ventas_clip)

# Normalizar cada fila: (x - min_fila) / (max_fila - min_fila)
min_f = ventas.min(axis=1, keepdims=True)
max_f = ventas.max(axis=1, keepdims=True)
ventas_norm = (ventas - min_f) / (max_f - min_f)
print("\nVentas normalizadas [0,1] por ciudad:\n", ventas_norm.round(2))
"""),

md(r"""
### El parámetro axis: diagrama mental

```
axis=0: opera "hacia abajo" (colapsa filas)

    col 0  col 1  col 2
    ──────────────────
    [120k,  89k, 240k]  ↕
    [ 56k, 190k,  75k]  ↕ axis=0
    [ 88k,  95k, 180k]  ↕
    ──────────────────
    [264k, 374k, 495k]  ← resultado: un valor por columna

axis=1: opera "hacia la derecha" (colapsa columnas)

    [120k,  89k, 240k, 310k]  → [759k]
    [ 56k, 190k,  75k, 210k]  → [531k]  ← resultado: un valor por fila
    [ 88k,  95k, 180k, 320k]  → [683k]
```
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- ¿Qué diferencia hay entre `np.sum(ventas)` y `np.sum(ventas, axis=0)`?
  (El primero devuelve un escalar; el segundo un array de 4 elementos.)
- `keepdims=True` en el ejemplo de normalización: ¿por qué es necesario?
  (Para que el resultado tenga shape (3,1) y el broadcasting con la matriz (3,4)
  funcione correctamente. Sin `keepdims`, el resultado tendría shape (3,) y
  la resta no se haría fila por fila.)
"""),
]


# ===================================================================== #
# 8. INDEXING BOOLEANO (FANCY INDEXING)
# ===================================================================== #
C += [
md(r"""
## 8. Indexing booleano (fancy indexing): filtrar como un experto

El **indexing booleano** permite seleccionar elementos de un array usando
otro array de booleanos del mismo shape. Es la forma NumPy de filtrar datos:

```python
mask = arr > 100_000        # array de True/False, mismo shape que arr
arr[mask]                   # solo los elementos donde mask es True
```

Equivale a un `WHERE` de SQL o a un `.query()` de pandas, pero más rápido
y sin crear un nuevo DataFrame.
"""),

code(r"""
import numpy as np

montos = np.array([45_000, 280_000, 12_000, 195_000, 350_000,
                   88_000, 420_000, 67_000, 310_000,  34_000])

# Filtrar transacciones grandes (>= 200k)
mask_grande = montos >= 200_000
print("Mascara:", mask_grande)
print("Transacciones grandes:", montos[mask_grande])
print("Cuantas:", mask_grande.sum())   # True cuenta como 1

# Filtrar por rango: entre 50k y 200k
mask_rango = (montos >= 50_000) & (montos < 200_000)   # & para AND booleano
print("\nTransacciones en rango [50k, 200k):", montos[mask_rango])
"""),

code(r"""
import numpy as np

# Indexing booleano en 2D: seleccionar filas que cumplen una condición
ventas = np.array([
    [120_000,  89_000, 240_000],   # Bogota
    [ 30_000,  25_000,  18_000],   # Ciudad pequeña (ventas bajas)
    [310_000, 190_000, 280_000],   # Medellin
    [ 56_000,  70_000,  88_000],   # Cali
    [420_000, 380_000, 450_000],   # Barranquilla (ventas muy altas)
])
ciudades = np.array(["Bogota", "PequeA", "Medellin", "Cali", "Barranquilla"])

# Ciudades cuyo promedio de ventas supera 150k
promedio_ciudad = ventas.mean(axis=1)
mask_activa = promedio_ciudad > 150_000

print("Promedios por ciudad:", promedio_ciudad.astype(int))
print("Ciudades con promedio > 150k:", ciudades[mask_activa])
print("Sus ventas:\n", ventas[mask_activa])
"""),

md(r"""
### Indexing booleano vs bucle: comparación

```python
# Con bucle:
resultado = []
for i in range(len(montos)):
    if montos[i] >= 200_000:
        resultado.append(montos[i])

# Con indexing booleano (más conciso y más rápido):
resultado = montos[montos >= 200_000]
```

El indexing booleano devuelve siempre una **copia** (no una vista). Modificar
`resultado` no modifica `montos`.

> 💡 Puedes usar `np.where(condicion, valor_si_true, valor_si_false)` para
> aplicar una función condicional elemento a elemento sin crear listas separadas.
"""),

code(r"""
import numpy as np

montos = np.array([45_000, 280_000, 12_000, 195_000, 350_000])

# np.where: clasificar cada monto como 'alto' o 'normal'
etiquetas = np.where(montos >= 200_000, "alto", "normal")
print("Montos:   ", montos)
print("Etiquetas:", etiquetas)
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- ¿Qué devuelve `montos[(montos < 100_000) | (montos > 300_000)]`?
  (Los montos que son menores a 100k O mayores a 300k, es decir, los extremos.
  `|` es OR booleano en NumPy.)
- ¿Por qué hay que escribir `(montos >= 50_000) & (montos < 200_000)` con
  paréntesis? (Porque `&` tiene mayor precedencia que `>=` y `<` en Python;
  sin paréntesis, la expresión se evaluaría de forma incorrecta.)
"""),
]


# ===================================================================== #
# 9. RESHAPING
# ===================================================================== #
C += [
md(r"""
## 9. Reshaping: cambiar la forma sin cambiar los datos

Un array es fundamentalmente un bloque de datos en memoria más una
descripción de su **forma** (shape). Cambiar la forma no mueve datos:
solo cambia cómo se interpretan.

| Función | Qué hace |
|---|---|
| `arr.reshape(nueva_forma)` | cambia el shape (devuelve vista si puede) |
| `arr.flatten()` | convierte a 1-D, siempre devuelve copia |
| `arr.ravel()` | convierte a 1-D, devuelve vista si puede |
| `arr.T` o `arr.transpose()` | transpone ejes |

**Regla:** el producto de los elementos del nuevo shape debe ser igual al
del shape original. `(12,)` puede reshapearse a `(3, 4)`, `(4, 3)`, `(2, 6)`,
`(2, 2, 3)`... pero no a `(3, 5)` (producto 15 ≠ 12).
"""),

code(r"""
import numpy as np

# Datos de ventas diarias: 12 valores (4 semanas x 3 canales)
ventas_diarias = np.arange(12) * 10_000 + 50_000
print("Original (1-D):", ventas_diarias)

# Reorganizar como 4 semanas x 3 canales
por_semana = ventas_diarias.reshape(4, 3)
print("\nPor semana (4x3):\n", por_semana)

# Transponer: ahora 3 canales x 4 semanas
por_canal = por_semana.T
print("\nPor canal (3x4):\n", por_canal)
print("Shape original:", por_semana.shape, "| Transpuesto:", por_canal.shape)
"""),

code(r"""
import numpy as np

# reshape(-1, n): el -1 le dice a NumPy "calcula tú la dimensión que falta"
datos = np.arange(1, 25)           # 24 elementos
m = datos.reshape(-1, 6)           # -1 → NumPy calcula: 24 / 6 = 4 filas
print("reshape(-1, 6):\n", m)
print("shape:", m.shape)

# flatten vs ravel: ambos dan un array 1-D
f = m.flatten()    # siempre copia
r = m.ravel()      # vista cuando es posible

f[0] = 9999        # modificar la copia NO cambia m
r[0] = 9999        # modificar el ravel SÍ puede cambiar m

print("\nm[0,0] tras flatten:", m[0, 0])   # puede ser 9999 (ravel es vista)
"""),

md(r"""
### Diagrama: reshape y transpose

```
ventas_diarias = [50k, 60k, 70k, 80k, 90k, 100k, 110k, 120k, 130k, 140k, 150k, 160k]

          reshape(4, 3)              .T
┌──────────────────────┐    ┌────────────────────────┐
│ semana 0: 50k 60k 70k│    │ canal 0: 50k  80k 110k 140k│
│ semana 1: 80k 90k100k│ ─▶ │ canal 1: 60k  90k 120k 150k│
│ semana 2:110k120k130k│    │ canal 2: 70k 100k 130k 160k│
│ semana 3:140k150k160k│    └────────────────────────┘
└──────────────────────┘
     shape (4, 3)                shape (3, 4)
```
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- Tienes `a = np.zeros((6, 4))`. ¿Puedes reshapearlo a `(8, 3)`? ¿Y a `(5, 5)`?
  (6×4=24: sí a (8,3) porque 8×3=24; no a (5,5) porque 5×5=25≠24.)
- ¿Qué devuelve `np.eye(3).T`? (La identidad: es simétrica, su transpuesta es
  ella misma.)
"""),
]


# ===================================================================== #
# 10. ÁLGEBRA LINEAL BÁSICA
# ===================================================================== #
C += [
md(r"""
## 10. Álgebra lineal básica: dot, matmul, linalg.norm

NumPy tiene soporte nativo para las operaciones de álgebra lineal más comunes.
Son el corazón de machine learning, visión computacional y optimización.

| Función | Qué hace |
|---|---|
| `np.dot(a, b)` | producto punto (vectores) o multiplicación matricial |
| `a @ b` | equivalente a `np.matmul(a, b)` (operador `@`) |
| `np.linalg.norm(v)` | norma (longitud) de un vector |
| `np.linalg.det(m)` | determinante |
| `np.linalg.inv(m)` | inversa de una matriz |
| `np.linalg.solve(A, b)` | resolver sistema lineal Ax = b |

> ⚠️ Diferencia entre `*` y `@`:
> - `A * B` → multiplicación elemento a elemento (broadcasting)
> - `A @ B` → multiplicación matricial (producto de matrices)
"""),

code(r"""
import numpy as np

# Producto punto: ventas x precio_unitario
unidades = np.array([100, 250, 180, 75])          # unidades vendidas por producto
precio   = np.array([15_000, 8_000, 25_000, 50_000])  # precio unitario

ingreso_total = np.dot(unidades, precio)
print("Ingreso total (producto punto):", "${:,.0f}".format(ingreso_total))
# Equivalente: (100*15000) + (250*8000) + (180*25000) + (75*50000)

# Distancia euclidiana: comparar dos vectors de ventas
v_bogota   = np.array([120_000, 89_000, 240_000])
v_medellin = np.array([310_000, 56_000, 190_000])

distancia = np.linalg.norm(v_bogota - v_medellin)
print("Distancia euclidiana entre ciudades: ${:,.0f}".format(distancia))
"""),

code(r"""
import numpy as np

# Multiplicación matricial: calcular ingresos por ciudad en distintos periodos
# ciudades x productos . precios → ciudades x ingresos
ventas_unidades = np.array([
    [100, 200, 50],    # Bogota: prod A, B, C
    [150, 100, 80],    # Medellin
    [ 80, 300, 30],    # Cali
])  # shape (3, 3)

precios = np.array([
    [15_000],   # precio prod A
    [ 8_000],   # precio prod B
    [25_000],   # precio prod C
])  # shape (3, 1)

ingresos = ventas_unidades @ precios   # (3,3) @ (3,1) → (3,1)
ciudades = ["Bogota", "Medellin", "Cali"]
for c, ing in zip(ciudades, ingresos.flatten()):
    print("  {}: ${:,.0f}".format(c, ing))
"""),

md(r"""
### La norma euclidiana y por qué importa

La norma de un vector `v` es su "longitud" en espacio n-dimensional:

```
||v|| = sqrt(v[0]² + v[1]² + ... + v[n]²)
```

En ciencia de datos la usamos para:
- Medir **distancias** entre observaciones (K-NN, clustering).
- **Normalizar** vectores (dividir por su norma para que tengan longitud 1).
- Medir el **error** de un modelo (norma L2 del vector de residuos).

> 💡 `np.linalg.norm(v - u)` es exactamente la distancia euclidiana
> entre los puntos `v` y `u`.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- ¿Cuál es la diferencia entre `np.dot(A, B)` y `A * B` cuando `A` y `B` son
  matrices 2×2? (`*` multiplica elemento a elemento; `np.dot` hace la
  multiplicación matricial estándar.)
- ¿Por qué un vector de norma 1 es útil en machine learning?
  (Porque todas las features tienen la misma "escala" de longitud; facilita la
  comparación entre vectores y la convergencia de algoritmos de optimización.)
"""),
]


# ===================================================================== #
# 11. NÚMEROS ALEATORIOS REPRODUCIBLES
# ===================================================================== #
C += [
md(r"""
## 11. Números aleatorios reproducibles: default_rng(seed)

Los números "aleatorios" de NumPy son en realidad **pseudoaleatorios**: siguen
una secuencia determinista iniciada por una **semilla** (seed). Esto es
fundamental en ciencia de datos: necesitas reproducibilidad.

```python
# FORMA ANTIGUA (desaconsejada): estado global
np.random.seed(42)
np.random.randn(5)

# FORMA MODERNA (recomendada desde NumPy 1.17): generador explícito
rng = np.random.default_rng(42)
rng.standard_normal(5)
```

La nueva API con `default_rng` es más segura (sin estado global que se pueda
contaminar) y más rápida.
"""),

code(r"""
import numpy as np

rng = np.random.default_rng(42)   # semilla fija: resultados reproducibles

# Distribuciones útiles
normal    = rng.standard_normal(5)            # N(0, 1)
uniforme  = rng.uniform(0, 1, size=5)         # U(0, 1)
enteros   = rng.integers(1, 100, size=5)      # enteros en [1, 100)
normal2   = rng.normal(loc=50_000, scale=15_000, size=5)  # N(50k, 15k)

print("Normal estándar:", normal.round(3))
print("Uniforme [0,1]: ", uniforme.round(3))
print("Enteros:        ", enteros)
print("Normal(50k,15k):", normal2.astype(int))
"""),

code(r"""
import numpy as np

# Simulación: generar 10.000 visitas a una tienda con monto de compra N(80k, 30k)
rng = np.random.default_rng(99)
montos = rng.normal(loc=80_000, scale=30_000, size=10_000)
montos = np.clip(montos, 1_000, None)   # eliminar valores negativos irreales

print("Simulacion de 10.000 transacciones:")
print("  Media:  ${:,.0f}".format(montos.mean()))
print("  Std:    ${:,.0f}".format(montos.std()))
print("  Min:    ${:,.0f}".format(montos.min()))
print("  Max:    ${:,.0f}".format(montos.max()))
print("  > 100k: {:.1f}%".format((montos > 100_000).mean() * 100))
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- Si ejecutas la misma celda dos veces (con la misma semilla), ¿obtienes los
  mismos números? (Sí, siempre que el `rng` se cree con la misma semilla.)
- ¿Qué pasa si creas `rng1 = np.random.default_rng(42)` y
  `rng2 = np.random.default_rng(42)`? ¿Producen la misma secuencia?
  (Sí: la misma semilla → la misma secuencia. Son generadores independientes
  pero equivalentes.)
"""),
]


# ===================================================================== #
# 12. ERRORES COMUNES
# ===================================================================== #
C += [
md(r"""
## 12. Errores comunes (y cómo evitarlos)

Estos son los errores que verás una y otra vez al empezar con NumPy:

**1. Mutar una vista creyendo que es una copia.**
El slicing devuelve una vista. Si modificas la "subcopia", modificas el original.
Solución: `.copy()` explícita.

**2. Broadcasting con shapes incompatibles.**
`(3, 4) + (4, 3)` lanza error aunque tengan el mismo número de elementos.
Solución: revisar shape antes de operar; usar `.reshape()` si es necesario.

**3. Usar `*` cuando quieres multiplicación matricial.**
`A * B` es elemento a elemento. `A @ B` es multiplicación de matrices.
Solución: recordar que `@` = matmul.

**4. Comparar arrays con `==` en una condición de Python.**
`if arr == 0` lanza una advertencia/error. Usar `if (arr == 0).all()` o
`if (arr == 0).any()`.

**5. Olvidar `keepdims=True` en reducciones para broadcasting posterior.**
Si reduces y luego quieres operar contra el original, `keepdims` mantiene la
dimensión colapsada como 1 para que el broadcasting funcione.
"""),

code(r"""
import numpy as np

# --- Error 1: mutar vista ---
original = np.array([1, 2, 3, 4, 5])
vista = original[2:4]      # vista, NO copia
vista[0] = 99
print("Error 1 - original contaminado:", original)

# Forma correcta:
original2 = np.array([1, 2, 3, 4, 5])
copia = original2[2:4].copy()
copia[0] = 99
print("Forma correcta - original intacto:", original2)
"""),

code(r"""
import numpy as np

# --- Error 2: shapes incompatibles ---
a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])   # (3, 4)
b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]) # (4, 3)

# a + b → ERROR (shapes distintos)
try:
    c = a + b
except ValueError as e:
    print("Error 2 - shapes incompatibles:", e)

# Si quieres sumar, primero transpón o reshapea según tu intención:
c_ok = a + b.T   # b.T tiene shape (3, 4), igual que a
print("a + b.T (correcto):\n", c_ok)
"""),

code(r"""
import numpy as np

# --- Error 3: * vs @ ---
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print("A * B (elemento a elemento):\n", A * B)
print("\nA @ B (multiplicacion matricial):\n", A @ B)
# [1*5+2*7, 1*6+2*8]   = [19, 22]
# [3*5+4*7, 3*6+4*8]   = [43, 50]
"""),
]


# ===================================================================== #
# 13. RESUMEN Y QUIZ
# ===================================================================== #
C += [
md(r"""
## 13. Resumen de la clase

| Concepto | En una frase |
|---|---|
| **ndarray** | bloque contiguo de datos homogéneos; describe por shape/dtype/ndim |
| **Crear arrays** | `zeros`, `ones`, `arange`, `linspace`, `random.default_rng` |
| **Indexing** | `[i, j]`, `[a:b, c:d]`; slicing devuelve vista, usar `.copy()` |
| **Vectorización** | operaciones elemento a elemento sin bucles; 10-100x más rápido |
| **Broadcasting** | operar arrays de shapes distintos según reglas de extensión |
| **ufuncs** | `abs`, `sqrt`, `exp`, `log`, `clip`, `round` sobre todo el array |
| **Reducciones** | `sum`, `mean`, `std`, `min`, `max` con `axis=` para elegir dimensión |
| **Indexing booleano** | filtrar con mask de True/False; devuelve copia |
| **Reshaping** | `reshape`, `flatten`, `T`; producto de dims debe conservarse |
| **Álgebra lineal** | `dot`/`@` para matmul, `linalg.norm` para distancias |
| **Aleatorios** | `default_rng(seed)` para reproducibilidad |
| **Errores comunes** | vista vs copia, `*` vs `@`, shapes incompatibles |

### Lo más importante que te llevas
> **Piensa en arrays, no en bucles.** Cada vez que sientas el impulso de
> escribir `for i in range(len(arr))`, pregúntate si NumPy tiene una
> operación vectorizada. Casi siempre la tiene, y es más rápida y más legible.
"""),

md(r"""
## Quiz de autoevaluación

Responde mentalmente antes de ejecutar.

1. `a = np.array([[1,2],[3,4]]); b = a[0]`. Si hago `b[0] = 99`, ¿cambia `a`?
2. ¿Cuál es el shape del resultado de `np.ones((3,1)) + np.zeros((1,4))`?
3. `np.sum(m, axis=0)` sobre una matriz (3,4): ¿cuál es el shape del resultado?
4. ¿Qué diferencia hay entre `a * b` y `a @ b`?
5. ¿Cómo generarías 1000 números normales con media 0 y desviación 1,
   de forma reproducible?
"""),

code(r"""
# Respuestas:
respuestas = {
    1: "SÍ cambia a. b = a[0] es una VISTA (alias) de la primera fila.",
    2: "(3, 4): broadcasting de (3,1) y (1,4) expande ambas dimensiones.",
    3: "(4,): axis=0 colapsa las 3 filas, queda 1 valor por columna.",
    4: ("a * b = elemento a elemento (broadcasting); "
        "a @ b = multiplicacion matricial (producto de matrices)."),
    5: "rng = np.random.default_rng(42); rng.standard_normal(1000)",
}
for k, v in respuestas.items():
    print("{}.  {}\n".format(k, v))
"""),

md(r"""
## Retos para practicar

1. **Normalización:** dado un array de precios, aplica la fórmula
   `(x - x.min()) / (x.max() - x.min())` de forma vectorizada.
2. **Filtro doble:** en una matriz de transacciones, selecciona las filas
   donde el monto es mayor que el promedio Y la ciudad es Bogotá (dos máscaras
   combinadas con `&`).
3. **Moving average:** implementa la media móvil de ventana 3 sobre un array
   de precios usando solo operaciones NumPy (sin `convolve`, sin bucle).
4. **Simulación:** simula 10.000 lanzamientos de dos dados y calcula la
   probabilidad de obtener 7 como suma.

---

### Siguiente paso

- **practice01.ipynb** — 10 ejercicios graduales con solución oculta.
- **practice02.ipynb** — análisis numérico de transacciones con NumPy.
- **homework01.ipynb** y **homework02.ipynb** — tareas autocalificables.
"""),
]


# ===================================================================== #
# CELDAS ADICIONALES (insertar_despues)
# ===================================================================== #

def insertar_despues(celdas, marcador_texto, nuevas):
    """Inserta 'nuevas' justo después de la primera celda cuyo source contiene 'marcador_texto'."""
    for i, c in enumerate(celdas):
        if marcador_texto in c.source:
            return celdas[: i + 1] + nuevas + celdas[i + 1 :]
    return celdas + nuevas


# --- Ampliación MOTIVACIÓN: anatomía de un array en memoria ----------------
EXTRA_MEMORIA = [
md(r"""
### Anatomía de un array NumPy en memoria

Todo ndarray tiene tres componentes:

```
┌──────────────────────────────────────────────────────────┐
│ METADATA (cabecera)                                      │
│   shape   = (3,)        ← cuántos elementos por eje     │
│   dtype   = float64     ← tipo de cada elemento          │
│   strides = (8,)        ← bytes a saltar para ir al      │
│                           siguiente elemento en cada eje │
│   data ptr → ────────────────────────────────────┐       │
└──────────────────────────────────────────────────│───────┘
                                                   ↓
┌──────────────────────────────────────────────────────────┐
│ DATOS (bloque contiguo)                                  │
│  [  45000.0  │  120000.0  │   88000.0  ]                 │
│   8 bytes       8 bytes      8 bytes                     │
└──────────────────────────────────────────────────────────┘
```

Los **strides** son la clave del reshaping y la transposición sin copiar datos:
cambiar la forma solo cambia los metadatos, el bloque de datos no se mueve.
"""),

code(r"""
import numpy as np

a = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0]])
print("shape:  ", a.shape)
print("dtype:  ", a.dtype)
print("strides:", a.strides,
      "← {} bytes por col, {} bytes por fila".format(a.strides[1], a.strides[0]))

# Al transponer, solo cambian los strides (sin copiar datos):
t = a.T
print("\nTranspuesta:")
print("shape:  ", t.shape)
print("strides:", t.strides, "<- se invierten los strides")
print("Mismos datos en memoria?", np.shares_memory(a, t))
"""),
]

# --- Ampliación INDEXING: fancy indexing con array de índices ---------------
EXTRA_FANCY = [
md(r"""
### Fancy indexing con arrays de índices

Además del indexing booleano, puedes pasar un **array de índices enteros**:

```python
arr[[2, 0, 1]]    # selecciona elementos en ese orden
```

Esto permite reordenar, duplicar o seleccionar elementos no contiguos.
Es útil para shuffling, muestreo y ordenamiento personalizado.
"""),

code(r"""
import numpy as np

ciudades = np.array(["Bogota", "Medellin", "Cali", "Barranquilla", "Cartagena"])
ventas   = np.array([250_000, 180_000, 310_000, 95_000, 140_000])

# Ordenar ciudades por ventas de mayor a menor
orden_desc = np.argsort(ventas)[::-1]   # argsort devuelve índices que ordenarían
print("Ciudades ordenadas por ventas (desc):")
for c, v in zip(ciudades[orden_desc], ventas[orden_desc]):
    print("  {}: ${:,.0f}".format(c, v))

# Selección por índices explícitos: las 3 más grandes
top3_idx = orden_desc[:3]
print("\nTop 3:", ciudades[top3_idx])
"""),
]

# --- Ampliación BROADCASTING: tabla de multiplicar --------------------------
EXTRA_TABLA_MULT = [
md(r"""
### Broadcasting en acción: tabla de multiplicar

El broadcasting 2D real es más fácil de entender con un ejemplo concreto.
La tabla de multiplicar del 1 al 5:

```
filas = [[1],[2],[3],[4],[5]]   shape (5, 1) — columna
cols  = [1, 2, 3, 4, 5]        shape (5,)   — fila

resultado = filas * cols        shape (5, 5) — tabla completa
```
"""),

code(r"""
import numpy as np

n = 5
filas = np.arange(1, n + 1).reshape(-1, 1)   # shape (5, 1)
cols  = np.arange(1, n + 1)                   # shape (5,)

tabla = filas * cols   # broadcasting: (5,1) * (5,) → (5,5)
print("Tabla de multiplicar del 1 al {}:".format(n))
print(tabla)

# Aplicación real: tabla de precios (base_ciudad * factor_categoria)
bases   = np.array([100, 120, 90]).reshape(-1, 1)  # 3 ciudades, shape (3,1)
factores = np.array([1.0, 1.2, 0.8, 1.5])           # 4 categorias, shape (4,)
tabla_precios = bases * factores                     # (3,1)*(4,) → (3,4)
print("\nTabla de precios (ciudad x categoria):\n", tabla_precios)
"""),
]

# --- Ampliación UFUNCS: aplicación financiera con np.where -----------------
EXTRA_UFUNCS2 = [
md(r"""
### Aplicación financiera: categorizar transacciones con ufuncs

Combinamos `np.where`, `np.abs` y `np.clip` para un preprocesamiento real:
"""),

code(r"""
import numpy as np

rng = np.random.default_rng(5)
montos = rng.normal(150_000, 80_000, size=20).astype(int)
montos[3] = -5_000     # error de datos: monto negativo
montos[7] = 2_500_000  # outlier extremo

print("Montos originales:", montos)

# 1. Corregir negativos: tomar valor absoluto
montos_limpios = np.abs(montos)

# 2. Recortar outliers extremos en percentil 95
p95 = np.percentile(montos_limpios, 95)
montos_clip = np.clip(montos_limpios, 0, p95)

# 3. Categorizar
cats = np.where(montos_clip < 50_000, "bajo",
       np.where(montos_clip < 200_000, "medio", "alto"))

print("\nMontos procesados (primeros 10):", montos_clip[:10])
print("Categorias (primeros 10):      ", cats[:10])
print("Distribucion:", {c: (cats == c).sum() for c in ["bajo", "medio", "alto"]})
"""),
]

# --- Ampliación ALGEBRA LINEAL: sistema de ecuaciones ----------------------
EXTRA_LINALG = [
md(r"""
### Caso real: resolver un sistema de ecuaciones con NumPy

Una empresa vende 3 productos. Sabe que en el mes vendió:
- 200 unidades en total de los 3 productos.
- Ingreso de $500.000 del producto A y B combinados.
- Doble de unidades del C que del A.

¿Cuántas unidades vendió de cada producto? Es un sistema lineal Ax = b.
"""),

code(r"""
import numpy as np

# A x = b
# x[0] + x[1] + x[2] = 200        (total unidades)
# x[0] + x[1]         = 100        (del A y B: 100 unidades)
# x[2] = 2 * x[0]   →  -2x[0] + x[2] = 0

A = np.array([
    [ 1,  1,  1],
    [ 1,  1,  0],
    [-2,  0,  1],
], dtype=float)

b = np.array([200, 100, 0], dtype=float)

x = np.linalg.solve(A, b)
print("Unidades vendidas:")
print("  Producto A: {:.0f}".format(x[0]))
print("  Producto B: {:.0f}".format(x[1]))
print("  Producto C: {:.0f}".format(x[2]))

# Verificar: A @ x debería ser b
print("\nVerificacion A @ x:", np.allclose(A @ x, b))
"""),
]

# --- Ampliación RANDOM: simulación de Monte Carlo simple -------------------
EXTRA_MONTECARLO = [
md(r"""
### Números aleatorios en acción: estimando π con Monte Carlo

Un ejemplo clásico de simulación: estima π lanzando puntos aleatorios en
un cuadrado de lado 2 y contando cuántos caen dentro del círculo inscrito.

```
        r=1
    ┌────◠────┐
    │  ·  ·  │
    │ ·π·ₒ   │
    │  ·  ·  │
    └────◡────┘
    2×2 = 4 área
    π×1² = π área círculo

    π ≈ 4 × (puntos_en_circulo / total_puntos)
```
"""),

code(r"""
import numpy as np

rng = np.random.default_rng(123)
n = 1_000_000   # un millón de puntos

x = rng.uniform(-1, 1, n)
y = rng.uniform(-1, 1, n)

# Puntos dentro del círculo unitario: x² + y² <= 1
dentro = (x**2 + y**2) <= 1.0
pi_estimado = 4 * dentro.mean()

print("Pi estimado con {:,} puntos: {:.6f}".format(n, pi_estimado))
print("Pi real:                    3.141593")
print("Error: {:.4f}%".format(abs(pi_estimado - 3.141593) / 3.141593 * 100))
"""),
]

# --- Ampliación GLOSARIO + errores adicionales -----------------------------
EXTRA_GLOSARIO = [
md(r"""
## Glosario de la Clase 5

| Término | Definición breve |
|---|---|
| **ndarray** | array n-dimensional de NumPy, bloque contiguo de tipo homogéneo |
| **shape** | tupla que describe el tamaño de cada dimensión |
| **dtype** | tipo de dato de cada elemento (`float64`, `int32`, `bool`...) |
| **stride** | bytes a saltar para pasar al siguiente elemento en cada eje |
| **vista (view)** | alias al mismo bloque de memoria; modificarla modifica el original |
| **copia (copy)** | nuevo bloque de memoria independiente; `.copy()` la garantiza |
| **vectorización** | operación aplicada a todo el array sin bucle Python explícito |
| **broadcasting** | operar arrays de shapes distintos expandiendo las dims de tamaño 1 |
| **ufunc** | función universal que opera elemento a elemento sobre arrays |
| **reducción** | colapsar una dimensión aplicando una función (sum, mean...) |
| **axis** | eje sobre el que opera una reducción; `axis=0` colapsa filas |
| **indexing booleano** | filtrar con una máscara de True/False; devuelve copia |
| **fancy indexing** | seleccionar elementos con un array de índices enteros |
| **norm** | longitud/magnitud de un vector (norma euclidiana L2) |
| **seed** | valor inicial del generador pseudoaleatorio; fija la reproducibilidad |
"""),
]

# Insertar bloques en posiciones estratégicas
C = insertar_despues(C, "NumPy es más seguro", EXTRA_MEMORIA)
C = insertar_despues(C, "Mutar una vista creyendo", EXTRA_FANCY)
C = insertar_despues(C, "tabla_precios shape:", EXTRA_TABLA_MULT)
C = insertar_despues(C, "Reducciones (colapsan el array)", EXTRA_UFUNCS2)
C = insertar_despues(C, "np.linalg.solve(A, b)", EXTRA_LINALG)
C = insertar_despues(C, "la misma secuencia.", EXTRA_MONTECARLO)
C = insertar_despues(C, "Eso es justo lo que vas a arreglar", EXTRA_GLOSARIO)


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase05", "lecture.ipynb")
build(os.path.abspath(ruta), C)
