"""Construye curso/clase04/homework01.ipynb — 8 ejercicios autocalificables.

Temas: operaciones con listas, dicts y sets, comprensiones, patrones
algorítmicos eficientes con estructuras de datos.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    {
        "n": 1,
        "titulo": "Contador de palabras ignorando puntuación",
        "enunciado": (
            "Implementa `contar_palabras(texto)` que reciba un string con puntuación "
            "y devuelva un dict `{palabra: frecuencia}`. Debe ignorar la puntuación "
            "y convertir todo a minúsculas antes de contar.\n\n"
            "Puntuación a eliminar: `.,;:!?\"'()`\n\n"
            "**Ejemplo:** `contar_palabras(\"Hola, mundo. Hola!\")` "
            "→ `{\"hola\": 2, \"mundo\": 1}`\n\n"
            "Pista: itera sobre el texto y reemplaza cada carácter de puntuación por espacio,\n"
            "luego divide por espacios y filtra strings vacíos."
        ),
        "plantilla": "def contar_palabras(texto):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def contar_palabras(texto):\n"
            "    puntuacion = '.,;:!?\"\\''()\n"
            "    limpio = ''\n"
            "    for c in texto.lower():\n"
            "        if c in puntuacion:\n"
            "            limpio += ' '\n"
            "        else:\n"
            "            limpio += c\n"
            "    conteo = {}\n"
            "    for p in limpio.split():\n"
            "        if p:\n"
            "            conteo[p] = conteo.get(p, 0) + 1\n"
            "    return conteo"
        ),
        "visibles": [
            "assert contar_palabras('Hola, mundo. Hola!') == {'hola': 2, 'mundo': 1}",
            "assert contar_palabras('python') == {'python': 1}",
        ],
        "ocultos": [
            "assert contar_palabras('') == {}",
            "assert contar_palabras('a, a, a!') == {'a': 3}",
            "assert contar_palabras('El sol sale.') == {'el': 1, 'sol': 1, 'sale': 1}",
        ],
    },
    {
        "n": 2,
        "titulo": "Índice invertido de posiciones",
        "enunciado": (
            "Implementa `indice_invertido(texto)` que reciba un string y devuelva un dict "
            "`{palabra: [lista_de_posiciones]}` donde cada posición es el índice (comenzando "
            "en 0) de la palabra en el texto.\n\n"
            "**Ejemplo:**\n"
            "`indice_invertido(\"el sol sale el sol\")`\n"
            "→ `{\"el\": [0, 3], \"sol\": [1, 4], \"sale\": [2]}`\n\n"
            "El texto ya llega en minúsculas y sin puntuación."
        ),
        "plantilla": "def indice_invertido(texto):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def indice_invertido(texto):\n"
            "    indice = {}\n"
            "    for pos, palabra in enumerate(texto.split()):\n"
            "        if palabra not in indice:\n"
            "            indice[palabra] = []\n"
            "        indice[palabra].append(pos)\n"
            "    return indice"
        ),
        "visibles": [
            "assert indice_invertido('el sol sale el sol') == {'el': [0, 3], 'sol': [1, 4], 'sale': [2]}",
        ],
        "ocultos": [
            "assert indice_invertido('') == {}",
            "assert indice_invertido('a') == {'a': [0]}",
            "assert indice_invertido('x y x y x') == {'x': [0, 2, 4], 'y': [1, 3]}",
        ],
    },
    {
        "n": 3,
        "titulo": "Primer carácter no repetido",
        "enunciado": (
            "Implementa `primer_no_repetido(cadena)` que devuelva el **primer carácter** "
            "de la cadena que aparece exactamente una vez. Si no existe, devuelve `None`.\n\n"
            "**Ejemplo:** `primer_no_repetido(\"aabbcde\")` → `'c'`\n\n"
            "**Ejemplo:** `primer_no_repetido(\"aabb\")` → `None`\n\n"
            "Pista: construye primero un dict de frecuencias, luego recorre la cadena\n"
            "buscando el primer carácter con frecuencia 1."
        ),
        "plantilla": "def primer_no_repetido(cadena):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def primer_no_repetido(cadena):\n"
            "    freq = {}\n"
            "    for c in cadena:\n"
            "        freq[c] = freq.get(c, 0) + 1\n"
            "    for c in cadena:\n"
            "        if freq[c] == 1:\n"
            "            return c\n"
            "    return None"
        ),
        "visibles": [
            "assert primer_no_repetido('aabbcde') == 'c'",
            "assert primer_no_repetido('aabb') is None",
        ],
        "ocultos": [
            "assert primer_no_repetido('a') == 'a'",
            "assert primer_no_repetido('') is None",
            "assert primer_no_repetido('abacabad') == 'c'",
            "assert primer_no_repetido('aabbcc') is None",
        ],
    },
    {
        "n": 4,
        "titulo": "Histograma de valores",
        "enunciado": (
            "Implementa `histograma(valores)` que reciba una lista de números enteros "
            "y devuelva un dict `{valor: frecuencia}` (igual a un contador de frecuencias).\n\n"
            "Luego imprime el histograma con barras de asteriscos, ordenado por valor.\n\n"
            "La función solo devuelve el dict; la impresión es parte del análisis.\n\n"
            "**Ejemplo:** `histograma([1, 2, 1, 3, 2, 1])` → `{1: 3, 2: 2, 3: 1}`"
        ),
        "plantilla": "def histograma(valores):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def histograma(valores):\n"
            "    h = {}\n"
            "    for v in valores:\n"
            "        h[v] = h.get(v, 0) + 1\n"
            "    return h"
        ),
        "visibles": [
            "assert histograma([1, 2, 1, 3, 2, 1]) == {1: 3, 2: 2, 3: 1}",
            "assert histograma([]) == {}",
        ],
        "ocultos": [
            "assert histograma([5]) == {5: 1}",
            "assert histograma([1, 1, 1]) == {1: 3}",
            "assert histograma([3, 1, 2, 1, 3, 3]) == {3: 3, 1: 2, 2: 1}",
        ],
    },
    {
        "n": 5,
        "titulo": "Total de compras con manejo de clave inexistente",
        "enunciado": (
            "Implementa `total_compras(precios, lista_compras)` que reciba:\n"
            "- `precios`: dict `{producto: precio}`\n"
            "- `lista_compras`: lista de nombres de producto\n\n"
            "Devuelve la suma de los precios de los productos en `lista_compras`.\n"
            "Si un producto **no está en el catálogo**, su precio se trata como 0\n"
            "(no lanza error).\n\n"
            "**Ejemplo:**\n"
            "`total_compras({'laptop': 2500, 'teclado': 120}, ['laptop', 'mouse'])`\n"
            "→ `2500`  (mouse no está, su precio es 0)"
        ),
        "plantilla": "def total_compras(precios, lista_compras):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def total_compras(precios, lista_compras):\n"
            "    total = 0\n"
            "    for producto in lista_compras:\n"
            "        total += precios.get(producto, 0)\n"
            "    return total"
        ),
        "visibles": [
            "assert total_compras({'laptop': 2500, 'teclado': 120}, ['laptop', 'mouse']) == 2500",
            "assert total_compras({'a': 10, 'b': 20}, ['a', 'b']) == 30",
        ],
        "ocultos": [
            "assert total_compras({}, ['x', 'y']) == 0",
            "assert total_compras({'x': 5}, []) == 0",
            "assert total_compras({'a': 100}, ['a', 'a', 'a']) == 300",
        ],
    },
    {
        "n": 6,
        "titulo": "Comparar dos conjuntos",
        "enunciado": (
            "Implementa `comparar_conjuntos(a, b)` que reciba dos listas (o sets) y "
            "devuelva una **tupla** `(solo_en_a, solo_en_b, en_ambos)` donde cada "
            "componente es un **set** ordenado.\n\n"
            "**Ejemplo:**\n"
            "`comparar_conjuntos([1, 2, 3, 4], [3, 4, 5, 6])`\n"
            "→ `({1, 2}, {5, 6}, {3, 4})`"
        ),
        "plantilla": "def comparar_conjuntos(a, b):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def comparar_conjuntos(a, b):\n"
            "    sa = set(a)\n"
            "    sb = set(b)\n"
            "    return (sa - sb, sb - sa, sa & sb)"
        ),
        "visibles": [
            "assert comparar_conjuntos([1, 2, 3, 4], [3, 4, 5, 6]) == ({1, 2}, {5, 6}, {3, 4})",
        ],
        "ocultos": [
            "assert comparar_conjuntos([], []) == (set(), set(), set())",
            "assert comparar_conjuntos([1, 2], []) == ({1, 2}, set(), set())",
            "assert comparar_conjuntos([1], [1]) == (set(), set(), {1})",
            "assert comparar_conjuntos([1, 1, 2], [2, 3]) == ({1}, {3}, {2})",
        ],
    },
    {
        "n": 7,
        "titulo": "Aplanar un dict anidado",
        "enunciado": (
            "Implementa `aplanar_dict(d)` que reciba un dict donde los valores son "
            "también dicts, y devuelva un dict plano con **tuplas** como claves.\n\n"
            "**Ejemplo:**\n"
            "`aplanar_dict({'a': {'x': 1, 'y': 2}, 'b': {'x': 3}})`\n"
            "→ `{('a', 'x'): 1, ('a', 'y'): 2, ('b', 'x'): 3}`\n\n"
            "Solo se aplana un nivel (el valor interno puede ser cualquier tipo)."
        ),
        "plantilla": "def aplanar_dict(d):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def aplanar_dict(d):\n"
            "    resultado = {}\n"
            "    for clave_ext, sub_dict in d.items():\n"
            "        for clave_int, valor in sub_dict.items():\n"
            "            resultado[(clave_ext, clave_int)] = valor\n"
            "    return resultado"
        ),
        "visibles": [
            "assert aplanar_dict({'a': {'x': 1, 'y': 2}, 'b': {'x': 3}}) == {('a', 'x'): 1, ('a', 'y'): 2, ('b', 'x'): 3}",
        ],
        "ocultos": [
            "assert aplanar_dict({}) == {}",
            "assert aplanar_dict({'k': {'v': 99}}) == {('k', 'v'): 99}",
            "assert aplanar_dict({'x': {'a': 1}, 'y': {'b': 2}}) == {('x', 'a'): 1, ('y', 'b'): 2}",
        ],
    },
    {
        "n": 8,
        "titulo": "Moda con dict (O(n) vs O(n²) de la Clase 1)",
        "enunciado": (
            "Implementa `moda(lista)` que devuelva el elemento que **más veces** aparece "
            "en la lista. En caso de empate, devuelve el que aparece **primero** al "
            "recorrer la lista (no necesariamente el de menor valor).\n\n"
            "**Esta vez usa un dict** para hacerlo en O(n), no en O(n²).\n\n"
            "**Ejemplo:** `moda([1, 2, 2, 3, 3, 3])` → `3`\n\n"
            "**Ejemplo:** `moda([4, 4, 5, 5])` → `4` (empate: gana el primero)"
        ),
        "plantilla": "def moda(lista):\n    # ✏️ TU CÓDIGO AQUÍ (usa dict, no dos bucles)\n    " + NI,
        "solucion": (
            "def moda(lista):\n"
            "    freq = {}\n"
            "    orden = []\n"
            "    for x in lista:\n"
            "        if x not in freq:\n"
            "            orden.append(x)\n"
            "        freq[x] = freq.get(x, 0) + 1\n"
            "    mejor = orden[0]\n"
            "    for x in orden:\n"
            "        if freq[x] > freq[mejor]:\n"
            "            mejor = x\n"
            "    return mejor"
        ),
        "visibles": [
            "assert moda([1, 2, 2, 3, 3, 3]) == 3",
            "assert moda([4, 4, 5, 5]) == 4",
        ],
        "ocultos": [
            "assert moda([7]) == 7",
            "assert moda(['a', 'b', 'a']) == 'a'",
            "assert moda([1, 2, 3, 2, 1, 2]) == 2",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 4 · Tarea 01 — 8 ejercicios autocalificables

### Estructuras de datos Python

**Instrucciones**

1. Implementa cada función reemplazando la línea `raise NotImplementedError`.
2. **No cambies el nombre ni los parámetros** de las funciones.
3. Ejecuta las celdas de tests visibles y adicionales; si todo está bien,
   verás ✅. Si no, el `AssertionError` indica qué caso falla.
4. Objetivo: que **todas** las celdas de tests pasen sin error.

> 🧠 Antes de programar cada función, decide qué estructura de datos
> usarás y por qué. Esa decisión es parte de la solución.

> ⚠️ Al abrir la tarea, las celdas de tests fallarán hasta que implementes
> cada función. ¡Eso es exactamente lo que vas a arreglar!
""",
    "cierre_md": r"""
---
## Entrega

Cuando **todas** las celdas de tests muestren ✅, has completado la tarea.

| Ejercicio | Estructura clave | Patrón |
|---|---|---|
| 1 Contador de palabras | `dict` | contador con `.get(k, 0) + 1` |
| 2 Índice invertido | `dict` de listas | mapeo valor → posiciones |
| 3 Primer no repetido | `dict` | dos pasadas: frecuencias → búsqueda |
| 4 Histograma | `dict` | contador genérico |
| 5 Total compras | `dict` | `.get(k, 0)` para clave inexistente |
| 6 Comparar conjuntos | `set` | operaciones `&`, `-` |
| 7 Aplanar dict | `dict` de dicts | tupla como clave compuesta |
| 8 Moda con dict | `dict` | O(n) vs O(n²) de la Clase 1 |

> 💡 **Reflexión:** el ejercicio 8 es el mismo problema que en la Clase 1
> (tarea 01, ejercicio 8), pero ahora lo resuelves en O(n) con un dict.
> Compara ambas implementaciones: ¿cuánto más corto y eficiente es?
""",
}

validar(ejercicios)
construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase04", "homework01.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "clase04_homework01_solved.ipynb"),
)
