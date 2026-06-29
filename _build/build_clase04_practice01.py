"""Construye curso/clase04/practice01.ipynb — 10 ejercicios graduales.

Patrón por ejercicio:
  1. Markdown con enunciado + ejemplo.
  2. Celda plantilla (el estudiante escribe aquí; devuelve None por defecto).
  3. Celda de comprobación suave (revisar(): imprime ✅/❌ pero no lanza error).
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
# Clase 4 · Práctica 01 — 10 ejercicios con estructuras de datos

### Listas, tuplas, diccionarios y conjuntos

Estos 10 ejercicios van **de menor a mayor dificultad**. Para cada uno:

1. Lee el enunciado y el ejemplo.
2. Escribe tu solución en la celda que dice `# ✏️ TU CÓDIGO AQUÍ`.
3. Ejecuta la celda de **comprobación**: verás ✅ o ❌ por cada caso.
4. ¿Atascado? Despliega **💡 Ver solución** al final de cada ejercicio.

> 🧠 **Antes de teclear**, decide qué estructura usarás y por qué.
> La elección de estructura ES parte de la solución.
"""),

code(r"""
import os, sys
sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar
print("Listo. Usa revisar(nombre, condicion) para comprobar tus respuestas.")
"""),
]


def ejercicio(numero, titulo, enunciado_md, plantilla, check_code, solucion_md):
    C.append(md("## Ejercicio {} · {}\n\n{}".format(numero, titulo, enunciado_md)))
    C.append(code(plantilla))
    C.append(code(check_code))
    C.append(md(solucion_md))


# ---- 1 --------------------------------------------------------------------
ejercicio(
    1, "Contador de frecuencia de palabras (dict)",
    r"""Escribe `contar_palabras(texto)` que reciba un string y devuelva un
`dict` con la frecuencia de cada palabra.

**Ejemplo:**
`contar_palabras("hola mundo hola")` → `{"hola": 2, "mundo": 1}`

Las palabras ya llegan en minúsculas y sin puntuación.""",
    r"""
def contar_palabras(texto):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("hola mundo hola", contar_palabras("hola mundo hola") == {"hola": 2, "mundo": 1})
revisar("una sola palabra", contar_palabras("python") == {"python": 1})
revisar("tres palabras distintas",
        contar_palabras("a b c") == {"a": 1, "b": 1, "c": 1})
revisar("palabra triple",
        contar_palabras("si si si") == {"si": 3})
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def contar_palabras(texto):
    conteo = {}
    for palabra in texto.split():
        conteo[palabra] = conteo.get(palabra, 0) + 1
    return conteo
```
Patrón contador clásico: `d.get(k, 0) + 1`. Una sola pasada → O(n).
</details>
""",
)

# ---- 2 --------------------------------------------------------------------
ejercicio(
    2, "Invertir un diccionario (comprensión de dict)",
    r"""Escribe `invertir_dict(d)` que devuelva un nuevo dict donde las claves
son los valores originales y los valores son las claves originales.

**Ejemplo:**
`invertir_dict({"BOG": "Bogota", "CLO": "Cali"})` → `{"Bogota": "BOG", "Cali": "CLO"}`

Puedes asumir que todos los valores son únicos.""",
    r"""
def invertir_dict(d):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("codigos a ciudades",
        invertir_dict({"BOG": "Bogota", "CLO": "Cali"}) == {"Bogota": "BOG", "Cali": "CLO"})
revisar("dict de un elemento",
        invertir_dict({"a": 1}) == {1: "a"})
revisar("dict vacio",
        invertir_dict({}) == {})
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def invertir_dict(d):
    return {v: k for k, v in d.items()}
```
Comprensión de diccionario en una línea: intercambia claves y valores.
</details>
""",
)

