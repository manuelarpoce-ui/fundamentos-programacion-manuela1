"""Construye curso/clase03/practice01.ipynb — 10 ejercicios de ciclos, funciones y lambdas.

Patrón por ejercicio:
  1. Markdown con enunciado + ejemplo.
  2. Celda plantilla (el estudiante escribe aquí; por defecto devuelve None).
  3. Celda de comprobación SUAVE (revisar(): imprime OK/FAIL pero NO lanza error).
  4. Markdown <details> con la solución comentada (oculta).

Las soluciones se VALIDAN en tiempo de construcción con asserts.
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
# Clase 3 · Práctica 01 — 10 ejercicios: ciclos, funciones y lambdas

### Fundamentos de Programación para Ciencia de Datos

Estos 10 ejercicios van **de menor a mayor dificultad**. Para cada uno:

1. Lee el enunciado y el ejemplo.
2. Escribe tu solución en la celda que dice `# ✏️ TU CÓDIGO AQUÍ`.
3. Ejecuta la celda de **comprobación**: verás ✅ o ❌ por cada caso.
4. ¿Atascado? Despliega **💡 Ver solución** al final de cada ejercicio.

> 🧠 **Metodología:** antes de teclear, escribe el pseudocódigo y traza un
> ejemplo a mano. El código debe ser la traducción de tu pseudocódigo.

> ⚙️ Las comprobaciones son *suaves*: si tu función aún no está lista, verás ❌
> pero el notebook seguirá ejecutándose sin romperse.
"""),

code(r"""
# Cargamos la utilidad de comprobación del curso.
import os, sys
sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar
print("Listo. Comprobaciones activas.")
"""),
]


# --------------------------------------------------------------------------- #
# Helper local para definir ejercicios
# --------------------------------------------------------------------------- #
def ejercicio(numero, titulo, enunciado_md, plantilla, check_code, solucion_md):
    C.append(md("## Ejercicio " + str(numero) + " · " + titulo + "\n\n" + enunciado_md))
    C.append(code(plantilla))
    C.append(code(check_code))
    C.append(md(solucion_md))


# ---- 1 --------------------------------------------------------------------
ejercicio(
    1, "FizzBuzz clásico",
    r"""Escribe `fizzbuzz(n)` que devuelva una **lista** con los valores 1..n donde:
- Múltiplos de 3 → `"Fizz"`
- Múltiplos de 5 → `"Buzz"`
- Múltiplos de ambos → `"FizzBuzz"`
- El resto → el número entero

**Ejemplo:** `fizzbuzz(15)` termina en `[..., "FizzBuzz"]` y contiene `"Fizz"` en la pos 2 (índice 2 = número 3).""",
    r"""
def fizzbuzz(n):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("fizzbuzz(15)[2] == 'Fizz'",   fizzbuzz(15) is not None and fizzbuzz(15)[2]  == "Fizz")
revisar("fizzbuzz(15)[4] == 'Buzz'",   fizzbuzz(15) is not None and fizzbuzz(15)[4]  == "Buzz")
revisar("fizzbuzz(15)[14] == 'FizzBuzz'", fizzbuzz(15) is not None and fizzbuzz(15)[14] == "FizzBuzz")
revisar("fizzbuzz(15)[0] == 1",        fizzbuzz(15) is not None and fizzbuzz(15)[0]  == 1)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def fizzbuzz(n):
    resultado = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            resultado.append("FizzBuzz")
        elif i % 3 == 0:
            resultado.append("Fizz")
        elif i % 5 == 0:
            resultado.append("Buzz")
        else:
            resultado.append(i)
    return resultado
```
El truco: comprobar `% 15` primero (múltiplo de ambos), porque si comprobas
`% 3` primero, los múltiplos de 15 ya entrarían como "Fizz".
</details>
""",
)

# ---- 2 --------------------------------------------------------------------
ejercicio(
    2, "Tabla de multiplicar",
    r"""Escribe `tabla_multiplicar(n)` que devuelva una **lista de strings** con la tabla
de multiplicar de `n`, del 1 al 10.

**Ejemplo:** `tabla_multiplicar(3)` → `["3 x 1 = 3", "3 x 2 = 6", ..., "3 x 10 = 30"]`.""",
    r"""
def tabla_multiplicar(n):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("longitud 10",     tabla_multiplicar(3) is not None and len(tabla_multiplicar(3)) == 10)
revisar("primer elemento", tabla_multiplicar(3) is not None and tabla_multiplicar(3)[0] == "3 x 1 = 3")
revisar("ultimo elemento", tabla_multiplicar(3) is not None and tabla_multiplicar(3)[9] == "3 x 10 = 30")
revisar("tabla del 7",     tabla_multiplicar(7) is not None and tabla_multiplicar(7)[6] == "7 x 7 = 49")
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def tabla_multiplicar(n):
    resultado = []
    for k in range(1, 11):
        resultado.append(str(n) + " x " + str(k) + " = " + str(n * k))
    return resultado
```
O con list comprehension:
```python
def tabla_multiplicar(n):
    return [str(n) + " x " + str(k) + " = " + str(n * k) for k in range(1, 11)]
```
</details>
""",
)

