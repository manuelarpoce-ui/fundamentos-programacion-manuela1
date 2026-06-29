"""Construye curso/clase04/lecture.ipynb — Estructuras de datos Python."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []


# ===================================================================== #
# 0. PORTADA Y AGENDA
# ===================================================================== #
C += [
md(r"""
# Clase 4 · Estructuras de datos Python

### Fundamentos de Programación para Ciencia de Datos

> *"Los datos estructurados son la diferencia entre tener información y poder usarla."*

---

**Duración:** 3 horas · **Modalidad:** notebook interactivo

En las clases anteriores trabajamos con valores sueltos y listas simples.
Hoy damos el salto a las **cuatro estructuras de datos fundamentales de Python**:
`list`, `tuple`, `dict` y `set`. Cada una resuelve un problema diferente con una
eficiencia diferente — y elegir la correcta separa el código que funciona del
código que *escala*.

Al final de esta clase podrás responder con seguridad:

- ¿Por qué un diccionario encuentra una clave en tiempo constante?
- ¿Cuándo usar una tupla en lugar de una lista?
- ¿Cómo deduplicar 10 millones de registros sin un bucle explícito?
- ¿Cómo construir un índice invertido —como el de Google— con 5 líneas?
"""),

md(r"""
## Mapa de la clase

| Bloque | Tiempo | Contenido |
|---|---|---|
| 1. Motivación | 15 min | Por qué necesitamos estructuras distintas |
| 2. Lista (`list`) | 20 min | Repaso, slicing avanzado, métodos clave |
| 3. Comprensiones de lista | 20 min | Sintaxis, condición, anidadas |
| 4. Tupla (`tuple`) | 20 min | Inmutabilidad, desempaquetado, uso como clave |
| 5. Diccionario (`dict`) | 30 min | Hash table, métodos, O(1) en promedio |
| 6. Comprensiones de dict | 15 min | Transformar y filtrar dicts |
| 7. Conjunto (`set`) | 20 min | Sin orden, sin duplicados, operaciones |
| 8. Comprensiones de set | 10 min | |
| 9. ¿Cuándo usar qué? | 15 min | Tabla comparativa con criterios de decisión |
| 10. Patrones algorítmicos | 20 min | Agrupar, deduplicar, índice invertido |
| 11. Anidamiento | 15 min | dict de listas, list de dicts |
| 12. Errores comunes | 10 min | |
| 13. Resumen, quiz y retos | 10 min | |

> 🧭 **Cómo usar este notebook:** lee cada celda de texto antes de ejecutar el
> código. Detente en cada bloque **🤔 ¿Qué pasaría si...?** e intenta responder
> mentalmente antes de seguir.
"""),
]


# ===================================================================== #
# 1. MOTIVACIÓN
# ===================================================================== #
C += [
md(r"""
## 1. Motivación: ¿por qué existen cuatro estructuras?

Imagina que eres analista en una empresa de logística con 50.000 envíos
registrados. Recibes tres preguntas distintas:

1. **"¿Cuántos envíos llegaron hoy?"** — necesitas *contar* elementos.
2. **"¿Cuánto pagó el cliente 1042?"** — necesitas *buscar por clave*.
3. **"¿Qué clientes compraron en ambas ciudades?"** — necesitas *intersección*.

Con solo listas podrías resolver las tres... pero la pregunta 2 implicaría
recorrer los 50.000 registros uno a uno (O(n)). Con un diccionario, la
respuesta llega en tiempo constante (O(1) promedio). Con un conjunto, la
intersección de dos listas es una línea.

**Las estructuras de datos no son capricho de diseño: son elecciones de eficiencia.**

```
  PROBLEMA                ESTRUCTURA IDEAL
  ──────────────────────────────────────────
  colección ordenada       list
  registro inmutable       tuple
  búsqueda por clave       dict
  pertenencia / unicidad   set
```
"""),

md(r"""
### El costo de elegir mal

Con 50.000 clientes, buscar uno a uno es:
- **Búsqueda en lista:** O(n) → hasta 50.000 comparaciones.
- **Búsqueda en dict:** O(1) promedio → 1 operación.

Ejecutemos esta diferencia de forma concreta:
"""),

code(r"""
import time

# Preparamos datos de prueba: 50.000 ids de cliente
clientes_lista = list(range(50_000))
clientes_dict  = {i: True for i in range(50_000)}

objetivo = 49_999   # el peor caso para la lista

# Búsqueda en lista — O(n)
t0 = time.perf_counter()
for _ in range(1000):
    resultado = objetivo in clientes_lista
t1 = time.perf_counter()
tiempo_lista = (t1 - t0) * 1000  # ms

# Búsqueda en dict — O(1) promedio
t2 = time.perf_counter()
for _ in range(1000):
    resultado = objetivo in clientes_dict
t3 = time.perf_counter()
tiempo_dict = (t3 - t2) * 1000  # ms

print("Buscar el elemento 49.999 (1000 veces):")
print("  lista  : {:.3f} ms".format(tiempo_lista))
print("  dict   : {:.3f} ms".format(tiempo_dict))
print("  factor : {:.0f}x mas rapido con dict".format(tiempo_lista / max(tiempo_dict, 0.001)))
"""),

md(r"""
El diccionario no es marginalmente más rápido: es **órdenes de magnitud** más
rápido. Esa diferencia se multiplica cuando los datos son millones.

Antes de entrar a cada estructura, tengamos el panorama completo:

| Estructura | Ordenada | Mutable | Duplicados | Clave de acceso |
|---|---|---|---|---|
| `list` | sí | sí | sí | índice entero |
| `tuple` | sí | **no** | sí | índice entero |
| `dict` | sí* | sí | no en clave | clave arbitraria |
| `set` | no | sí | **no** | (no se accede por índice) |

*desde Python 3.7, los dicts mantienen orden de inserción.
"""),
]


# ===================================================================== #
# 2. LISTA
# ===================================================================== #
C += [
md(r"""
## 2. Lista (`list`): repaso y slicing avanzado

La lista es la estructura más versátil de Python. Ya la conoces — hoy nos
enfocamos en las operaciones que los principiantes suelen no aprovechar.

### Slicing avanzado: `lista[inicio:fin:paso]`

```
  ventas = [100, 200, 300, 400, 500, 600]
  índices:   0    1    2    3    4    5

  ventas[1:4]    →  [200, 300, 400]      # desde 1 hasta 3
  ventas[::2]    →  [100, 300, 500]      # cada dos elementos
  ventas[::-1]   →  [600, 500, 400, 300, 200, 100]  # invertida
  ventas[-3:]    →  [400, 500, 600]      # los últimos 3
```
"""),

code(r"""
ventas = [100, 200, 300, 400, 500, 600]

