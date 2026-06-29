"""Construye curso/clase01/homework01.ipynb — 8 ejercicios autocalificables."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    {
        "n": 1,
        "titulo": "Clasificar una edad (decisión)",
        "enunciado": (
            "Implementa `clasificar(edad)` que devuelva:\n"
            "- `\"menor\"` si `edad < 18`\n"
            "- `\"adulto\"` si `18 <= edad < 65`\n"
            "- `\"adulto mayor\"` si `edad >= 65`\n\n"
            "**Casos de ejemplo:** `clasificar(10)` → `\"menor\"`, "
            "`clasificar(40)` → `\"adulto\"`, `clasificar(70)` → `\"adulto mayor\"`."
        ),
        "plantilla": f"def clasificar(edad):\n    # ✏️ TU CÓDIGO AQUÍ\n    {NI}",
        "solucion": (
            "def clasificar(edad):\n"
            "    if edad < 18:\n"
            "        return 'menor'\n"
            "    elif edad < 65:\n"
            "        return 'adulto'\n"
            "    else:\n"
            "        return 'adulto mayor'"
        ),
        "visibles": [
            "assert clasificar(10) == 'menor'",
            "assert clasificar(40) == 'adulto'",
            "assert clasificar(70) == 'adulto mayor'",
        ],
        "ocultos": [
            "assert clasificar(17) == 'menor'",
            "assert clasificar(18) == 'adulto'",
            "assert clasificar(64) == 'adulto'",
            "assert clasificar(65) == 'adulto mayor'",
        ],
    },
    {
        "n": 2,
        "titulo": "Suma de los pares hasta n (bucle + condición)",
        "enunciado": (
            "Implementa `suma_pares(n)` que devuelva la suma de todos los números "
            "**pares** desde 1 hasta `n` (inclusive).\n\n"
            "**Casos de ejemplo:** `suma_pares(6)` → `12` (2+4+6); `suma_pares(1)` → `0`."
        ),
        "plantilla": f"def suma_pares(n):\n    # ✏️ TU CÓDIGO AQUÍ\n    {NI}",
        "solucion": (
            "def suma_pares(n):\n"
            "    total = 0\n"
            "    for k in range(1, n + 1):\n"
            "        if k % 2 == 0:\n"
            "            total += k\n"
            "    return total"
        ),
        "visibles": [
            "assert suma_pares(6) == 12",
            "assert suma_pares(1) == 0",
        ],
        "ocultos": [
            "assert suma_pares(2) == 2",
            "assert suma_pares(10) == 30",
            "assert suma_pares(0) == 0",
        ],
    },
    {
        "n": 3,
        "titulo": "Factorial (acumulador multiplicativo)",
        "enunciado": (
            "Implementa `factorial(n)` que devuelva `n!` = 1·2·3·…·n. "
            "Por convención, `factorial(0)` → `1`.\n\n"
            "**Casos de ejemplo:** `factorial(5)` → `120`; `factorial(0)` → `1`."
        ),
        "plantilla": f"def factorial(n):\n    # ✏️ TU CÓDIGO AQUÍ\n    {NI}",
        "solucion": (
            "def factorial(n):\n"
            "    producto = 1\n"
            "    for k in range(2, n + 1):\n"
            "        producto *= k\n"
            "    return producto"
        ),
        "visibles": [
            "assert factorial(5) == 120",
            "assert factorial(0) == 1",
        ],
        "ocultos": [
            "assert factorial(1) == 1",
            "assert factorial(3) == 6",
            "assert factorial(7) == 5040",
        ],
    },
    {
        "n": 4,
        "titulo": "Contar vocales (recorrer una cadena)",
        "enunciado": (
            "Implementa `contar_vocales(texto)` que cuente las vocales "
            "(`a, e, i, o, u`) en un texto **en minúsculas**.\n\n"
            "**Casos de ejemplo:** `contar_vocales(\"murcielago\")` → `5`; "
            "`contar_vocales(\"xyz\")` → `0`."
        ),
        "plantilla": f"def contar_vocales(texto):\n    # ✏️ TU CÓDIGO AQUÍ\n    {NI}",
        "solucion": (
            "def contar_vocales(texto):\n"
            "    vocales = 'aeiou'\n"
            "    cuenta = 0\n"
            "    for c in texto:\n"
            "        if c in vocales:\n"
            "            cuenta += 1\n"
            "    return cuenta"
        ),
        "visibles": [
            "assert contar_vocales('murcielago') == 5",
            "assert contar_vocales('xyz') == 0",
        ],
        "ocultos": [
            "assert contar_vocales('') == 0",
            "assert contar_vocales('aeiou') == 5",
            "assert contar_vocales('programacion') == 5",
        ],
    },
    {
        "n": 5,
        "titulo": "Segundo número más grande (dos campeones)",
        "enunciado": (
            "Implementa `segundo_mayor(lista)` que devuelva el **segundo** valor más "
            "grande de una lista con al menos 2 elementos. Si el máximo se repite, el "
            "segundo mayor puede ser igual al mayor.\n\n"
            "**Casos de ejemplo:** `segundo_mayor([3, 9, 7, 9])` → `9`; "
            "`segundo_mayor([1, 2])` → `1`."
        ),
        "plantilla": f"def segundo_mayor(lista):\n    # ✏️ TU CÓDIGO AQUÍ\n    {NI}",
        "solucion": (
            "def segundo_mayor(lista):\n"
            "    ordenada = sorted(lista, reverse=True)\n"
            "    return ordenada[1]"
        ),
        "visibles": [
            "assert segundo_mayor([3, 9, 7, 9]) == 9",
            "assert segundo_mayor([1, 2]) == 1",
        ],
        "ocultos": [
            "assert segundo_mayor([5, 4, 3, 2, 1]) == 4",
            "assert segundo_mayor([-1, -2, -3]) == -2",
            "assert segundo_mayor([10, 10, 10]) == 10",
        ],
    },
    {
        "n": 6,
        "titulo": "Invertir una lista (sin reverse ni [::-1])",
        "enunciado": (
            "Implementa `invertir(lista)` que devuelva una **nueva** lista con los "
            "elementos en orden inverso, **sin** usar `lista[::-1]` ni `.reverse()`.\n\n"
            "**Casos de ejemplo:** `invertir([1, 2, 3])` → `[3, 2, 1]`; "
            "`invertir([])` → `[]`."
        ),
        "plantilla": f"def invertir(lista):\n    # ✏️ TU CÓDIGO AQUÍ\n    {NI}",
        "solucion": (
            "def invertir(lista):\n"
            "    resultado = []\n"
            "    for i in range(len(lista) - 1, -1, -1):\n"
            "        resultado.append(lista[i])\n"
            "    return resultado"
        ),
        "visibles": [
            "assert invertir([1, 2, 3]) == [3, 2, 1]",
            "assert invertir([]) == []",
        ],
        "ocultos": [
            "assert invertir([7]) == [7]",
            "assert invertir(['a', 'b']) == ['b', 'a']",
            "assert invertir([1, 1, 2]) == [2, 1, 1]",
        ],
    },
    {
        "n": 7,
        "titulo": "¿Es primo? (bucle + salida temprana)",
        "enunciado": (
            "Implementa `es_primo(n)` que devuelva `True` si `n` es primo y `False` "
            "si no. Recuerda: los primos son enteros `>= 2` divisibles solo por 1 y "
            "por sí mismos. `0` y `1` no son primos.\n\n"
            "**Casos de ejemplo:** `es_primo(7)` → `True`; `es_primo(1)` → `False`; "
            "`es_primo(9)` → `False`."
        ),
        "plantilla": f"def es_primo(n):\n    # ✏️ TU CÓDIGO AQUÍ\n    {NI}",
        "solucion": (
            "def es_primo(n):\n"
            "    if n < 2:\n"
            "        return False\n"
            "    d = 2\n"
            "    while d * d <= n:\n"
            "        if n % d == 0:\n"
            "            return False\n"
            "        d += 1\n"
            "    return True"
        ),
        "visibles": [
            "assert es_primo(7) is True",
            "assert es_primo(1) is False",
            "assert es_primo(9) is False",
        ],
        "ocultos": [
            "assert es_primo(2) is True",
            "assert es_primo(0) is False",
            "assert es_primo(97) is True",
            "assert es_primo(100) is False",
        ],
    },
    {
        "n": 8,
        "titulo": "La moda: el valor más frecuente (contador)",
        "enunciado": (
            "Implementa `moda(lista)` que devuelva el elemento que **más veces** "
            "aparece en una lista no vacía. Si hay empate, devuelve el que aparece "
            "primero al recorrer la lista.\n\n"
            "**Casos de ejemplo:** `moda([1, 2, 2, 3])` → `2`; `moda([5])` → `5`."
        ),
        "plantilla": f"def moda(lista):\n    # ✏️ TU CÓDIGO AQUÍ\n    {NI}",
        "solucion": (
            "def moda(lista):\n"
            "    mejor = lista[0]\n"
            "    mejor_conteo = 0\n"
            "    for x in lista:\n"
            "        conteo = 0\n"
            "        for y in lista:\n"
            "            if y == x:\n"
            "                conteo += 1\n"
            "        if conteo > mejor_conteo:\n"
            "            mejor_conteo = conteo\n"
            "            mejor = x\n"
            "    return mejor"
        ),
        "visibles": [
            "assert moda([1, 2, 2, 3]) == 2",
            "assert moda([5]) == 5",
        ],
        "ocultos": [
            "assert moda([4, 4, 4, 1, 1]) == 4",
            "assert moda(['a', 'b', 'a']) == 'a'",
            "assert moda([7, 8, 8, 7, 7]) == 7",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 1 · Tarea 01 — 8 ejercicios autocalificables

### Pensamiento algorítmico y pseudocódigo

**Instrucciones**

1. Implementa cada función en la celda que dice `# ✏️ TU CÓDIGO AQUÍ`
   (reemplaza la línea `raise NotImplementedError`).
2. **No cambies el nombre ni los parámetros** de las funciones: los tests dependen de ellos.
3. Ejecuta las celdas de **tests visibles** y **tests adicionales**. Si una función
   está bien, verás un mensaje ✅; si no, saltará un `AssertionError` señalando el caso que falla.
4. Tu objetivo: que **todas** las celdas de tests pasen sin error.

> 🔎 Antes de programar cada función, escribe su pseudocódigo y traza un ejemplo a mano.

> ⚠️ Recién abierta, esta tarea **no** corre de principio a fin: las celdas de tests
> fallarán hasta que implementes cada función. ¡Eso es justo lo que vas a arreglar!
""",
    "cierre_md": r"""
---
## Entrega

Cuando **todas** las celdas de tests muestren ✅, has completado la tarea.

Repaso de patrones ejercitados:

| Ejercicio | Patrón principal |
|---|---|
| 1 Clasificar edad | decisión escalonada |
| 2 Suma de pares | bucle + condición |
| 3 Factorial | acumulador multiplicativo |
| 4 Contar vocales | contador sobre cadena |
| 5 Segundo mayor | ordenar / campeones |
| 6 Invertir lista | construir lista nueva |
| 7 Es primo | bucle + salida temprana |
| 8 Moda | contador anidado (O(n²)) |

> 💭 **Reflexión:** el ejercicio 8 usa dos bucles anidados → O(n²). En la Clase 4,
> con diccionarios, lo resolverás en O(n). Piensa desde ya cómo lo harías.
""",
}

validar(ejercicios)
construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase01", "homework01.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "homework01_solved.ipynb"),
)
