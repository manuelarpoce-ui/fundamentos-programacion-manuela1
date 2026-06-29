"""Construye curso/clase01/practice01.ipynb — 10 ejercicios graduales.

Patrón por ejercicio:
  1. Markdown con enunciado + ejemplo.
  2. Celda plantilla (el estudiante escribe aquí; por defecto devuelve None).
  3. Celda de comprobación SUAVE (revisar(): imprime ✅/❌ pero NO lanza error),
     de modo que el notebook se ejecuta de principio a fin aunque falte resolver.
  4. Markdown <details> con la solución comentada (oculta).

Las soluciones se VALIDAN en tiempo de construcción con asserts: si este script
corre sin fallar, las soluciones de referencia son correctas.
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
# Clase 1 · Práctica 01 — 10 ejercicios graduales

### Pensamiento algorítmico y pseudocódigo

Estos 10 ejercicios van **de menor a mayor dificultad**. Para cada uno:

1. Lee el enunciado y el ejemplo.
2. Escribe tu solución en la celda que dice `# ✏️ TU CÓDIGO AQUÍ`.
3. Ejecuta la celda de **comprobación**: verás ✅ o ❌ por cada caso.
4. ¿Atascado? Despliega **💡 Ver solución** al final de cada ejercicio.

> 🧠 **Antes de teclear**, escribe el pseudocódigo en una hoja. La práctica de hoy
> es pensar el algoritmo, no solo lograr que pase la comprobación.

> ⚙️ Las comprobaciones son *suaves*: si tu función aún no está lista, verás ❌
> pero el notebook seguirá ejecutándose sin romperse.
"""),

code(r"""
# Cargamos la utilidad de comprobación compartida del curso.
import os, sys
sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar
print("Listo. Usa revisar(nombre, condicion) para comprobar tus respuestas.")
"""),
]


# --------------------------------------------------------------------------- #
# Definición de ejercicios. Cada uno: enunciado, plantilla, nombre de función,
# casos de prueba (para la celda de comprobación) y solución de referencia.
# --------------------------------------------------------------------------- #

def ejercicio(numero, titulo, enunciado_md, plantilla, check_code, solucion_md):
    C.append(md(f"## Ejercicio {numero} · {titulo}\n\n{enunciado_md}"))
    C.append(code(plantilla))
    C.append(code(check_code))
    C.append(md(solucion_md))


# ---- 1 --------------------------------------------------------------------
ejercicio(
    1, "Área de un rectángulo (Entrada → Proceso → Salida)",
    r"""Escribe `area_rectangulo(base, altura)` que devuelva el área.

**Ejemplo:** `area_rectangulo(3, 4)` → `12`.

Es el patrón EPS más simple: entran dos números, sale uno.""",
    r"""
def area_rectangulo(base, altura):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("3 x 4 = 12", area_rectangulo(3, 4) == 12)
revisar("10 x 2 = 20", area_rectangulo(10, 2) == 20)
revisar("0 de base = 0", area_rectangulo(0, 5) == 0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def area_rectangulo(base, altura):
    return base * altura
```
El área es simplemente `base * altura`. No hay decisiones ni repeticiones: pura
secuencia.
</details>
""",
)

# ---- 2 --------------------------------------------------------------------
ejercicio(
    2, "El mayor de tres números (decisión)",
    r"""Escribe `mayor_de_tres(a, b, c)` que devuelva el más grande de los tres.

**Ejemplo:** `mayor_de_tres(4, 9, 2)` → `9`.

Pista: usa comparaciones. (Puedes usar `max`, pero intenta primero con `if`.)""",
    r"""
def mayor_de_tres(a, b, c):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("4,9,2 -> 9", mayor_de_tres(4, 9, 2) == 9)
revisar("el primero", mayor_de_tres(10, 1, 5) == 10)
revisar("negativos", mayor_de_tres(-3, -1, -7) == -1)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def mayor_de_tres(a, b, c):
    mayor = a
    if b > mayor:
        mayor = b
    if c > mayor:
        mayor = c
    return mayor
```
Reutilizamos el patrón **campeón**: empezamos suponiendo que `a` es el mayor y lo
actualizamos si encontramos algo más grande.
</details>
""",
)

# ---- 3 --------------------------------------------------------------------
ejercicio(
    3, "Máximo de una lista (patrón campeón)",
    r"""Escribe `maximo(lista)` que devuelva el mayor valor de una lista **no vacía**,
sin usar `max`.

**Ejemplo:** `maximo([3, 9, 2, 9, 1])` → `9`.""",
    r"""
def maximo(lista):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("ejemplo", maximo([3, 9, 2, 9, 1]) == 9)
revisar("un solo elemento", maximo([7]) == 7)
revisar("todos negativos", maximo([-5, -2, -9]) == -2)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def maximo(lista):
    campeon = lista[0]
    for x in lista:
        if x > campeon:
            campeon = x
    return campeon
```
El primer elemento es el campeón provisional; recorremos y actualizamos.
</details>
""",
)