print("ventas[1:4]  =", ventas[1:4])    # desde índice 1 hasta 3
print("ventas[::2]  =", ventas[::2])    # de dos en dos
print("ventas[::-1] =", ventas[::-1])   # invertida
print("ventas[-3:]  =", ventas[-3:])    # ultimos tres

# Slicing de columnas en una tabla (lista de listas)
tabla = [[1, "Bogota", 50000],
         [2, "Cali",   30000],
         [3, "Bogota", 80000]]
montos = [fila[2] for fila in tabla]    # columna de montos
print("montos:", montos)
"""),

md(r"""
### Métodos clave de lista

| Método | Qué hace | Costo |
|---|---|---|
| `.append(x)` | agrega al final | O(1) amortizado |
| `.insert(i, x)` | inserta en posición `i` | O(n) |
| `.pop()` | elimina y devuelve el último | O(1) |
| `.pop(i)` | elimina y devuelve el de índice `i` | O(n) |
| `.remove(x)` | elimina la primera ocurrencia de `x` | O(n) |
| `.sort()` | ordena *in place* | O(n log n) |
| `.index(x)` | posición de `x` | O(n) |
| `.count(x)` | cuántas veces aparece `x` | O(n) |

> **Trampa frecuente:** `.insert(0, x)` es O(n) porque desplaza todos los
> elementos. Para agregar al principio de forma eficiente, usa `collections.deque`.
"""),

code(r"""
# Demostración de métodos clave con datos de logística
envios = [1004, 1079, 1067, 1063, 1105]

envios.append(1200)                # llega nuevo envio
print("tras append(1200):", envios)

envios.insert(2, 1050)             # insertar en posición 2
print("tras insert(2, 1050):", envios)

ultimo = envios.pop()              # sacar el último
print("pop() devolvio:", ultimo, "| lista:", envios)

envios.sort()
print("ordenada:", envios)

print("count(1063):", envios.count(1063))   # cuantas veces aparece
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- Tienes una lista de 100.000 transacciones y necesitas verificar si el id 99999
  ya fue procesado. ¿`id in lista` o `id in conjunto`? ¿Por qué?
- ¿Qué devuelve `ventas[-1]`? ¿Y `ventas[-2:]`?
"""),
]


# ===================================================================== #
# 3. COMPRENSIONES DE LISTA
# ===================================================================== #
C += [
md(r"""
## 3. Comprensiones de lista

Las **comprensiones** son la forma pythónica de construir listas a partir de
otras colecciones. Reemplazan bucles verbosos por expresiones declarativas.

### Anatomía de una comprensión

```
  [expresion  for  variable  in  iterable  if  condicion]
      │              │              │              │
   qué poner    nombre local     de dónde     filtro (opcional)
```

**Equivalencia:**
```python
# Bucle clásico:
resultado = []
for x in iterable:
    if condicion:
        resultado.append(expresion)

# Comprensión equivalente:
resultado = [expresion for x in iterable if condicion]
```
"""),

code(r"""
precios = [120_000, 89_000, 240_000, 56_000, 310_000, 45_000, 180_000]

# Aplicar descuento del 10% a todos los precios
con_descuento = [p * 0.9 for p in precios]
print("con descuento:", [int(x) for x in con_descuento])

# Solo los precios mayores a $100.000
caros = [p for p in precios if p > 100_000]
print("caros (>100k):", caros)

# Clasificar cada precio como 'alto' o 'normal'
etiquetas = ["alto" if p > 150_000 else "normal" for p in precios]
print("etiquetas:", etiquetas)

# Extraer ciudades de una lista de dicts (patrón muy común en data)
transacciones = [
    {"ciudad": "Bogota", "monto": 50_000},
    {"ciudad": "Cali",   "monto": 80_000},
    {"ciudad": "Bogota", "monto": 120_000},
]
ciudades = [t["ciudad"] for t in transacciones]
print("ciudades:", ciudades)
"""),

md(r"""
### Comprensiones anidadas

Puedes anidar `for` dentro de una comprensión para "aplanar" estructuras:

```python
# Equivale a: for fila in matriz: for x in fila: resultado.append(x)
plana = [x for fila in matriz for x in fila]
```

Con moderación: si la comprensión necesita más de dos `for`, probablemente
es más legible como bucle explícito.
"""),

code(r"""
# Aplanar una tabla de ventas (lista de listas) en una lista plana
tabla_ventas = [[1000, 2000], [3000, 4000], [5000, 6000]]

plana = [v for fila in tabla_ventas for v in fila]
print("plana:", plana)

# Pares (ciudad, categoria) de todas las combinaciones
ciudades_validas = ["Bogota", "Cali"]
categorias = ["tecnologia", "hogar"]
pares = [(c, k) for c in ciudades_validas for k in categorias]
print("pares (ciudad, categoria):")
for par in pares:
    print(" ", par)
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

¿Qué devuelve esta comprensión?
```python
[x**2 for x in range(5) if x % 2 == 0]
```
Respóndelo en papel y luego verifica ejecutando la celda.
"""),

code(r"""
# Verifica tu respuesta:
resultado = [x**2 for x in range(5) if x % 2 == 0]
print(resultado)
# ¿Es lo que esperabas?
"""),
]


# ===================================================================== #
# 4. TUPLA
# ===================================================================== #
C += [
md(r"""
## 4. Tupla (`tuple`): inmutabilidad con propósito

Una tupla parece una lista con paréntesis, pero su diferencia esencial es la
**inmutabilidad**: una vez creada, no se puede modificar.

```
  lista  = [1, 2, 3]    # se puede cambiar
  tupla  = (1, 2, 3)    # no se puede cambiar
```

### ¿Por qué querríamos algo inmutable?

1. **Claridad semántica:** una tupla dice "estos valores van juntos y no
   cambian". Una coordenada GPS `(lat, lon)`, un par `(nombre, nota)`,
   los datos de un producto `(id, precio, stock)`.

2. **Seguridad:** impide modificaciones accidentales en datos que no deberían
   cambiar (fechas de transacción, ids).

3. **Hashable:** las tuplas se pueden usar como **clave de diccionario** o
   como elemento de un conjunto. Las listas no.

4. **Ligeramente más eficiente** en memoria y acceso que las listas.
"""),

code(r"""
# Tupla como registro inmutable
producto = ("laptop", 2_500_000, 15)   # (nombre, precio, stock)
nombre, precio, stock = producto        # desempaquetado

print("nombre:", nombre)
print("precio:", precio)
print("stock :", stock)

# Intentar modificar una tupla genera error (descomenta para verlo):
# producto[1] = 3_000_000   # TypeError: 'tuple' object does not support item assignment