# ---- 3 --------------------------------------------------------------------
ejercicio(
    3, "Suma de dígitos",
    r"""Escribe `suma_digitos(n)` que devuelva la suma de los **dígitos** de un entero
positivo `n`.

**Ejemplo:** `suma_digitos(1234)` → `10` (1+2+3+4); `suma_digitos(100)` → `1`.""",
    r"""
def suma_digitos(n):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("1234 -> 10",  suma_digitos(1234) == 10)
revisar("100  -> 1",   suma_digitos(100)  == 1)
revisar("9    -> 9",   suma_digitos(9)    == 9)
revisar("999  -> 27",  suma_digitos(999)  == 27)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def suma_digitos(n):
    total = 0
    for digito in str(n):      # convierte el número a cadena y recorre cada caracter
        total += int(digito)   # convierte el caracter de vuelta a int
    return total
```
Truco: `str(1234)` → `"1234"` → iterar da `"1"`, `"2"`, `"3"`, `"4"`.
</details>
""",
)

# ---- 4 --------------------------------------------------------------------
ejercicio(
    4, "Contar palabras en una oración",
    r"""Escribe `contar_palabras(oracion)` que devuelva el número de palabras en `oracion`.
Puedes asumir que las palabras están separadas por un solo espacio.

**Ejemplo:** `contar_palabras("el perro come carne")` → `4`.""",
    r"""
def contar_palabras(oracion):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("4 palabras",     contar_palabras("el perro come carne") == 4)
revisar("1 palabra",      contar_palabras("hola") == 1)
revisar("cadena vacia",   contar_palabras("") == 0)
revisar("5 palabras",     contar_palabras("a b c d e") == 5)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def contar_palabras(oracion):
    if oracion == "":
        return 0
    return len(oracion.split())
```
`str.split()` sin argumentos divide por cualquier espacio en blanco y maneja
múltiples espacios automáticamente. `len()` cuenta el resultado.
</details>
""",
)

# ---- 5 --------------------------------------------------------------------
ejercicio(
    5, "Máximo de una lista (sin usar max())",
    r"""Escribe `maximo_lista(lista)` que devuelva el valor más grande de una lista
**no vacía**, **sin usar** `max()` ni `sorted()`.

**Ejemplo:** `maximo_lista([3, 9, 2, 7])` → `9`.""",
    r"""
def maximo_lista(lista):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("ejemplo [3,9,2,7]",       maximo_lista([3, 9, 2, 7]) == 9)
revisar("un solo elemento",        maximo_lista([42]) == 42)
revisar("todos negativos",         maximo_lista([-5, -1, -9]) == -1)
revisar("lista con repetidos",     maximo_lista([3, 3, 3]) == 3)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def maximo_lista(lista):
    campeon = lista[0]
    for x in lista:
        if x > campeon:
            campeon = x
    return campeon
```
Patrón **campeón**: el primer elemento es el mejor provisional; actualizamos
si encontramos algo mejor. Recorremos toda la lista garantizando correctitud.
</details>
""",
)

# ---- 6 --------------------------------------------------------------------
ejercicio(
    6, "Fibonacci hasta n términos",
    r"""Escribe `fibonacci(n)` que devuelva una **lista** con los primeros `n` números
de la secuencia de Fibonacci. `fibonacci(1)` → `[0]`, `fibonacci(2)` → `[0, 1]`.

La secuencia: 0, 1, 1, 2, 3, 5, 8, 13, ... (cada número es la suma de los dos anteriores).""",
    r"""
def fibonacci(n):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("fibonacci(1) = [0]",           fibonacci(1) == [0])
revisar("fibonacci(2) = [0, 1]",        fibonacci(2) == [0, 1])
revisar("fibonacci(7) = [0,1,1,2,3,5,8]", fibonacci(7) == [0, 1, 1, 2, 3, 5, 8])
revisar("longitud correcta para n=10",  fibonacci(10) is not None and len(fibonacci(10)) == 10)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def fibonacci(n):
    if n == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, n):        # generamos desde el índice 2 hasta n-1
        seq.append(seq[-2] + seq[-1])   # suma de los dos últimos
    return seq
```
`seq[-1]` es el último elemento, `seq[-2]` el penúltimo. El bucle se ejecuta
`n - 2` veces (ya tenemos los dos primeros).
</details>
""",
)