# ---- 4 --------------------------------------------------------------------
ejercicio(
    4, "Contar números pares (contador)",
    r"""Escribe `contar_pares(lista)` que cuente cuántos números pares hay.

**Ejemplo:** `contar_pares([1, 2, 3, 4, 6])` → `3`.""",
    r"""
def contar_pares(lista):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("ejemplo", contar_pares([1, 2, 3, 4, 6]) == 3)
revisar("ninguno", contar_pares([1, 3, 5]) == 0)
revisar("lista vacía", contar_pares([]) == 0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def contar_pares(lista):
    cuenta = 0
    for x in lista:
        if x % 2 == 0:
            cuenta += 1
    return cuenta
```
Patrón **contador**: una variable que aumenta cuando se cumple la condición. Con
la lista vacía, el bucle no se ejecuta y devuelve 0 — ¡el caso borde sale gratis!
</details>
""",
)

# ---- 5 --------------------------------------------------------------------
ejercicio(
    5, "Promedio seguro (acumulador + caso borde)",
    r"""Escribe `promedio(lista)` que devuelva el promedio. Si la lista está **vacía**,
devuelve `None` (no se puede dividir entre cero).

**Ejemplo:** `promedio([4, 6, 8])` → `6.0`; `promedio([])` → `None`.""",
    r"""
def promedio(lista):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("ejemplo", promedio([4, 6, 8]) == 6.0)
revisar("un valor", promedio([10]) == 10.0)
revisar("vacía -> None", promedio([]) is None)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def promedio(lista):
    if len(lista) == 0:      # validar ANTES de dividir
        return None
    total = 0
    for x in lista:
        total += x           # acumulador
    return total / len(lista)
```
Primero validamos el caso borde (lista vacía), luego acumulamos y dividimos.
</details>
""",
)

# ---- 6 --------------------------------------------------------------------
ejercicio(
    6, "Posición de un valor (búsqueda lineal)",
    r"""Escribe `posicion(lista, objetivo)` que devuelva el **índice** de la primera
aparición de `objetivo`, o `-1` si no está.

**Ejemplo:** `posicion([10, 20, 30], 20)` → `1`; `posicion([10, 20], 99)` → `-1`.""",
    r"""
def posicion(lista, objetivo):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("encuentra en medio", posicion([10, 20, 30], 20) == 1)
revisar("primera posición", posicion([7, 7, 7], 7) == 0)
revisar("no está -> -1", posicion([10, 20], 99) == -1)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def posicion(lista, objetivo):
    for i in range(len(lista)):
        if lista[i] == objetivo:
            return i           # salida temprana en la primera aparición
    return -1
```
Recorremos por **índice** con `range(len(lista))` para poder devolver la posición.
</details>
""",
)

# ---- 7 --------------------------------------------------------------------
ejercicio(
    7, "Días que subió la temperatura (comparar con el anterior)",
    r"""Escribe `dias_que_subio(temps)` que cuente en cuántos días la temperatura fue
**mayor que la del día anterior**.

**Ejemplo:** `dias_que_subio([20, 22, 21, 25])` → `2` (subió 20→22 y 21→25).""",
    r"""
def dias_que_subio(temps):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("ejemplo", dias_que_subio([20, 22, 21, 25]) == 2)
revisar("siempre baja", dias_que_subio([5, 4, 3, 2]) == 0)
revisar("un solo día", dias_que_subio([10]) == 0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def dias_que_subio(temps):
    subidas = 0
    for i in range(1, len(temps)):   # desde el segundo día
        if temps[i] > temps[i - 1]:
            subidas += 1
    return subidas
```
Empezamos en `i = 1` porque el primer día no tiene "anterior". Con un solo día el
bucle no corre y devuelve 0.
</details>
""",
)

# ---- 8 --------------------------------------------------------------------
ejercicio(
    8, "¿Es palíndromo? (recorrer una cadena)",
    r"""Escribe `es_palindromo(texto)` que devuelva `True` si `texto` se lee igual al
derecho y al revés. Considera el texto ya en minúsculas y sin espacios.

**Ejemplo:** `es_palindromo("reconocer")` → `True`; `es_palindromo("python")` → `False`.

Pista: en Python, `texto[::-1]` invierte una cadena.""",
    r"""
def es_palindromo(texto):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("reconocer", es_palindromo("reconocer") is True)
revisar("python", es_palindromo("python") is False)
revisar("una letra", es_palindromo("a") is True)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def es_palindromo(texto):
    return texto == texto[::-1]
```
`texto[::-1]` es el texto invertido; si coincide con el original, es palíndromo.

**Versión sin trucos** (recorriendo con dos índices), por si quieres ver la lógica:
```python
def es_palindromo(texto):
    i, j = 0, len(texto) - 1
    while i < j:
        if texto[i] != texto[j]:
            return False
        i += 1
        j -= 1
    return True
```
</details>
""",
)