# Tupla como clave de diccionario (una lista NO puede serlo)
ventas_por_zona = {}
ventas_por_zona[("Bogota", "tecnologia")] = 450_000
ventas_por_zona[("Cali",   "tecnologia")] = 310_000
ventas_por_zona[("Bogota", "hogar")]      = 280_000

print("\nventas por zona:")
for zona, total in ventas_por_zona.items():
    print("  {} -> ${}".format(zona, total))
"""),

md(r"""
### Desempaquetado de tuplas

```python
# Desempaquetado clásico
punto = (3.5, -1.2)
x, y = punto

# En bucles (patrón muy común)
registros = [("Ana", 4.5), ("Luis", 3.0), ("Sara", 4.8)]
for nombre, nota in registros:
    print(nombre, "->", nota)

# Desempaquetado extendido con *
primero, *resto = (1, 2, 3, 4, 5)
# primero = 1, resto = [2, 3, 4, 5]
```
"""),

code(r"""
# Desempaquetado en bucle — patrón clásico de data science
registros = [
    ("Ana",  4.5, "Bogota"),
    ("Luis", 3.0, "Cali"),
    ("Sara", 4.8, "Bogota"),
]

print("Registros aprobados (nota >= 4.0):")
for nombre, nota, ciudad in registros:
    if nota >= 4.0:
        print("  {} ({}): {:.1f}".format(nombre, ciudad, nota))

# Desempaquetado extendido
primero, *medio, ultimo = (10, 20, 30, 40, 50)
print("\nprimero:", primero)
print("medio  :", medio)
print("ultimo :", ultimo)
"""),

md(r"""
### Trazado: mutabilidad vs. inmutabilidad

```
  lista  = [1, 2, 3]
  tupla  = (1, 2, 3)

  lista[0] = 99  →  lista = [99, 2, 3]  ✔
  tupla[0] = 99  →  TypeError           ✘
```

### 🤔 ¿Qué pasaría si...?

Tienes una función que recibe las coordenadas de un almacén y calcula la
ruta de entrega. ¿Usarías `list` o `tuple` para pasar las coordenadas?
¿Por qué? ¿Qué riesgo evitarías?
"""),
]


# ===================================================================== #
# 5. DICCIONARIO
# ===================================================================== #
C += [
md(r"""
## 5. Diccionario (`dict`): clave → valor en tiempo constante

El diccionario es probablemente la estructura más poderosa de Python.
Detrás de su interfaz simple se esconde una **tabla hash**, la estructura
de datos que hace posible la búsqueda en O(1) promedio.

### ¿Cómo funciona una tabla hash? (intuición)

```
  Queremos guardar:  "Bogota" → 450000

  1. Python calcula hash("Bogota")  →  un número entero grande
  2. Ese número determina el "cajón" (bucket) donde guardar el valor
  3. Para buscar "Bogota", se recalcula el hash → se va directo al cajón

  No hay recorrido: sabemos exactamente dónde está. → O(1) promedio
```

Diagrama ASCII:

```
  clave         hash(clave) % N    cajón    valor
  ─────────     ───────────────    ─────    ─────
  "Bogota"   →       3          →  [3]   →  450000
  "Cali"     →       7          →  [7]   →  310000
  "Medellin" →       1          →  [1]   →  280000
```
"""),

code(r"""
# Crear y acceder a diccionarios
ventas = {
    "Bogota":      450_000,
    "Cali":        310_000,
    "Medellin":    280_000,
    "Barranquilla": 190_000,
    "Bucaramanga": 150_000,
}

# Acceso por clave — O(1)
print("Bogota:", ventas["Bogota"])

# Acceso seguro con .get (devuelve None si no existe, sin error)
print("Cartagena:", ventas.get("Cartagena"))         # None
print("Cartagena:", ventas.get("Cartagena", 0))      # valor por defecto

# Agregar y modificar
ventas["Pereira"] = 120_000    # nueva clave
ventas["Bogota"]  += 50_000    # actualizar
print("\nventas actualizadas:", ventas)
"""),

md(r"""
### Métodos clave de diccionario

| Método / operación | Qué devuelve | Uso típico |
|---|---|---|
| `d[k]` | valor de `k` (error si no existe) | acceso directo |
| `d.get(k, default)` | valor o `default` | acceso seguro |
| `d[k] = v` | — | insertar / actualizar |
| `k in d` | `True/False` | verificar existencia, O(1) |
| `d.keys()` | vista de claves | iterar claves |
| `d.values()` | vista de valores | iterar valores |
| `d.items()` | vista de pares `(k, v)` | iterar pares |
| `d.pop(k)` | elimina y devuelve `v` | eliminar clave |
| `d.update(otro)` | — | fusionar dicts |
| `d.setdefault(k, v)` | valor actual o `v` si nuevo | inicializar |
"""),

code(r"""
inventario = {"laptop": 15, "teclado": 45, "monitor": 8}

# Iterar sobre pares clave-valor
print("Inventario:")
for producto, stock in inventario.items():
    print("  {:<12} {}".format(producto, stock))

# Verificar existencia en O(1)
buscar = "laptop"
if buscar in inventario:
    print("\n{} tiene {} unidades".format(buscar, inventario[buscar]))

# setdefault: inicializa si la clave no existe
conteo = {}
palabras = ["hola", "mundo", "hola", "python", "mundo", "mundo"]
for p in palabras:
    conteo[p] = conteo.get(p, 0) + 1     # patrón de conteo clásico
print("\nconteo:", conteo)
"""),

md(r"""
### El patrón contador: `d.get(k, 0) + 1`

Este patrón aparece en toda la ciencia de datos:

```python
conteo = {}
for item in coleccion:
    conteo[item] = conteo.get(item, 0) + 1
```

Es el equivalente eficiente de la moda que en la Clase 1 hacíamos con
dos bucles anidados (O(n²)). Con un diccionario: **O(n)**.

### 🤔 ¿Qué pasaría si...?

¿Qué pasa si haces `d["clave_que_no_existe"]` sin `.get()`?
¿Y si iteras un dict mientras lo modificas?
"""),

code(r"""
# Error clásico: acceder a clave inexistente
d = {"a": 1}
# d["b"]    # KeyError: 'b'  — descomenta para verlo

# Forma segura:
print(d.get("b", "no existe"))   # no explota

# Error grave: modificar un dict mientras se itera
# (descomenta para ver el RuntimeError)
# for k in d:
#     d[k + "_copia"] = d[k]   # RuntimeError: dictionary changed size during iteration

# Forma correcta: iterar sobre una copia de las claves
d = {"a": 1, "b": 2}
for k in list(d.keys()):          # list() hace una copia
    d[k + "_v2"] = d[k] * 10