# ---- 7 --------------------------------------------------------------------
ejercicio(
    7, "Filtrar lista por condición",
    r"""Escribe `filtrar(lista, condicion)` que devuelva una **nueva lista** con solo
los elementos para los que `condicion(elemento)` es `True`.

**Ejemplo:** `filtrar([1, 2, 3, 4, 5], lambda x: x % 2 == 0)` → `[2, 4]`.""",
    r"""
def filtrar(lista, condicion):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("pares de [1..5]",    filtrar([1, 2, 3, 4, 5], lambda x: x % 2 == 0) == [2, 4])
revisar("mayores de 3",       filtrar([1, 2, 3, 4, 5], lambda x: x > 3) == [4, 5])
revisar("lista vacia",        filtrar([], lambda x: True) == [])
revisar("ninguno cumple",     filtrar([1, 3, 5], lambda x: x % 2 == 0) == [])
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def filtrar(lista, condicion):
    resultado = []
    for x in lista:
        if condicion(x):
            resultado.append(x)
    return resultado
```
Esta es, básicamente, una implementación manual de `filter()`. La ventaja de
hacerlo a mano: entiendes exactamente qué hace `filter` por dentro.
</details>
""",
)

# ---- 8 --------------------------------------------------------------------
ejercicio(
    8, "Aplanar lista de listas",
    r"""Escribe `aplanar(lista_de_listas)` que convierta una lista de listas en una
**lista plana** (un solo nivel).

**Ejemplo:** `aplanar([[1, 2], [3, 4], [5]])` → `[1, 2, 3, 4, 5]`.""",
    r"""
def aplanar(lista_de_listas):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("ejemplo basico",     aplanar([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5])
revisar("sublistas vacias",   aplanar([[], [1], []]) == [1])
revisar("lista vacia",        aplanar([]) == [])
revisar("strings",            aplanar([["a", "b"], ["c"]]) == ["a", "b", "c"])
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def aplanar(lista_de_listas):
    resultado = []
    for sublista in lista_de_listas:       # bucle exterior: recorre cada sublista
        for elemento in sublista:          # bucle interior: recorre cada elemento
            resultado.append(elemento)
    return resultado
```
Bucle anidado clásico: el exterior recorre las sublistas, el interior recorre
los elementos dentro de cada sublista.
</details>
""",
)

# ---- 9 --------------------------------------------------------------------
ejercicio(
    9, "Buscar elemento con lambda + filter",
    r"""Escribe `buscar_por(lista_de_dicts, campo, valor)` que devuelva una **lista**
con todos los diccionarios de `lista_de_dicts` donde `d[campo] == valor`.

**Ejemplo:**
```python
productos = [{"nombre": "laptop", "categoria": "tech"},
             {"nombre": "silla",  "categoria": "hogar"},
             {"nombre": "tablet", "categoria": "tech"}]
buscar_por(productos, "categoria", "tech")
# → [{"nombre": "laptop", ...}, {"nombre": "tablet", ...}]
```""",
    r"""
def buscar_por(lista_de_dicts, campo, valor):
    # ✏️ TU CÓDIGO AQUÍ (usa filter + lambda)
    return None
""",
    r"""
productos = [
    {"nombre": "laptop",  "categoria": "tecnologia"},
    {"nombre": "silla",   "categoria": "hogar"},
    {"nombre": "tablet",  "categoria": "tecnologia"},
    {"nombre": "cama",    "categoria": "hogar"},
]
tech = buscar_por(productos, "categoria", "tecnologia")
revisar("2 tech encontrados",  tech is not None and len(tech) == 2)
revisar("primer resultado es laptop", tech is not None and tech[0]["nombre"] == "laptop")
revisar("busqueda sin resultados",    len(buscar_por(productos, "categoria", "deportes")) == 0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def buscar_por(lista_de_dicts, campo, valor):
    return list(filter(lambda d: d[campo] == valor, lista_de_dicts))
```
`filter` recibe la función criterio y el iterable. La lambda captura `campo` y
`valor` del scope exterior (closure). Envolvemos en `list()` para materializar.
</details>
""",
)

# ---- 10 -------------------------------------------------------------------
ejercicio(
    10, "Potencia sin usar **",
    r"""Escribe `potencia(base, exponente)` que calcule `base ** exponente` usando un
**bucle `while` multiplicativo**, sin usar el operador `**` ni `pow()`.
Asume `exponente >= 0` y entero.

**Ejemplo:** `potencia(2, 10)` → `1024`; `potencia(5, 0)` → `1`.""",
    r"""
def potencia(base, exponente):
    # ✏️ TU CÓDIGO AQUÍ (while, sin usar **)
    return None
""",
    r"""
revisar("2^10 = 1024",  potencia(2, 10) == 1024)
revisar("5^0  = 1",     potencia(5, 0)  == 1)
revisar("3^4  = 81",    potencia(3, 4)  == 81)
revisar("7^1  = 7",     potencia(7, 1)  == 7)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def potencia(base, exponente):
    resultado = 1
    while exponente > 0:
        resultado *= base
        exponente -= 1
    return resultado
```
**Trazado para `potencia(2, 3)`:**

| `exponente` | `resultado` antes | operación | `resultado` después |
|-------------|-------------------|-----------|---------------------|
| 3 | 1 | 1 × 2 | 2 |
| 2 | 2 | 2 × 2 | 4 |
| 1 | 4 | 4 × 2 | 8 |
| 0 | — | bucle termina | 8 |

Para `exponente = 0`, el bucle no entra y devuelve 1 (correcto: cualquier
número elevado a 0 es 1).
</details>
""",
)