# ---- 3 --------------------------------------------------------------------
ejercicio(
    3, "N-ésimo elemento único (set + sorted)",
    r"""Escribe `enesimo_unico(lista, n)` que devuelva el **n-ésimo elemento
único** de la lista, ordenados de menor a mayor. `n` comienza en 1.

**Ejemplo:**
`enesimo_unico([3, 1, 4, 1, 5, 9, 2, 6, 5], 3)` → `4`
(los únicos ordenados son `[1, 2, 3, 4, 5, 6, 9]`, el 3.º es `4`)""",
    r"""
def enesimo_unico(lista, n):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("ejemplo base", enesimo_unico([3, 1, 4, 1, 5, 9, 2, 6, 5], 3) == 4)
revisar("primer unico", enesimo_unico([5, 3, 1, 3, 5], 1) == 1)
revisar("todos distintos", enesimo_unico([10, 20, 30], 2) == 20)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def enesimo_unico(lista, n):
    unicos = sorted(set(lista))
    return unicos[n - 1]
```
`set(lista)` deduplica; `sorted()` ordena; indexamos con `n - 1` porque n empieza en 1.
</details>
""",
)

# ---- 4 --------------------------------------------------------------------
ejercicio(
    4, "Agrupar ventas por ciudad (dict de listas)",
    r"""Escribe `agrupar_por_ciudad(ventas)` que reciba una lista de dicts con
claves `"ciudad"` y `"monto"`, y devuelva un dict donde cada clave es una
ciudad y el valor es la lista de montos de esa ciudad.

**Ejemplo:**
```python
ventas = [{"ciudad": "Bogota", "monto": 100},
          {"ciudad": "Cali",   "monto": 200},
          {"ciudad": "Bogota", "monto": 150}]
agrupar_por_ciudad(ventas)
# -> {"Bogota": [100, 150], "Cali": [200]}
```""",
    r"""
def agrupar_por_ciudad(ventas):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
ventas_test = [
    {"ciudad": "Bogota", "monto": 100},
    {"ciudad": "Cali",   "monto": 200},
    {"ciudad": "Bogota", "monto": 150},
]
resultado = agrupar_por_ciudad(ventas_test)
revisar("montos Bogota", sorted(resultado.get("Bogota", [])) == [100, 150])
revisar("montos Cali",   resultado.get("Cali") == [200])
revisar("solo dos ciudades", set(resultado.keys()) == {"Bogota", "Cali"})

# Lista vacia
revisar("lista vacia", agrupar_por_ciudad([]) == {})
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def agrupar_por_ciudad(ventas):
    grupos = {}
    for v in ventas:
        ciudad = v["ciudad"]
        if ciudad not in grupos:
            grupos[ciudad] = []
        grupos[ciudad].append(v["monto"])
    return grupos
```
O con `setdefault`:
```python
def agrupar_por_ciudad(ventas):
    grupos = {}
    for v in ventas:
        grupos.setdefault(v["ciudad"], []).append(v["monto"])
    return grupos
```
</details>
""",
)

# ---- 5 --------------------------------------------------------------------
ejercicio(
    5, "Clasificar temperaturas con comprensión de dict",
    r"""Escribe `clasificar_temperaturas(temps)` que reciba una lista de
temperaturas (números) y devuelva un dict `{temperatura: clasificacion}`.

Clasificación:
- `< 10`: `"frio"`
- `10 <= t < 25`: `"templado"`
- `>= 25`: `"calido"`

**Ejemplo:**
`clasificar_temperaturas([5, 15, 30])` → `{5: "frio", 15: "templado", 30: "calido"}`""",
    r"""
def clasificar_temperaturas(temps):
    # ✏️ TU CÓDIGO AQUÍ (usa comprensión de dict)
    return None
""",
    r"""
revisar("tres categorias",
        clasificar_temperaturas([5, 15, 30]) == {5: "frio", 15: "templado", 30: "calido"})
revisar("bordes exactos",
        clasificar_temperaturas([10, 25]) == {10: "templado", 25: "calido"})
revisar("lista vacia",
        clasificar_temperaturas([]) == {})
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def clasificar_temperaturas(temps):
    def cat(t):
        if t < 10:
            return "frio"
        elif t < 25:
            return "templado"
        else:
            return "calido"
    return {t: cat(t) for t in temps}
```
</details>
""",
)