print("d con copias:", d)
"""),
]


# ===================================================================== #
# 6. COMPRENSIONES DE DICCIONARIO
# ===================================================================== #
C += [
md(r"""
## 6. Comprensiones de diccionario

Al igual que las comprensiones de lista, las de diccionario permiten construir
dicts de forma concisa.

### Anatomía

```python
{clave_expr: valor_expr for variable in iterable if condicion}
```

**Caso de uso típico:** transformar o filtrar un dict existente.
"""),

code(r"""
precios = {"laptop": 2_500_000, "teclado": 120_000, "monitor": 800_000, "mouse": 80_000}

# Aplicar IVA del 19% a todos los productos
con_iva = {producto: int(precio * 1.19) for producto, precio in precios.items()}
print("con IVA:", con_iva)

# Solo productos que cuestan más de $200.000
premium = {p: v for p, v in precios.items() if v > 200_000}
print("premium:", premium)

# Invertir un diccionario {k: v} -> {v: k}
codigo_ciudad = {"BOG": "Bogota", "CLO": "Cali", "MDE": "Medellin"}
ciudad_codigo = {v: k for k, v in codigo_ciudad.items()}
print("invertido:", ciudad_codigo)

# Construir desde dos listas paralelas
productos = ["laptop", "teclado", "monitor"]
stocks    = [15, 45, 8]
inventario = {p: s for p, s in zip(productos, stocks)}
print("inventario:", inventario)
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Al invertir un diccionario `{k: v} → {v: k}`, ¿qué pasa si hay dos claves
con el mismo valor?

```python
d = {"a": 1, "b": 1, "c": 2}
inv = {v: k for k, v in d.items()}
# ¿cuántas claves tiene inv? ¿cuál "gana"?
```
"""),

code(r"""
d = {"a": 1, "b": 1, "c": 2}
inv = {v: k for k, v in d.items()}
print("d original:", d)
print("invertido :", inv)
# Como 1 aparece dos veces como valor, solo sobrevive el ULTIMO (b)
# porque la comprension sobreescribe la clave 1 al encontrar 'b'.
"""),
]


# ===================================================================== #
# 7. CONJUNTO (SET)
# ===================================================================== #
C += [
md(r"""
## 7. Conjunto (`set`): sin orden, sin duplicados

Un conjunto almacena elementos **únicos** sin un orden garantizado.
Internamente también usa una tabla hash, por lo que `in` es O(1).

### Cuándo usar un set

- Deduplicar una colección (eliminar repetidos).
- Verificar pertenencia rápida cuando no importa el orden.
- Operaciones matemáticas de conjuntos: unión, intersección, diferencia.

```python
# Crear un set
s = {1, 2, 3}         # literal
s = set([1, 2, 2, 3]) # desde lista (los duplicados desaparecen)
s = set()             # set vacío — ¡NO {} que es dict vacío!
```
"""),

code(r"""
# Deduplicar clientes
clientes_con_repetidos = [1001, 1005, 1002, 1005, 1003, 1001, 1007]
clientes_unicos = set(clientes_con_repetidos)
print("original:", clientes_con_repetidos)
print("unicos  :", clientes_unicos)
print("cantidad:", len(clientes_unicos))

# Verificar pertenencia — O(1)
print("\n1005 en clientes?", 1005 in clientes_unicos)
print("9999 en clientes?", 9999 in clientes_unicos)

# Agregar y eliminar
clientes_unicos.add(1010)
clientes_unicos.discard(1001)   # no lanza error si no existe
print("\ntras add(1010) y discard(1001):", clientes_unicos)
"""),

md(r"""
### Operaciones de conjuntos

```
  A = {1, 2, 3, 4}
  B = {3, 4, 5, 6}

  A | B  (unión)         →  {1, 2, 3, 4, 5, 6}   todos los de A o B
  A & B  (intersección)  →  {3, 4}                solo los que están en ambos
  A - B  (diferencia)    →  {1, 2}                en A pero NO en B
  A ^ B  (diferencia sim)→  {1, 2, 5, 6}          en uno pero no en ambos
```

Estas operaciones son O(min(len(A), len(B))) — muy eficientes.
"""),

code(r"""
# Clientes de Bogota vs clientes de Cali
clientes_bogota = {1001, 1005, 1002, 1008, 1010}
clientes_cali   = {1003, 1005, 1007, 1008, 1011}

union         = clientes_bogota | clientes_cali
interseccion  = clientes_bogota & clientes_cali
solo_bogota   = clientes_bogota - clientes_cali
solo_cali     = clientes_cali - clientes_bogota
simetrica     = clientes_bogota ^ clientes_cali

print("union          :", union)
print("interseccion   :", interseccion)
print("solo en bogota :", solo_bogota)
print("solo en cali   :", solo_cali)
print("simetrica      :", simetrica)

# Pregunta de negocio: clientes que compraron en AMBAS ciudades
print("\nClientes fieles a ambas ciudades:", interseccion)
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- ¿Por qué `{} ` crea un diccionario vacío y no un set vacío?
- ¿Puedes poner una lista dentro de un set? ¿Y una tupla?
- Si tienes dos listas de 100.000 elementos cada una y quieres saber cuáles
  aparecen en ambas, ¿sería más rápido con listas o con sets?
"""),

code(r"""
# Listas dentro de sets -> ERROR porque las listas no son hashable
# {[1, 2, 3]}   # TypeError: unhashable type: 'list'

# Tuplas si se pueden (son inmutables -> hashable)
s = {(1, 2), (3, 4), (1, 2)}  # (1,2) aparece dos veces -> queda una vez
print("set de tuplas:", s)