C.append(md(r"""
---
## ¡Terminaste la práctica 01!

Si todas tus comprobaciones muestran ✅, dominas los patrones clave de la clase:
**for, while, break, continue, funciones, parámetros, lambda y filter**.

➡️ Continúa con **practice02.ipynb** para aplicar estas ideas a un pipeline real
de procesamiento de transacciones con datos de negocio.
"""))


# ===================================================================== #
# VALIDACIÓN EN TIEMPO DE CONSTRUCCIÓN
# ===================================================================== #
def _validar():
    def fizzbuzz(n):
        resultado = []
        for i in range(1, n + 1):
            if i % 15 == 0:
                resultado.append("FizzBuzz")
            elif i % 3 == 0:
                resultado.append("Fizz")
            elif i % 5 == 0:
                resultado.append("Buzz")
            else:
                resultado.append(i)
        return resultado
    assert fizzbuzz(15)[2] == "Fizz"
    assert fizzbuzz(15)[4] == "Buzz"
    assert fizzbuzz(15)[14] == "FizzBuzz"
    assert fizzbuzz(15)[0] == 1

    def tabla_multiplicar(n):
        return [str(n) + " x " + str(k) + " = " + str(n * k) for k in range(1, 11)]
    assert len(tabla_multiplicar(3)) == 10
    assert tabla_multiplicar(3)[0] == "3 x 1 = 3"
    assert tabla_multiplicar(3)[9] == "3 x 10 = 30"
    assert tabla_multiplicar(7)[6] == "7 x 7 = 49"

    def suma_digitos(n):
        return sum(int(d) for d in str(n))
    assert suma_digitos(1234) == 10
    assert suma_digitos(100) == 1
    assert suma_digitos(999) == 27

    def contar_palabras(oracion):
        if oracion == "":
            return 0
        return len(oracion.split())
    assert contar_palabras("el perro come carne") == 4
    assert contar_palabras("hola") == 1
    assert contar_palabras("") == 0

    def maximo_lista(lista):
        campeon = lista[0]
        for x in lista:
            if x > campeon:
                campeon = x
        return campeon
    assert maximo_lista([3, 9, 2, 7]) == 9
    assert maximo_lista([42]) == 42
    assert maximo_lista([-5, -1, -9]) == -1

    def fibonacci(n):
        if n == 1:
            return [0]
        seq = [0, 1]
        for _ in range(2, n):
            seq.append(seq[-2] + seq[-1])
        return seq
    assert fibonacci(1) == [0]
    assert fibonacci(2) == [0, 1]
    assert fibonacci(7) == [0, 1, 1, 2, 3, 5, 8]
    assert len(fibonacci(10)) == 10

    def filtrar(lista, condicion):
        return [x for x in lista if condicion(x)]
    assert filtrar([1, 2, 3, 4, 5], lambda x: x % 2 == 0) == [2, 4]
    assert filtrar([], lambda x: True) == []

    def aplanar(lista_de_listas):
        resultado = []
        for sublista in lista_de_listas:
            for elemento in sublista:
                resultado.append(elemento)
        return resultado
    assert aplanar([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]
    assert aplanar([[], [1], []]) == [1]
    assert aplanar([]) == []

    def buscar_por(lista_de_dicts, campo, valor):
        return list(filter(lambda d: d[campo] == valor, lista_de_dicts))
    productos = [
        {"nombre": "laptop",  "categoria": "tecnologia"},
        {"nombre": "silla",   "categoria": "hogar"},
        {"nombre": "tablet",  "categoria": "tecnologia"},
    ]
    assert len(buscar_por(productos, "categoria", "tecnologia")) == 2
    assert buscar_por(productos, "categoria", "deportes") == []

    def potencia(base, exponente):
        resultado = 1
        while exponente > 0:
            resultado *= base
            exponente -= 1
        return resultado
    assert potencia(2, 10) == 1024
    assert potencia(5, 0) == 1
    assert potencia(3, 4) == 81

    print("OK Todas las soluciones de referencia de practice01 (clase03) pasan sus pruebas.")

_validar()


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase03", "practice01.ipynb")
build(os.path.abspath(ruta), C)