# ---- 6 --------------------------------------------------------------------
ejercicio(
    6, "Intersección de listas de clientes (set)",
    r"""Escribe `clientes_comunes(lista_a, lista_b)` que devuelva una **lista**
(no set) con los ids de clientes que aparecen en **ambas** listas, ordenada.

**Ejemplo:**
`clientes_comunes([1, 2, 3, 4], [3, 4, 5, 6])` → `[3, 4]`""",
    r"""
def clientes_comunes(lista_a, lista_b):
    # ✏️ TU CÓDIGO AQUÍ (usa operaciones de set)
    return None
""",
    r"""
revisar("ejemplo base", clientes_comunes([1, 2, 3, 4], [3, 4, 5, 6]) == [3, 4])
revisar("sin comunes",  clientes_comunes([1, 2], [3, 4]) == [])
revisar("todos comunes",clientes_comunes([1, 2], [2, 1]) == [1, 2])
revisar("lista vacia",  clientes_comunes([], [1, 2]) == [])
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def clientes_comunes(lista_a, lista_b):
    return sorted(set(lista_a) & set(lista_b))
```
`&` es la intersección; `sorted()` garantiza el orden para la comparación.
</details>
""",
)

# ---- 7 --------------------------------------------------------------------
ejercicio(
    7, "Filtrar por precio en lista de tuplas",
    r"""Escribe `filtrar_por_precio(productos, precio_max)` que reciba una lista
de tuplas `(nombre, precio)` y devuelva solo las tuplas cuyo precio sea
**menor o igual** a `precio_max`.

**Ejemplo:**
```python
productos = [("laptop", 3_000_000), ("teclado", 150_000), ("mouse", 80_000)]
filtrar_por_precio(productos, 200_000)
# -> [("teclado", 150_000), ("mouse", 80_000)]
```""",
    r"""
def filtrar_por_precio(productos, precio_max):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
prods = [("laptop", 3_000_000), ("teclado", 150_000), ("mouse", 80_000)]
revisar("dos productos", filtrar_por_precio(prods, 200_000) == [("teclado", 150_000), ("mouse", 80_000)])
revisar("todos pasan",   filtrar_por_precio(prods, 5_000_000) == prods)
revisar("ninguno pasa",  filtrar_por_precio(prods, 50_000) == [])
revisar("lista vacia",   filtrar_por_precio([], 100_000) == [])
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def filtrar_por_precio(productos, precio_max):
    return [(nombre, precio) for nombre, precio in productos if precio <= precio_max]
```
Desempaquetamos la tupla directamente en la comprensión para mayor legibilidad.
</details>
""",
)

# ---- 8 --------------------------------------------------------------------
ejercicio(
    8, "Tabla de conteos anidados: ciudad × categoría",
    r"""Escribe `conteo_anidado(transacciones)` que reciba una lista de dicts
con claves `"ciudad"` y `"categoria"`, y devuelva un dict
`{ciudad: {categoria: total_transacciones}}`.

**Ejemplo:**
```python
transacciones = [
    {"ciudad": "Bogota", "categoria": "tecnologia"},
    {"ciudad": "Bogota", "categoria": "tecnologia"},
    {"ciudad": "Cali",   "categoria": "hogar"},
]
conteo_anidado(transacciones)
# -> {"Bogota": {"tecnologia": 2}, "Cali": {"hogar": 1}}
```""",
    r"""
def conteo_anidado(transacciones):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
txs = [
    {"ciudad": "Bogota", "categoria": "tecnologia"},
    {"ciudad": "Bogota", "categoria": "tecnologia"},
    {"ciudad": "Cali",   "categoria": "hogar"},
    {"ciudad": "Bogota", "categoria": "hogar"},
]
res = conteo_anidado(txs)
revisar("Bogota tecnologia = 2", res.get("Bogota", {}).get("tecnologia") == 2)
revisar("Bogota hogar = 1",      res.get("Bogota", {}).get("hogar") == 1)
revisar("Cali hogar = 1",        res.get("Cali", {}).get("hogar") == 1)
revisar("lista vacia",           conteo_anidado([]) == {})
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def conteo_anidado(transacciones):
    tabla = {}
    for t in transacciones:
        c = t["ciudad"]
        k = t["categoria"]
        if c not in tabla:
            tabla[c] = {}
        tabla[c][k] = tabla[c].get(k, 0) + 1
    return tabla
```
O con setdefault:
```python
def conteo_anidado(transacciones):
    tabla = {}
    for t in transacciones:
        tabla.setdefault(t["ciudad"], {})[t["categoria"]] = \
            tabla.setdefault(t["ciudad"], {}).get(t["categoria"], 0) + 1
    return tabla
```
La primera versión es más clara.
</details>
""",
)