# ---- 9 --------------------------------------------------------------------
ejercicio(
    9, "Dar el vuelto (algoritmo voraz)",
    r"""Escribe `contar_billetes(monto)` que devuelva el **número total de billetes**
necesarios para entregar `monto`, usando denominaciones
`[50000, 20000, 10000, 5000, 1000]` y la estrategia voraz.

**Ejemplo:** `contar_billetes(87000)` → `6`
(1×50000 + 1×20000 + 1×10000 + 1×5000 + 2×1000 = 87000, en total 6 billetes).""",
    r"""
def contar_billetes(monto):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("87000 -> 6", contar_billetes(87000) == 6)
revisar("50000 -> 1", contar_billetes(50000) == 1)
revisar("0 -> 0", contar_billetes(0) == 0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def contar_billetes(monto):
    billetes = [50000, 20000, 10000, 5000, 1000]
    total = 0
    for b in billetes:
        total += monto // b      # cuántos billetes de 'b' caben
        monto = monto % b        # lo que queda por entregar
    return total
```
Por cada denominación tomamos cuántas caben (`//`) y nos quedamos con el residuo
(`%`). Sumamos todas las cantidades.
</details>
""",
)

# ---- 10 -------------------------------------------------------------------
ejercicio(
    10, "¿Hay duplicados? (de O(n²) a O(n))",
    r"""Escribe `hay_duplicados(lista)` que devuelva `True` si algún valor se repite.

**Ejemplo:** `hay_duplicados([1, 2, 3, 2])` → `True`; `hay_duplicados([1, 2, 3])` → `False`.

Reto extra (mental): ¿tu solución es O(n²) o O(n)? La solución eficiente recuerda
lo ya visto en un `set`.""",
    r"""
def hay_duplicados(lista):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("hay repetido", hay_duplicados([1, 2, 3, 2]) is True)
revisar("sin repetidos", hay_duplicados([1, 2, 3]) is False)
revisar("lista vacía", hay_duplicados([]) is False)
""",
    r"""
<details><summary>💡 Ver solución</summary>

**Eficiente — O(n):**
```python
def hay_duplicados(lista):
    vistos = set()
    for x in lista:
        if x in vistos:
            return True
        vistos.add(x)
    return False
```

**Ingenua — O(n²)** (correcta pero lenta, para comparar):
```python
def hay_duplicados(lista):
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] == lista[j]:
                return True
    return False
```
Ambas dan la misma respuesta; la primera recorre una sola vez recordando lo visto.
</details>
""",
)

C.append(md(r"""
---
## ¡Terminaste la práctica 01! 🎉

Si todas tus comprobaciones muestran ✅, dominas los patrones base de la clase:
**EPS, decisión, campeón, contador, acumulador, búsqueda lineal, voraz y
eficiencia**.

➡️ Continúa con **practice02.ipynb**, donde aplicaremos estas ideas a un caso real
de ciencia de datos con un dataset de transacciones.
"""))


# ===================================================================== #
# VALIDACIÓN EN TIEMPO DE CONSTRUCCIÓN de las soluciones de referencia
# ===================================================================== #
def _validar():
    def area_rectangulo(base, altura):
        return base * altura
    assert area_rectangulo(3, 4) == 12 and area_rectangulo(0, 5) == 0

    def mayor_de_tres(a, b, c):
        m = a
        if b > m: m = b
        if c > m: m = c
        return m
    assert mayor_de_tres(4, 9, 2) == 9 and mayor_de_tres(-3, -1, -7) == -1

    def maximo(lista):
        c = lista[0]
        for x in lista:
            if x > c: c = x
        return c
    assert maximo([3, 9, 2, 9, 1]) == 9 and maximo([-5, -2, -9]) == -2

    def contar_pares(lista):
        return sum(1 for x in lista if x % 2 == 0)
    assert contar_pares([1, 2, 3, 4, 6]) == 3 and contar_pares([]) == 0

    def promedio(lista):
        if len(lista) == 0: return None
        return sum(lista) / len(lista)
    assert promedio([4, 6, 8]) == 6.0 and promedio([]) is None

    def posicion(lista, objetivo):
        for i in range(len(lista)):
            if lista[i] == objetivo: return i
        return -1
    assert posicion([10, 20, 30], 20) == 1 and posicion([10, 20], 99) == -1

    def dias_que_subio(temps):
        return sum(1 for i in range(1, len(temps)) if temps[i] > temps[i - 1])
    assert dias_que_subio([20, 22, 21, 25]) == 2 and dias_que_subio([10]) == 0

    def es_palindromo(texto):
        return texto == texto[::-1]
    assert es_palindromo("reconocer") is True and es_palindromo("python") is False

    def contar_billetes(monto):
        total = 0
        for b in [50000, 20000, 10000, 5000, 1000]:
            total += monto // b
            monto = monto % b
        return total
    assert contar_billetes(87000) == 6 and contar_billetes(50000) == 1 and contar_billetes(0) == 0

    def hay_duplicados(lista):
        vistos = set()
        for x in lista:
            if x in vistos: return True
            vistos.add(x)
        return False
    assert hay_duplicados([1, 2, 3, 2]) is True and hay_duplicados([]) is False

    print("✔ Todas las soluciones de referencia de practice01 pasan sus pruebas.")

_validar()


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase01", "practice01.ipynb")
build(os.path.abspath(ruta), C)
