"""Construye curso/clase05/homework01.ipynb — 8 ejercicios autocalificables de NumPy."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    {
        "n": 1,
        "titulo": "Producto punto sin np.dot",
        "enunciado": (
            "Implementa `producto_punto(u, v)` que calcule el producto punto\n"
            "de dos vectores NumPy **sin usar `np.dot` ni el operador `@`**.\n\n"
            "Usa: `np.sum` y la multiplicación elemento a elemento `*`.\n\n"
            "**Fórmula:** `u · v = sum(u[i] * v[i])` para todo i.\n\n"
            "**Ejemplo:** `producto_punto(np.array([1,2,3]), np.array([4,5,6]))` → `32`\n"
            "(1·4 + 2·5 + 3·6 = 4 + 10 + 18 = 32)."
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def producto_punto(u, v):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — usa np.sum y *, sin np.dot ni @\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def producto_punto(u, v):\n"
            "    return np.sum(u * v)"
        ),
        "visibles": [
            "import numpy as np",
            "assert producto_punto(np.array([1,2,3]), np.array([4,5,6])) == 32",
            "assert producto_punto(np.array([0,0,0]), np.array([1,2,3])) == 0",
        ],
        "ocultos": [
            "import numpy as np",
            "assert producto_punto(np.array([1.0, -1.0]), np.array([3.0, 3.0])) == 0.0",
            "assert abs(producto_punto(np.array([0.5, 0.5]), np.array([2.0, 2.0])) - 2.0) < 1e-9",
            "# Verificar que coincide con np.dot",
            "_u = np.array([7, 2, -3]); _v = np.array([1, 4, 5])",
            "assert producto_punto(_u, _v) == int(np.dot(_u, _v))",
        ],
    },
    {
        "n": 2,
        "titulo": "Distancia euclidiana entre dos vectores",
        "enunciado": (
            "Implementa `distancia_euclidiana(u, v)` que calcule la distancia\n"
            "euclidiana entre dos vectores NumPy:\n\n"
            "```\n"
            "d(u, v) = sqrt( sum( (u[i] - v[i])^2 ) )\n"
            "```\n\n"
            "Puedes usar `np.sqrt` y `np.sum`, o `np.linalg.norm`.\n\n"
            "**Ejemplo:** `distancia_euclidiana(np.array([0,0]), np.array([3,4]))` → `5.0`"
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def distancia_euclidiana(u, v):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def distancia_euclidiana(u, v):\n"
            "    return float(np.linalg.norm(u - v))"
        ),
        "visibles": [
            "import numpy as np",
            "assert abs(distancia_euclidiana(np.array([0,0]), np.array([3,4])) - 5.0) < 1e-9",
            "assert distancia_euclidiana(np.array([1,1]), np.array([1,1])) == 0.0",
        ],
        "ocultos": [
            "import numpy as np",
            "assert abs(distancia_euclidiana(np.array([1.0,0,0]), np.array([0.0,0,0])) - 1.0) < 1e-9",
            "_a = np.array([1,2,3]); _b = np.array([4,6,3])",
            "assert abs(distancia_euclidiana(_a, _b) - 5.0) < 1e-9",
        ],
    },
    {
        "n": 3,
        "titulo": "Centrar y escalar una matriz (estandarización por columna)",
        "enunciado": (
            "Implementa `estandarizar(M)` que reciba una matriz 2-D y devuelva\n"
            "una copia donde cada **columna** tiene media 0 y desviación estándar 1.\n\n"
            "Fórmula por columna j: `(M[:,j] - mean(M[:,j])) / std(M[:,j])`.\n\n"
            "Usa `axis=0` en `mean` y `std`, y broadcasting para la resta y división.\n"
            "Si una columna tiene std=0, deja esa columna en ceros.\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "M = np.array([[1.0,10.0],[2.0,20.0],[3.0,30.0]])\n"
            "estandarizar(M)  # columnas: media 0, std 1\n"
            "```"
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def estandarizar(M):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — usa axis=0 y broadcasting\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def estandarizar(M):\n"
            "    M = M.astype(float)\n"
            "    media = M.mean(axis=0)\n"
            "    std   = M.std(axis=0)\n"
            "    std_safe = np.where(std == 0, 1.0, std)  # evita division por cero\n"
            "    resultado = (M - media) / std_safe\n"
            "    resultado[:, std == 0] = 0.0\n"
            "    return resultado"
        ),
        "visibles": [
            "import numpy as np",
            "M = np.array([[1.0,10.0],[2.0,20.0],[3.0,30.0]])",
            "E = estandarizar(M)",
            "assert abs(E[:,0].mean()) < 1e-9",
            "assert abs(E[:,0].std() - 1.0) < 1e-9",
            "assert abs(E[:,1].mean()) < 1e-9",
        ],
        "ocultos": [
            "import numpy as np",
            "# Columna constante: debe quedar en ceros",
            "M2 = np.array([[5.0, 1.0],[5.0, 3.0],[5.0, 5.0]])",
            "E2 = estandarizar(M2)",
            "assert np.all(E2[:, 0] == 0.0)",
            "assert abs(E2[:,1].mean()) < 1e-9",
        ],
    },
    {
        "n": 4,
        "titulo": "Simulación Monte Carlo: lanzamientos de dado",
        "enunciado": (
            "Implementa `simular_dado(n, seed)` que:\n"
            "1. Genere `n` lanzamientos de un dado de 6 caras (enteros 1-6 uniformes)\n"
            "   usando `np.random.default_rng(seed)`.\n"
            "2. Devuelva un diccionario `{cara: frecuencia_relativa}` con la\n"
            "   frecuencia relativa (proporción) de cada cara.\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "res = simular_dado(600_000, seed=0)\n"
            "# cada valor cercano a 1/6 ≈ 0.1667\n"
            "```\n\n"
            "Pista: usa `np.unique` con `return_counts=True`."
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def simular_dado(n, seed=42):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def simular_dado(n, seed=42):\n"
            "    rng = np.random.default_rng(seed)\n"
            "    lanzamientos = rng.integers(1, 7, size=n)\n"
            "    caras, conteos = np.unique(lanzamientos, return_counts=True)\n"
            "    return {int(c): float(cnt / n) for c, cnt in zip(caras, conteos)}"
        ),
        "visibles": [
            "import numpy as np",
            "res = simular_dado(600_000, seed=0)",
            "assert set(res.keys()) == {1,2,3,4,5,6}",
            "assert abs(sum(res.values()) - 1.0) < 1e-9",
        ],
        "ocultos": [
            "import numpy as np",
            "# Con muchos lanzamientos, cada cara debe estar cerca de 1/6",
            "res2 = simular_dado(1_000_000, seed=99)",
            "for cara in range(1, 7):\n    assert abs(res2[cara] - 1/6) < 0.01",
        ],
    },
    {
        "n": 5,
        "titulo": "Media móvil de ventana k",
        "enunciado": (
            "Implementa `moving_average(arr, k)` que calcule la **media móvil**\n"
            "de ventana `k` sobre el array `arr`.\n\n"
            "El resultado tiene longitud `len(arr) - k + 1`: el i-ésimo valor es\n"
            "el promedio de `arr[i:i+k]`.\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "moving_average(np.array([1,2,3,4,5]), 3)\n"
            "# → array([2.0, 3.0, 4.0])  (media de [1,2,3], [2,3,4], [3,4,5])\n"
            "```\n\n"
            "Pista: `np.cumsum` con manipulación de índices es una forma eficiente."
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def moving_average(arr, k):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def moving_average(arr, k):\n"
            "    arr = arr.astype(float)\n"
            "    cum = np.cumsum(arr)\n"
            "    cum = np.concatenate([[0.0], cum])\n"
            "    return (cum[k:] - cum[:-k]) / k"
        ),
        "visibles": [
            "import numpy as np",
            "res = moving_average(np.array([1.0,2,3,4,5]), 3)",
            "assert len(res) == 3",
            "assert abs(res[0] - 2.0) < 1e-9",
            "assert abs(res[-1] - 4.0) < 1e-9",
        ],
        "ocultos": [
            "import numpy as np",
            "res2 = moving_average(np.array([10.0,20,30,40,50,60]), 2)",
            "assert len(res2) == 5",
            "assert abs(res2[0] - 15.0) < 1e-9",
            "assert abs(res2[-1] - 55.0) < 1e-9",
            "# Ventana de tamaño 1: igual al array original",
            "arr3 = np.array([5.0, 7.0, 3.0])",
            "assert np.allclose(moving_average(arr3, 1), arr3)",
        ],
    },
    {
        "n": 6,
        "titulo": "Correlación de Pearson sin np.corrcoef",
        "enunciado": (
            "Implementa `correlacion(x, y)` que calcule el coeficiente de\n"
            "correlación de Pearson entre dos arrays usando la fórmula:\n\n"
            "```\n"
            "r = cov(x, y) / (std(x) * std(y))\n"
            "```\n\n"
            "donde `cov(x, y) = mean((x - mean(x)) * (y - mean(y)))`.\n\n"
            "**Sin usar** `np.corrcoef` ni `np.cov`.\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "x = np.array([1.0, 2, 3, 4, 5])\n"
            "y = np.array([2.0, 4, 6, 8, 10])  # y = 2x → correlación perfecta\n"
            "correlacion(x, y)  # → 1.0\n"
            "```"
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def correlacion(x, y):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — sin np.corrcoef ni np.cov\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def correlacion(x, y):\n"
            "    x = x.astype(float)\n"
            "    y = y.astype(float)\n"
            "    cov = np.mean((x - x.mean()) * (y - y.mean()))\n"
            "    return float(cov / (x.std() * y.std()))"
        ),
        "visibles": [
            "import numpy as np",
            "x = np.array([1.0, 2, 3, 4, 5])",
            "y = np.array([2.0, 4, 6, 8, 10])",
            "assert abs(correlacion(x, y) - 1.0) < 1e-9",
            "# correlacion perfecta negativa",
            "assert abs(correlacion(x, -y) - (-1.0)) < 1e-9",
        ],
        "ocultos": [
            "import numpy as np",
            "# Verificar contra np.corrcoef",
            "_x = np.array([1.0, 3, 2, 5, 4])",
            "_y = np.array([2.0, 6, 4, 8, 7])",
            "assert abs(correlacion(_x, _y) - float(np.corrcoef(_x, _y)[0,1])) < 1e-9",
            "# Arrays sin correlacion (ortogonales)",
            "_a = np.array([1.0, 0, -1.0, 0])",
            "_b = np.array([0.0, 1,  0.0,-1])",
            "assert abs(correlacion(_a, _b)) < 1e-9",
        ],
    },
    {
        "n": 7,
        "titulo": "Índice del mínimo de cada columna",
        "enunciado": (
            "Implementa `indice_minimo_columnas(M)` que reciba una matriz 2-D\n"
            "y devuelva un array con el **índice de la fila** que contiene el\n"
            "valor mínimo de cada columna.\n\n"
            "Usa `np.argmin` con `axis=0`.\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "M = np.array([[3, 1, 4], [1, 5, 9], [2, 6, 5]])\n"
            "indice_minimo_columnas(M)  # → array([1, 0, 0])\n"
            "# col 0: min es 1 en fila 1\n"
            "# col 1: min es 1 en fila 0\n"
            "# col 2: min es 4 en fila 0\n"
            "```"
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def indice_minimo_columnas(M):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — una línea con np.argmin\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def indice_minimo_columnas(M):\n"
            "    return np.argmin(M, axis=0)"
        ),
        "visibles": [
            "import numpy as np",
            "M = np.array([[3,1,4],[1,5,9],[2,6,5]])",
            "res = indice_minimo_columnas(M)",
            "assert np.array_equal(res, np.array([1,0,0]))",
        ],
        "ocultos": [
            "import numpy as np",
            "M2 = np.array([[10,1],[2,8],[5,3]])",
            "res2 = indice_minimo_columnas(M2)",
            "assert np.array_equal(res2, np.array([1,0]))",
            "# Verificar que el mínimo de cada columna está en el índice indicado",
            "M3 = np.array([[9,7,2],[1,5,8],[3,4,6]])",
            "idx = indice_minimo_columnas(M3)",
            "for j in range(3):\n    assert M3[idx[j], j] == M3[:, j].min()",
        ],
    },
    {
        "n": 8,
        "titulo": "Tabla de multiplicar como matriz (np.outer o broadcasting)",
        "enunciado": (
            "Implementa `tabla_multiplicar(n)` que genere la tabla de multiplicar\n"
            "del 1 al `n` como una matriz NumPy de shape `(n, n)`, donde el elemento\n"
            "`[i, j]` es `(i+1) * (j+1)`.\n\n"
            "Usa `np.outer` **o** broadcasting (sin bucles).\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "tabla_multiplicar(3)\n"
            "# → array([[1, 2, 3],\n"
            "#           [2, 4, 6],\n"
            "#           [3, 6, 9]])\n"
            "```"
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def tabla_multiplicar(n):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — usa np.outer o broadcasting, sin bucles\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def tabla_multiplicar(n):\n"
            "    v = np.arange(1, n + 1)\n"
            "    return np.outer(v, v)"
        ),
        "visibles": [
            "import numpy as np",
            "T = tabla_multiplicar(3)",
            "assert T.shape == (3, 3)",
            "assert T[0, 0] == 1",
            "assert T[1, 1] == 4",
            "assert T[2, 2] == 9",
        ],
        "ocultos": [
            "import numpy as np",
            "T5 = tabla_multiplicar(5)",
            "assert T5.shape == (5, 5)",
            "assert T5[4, 4] == 25",
            "assert T5[3, 2] == 12",
            "# La tabla debe ser simétrica",
            "assert np.array_equal(T5, T5.T)",
            "# Verificar la diagonal",
            "v = np.arange(1, 6)",
            "assert np.array_equal(np.diag(T5), v**2)",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 5 · Tarea 01 — 8 ejercicios autocalificables de NumPy

### Arrays numéricos de alto rendimiento

**Instrucciones**

1. Implementa cada función en la celda que dice `# ✏️ TU CÓDIGO AQUÍ`
   (reemplaza la línea `raise NotImplementedError`).
2. **No cambies el nombre ni los parámetros** de las funciones.
3. Ejecuta las celdas de **tests visibles** y **tests adicionales**.
   Si una función está bien, verás ✅; si no, saltará un `AssertionError`.
4. Tu objetivo: que **todas** las celdas de tests pasen sin error.

> 🔎 Para cada función, antes de escribir código, dibuja el shape de entrada
> y de salida, y decide qué operación NumPy resuelve el problema.

> ⚠️ Recién abierta, esta tarea no corre de principio a fin: los tests
> fallarán hasta que implementes cada función.

| Ejercicio | Concepto clave |
|---|---|
| 1 Producto punto | `np.sum` + `*` |
| 2 Distancia euclidiana | `np.linalg.norm` |
| 3 Estandarizar | `axis=0`, broadcasting |
| 4 Simular dado | `default_rng`, `np.unique` |
| 5 Moving average | `np.cumsum` |
| 6 Correlación | operaciones vectorizadas |
| 7 Índice mínimo por columna | `np.argmin(axis=0)` |
| 8 Tabla multiplicar | `np.outer` o broadcasting |
""",
    "cierre_md": r"""
---
## Entrega

Cuando **todas** las celdas de tests muestren ✅, has completado la tarea.

### Reflexión final

Estos 8 ejercicios cubren los patrones NumPy más usados en ciencia de datos:
- **Producto punto** y **norma** → son la base de similitud coseno (recomendadores).
- **Estandarización** → preprocesamiento obligatorio en ML.
- **Simulación** → Monte Carlo, bootstrapping.
- **Moving average** → series temporales, suavizado de señales.
- **Correlación** → selección de features.
- **argmin por eje** → algoritmos de clustering (K-Means).
- **Tabla de multiplicar** → broadcasting avanzado.

> 💡 En la Clase 6 (pandas), muchas de estas operaciones tendrán
> equivalentes de una sola línea como `.rolling(k).mean()` o
> `.corr()`. Pero ahora sabes qué hay por debajo.
""",
}

validar(ejercicios)
construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase05", "homework01.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "clase05_homework01_solved.ipynb"),
)