# ---- 9 --------------------------------------------------------------------
ejercicio(
    9, "Eliminar duplicados preservando orden original",
    r"""Escribe `deduplicar(lista)` que devuelva una nueva lista con los
elementos únicos de `lista`, **en el orden de su primera aparición**.

**Ejemplo:**
`deduplicar([3, 1, 4, 1, 5, 9, 2, 6, 5])` → `[3, 1, 4, 5, 9, 2, 6]`

*Nota:* `set(lista)` no garantiza el orden original; necesitas otra estrategia.""",
    r"""
def deduplicar(lista):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("ejemplo base",    deduplicar([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [3, 1, 4, 5, 9, 2, 6])
revisar("sin duplicados",  deduplicar([1, 2, 3]) == [1, 2, 3])
revisar("todos iguales",   deduplicar([7, 7, 7]) == [7])
revisar("lista vacia",     deduplicar([]) == [])
revisar("strings",         deduplicar(["a", "b", "a", "c"]) == ["a", "b", "c"])
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def deduplicar(lista):
    vistos = set()
    resultado = []
    for x in lista:
        if x not in vistos:
            resultado.append(x)
            vistos.add(x)
    return resultado
```
`x not in vistos` es O(1) porque `vistos` es un `set`. Sin el set, cada
comprobación sería O(n) y el total sería O(n²).
</details>
""",
)

# ---- 10 -------------------------------------------------------------------
ejercicio(
    10, "Comparar rendimiento set vs list para búsqueda",
    r"""Escribe `busqueda_set(coleccion, objetivo)` que use un `set` para la
búsqueda, y `busqueda_list(coleccion, objetivo)` que use la lista directamente.

Ambas devuelven `True` si `objetivo` está en `coleccion`, `False` si no.
El objetivo NO es medir tiempo aquí — es reconocer la diferencia de estructura.

**Ejemplo:**
`busqueda_set([1, 2, 3], 2)` → `True`
`busqueda_list([1, 2, 3], 9)` → `False`""",
    r"""
def busqueda_set(coleccion, objetivo):
    # ✏️ TU CÓDIGO AQUÍ (convierte coleccion a set)
    return None

def busqueda_list(coleccion, objetivo):
    # ✏️ TU CÓDIGO AQUÍ (busca directamente en la lista)
    return None
""",
    r"""
revisar("set: encuentra",     busqueda_set([1, 2, 3], 2) is True)
revisar("set: no encuentra",  busqueda_set([1, 2, 3], 9) is False)
revisar("list: encuentra",    busqueda_list([1, 2, 3], 2) is True)
revisar("list: no encuentra", busqueda_list([1, 2, 3], 9) is False)
revisar("set: lista vacia",   busqueda_set([], 1) is False)
revisar("list: lista vacia",  busqueda_list([], 1) is False)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def busqueda_set(coleccion, objetivo):
    return objetivo in set(coleccion)

def busqueda_list(coleccion, objetivo):
    return objetivo in coleccion
```

Ambas dan la misma respuesta. La diferencia está en el costo:
- `objetivo in set(coleccion)`: O(n) para construir el set, luego O(1) para buscar.
  Si vas a hacer MUCHAS búsquedas, construye el set una vez fuera de la función.
- `objetivo in coleccion`: O(n) cada vez.

Para una sola búsqueda, la versión con lista es suficiente. Para N búsquedas,
convierte a set una vez y busca N veces en O(1) cada una.
</details>
""",
)

C.append(md(r"""
---
## ¡Terminaste la práctica 01!

Si todas tus comprobaciones muestran ✅, dominas los patrones clave de la clase:
**contador con dict, comprensiones, set para deduplicar e intersectar,
dict de listas para agrupar, y la importancia de elegir la estructura correcta**.

➡️ Continúa con **practice02.ipynb**, donde aplicaremos estas estructuras al
análisis de transacciones reales.
"""))


