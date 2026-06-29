"""Construye curso/clase03/homework01.ipynb — 8 ejercicios autocalificables.

Tema: bucles, funciones y transformaciones funcionales.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    {
        "n": 1,
        "titulo": "Máximo Común Divisor (algoritmo de Euclides)",
        "enunciado": (
            "Implementa `mcd(a, b)` que devuelva el Máximo Común Divisor de dos "
            "enteros positivos usando el **algoritmo de Euclides**: mientras `b != 0`, "
            "reemplaza `(a, b)` por `(b, a % b)`; cuando `b == 0`, devuelve `a`.\n\n"
            "**Ejemplos:** `mcd(48, 18)` → `6`; `mcd(100, 75)` → `25`; `mcd(13, 7)` → `1`."
        ),
        "plantilla": "def mcd(a, b):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def mcd(a, b):\n"
            "    while b != 0:\n"
            "        a, b = b, a % b\n"
            "    return a"
        ),
        "visibles": [
            "assert mcd(48, 18) == 6",
            "assert mcd(100, 75) == 25",
            "assert mcd(13, 7) == 1",
        ],
        "ocultos": [
            "assert mcd(1, 1) == 1",
            "assert mcd(252, 105) == 21",
            "assert mcd(17, 17) == 17",
            "assert mcd(36, 24) == 12",
        ],
    },
    {
        "n": 2,
        "titulo": "Bubble sort (ordenamiento propio)",
        "enunciado": (
            "Implementa `bubble_sort(lista)` que ordene una lista de números de "
            "**menor a mayor** usando el algoritmo de burbuja: recorre la lista "
            "repetidamente e intercambia elementos adyacentes que estén en el orden "
            "incorrecto. Devuelve una **nueva lista** (no modifica la original).\n\n"
            "**Ejemplo:** `bubble_sort([5, 2, 4, 1, 3])` → `[1, 2, 3, 4, 5]`.\n\n"
            "Pista: una pasada completa 'burbujea' el mayor al final. Repite `n-1` pasadas."
        ),
        "plantilla": "def bubble_sort(lista):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def bubble_sort(lista):\n"
            "    arr = list(lista)   # copia para no mutar la original\n"
            "    n = len(arr)\n"
            "    for i in range(n - 1):\n"
            "        for j in range(n - 1 - i):\n"
            "            if arr[j] > arr[j + 1]:\n"
            "                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n"
            "    return arr"
        ),
        "visibles": [
            "assert bubble_sort([5, 2, 4, 1, 3]) == [1, 2, 3, 4, 5]",
            "assert bubble_sort([1]) == [1]",
            "assert bubble_sort([]) == []",
        ],
        "ocultos": [
            "assert bubble_sort([3, 3, 1]) == [1, 3, 3]",
            "assert bubble_sort([-2, 0, -5, 3]) == [-5, -2, 0, 3]",
            "_orig = [4, 2, 1]; bubble_sort(_orig); assert _orig == [4, 2, 1]",
        ],
    },
    {
        "n": 3,
        "titulo": "Contar ocurrencias de cada letra",
        "enunciado": (
            "Implementa `contar_letras(texto)` que reciba una cadena (solo letras "
            "minúsculas y espacios) y devuelva una **lista de tuplas** `(letra, conteo)` "
            "ordenada **alfabéticamente** por letra. Ignora los espacios.\n\n"
            "**Ejemplo:** `contar_letras(\"abba\")` → `[('a', 2), ('b', 2)]`.\n\n"
            "Pista: construye dos listas paralelas (letras únicas + conteos), luego ordena."
        ),
        "plantilla": "def contar_letras(texto):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def contar_letras(texto):\n"
            "    letras = []\n"
            "    conteos = []\n"
            "    for c in texto:\n"
            "        if c == ' ':\n"
            "            continue\n"
            "        if c in letras:\n"
            "            conteos[letras.index(c)] += 1\n"
            "        else:\n"
            "            letras.append(c)\n"
            "            conteos.append(1)\n"
            "    pares = list(zip(letras, conteos))\n"
            "    return sorted(pares, key=lambda p: p[0])"
        ),
        "visibles": [
            "assert contar_letras('abba') == [('a', 2), ('b', 2)]",
            "assert contar_letras('aaa') == [('a', 3)]",
        ],
        "ocultos": [
            "assert contar_letras('') == []",
            "assert contar_letras('cba') == [('a', 1), ('b', 1), ('c', 1)]",
            "assert contar_letras('hola mundo') == [('a', 1), ('d', 1), ('h', 1), ('l', 1), ('m', 1), ('n', 1), ('o', 2), ('u', 1)]",
        ],
    },
    {
        "n": 4,
        "titulo": "Números primos hasta n (criba manual)",
        "enunciado": (
            "Implementa `primos_hasta(n)` que devuelva una **lista** con todos los "
            "números primos desde 2 hasta `n` inclusive. Un número es primo si solo "
            "es divisible por 1 y por sí mismo.\n\n"
            "**Ejemplo:** `primos_hasta(20)` → `[2, 3, 5, 7, 11, 13, 17, 19]`.\n\n"
            "Pista: escribe una función auxiliar `es_primo(k)` y usa un bucle externo."
        ),
        "plantilla": "def primos_hasta(n):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def primos_hasta(n):\n"
            "    def es_primo(k):\n"
            "        if k < 2:\n"
            "            return False\n"
            "        d = 2\n"
            "        while d * d <= k:\n"
            "            if k % d == 0:\n"
            "                return False\n"
            "            d += 1\n"
            "        return True\n"
            "    return [k for k in range(2, n + 1) if es_primo(k)]"
        ),
        "visibles": [
            "assert primos_hasta(20) == [2, 3, 5, 7, 11, 13, 17, 19]",
            "assert primos_hasta(2) == [2]",
            "assert primos_hasta(1) == []",
        ],
        "ocultos": [
            "assert primos_hasta(10) == [2, 3, 5, 7]",
            "assert 97 in primos_hasta(100)",
            "assert 100 not in primos_hasta(100)",
        ],
    },
    {
        "n": 5,
        "titulo": "Aplicar descuentos con map y lambda",
        "enunciado": (
            "Implementa `aplicar_descuentos(precios, tasa)` que reciba una lista de "
            "precios y una tasa de descuento (ej: `0.10` = 10%) y devuelva una **nueva "
            "lista** con los precios tras el descuento, usando `map` y `lambda`.\n\n"
            "Los precios resultado deben ser enteros (usa `int()` en la lambda).\n\n"
            "**Ejemplo:** `aplicar_descuentos([100000, 200000], 0.10)` → `[90000, 180000]`."
        ),
        "plantilla": "def aplicar_descuentos(precios, tasa):\n    # ✏️ TU CÓDIGO AQUÍ (usa map + lambda)\n    " + NI,
        "solucion": (
            "def aplicar_descuentos(precios, tasa):\n"
            "    return list(map(lambda p: int(p * (1 - tasa)), precios))"
        ),
        "visibles": [
            "assert aplicar_descuentos([100000, 200000], 0.10) == [90000, 180000]",
            "assert aplicar_descuentos([50000], 0.50) == [25000]",
        ],
        "ocultos": [
            "assert aplicar_descuentos([], 0.20) == []",
            "assert aplicar_descuentos([10000, 20000, 30000], 0.0) == [10000, 20000, 30000]",
            "assert aplicar_descuentos([99999], 0.19) == [80999]",
        ],
    },
    {
        "n": 6,
        "titulo": "Potencias de 2 hasta 2^n",
        "enunciado": (
            "Implementa `potencias_de_2(n)` que devuelva una **lista** con las "
            "potencias de 2 desde 2^0 hasta 2^n inclusive.\n\n"
            "**Ejemplo:** `potencias_de_2(5)` → `[1, 2, 4, 8, 16, 32]`.\n\n"
            "La lista tiene `n + 1` elementos."
        ),
        "plantilla": "def potencias_de_2(n):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def potencias_de_2(n):\n"
            "    resultado = []\n"
            "    valor = 1\n"
            "    for _ in range(n + 1):\n"
            "        resultado.append(valor)\n"
            "        valor *= 2\n"
            "    return resultado"
        ),
        "visibles": [
            "assert potencias_de_2(5) == [1, 2, 4, 8, 16, 32]",
            "assert potencias_de_2(0) == [1]",
        ],
        "ocultos": [
            "assert potencias_de_2(1) == [1, 2]",
            "assert potencias_de_2(10)[-1] == 1024",
            "assert len(potencias_de_2(8)) == 9",
        ],
    },
    {
        "n": 7,
        "titulo": "Acumular comisión por tramos de ventas",
        "enunciado": (
            "Implementa `comision_total(ventas)` que reciba una lista de montos de "
            "venta y devuelva la **comisión total acumulada**. La tasa de comisión "
            "depende de cada venta individual:\n"
            "- venta < 500.000 → 5%\n"
            "- 500.000 <= venta <= 2.000.000 → 8%\n"
            "- venta > 2.000.000 → 12%\n\n"
            "**Ejemplo:** `comision_total([200000, 800000, 3000000])` → `10000 + 64000 + 360000 = 434000`."
        ),
        "plantilla": "def comision_total(ventas):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def comision_total(ventas):\n"
            "    def tasa(v):\n"
            "        if v < 500000:\n"
            "            return 0.05\n"
            "        elif v <= 2000000:\n"
            "            return 0.08\n"
            "        else:\n"
            "            return 0.12\n"
            "    total = 0\n"
            "    for v in ventas:\n"
            "        total += v * tasa(v)\n"
            "    return total"
        ),
        "visibles": [
            "assert comision_total([200000, 800000, 3000000]) == 434000.0",
            "assert comision_total([]) == 0",
        ],
        "ocultos": [
            "assert comision_total([100000]) == 5000.0",
            "assert comision_total([500000]) == 40000.0",
            "assert comision_total([2000001]) == 240000.12",
            "assert abs(comision_total([499999, 500000, 2000000, 2000001]) - (499999*0.05 + 500000*0.08 + 2000000*0.08 + 2000001*0.12)) < 0.01",
        ],
    },
    {
        "n": 8,
        "titulo": "Validar condición sobre todos/alguno de los elementos",
        "enunciado": (
            "Implementa dos funciones:\n"
            "- `todos_cumplen(lista, condicion)`: devuelve `True` si **todos** los "
            "elementos de la lista cumplen `condicion`. Lista vacía → `True`.\n"
            "- `alguno_cumple(lista, condicion)`: devuelve `True` si **al menos un** "
            "elemento cumple `condicion`. Lista vacía → `False`.\n\n"
            "Implementa internamente con un **bucle** (no uses `all()` ni `any()` "
            "directamente en la función principal).\n\n"
            "**Ejemplos:**\n"
            "`todos_cumplen([2, 4, 6], lambda x: x % 2 == 0)` → `True`\n"
            "`alguno_cumple([1, 3, 4], lambda x: x % 2 == 0)` → `True`"
        ),
        "plantilla": (
            "def todos_cumplen(lista, condicion):\n"
            "    # ✏️ TU CÓDIGO AQUÍ (usa bucle, no all())\n"
            "    " + NI + "\n\n"
            "def alguno_cumple(lista, condicion):\n"
            "    # ✏️ TU CÓDIGO AQUÍ (usa bucle, no any())\n"
            "    " + NI
        ),
        "solucion": (
            "def todos_cumplen(lista, condicion):\n"
            "    for x in lista:\n"
            "        if not condicion(x):\n"
            "            return False\n"
            "    return True\n\n"
            "def alguno_cumple(lista, condicion):\n"
            "    for x in lista:\n"
            "        if condicion(x):\n"
            "            return True\n"
            "    return False"
        ),
        "visibles": [
            "assert todos_cumplen([2, 4, 6], lambda x: x % 2 == 0) is True",
            "assert todos_cumplen([2, 3, 6], lambda x: x % 2 == 0) is False",
            "assert alguno_cumple([1, 3, 4], lambda x: x % 2 == 0) is True",
            "assert alguno_cumple([1, 3, 5], lambda x: x % 2 == 0) is False",
        ],
        "ocultos": [
            "assert todos_cumplen([], lambda x: False) is True",
            "assert alguno_cumple([], lambda x: True) is False",
            "assert todos_cumplen([10, 20, 30], lambda x: x > 5) is True",
            "assert alguno_cumple([-1, -2, 3], lambda x: x > 0) is True",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 3 · Tarea 01 — 8 ejercicios autocalificables

### Ciclos, funciones y lambdas

**Instrucciones**

1. Implementa cada función en la celda que dice `# ✏️ TU CÓDIGO AQUÍ`
   (reemplaza `raise NotImplementedError`).
2. **No cambies el nombre ni los parámetros** de las funciones.
3. Ejecuta las celdas de **tests visibles** y **tests adicionales**.
   Un ✅ indica que el caso pasa; un `AssertionError` señala qué caso falla.
4. Objetivo: que **todas** las celdas de tests pasen sin error.

> 🧠 Antes de programar, escribe el pseudocódigo y traza un ejemplo a mano.

> ⚠️ Recién abierta, la tarea **no** corre de principio a fin: los tests
> fallarán hasta que implementes cada función.
""",
    "cierre_md": r"""
---
## Entrega

Cuando **todas** las celdas de tests muestren ✅, has completado la tarea.

| Ejercicio | Concepto principal |
|---|---|
| 1 MCD (Euclides) | `while` con condición de parada |
| 2 Bubble sort | bucles anidados, intercambio |
| 3 Contar letras | listas paralelas + `sorted` con lambda |
| 4 Primos hasta n | función auxiliar interna + comprehension |
| 5 Aplicar descuentos | `map` + `lambda` |
| 6 Potencias de 2 | acumulador multiplicativo |
| 7 Comisión por tramos | función auxiliar + acumulador |
| 8 Todos/alguno cumplen | `return` temprano (short-circuit) |

> 💭 **Reflexión:** los ejercicios 7 y 8 te muestran cómo `sum()` con una
> comprehension y `all()`/`any()` incorporados hacen lo mismo de forma más
> compacta. Úsalos libremente a partir de ahora — pero hoy los implementaste
> a mano para entender su mecánica.
""",
}

validar(ejercicios)
construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase03", "homework01.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "clase03_homework01_solved.ipynb"),
)