# Comparar velocidad: interseccion con listas vs sets
import time
n = 100_000
lista_a = list(range(n))
lista_b = list(range(n // 2, n + n // 2))

t0 = time.perf_counter()
inter_set = set(lista_a) & set(lista_b)
t1 = time.perf_counter()
print("\nInterseccion con sets: {:.4f}s | {} elementos".format(t1 - t0, len(inter_set)))
"""),
]


# ===================================================================== #
# 8. COMPRENSIONES DE SET
# ===================================================================== #
C += [
md(r"""
## 8. Comprensiones de conjunto

La sintaxis es idéntica a la de lista pero con llaves `{}`:

```python
{expresion for variable in iterable if condicion}
```

Resultado: un `set` (sin duplicados, sin orden garantizado).
"""),

code(r"""
transacciones = [
    {"ciudad": "Bogota",   "categoria": "tecnologia", "monto": 50_000},
    {"ciudad": "Cali",     "categoria": "hogar",      "monto": 80_000},
    {"ciudad": "Bogota",   "categoria": "tecnologia", "monto": 120_000},
    {"ciudad": "Medellin", "categoria": "hogar",      "monto": 70_000},
    {"ciudad": "Cali",     "categoria": "alimentos",  "monto": 30_000},
]

# Ciudades únicas con comprensión de set (sin .append ni deduplicar manualmente)
ciudades = {t["ciudad"] for t in transacciones}
print("ciudades:", ciudades)

# Combinaciones únicas (ciudad, categoria)
combos = {(t["ciudad"], t["categoria"]) for t in transacciones}
print("combos:", combos)

# Ciudades con al menos una transaccion > $60.000
ciudades_grandes = {t["ciudad"] for t in transacciones if t["monto"] > 60_000}
print("ciudades con monto > 60k:", ciudades_grandes)
"""),
]


# ===================================================================== #
# 9. ¿CUÁNDO USAR QUÉ?
# ===================================================================== #
C += [
md(r"""
## 9. ¿Cuándo usar qué? Tabla de decisión

Antes de elegir una estructura, hazte estas preguntas:

| Pregunta | Si respuestas... | Usa |
|---|---|---|
| ¿Necesito orden y duplicados? | sí | `list` |
| ¿Los datos no deben cambiar? | sí | `tuple` |
| ¿Necesito buscar por un identificador? | sí | `dict` |
| ¿Me importa si un elemento está o no? | sí | `set` |
| ¿Necesito deduplicar? | sí | `set` |
| ¿Quiero un registro inmutable nombrado? | sí | `tuple` o `namedtuple` |

### Diagrama de decisión

```
   ¿los datos van en pares clave→valor?
        sí → dict
        no →
           ¿importa si hay duplicados?
               sí →
                   ¿necesita modificarse?
                       sí → list
                       no → tuple
               no → set
```

### Tabla comparativa de operaciones clave

| Operación | list | tuple | dict | set |
|---|---|---|---|---|
| Acceso por índice | O(1) | O(1) | — | — |
| Acceso por clave | — | — | O(1) prom. | — |
| Búsqueda (`in`) | O(n) | O(n) | O(1) prom. | O(1) prom. |
| Inserción al final | O(1) | — | O(1) prom. | O(1) prom. |
| Inserción al inicio | O(n) | — | — | — |
| Eliminación | O(n) | — | O(1) prom. | O(1) prom. |
| Ordenar | O(n log n) | — | — | — |
"""),

code(r"""
# Ejemplo integrador: mismo problema, cuatro estructuras distintas
# Tenemos IDs de pedidos procesados. Queremos saber si el pedido 1067 fue procesado.

pedidos_list  = [1004, 1079, 1067, 1063, 1105]       # list
pedidos_tuple = (1004, 1079, 1067, 1063, 1105)       # tuple
pedidos_dict  = {1004: True, 1079: True, 1067: True,
                 1063: True, 1105: True}              # dict {id: procesado}
pedidos_set   = {1004, 1079, 1067, 1063, 1105}       # set

buscar = 1067
print("list  :", buscar in pedidos_list,  "  # O(n)")
print("tuple :", buscar in pedidos_tuple, "  # O(n)")
print("dict  :", buscar in pedidos_dict,  "  # O(1) prom.")
print("set   :", buscar in pedidos_set,   "  # O(1) prom.")

# Para membresía pura (¿está o no?), set es la elección natural.
# Para clave->valor (¿cuánto pagó?), dict es la elección natural.
"""),
]


# ===================================================================== #
# 10. PATRONES ALGORÍTMICOS
# ===================================================================== #
C += [
md(r"""
## 10. Patrones algorítmicos con estructuras de datos

Estos tres patrones aparecen en casi todo proyecto de datos. Memorízalos como
recetas reutilizables.

### Patrón 1: Agrupar por clave (frecuencias y agrupaciones)

```python
# Frecuencias: {elemento: cuántas veces aparece}
conteo = {}
for x in coleccion:
    conteo[x] = conteo.get(x, 0) + 1

# Agrupar: {clave: [elementos que comparten esa clave]}
grupos = {}
for item in coleccion:
    k = item["ciudad"]   # o cualquier criterio
    if k not in grupos:
        grupos[k] = []
    grupos[k].append(item)
```
"""),

code(r"""
# Frecuencia de métodos de pago en transacciones
pagos = ["tarjeta", "efectivo", "tarjeta", "transferencia",
         "efectivo", "tarjeta", "efectivo", "efectivo"]

frecuencia = {}
for pago in pagos:
    frecuencia[pago] = frecuencia.get(pago, 0) + 1

print("frecuencia de pagos:", frecuencia)

# Encontrar el más frecuente (patrón campeón sobre dict)
mas_comun = max(frecuencia, key=frecuencia.get)
print("metodo mas comun:", mas_comun, "(", frecuencia[mas_comun], "veces)")
"""),

md(r"""
### Patrón 2: Índice invertido (de valor a clave)

Un índice invertido mapea **valores a las claves que los contienen**.
Es la estructura detrás de los motores de búsqueda:

```
  texto original:  "Python es poderoso. Python es popular."
  índice invertido:
    "Python"    → [0, 3]   (aparece en las posiciones 0 y 3)
    "es"        → [1, 4]
    "poderoso"  → [2]
    "popular"   → [5]
```

Permite responder *"¿en qué documentos aparece esta palabra?"* en O(1).
"""),

code(r"""
# Indice invertido: palabra -> lista de posiciones en el texto
texto = "bogota tiene el mayor volumen bogota lidera bogota"
palabras = texto.split()

indice = {}
for pos, palabra in enumerate(palabras):
    if palabra not in indice:
        indice[palabra] = []
    indice[palabra].append(pos)

print("indice invertido:")
for palabra, posiciones in sorted(indice.items()):
    print("  {:<12} -> {}".format(palabra, posiciones))

# Consulta: ¿dónde aparece 'bogota'?
print("\n'bogota' aparece en posiciones:", indice.get("bogota", []))
"""),

md(r"""
### Patrón 3: Deduplicar preservando orden

Un `set` elimina duplicados pero no garantiza el orden original.
Si el orden importa:

```python
vistos = set()
resultado = []
for x in original:
    if x not in vistos:
        resultado.append(x)
        vistos.add(x)
```

Este patrón es O(n) gracias a que `in vistos` es O(1).
"""),

code(r"""
# Deduplicar ids de cliente preservando el orden de primera aparicion
ids = [1004, 1079, 1004, 1067, 1063, 1079, 1105, 1067]

# Con set: perdemos el orden
print("con set:", set(ids))   # orden no garantizado

# Preservando orden
vistos = set()
unicos = []
for x in ids:
    if x not in vistos:
        unicos.append(x)
        vistos.add(x)

print("preservando orden:", unicos)
"""),
]


# ===================================================================== #
# 11. ANIDAMIENTO
# ===================================================================== #
C += [
md(r"""
## 11. Anidamiento: dict de listas y list de dicts

Las estructuras se anidan naturalmente para representar datos complejos.

### `list` de `dicts` — el patrón de tabla de datos

Cada dict es una fila; cada clave es una columna. Es exactamente como
trabaja pandas internamente.

```python
tabla = [
    {"id": 1, "ciudad": "Bogota", "monto": 50_000},
    {"id": 2, "ciudad": "Cali",   "monto": 80_000},
    ...
]
```
"""),

code(r"""
# Lista de dicts: la "tabla" más común en Python puro
transacciones = [
    {"id": 1001, "ciudad": "Bogota",   "categoria": "tecnologia", "monto": 120_000},
    {"id": 1002, "ciudad": "Cali",     "categoria": "hogar",      "monto":  80_000},
    {"id": 1003, "ciudad": "Bogota",   "categoria": "alimentos",  "monto":  45_000},
    {"id": 1004, "ciudad": "Medellin", "categoria": "tecnologia", "monto": 200_000},
    {"id": 1005, "ciudad": "Cali",     "categoria": "tecnologia", "monto":  95_000},
]

# Filtrar filas (como un WHERE de SQL)
bogota = [t for t in transacciones if t["ciudad"] == "Bogota"]
print("transacciones Bogota:", len(bogota))

# Proyectar columnas (como un SELECT)
ciudades_montos = [(t["ciudad"], t["monto"]) for t in transacciones]
print("ciudades y montos:", ciudades_montos)

# Agregar (como un GROUP BY + SUM)
total_por_ciudad = {}
for t in transacciones:
    c = t["ciudad"]
    total_por_ciudad[c] = total_por_ciudad.get(c, 0) + t["monto"]
print("total por ciudad:", total_por_ciudad)
"""),

md(r"""
### `dict` de `listas` — agrupar registros

```python
grupos = {
    "Bogota":   [fila1, fila3, fila7, ...],
    "Cali":     [fila2, fila5, ...],
    ...
}
```

Es el resultado de un GROUP BY: cada clave agrupa todos los elementos
que comparten ese valor.
"""),

code(r"""
# Agrupar transacciones por ciudad
por_ciudad = {}
for t in transacciones:
    c = t["ciudad"]
    if c not in por_ciudad:
        por_ciudad[c] = []
    por_ciudad[c].append(t)

for ciudad, filas in por_ciudad.items():
    total = sum(f["monto"] for f in filas)
    print("{:<12}: {} transacciones, total ${:,}".format(ciudad, len(filas), total))
"""),

md(r"""
### Tabla de conteos anidados: `dict` de `dicts`

```python
conteo = {
    "Bogota": {"tecnologia": 3, "hogar": 1},
    "Cali":   {"alimentos": 2, "hogar": 1},
}
```

Permite responder: *"¿Cuántas ventas de tecnología hubo en Bogota?"*
"""),

code(r"""
# Conteos anidados: ciudad -> categoria -> total de transacciones
conteo_anidado = {}
for t in transacciones:
    c = t["ciudad"]
    k = t["categoria"]
    if c not in conteo_anidado:
        conteo_anidado[c] = {}
    conteo_anidado[c][k] = conteo_anidado[c].get(k, 0) + 1

print("conteos ciudad x categoria:")
for ciudad, cats in conteo_anidado.items():
    print("  {}:".format(ciudad))
    for cat, n in cats.items():
        print("    {:15} {}".format(cat, n))
"""),
]


# ===================================================================== #
# 12. ERRORES COMUNES
# ===================================================================== #
C += [
md(r"""
## 12. Errores comunes con estructuras de datos

### Error 1: Modificar un dict (o list) mientras se itera

```python
# MALO — RuntimeError
for k in d:
    if alguna_condicion(k):
        del d[k]

# BUENO — iterar sobre copia
for k in list(d.keys()):
    if alguna_condicion(k):
        del d[k]
```

### Error 2: Usar listas como claves de dict

```python
# MALO — TypeError: unhashable type: 'list'
d = {[1, 2]: "valor"}

# BUENO — tupla es hashable
d = {(1, 2): "valor"}
```

### Error 3: Confundir `{}` con `set()`

```python
d = {}     # dict vacío
s = set()  # set vacío — NUNCA {}, eso es dict
```

### Error 4: Asumir orden en un set

```python
s = {3, 1, 2}
print(list(s))   # puede ser [1, 2, 3] o [3, 1, 2] — ¡no garantizado!
```

### Error 5: `.append()` vs `+=` en listas dentro de dicts

```python
d = {}
d["a"] = d.get("a", [])
d["a"].append(1)    # modifica la lista existente
d["a"] += [2]       # ¡OJO! += en listas modifica in-place (bien)
                    # pero en strings/ints crea nuevo objeto
```
"""),

code(r"""
# Demostrar error 1 y su solucion
inventario = {"laptop": 5, "teclado": 0, "monitor": 3, "mouse": 0}

# Eliminar productos sin stock (forma correcta)
sin_stock = [prod for prod, stock in inventario.items() if stock == 0]
for prod in sin_stock:
    del inventario[prod]
print("inventario sin stock cero:", inventario)

# Demostrar error 3
d = {}
s = set()
print("\ntipo de {} :", type(d))
print("tipo de set():", type(s))
print("son distintos:", type(d) != type(s))
"""),
]


# ===================================================================== #
# 13. RESUMEN, QUIZ Y RETOS
# ===================================================================== #
C += [
md(r"""
## 13. Resumen de la clase

| Concepto | En una frase |
|---|---|
| `list` | colección ordenada y mutable; slicing potente; búsqueda O(n) |
| `tuple` | como list pero inmutable; hashable; señal de "no cambies esto" |
| `dict` | clave→valor; tabla hash; búsqueda O(1) promedio |
| `set` | elementos únicos; sin orden; operaciones de conjuntos en O(n) |
| Comprensión | `[expr for x in it if cond]` — sustituye bucles de construcción |
| Patrón contador | `d[k] = d.get(k, 0) + 1` — frecuencias en O(n) |
| Patrón agrupar | `grupos[k].append(v)` — GROUP BY manual |
| Índice invertido | `{palabra: [posiciones]}` — búsqueda semántica rápida |
| Deduplicar con orden | `set` para membership + `list` para orden |
| Anidamiento | `list` de `dicts` es la "tabla"; `dict` de `listas` es el grupo |

### La pregunta que debes hacerte siempre

> **¿Cuál es la operación dominante?**
> Si es *buscar*, usa `dict` o `set`.
> Si es *iterar en orden*, usa `list` o `tuple`.
> Si es *garantizar unicidad*, usa `set`.
> Si es *relacionar*, usa `dict`.
"""),

md(r"""
## Quiz de autoevaluación

Responde mentalmente, luego ejecuta la celda para verificar.

1. ¿Por qué `d.get("clave", 0)` es preferible a `d["clave"]` cuando la clave
   puede no existir?
2. ¿Qué estructura usarías para almacenar los ids de clientes que ya recibieron
   una notificación? ¿Por qué?
3. ¿Cuál es el resultado de `{1, 2, 3} & {2, 3, 4}`?
4. ¿Por qué `["a", "b"]` no puede ser clave de un dict pero `("a", "b")` sí?
5. ¿Qué hace `{v: k for k, v in d.items()}`?
"""),

code(r"""
respuestas = {
    1: ("d.get() devuelve el valor por defecto sin lanzar KeyError. "
        "d['clave'] falla con KeyError si la clave no existe."),
    2: ("set: la operacion dominante es 'ya recibio notificacion?' (in), "
        "que es O(1) en set y O(n) en list."),
    3: "{2, 3}  — la interseccion contiene solo los elementos que estan en AMBOS.",
    4: ("Las listas son mutables (no hashables). Las tuplas son inmutables "
        "(hashables). El dict necesita un hash estable para la clave."),
    5: "Invierte el diccionario: los valores se convierten en claves y viceversa.",
}
for k, v in respuestas.items():
    print("{}. {}\n".format(k, v))
"""),

md(r"""
## Retos para practicar

Antes de pasar a los notebooks de práctica, intenta estos en papel:

1. **Contador con dict:** dada una lista de palabras, encuentra las 3 más
   frecuentes sin usar `collections.Counter`.

2. **Índice ciudad→clientes:** tienes una lista de dicts con `{cliente, ciudad}`.
   Construye `{ciudad: set_de_clientes}` usando dict de sets.

3. **Deduplicar tuplas:** tienes `[(ciudad, cat), (ciudad, cat), ...]` con
   repetidos. ¿Cuál es la forma más concisa de obtener los pares únicos
   manteniendo el orden de primera aparición?

4. **Análisis de complejidad:** explica por qué este código es O(n²) y cómo
   lo convertirías a O(n):
   ```python
   def tiene_duplicados_lento(lista):
       for i in range(len(lista)):
           for j in range(i + 1, len(lista)):
               if lista[i] == lista[j]:
                   return True
       return False
   ```

---

### Siguiente paso

- **practice01.ipynb** — 10 ejercicios graduales con solución oculta.
- **practice02.ipynb** — análisis de transacciones con diccionarios.
- **homework01.ipynb** y **homework02.ipynb** — tareas autocalificables.
"""),
]


# ===================================================================== #
# CELDAS ADICIONALES — insertar_despues para alcanzar densidad pedagógica
# ===================================================================== #

def insertar_despues(celdas, marcador_texto, nuevas):
    """Inserta 'nuevas' justo después de la primera celda cuyo source contiene 'marcador_texto'."""
    for i, c in enumerate(celdas):
        if marcador_texto in c.source:
            return celdas[: i + 1] + nuevas + celdas[i + 1 :]
    return celdas + nuevas


# --- Ampliacion de motivacion: hash function visual ---------------------
EXTRA_HASH = [
md(r"""
### ¿Qué es una función hash? (profundización)

Una función hash toma cualquier objeto y devuelve un entero:

```
  hash("Bogota")   →  algún entero grande
  hash(42)         →  42  (los enteros son su propio hash en CPython)
  hash((1, 2))     →  algún entero consistente
```

**Propiedades esenciales:**
1. El mismo objeto siempre da el mismo hash (dentro de una sesión de Python).
2. Objetos iguales tienen hashes iguales.
3. La operación es O(1) — no depende del tamaño de la colección.

Es por eso que listas y dicts **no** pueden ser claves: su contenido puede
cambiar, y si cambiara el hash, el dict ya no encontraría el cajón correcto.
"""),

code(r"""
# Explorar la funcion hash de Python
for obj in ["Bogota", "bogota", "Cali", 42, (1, 2, 3), True]:
    print("hash({!r:20}) = {}".format(obj, hash(obj)))

# Las listas no son hashables
try:
    hash([1, 2, 3])
except TypeError as e:
    print("\nhash([1,2,3]) -> TypeError:", e)

# Pero las tuplas si (son inmutables)
print("hash((1, 2, 3)) =", hash((1, 2, 3)))
"""),
]

# --- Ampliacion: namedtuple introductorio --------------------------------
EXTRA_NAMEDTUPLE = [
md(r"""
### `namedtuple`: tupla con campos nombrados

Una `namedtuple` es una tupla cuyos campos tienen nombre, como los de
un dict, pero con acceso por índice y hashable como una tupla.

```python
from collections import namedtuple

Producto = namedtuple("Producto", ["nombre", "precio", "stock"])
p = Producto("laptop", 2_500_000, 15)
p.nombre   # "laptop"    (por nombre)
p[1]       # 2_500_000   (por índice, como tupla)
```

Úsala cuando tengas registros inmutables con campos bien definidos.
Es más legible que una tupla anónima y más ligera que un dict o una clase.
"""),

code(r"""
from collections import namedtuple

# Definir el "tipo" Transaccion
Transaccion = namedtuple("Transaccion", ["id", "ciudad", "categoria", "monto"])

t = Transaccion(id=1001, ciudad="Bogota", categoria="tecnologia", monto=120_000)

# Acceso por nombre (legible)
print("ciudad  :", t.ciudad)
print("monto   :", t.monto)

# Acceso por índice (como tupla)
print("indice 0:", t[0])

# Sigue siendo una tupla
print("es tupla:", isinstance(t, tuple))
print("hashable:", hash(t) is not None)   # se puede usar como clave de dict

# Crear varias transacciones
datos = [
    Transaccion(1001, "Bogota",   "tecnologia", 120_000),
    Transaccion(1002, "Cali",     "hogar",       80_000),
    Transaccion(1003, "Medellin", "tecnologia",  200_000),
]
# Comprension sobre namedtuples
tecnologia = [t for t in datos if t.categoria == "tecnologia"]
print("\ntransacciones de tecnologia:", len(tecnologia))
"""),
]

# --- Ampliacion: setdefault y defaultdict --------------------------------
EXTRA_SETDEFAULT = [
md(r"""
### `setdefault` y el patrón de agrupación idiomático

Al construir `dict` de listas (agrupaciones), la combinación más idiomática
usa `setdefault`:

```python
# Con if-else clásico (verbose pero claro):
if clave not in d:
    d[clave] = []
d[clave].append(valor)

# Con setdefault (idiomático):
d.setdefault(clave, []).append(valor)
```

`setdefault(k, default)` inserta `default` si `k` no existe **y devuelve
el valor actual**, permitiendo encadenar `.append()` directamente.
"""),

code(r"""
# Agrupar transacciones por categoria usando setdefault
transacciones_raw = [
    ("t001", "Bogota",   "tecnologia", 120_000),
    ("t002", "Cali",     "hogar",       80_000),
    ("t003", "Bogota",   "alimentos",   45_000),
    ("t004", "Medellin", "tecnologia", 200_000),
    ("t005", "Bogota",   "tecnologia",  95_000),
]

por_categoria = {}
for tid, ciudad, categoria, monto in transacciones_raw:
    por_categoria.setdefault(categoria, []).append({
        "id": tid, "ciudad": ciudad, "monto": monto
    })

for cat, filas in por_categoria.items():
    total = sum(f["monto"] for f in filas)
    print("{:<15}: {} transacciones, total ${:,}".format(cat, len(filas), total))
"""),
]

# --- Ampliacion: frozenset -----------------------------------------------
EXTRA_FROZENSET = [
md(r"""
### `frozenset`: el set inmutable (y hashable)

Así como la tupla es la lista inmutable, el `frozenset` es el set inmutable.
Puede ser clave de dict o elemento de otro set.

```python
fs = frozenset({1, 2, 3})
d  = {fs: "valor"}    # válido porque frozenset es hashable
```

Caso de uso: representar un grupo de elementos sin orden ni duplicados como
clave de un índice.
"""),

code(r"""
from collections import defaultdict

# Usar frozenset para agrupar clientes por conjunto de ciudades visitadas
historial = [
    ("Ana",   ["Bogota", "Cali"]),
    ("Luis",  ["Cali", "Bogota"]),        # mismo conjunto que Ana
    ("Sara",  ["Medellin"]),
    ("Pedro", ["Bogota", "Cali", "Medellin"]),
]

grupos_rutas = defaultdict(list)
for nombre, ciudades in historial:
    ruta = frozenset(ciudades)    # {Bogota, Cali} == {Cali, Bogota}
    grupos_rutas[ruta].append(nombre)

print("Clientes agrupados por ruta:")
for ruta, clientes in grupos_rutas.items():
    print("  {}: {}".format(set(ruta), clientes))
"""),
]

# --- Ampliacion: comprensiones anidadas y de dict avanzadas ---------------
EXTRA_COMP_AVANZADAS = [
md(r"""
### Comprensiones anidadas: tabla de frecuencias

Las comprensiones de dict pueden construir tablas completas de una vez:
"""),

code(r"""
# Tabla de ventas: ciudad x categoria con totales
ventas_raw = [
    ("Bogota",   "tecnologia", 120_000),
    ("Bogota",   "hogar",       80_000),
    ("Cali",     "tecnologia",  95_000),
    ("Cali",     "hogar",       60_000),
    ("Bogota",   "tecnologia",  75_000),
    ("Medellin", "alimentos",   30_000),
]

# Construir tabla anidada {ciudad: {categoria: suma_montos}}
tabla = {}
for ciudad, cat, monto in ventas_raw:
    tabla.setdefault(ciudad, {}).setdefault(cat, 0)
    tabla[ciudad][cat] += monto

# Mostrar como tabla
ciudades_sorted = sorted(tabla.keys())
cats_sorted = sorted({c for fila in tabla.values() for c in fila})

print("Ciudad         | " + " | ".join("{:>12}".format(c) for c in cats_sorted))
print("-" * (15 + 15 * len(cats_sorted)))
for ciudad in ciudades_sorted:
    fila = [tabla[ciudad].get(c, 0) for c in cats_sorted]
    print("{:<15}| ".format(ciudad) + " | ".join("{:>12,}".format(v) for v in fila))
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Necesitas construir, a partir de la tabla anterior, un dict
`{categoria: ciudad_lider}` donde `ciudad_lider` es la ciudad con mayor
venta en cada categoría. ¿Cómo lo harías con lo que ya sabes?

Pista: primero invierte el problema: para cada categoría, ¿qué ciudades
tienes y con qué montos? Luego aplica el patrón campeón.
"""),
]

# --- Ampliacion: glosario ------------------------------------------------
EXTRA_GLOSARIO = [
md(r"""
## Glosario de la Clase 4

| Término | Definición breve |
|---|---|
| **Lista (`list`)** | colección ordenada, mutable, con duplicados; acceso por índice O(1) |
| **Tupla (`tuple`)** | lista inmutable; hashable; semántica de "registro fijo" |
| **Diccionario (`dict`)** | estructura clave→valor basada en tabla hash; búsqueda O(1) prom. |
| **Conjunto (`set`)** | colección sin orden ni duplicados; basado en hash; operaciones de conjuntos |
| **Tabla hash** | estructura que calcula un índice directamente desde la clave (hash) |
| **Hash** | entero calculado a partir de un objeto para determinar su posición en la tabla |
| **Hashable** | propiedad de un objeto cuyo hash no cambia (inmutable); requisito para clave de dict/set |
| **Comprensión** | expresión concisa para construir list/dict/set desde otro iterable |
| **Patrón contador** | `d[k] = d.get(k, 0) + 1` — frecuencias en O(n) |
| **Índice invertido** | `{valor: [claves que lo contienen]}` — base de motores de búsqueda |
| **`namedtuple`** | tupla con campos nombrados; más legible que tupla anónima |
| **`setdefault`** | inserta valor por defecto si clave no existe y devuelve el valor actual |
| **`frozenset`** | set inmutable y hashable |
| **Deduplicar** | eliminar duplicados; con set es O(n); preservar orden requiere set + list |
"""),
]

# Insertar bloques extra en puntos estratégicos
C = insertar_despues(C, "por lo que `in` es O(1).", EXTRA_HASH)
C = insertar_despues(C, "Esa diferencia se multiplica cuando los datos son millones.", EXTRA_NAMEDTUPLE)
C = insertar_despues(C, "permite encadenar `.append()` directamente.", EXTRA_SETDEFAULT)
C = insertar_despues(C, "elemento de otro set.", EXTRA_FROZENSET)
C = insertar_despues(C, "Patrón 3: Deduplicar preservando orden", EXTRA_COMP_AVANZADAS)
C = insertar_despues(C, "Retos para practicar", EXTRA_GLOSARIO)


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase04", "lecture.ipynb")
build(os.path.abspath(ruta), C)