# ===================================================================== #
# VALIDACIÓN EN TIEMPO DE CONSTRUCCIÓN
# ===================================================================== #
def _validar():
    def contar_palabras(texto):
        conteo = {}
        for p in texto.split():
            conteo[p] = conteo.get(p, 0) + 1
        return conteo
    assert contar_palabras("hola mundo hola") == {"hola": 2, "mundo": 1}
    assert contar_palabras("python") == {"python": 1}

    def invertir_dict(d):
        return {v: k for k, v in d.items()}
    assert invertir_dict({"BOG": "Bogota", "CLO": "Cali"}) == {"Bogota": "BOG", "Cali": "CLO"}
    assert invertir_dict({}) == {}

    def enesimo_unico(lista, n):
        return sorted(set(lista))[n - 1]
    assert enesimo_unico([3, 1, 4, 1, 5, 9, 2, 6, 5], 3) == 4
    assert enesimo_unico([5, 3, 1, 3, 5], 1) == 1

    def agrupar_por_ciudad(ventas):
        grupos = {}
        for v in ventas:
            grupos.setdefault(v["ciudad"], []).append(v["monto"])
        return grupos
    ventas_test = [{"ciudad": "Bogota", "monto": 100},
                   {"ciudad": "Cali",   "monto": 200},
                   {"ciudad": "Bogota", "monto": 150}]
    res = agrupar_por_ciudad(ventas_test)
    assert sorted(res["Bogota"]) == [100, 150]
    assert res["Cali"] == [200]
    assert agrupar_por_ciudad([]) == {}

    def clasificar_temperaturas(temps):
        def cat(t):
            if t < 10: return "frio"
            elif t < 25: return "templado"
            else: return "calido"
        return {t: cat(t) for t in temps}
    assert clasificar_temperaturas([5, 15, 30]) == {5: "frio", 15: "templado", 30: "calido"}
    assert clasificar_temperaturas([10, 25]) == {10: "templado", 25: "calido"}
    assert clasificar_temperaturas([]) == {}

    def clientes_comunes(lista_a, lista_b):
        return sorted(set(lista_a) & set(lista_b))
    assert clientes_comunes([1, 2, 3, 4], [3, 4, 5, 6]) == [3, 4]
    assert clientes_comunes([1, 2], [3, 4]) == []
    assert clientes_comunes([], [1, 2]) == []

    def filtrar_por_precio(productos, precio_max):
        return [(n, p) for n, p in productos if p <= precio_max]
    prods = [("laptop", 3_000_000), ("teclado", 150_000), ("mouse", 80_000)]
    assert filtrar_por_precio(prods, 200_000) == [("teclado", 150_000), ("mouse", 80_000)]
    assert filtrar_por_precio(prods, 50_000) == []
    assert filtrar_por_precio([], 100_000) == []

    def conteo_anidado(transacciones):
        tabla = {}
        for t in transacciones:
            c = t["ciudad"]
            k = t["categoria"]
            if c not in tabla:
                tabla[c] = {}
            tabla[c][k] = tabla[c].get(k, 0) + 1
        return tabla
    txs = [{"ciudad": "Bogota", "categoria": "tecnologia"},
           {"ciudad": "Bogota", "categoria": "tecnologia"},
           {"ciudad": "Cali",   "categoria": "hogar"},
           {"ciudad": "Bogota", "categoria": "hogar"}]
    res = conteo_anidado(txs)
    assert res["Bogota"]["tecnologia"] == 2
    assert res["Bogota"]["hogar"] == 1
    assert res["Cali"]["hogar"] == 1
    assert conteo_anidado([]) == {}

    def deduplicar(lista):
        vistos = set()
        resultado = []
        for x in lista:
            if x not in vistos:
                resultado.append(x)
                vistos.add(x)
        return resultado
    assert deduplicar([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [3, 1, 4, 5, 9, 2, 6]
    assert deduplicar([]) == []
    assert deduplicar([7, 7, 7]) == [7]

    def busqueda_set(coleccion, objetivo):
        return objetivo in set(coleccion)
    def busqueda_list(coleccion, objetivo):
        return objetivo in coleccion
    assert busqueda_set([1, 2, 3], 2) is True
    assert busqueda_set([1, 2, 3], 9) is False
    assert busqueda_list([1, 2, 3], 2) is True
    assert busqueda_list([], 1) is False

    print("✔ Todas las soluciones de referencia de practice01 (clase04) pasan sus pruebas.")

_validar()


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase04", "practice01.ipynb")
build(os.path.abspath(ruta), C)
