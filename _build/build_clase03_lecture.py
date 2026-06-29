"""Construye curso/clase03/lecture.ipynb — Ciclos, funciones y lambdas."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []  # lista de celdas


# ===================================================================== #
# 0. PORTADA Y AGENDA
# ===================================================================== #
C += [
md(r"""
# Clase 3 · Ciclos, funciones y lambdas

### Fundamentos de Programación para Ciencia de Datos

> *"Cualquier tonto puede escribir código que una computadora entiende. Los buenos
> programadores escriben código que los humanos entienden."* — Martin Fowler

---

**Duración:** 3 horas · **Modalidad:** notebook interactivo

En las clases anteriores aprendimos a pensar en algoritmos y a manejar los tipos
de datos básicos de Python. Hoy damos el salto más importante de las primeras
semanas: aprendemos a **automatizar la repetición** con bucles y a **empaquetar
lógica reutilizable** en funciones.

Al final de la clase serás capaz de:
- Recorrer cualquier colección con `for` y `while`, incluyendo control fino con
  `break`, `continue` y el cláusula `else` de bucle.
- Definir funciones claras, con parámetros por defecto y retorno múltiple.
- Entender por qué las variables "viven" donde viven (scope).
- Escribir transformaciones en una línea con `lambda`, `map()` y `filter()`.
"""),

md(r"""
## Mapa de la clase

| Bloque | Tiempo | Contenido |
|---|---|---|
| 1. Motivación | 15 min | El bucle como automatización del trabajo repetitivo |
| 2. Bucle `for` | 30 min | Rangos, listas, cadenas, `enumerate` |
| 3. Bucle `while` | 20 min | Cuándo usarlo, invariantes, bucle infinito |
| 4. Control de flujo en bucles | 20 min | `break`, `continue`, `else` |
| 5. Bucles anidados | 15 min | Matrices, productos, complejidad O(n²) |
| 6. Funciones | 30 min | Definición, parámetros, `return`, docstrings |
| 7. Parámetros avanzados | 15 min | Valores por defecto, posición vs nombre |
| 8. Scope | 15 min | Local vs global, por qué importa |
| 9. Funciones como valores | 10 min | Asignar, pasar como argumento |
| 10. Lambda, map, filter | 20 min | Funciones anónimas, aplicar a colecciones |
| 11. Errores comunes + cierre | 10 min | Resumen, quiz, retos |

> 🧭 **Cómo usar este notebook:** lee cada celda de texto antes de ejecutar la
> celda de código. Detente en cada bloque **🤔 ¿Qué pasaría si...?** e intenta
> responder mentalmente antes de continuar.
"""),
]


# ===================================================================== #
# 1. MOTIVACIÓN
# ===================================================================== #
C += [
md(r"""
## 1. Motivación: el bucle como automatización

Imagina que eres analista en una empresa de logística. Tu jefe te pide calcular
el impuesto (19%) sobre cada factura del día. Hoy hay 3 facturas:

```
Factura 1: $120.000  →  impuesto: $22.800
Factura 2: $340.000  →  impuesto: $64.600
Factura 3: $89.000   →  impuesto: $16.910
```

Fácil a mano. Pero mañana hay 500 facturas. ¿Y pasado mañana, 10.000?

**El bucle es la respuesta.** Escribes la operación una sola vez y le dices a la
computadora: *"aplica esto a todos los elementos"*. Eso es la automatización.
"""),

code(r"""
# Sin bucle: repetimos código 3 veces (no escala).
factura1, factura2, factura3 = 120000, 340000, 89000
print("impuesto 1:", factura1 * 0.19)
print("impuesto 2:", factura2 * 0.19)
print("impuesto 3:", factura3 * 0.19)
"""),

code(r"""
# CON bucle: funciona igual con 3, 500 o 10.000 facturas.
facturas = [120000, 340000, 89000, 215000, 67000]

for monto in facturas:
    print("Impuesto: $" + str(int(monto * 0.19)))
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- ¿Qué harías si la lista `facturas` tuviese 0 elementos? El bucle simplemente
  **no se ejecuta** — esto es un comportamiento clave y muy útil.
- ¿Qué pasaría si el impuesto fuera diferente para cada ciudad? ¿Cómo modificarías
  el código? (Pista: necesitarías pares ciudad–tasa, que veremos en la Clase 4).
"""),
]


# ===================================================================== #
# 2. EL BUCLE FOR
# ===================================================================== #
C += [
md(r"""
## 2. El bucle `for`: iterar sobre secuencias

### Contexto
El `for` de Python es un **bucle de recorrido**: recorre elemento a elemento
cualquier secuencia (lista, cadena, rango, tupla...). No necesitas índices
explícitos si solo te importan los valores.

### Solución intuitiva
"Por cada elemento en la colección, haz algo con él."

### Sintaxis
```
for variable in coleccion:
    bloque de código (indentado 4 espacios)
```
La `variable` toma el valor de cada elemento en cada vuelta.

### Pseudocódigo general
```
PARA CADA elemento EN coleccion HACER
    ... usar elemento ...
FIN_PARA
```
"""),

md(r"""
### 2.1 Iterar sobre rangos: `range()`

`range(inicio, fin, paso)` genera una secuencia de enteros. Es la forma de hacer
un bucle clásico "de 1 a n".

| Llamada | Valores generados |
|---|---|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(1, 6)` | 1, 2, 3, 4, 5 |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8 |
| `range(10, 0, -1)` | 10, 9, 8, ..., 1 |

> ⚠️ El extremo derecho (`fin`) **no se incluye**. Esto confunde a principiantes
> y es fuente del error *off-by-one*. Trazalo en papel si tienes dudas.
"""),

code(r"""
# Tabla de cuadrados de los primeros 6 enteros positivos.
print("n   n^2")
print("--------")
for n in range(1, 7):   # 1, 2, 3, 4, 5, 6
    print(str(n) + "   " + str(n * n))
"""),

md(r"""
### Trazado de ejecución: `range(1, 5)`

| Vuelta | `n` | operación | salida |
|--------|-----|-----------|--------|
| 1 | 1 | 1*1 | 1 |
| 2 | 2 | 2*2 | 4 |
| 3 | 3 | 3*3 | 9 |
| 4 | 4 | 4*4 | 16 |
| fin | — | bucle termina | — |
"""),

md(r"""
### 2.2 Iterar sobre listas

El caso más común en ciencia de datos: recorrer una lista de valores.
"""),

code(r"""
ciudades = ["Bogota", "Medellin", "Cali", "Barranquilla", "Cartagena"]

for ciudad in ciudades:
    print("Procesando sucursal:", ciudad)
"""),

md(r"""
### 2.3 Iterar sobre cadenas

Una cadena es una secuencia de caracteres. `for` la recorre letra por letra.
"""),

code(r"""
# Contar vocales en un nombre de ciudad.
def contar_vocales(texto):
    vocales = "aeiouAEIOU"
    total = 0
    for letra in texto:
        if letra in vocales:
            total += 1
    return total

for ciudad in ["Bogota", "Barranquilla", "Medellin"]:
    n = contar_vocales(ciudad)
    print(ciudad + ": " + str(n) + " vocales")
"""),

md(r"""
### 2.4 Iterar con índice: `enumerate()`

A veces necesitas tanto el **valor** como su **posición**. `enumerate()` devuelve
pares `(índice, valor)`, evitando el patrón feo `range(len(lista))`.

```
# Sin enumerate (funciona pero es torpe):
for i in range(len(lista)):
    print(i, lista[i])

# Con enumerate (limpio y legible):
for i, valor in enumerate(lista):
    print(i, valor)
```
"""),

code(r"""
productos = ["laptop", "teclado", "monitor", "mouse", "auriculares"]
precios   = [2500000, 120000, 890000, 45000, 180000]

print("Catálogo de productos:")
print("-" * 40)
for i, (prod, precio) in enumerate(zip(productos, precios), start=1):
    print(str(i) + ". " + prod.ljust(14) + " $" + "{:,}".format(precio))
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

1. Cambias `range(1, 7)` por `range(7)` en el ejemplo de cuadrados. ¿Qué cambia?
2. Usas `enumerate(ciudades, start=1)` para numerar las ciudades desde 1 en lugar
   de 0. ¿Para qué sirve el parámetro `start`?
3. ¿Qué produce `for letra in ""`? (cadena vacía)
"""),
]


# ===================================================================== #
# 3. EL BUCLE WHILE
# ===================================================================== #
C += [
md(r"""
## 3. El bucle `while`: repetir mientras se cumpla una condición

### Cuándo usar `while` vs `for`

| Situación | Usa |
|---|---|
| Sabes cuántas veces repetir, o tienes una colección | `for` |
| No sabes cuántas veces; dependes de un estado que cambia | `while` |

Ejemplos típicos de `while`:
- Pedir datos hasta que el usuario ingrese uno válido.
- Aplicar un proceso hasta que el error sea menor que un umbral.
- Simular hasta que el saldo llegue a cero.

### Pseudocódigo
```
MIENTRAS condicion HACER
    ... bloque ...
    (actualizar la condicion para que algún día sea Falsa)
FIN_MIENTRAS
```

> ⚠️ **Invariante:** al diseñar un `while`, pregúntate *"¿qué condición garantiza
> que el bucle siempre termina?"*. Si no puedes responder, probablemente tengas
> un **bucle infinito**.
"""),

code(r"""
# Ejemplo: calcular cuántos dias tarda en duplicarse una inversión al 5% diario.
# No sabemos de antemano cuántos días serán -> while.

capital = 10000   # pesos
dias = 0
objetivo = capital * 2

while capital < objetivo:
    capital = capital * 1.05  # 5% de interes diario
    dias += 1

print("Dias para duplicar el capital: " + str(dias))
print("Capital final: $" + "{:.2f}".format(capital))
"""),

md(r"""
### Trazado de las primeras vueltas

| Día | Capital antes | Condición `< 20000` | Capital después |
|-----|--------------|---------------------|----------------|
| 1 | 10.000 | True | 10.500 |
| 2 | 10.500 | True | 11.025 |
| 3 | 11.025 | True | 11.576 |
| ... | ... | True | ... |
| 15 | 19.799 | True | 20.789 |
| — | 20.789 | **False** | bucle termina |
"""),

code(r"""
# Peligro: bucle infinito. NUNCA ejecutes esto tal cual (tiene un comentario de guarda).
# La condicion nunca se vuelve False si no actualizamos la variable correcta.

# MALO (bucle infinito — no descomentar):
# saldo = 100
# while saldo > 0:
#     print("procesando...")
#     # se nos olvidó descontar algo -> saldo nunca cambia -> loop infinito

# CORRECTO: siempre asegurar que la condicion eventualmente sea False.
saldo = 100
intentos = 0
while saldo > 0 and intentos < 10:   # doble guarda de seguridad
    saldo -= 30
    intentos += 1
    print("Saldo: " + str(saldo))
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- El capital inicial ya fuera `>= objetivo` desde el inicio. ¿Cuántas veces
  ejecutaría el bucle? (Respuesta: cero. El `while` verifica la condición
  **antes** de entrar).
- El tipo de interés fuera `0.0`. ¿Terminaría el bucle? ¿Por qué?
"""),
]


# ===================================================================== #
# 4. BREAK, CONTINUE, ELSE
# ===================================================================== #
C += [
md(r"""
## 4. Control fino del flujo: `break`, `continue`, `else`

### `break` — salir del bucle inmediatamente

Útil para salida temprana: en cuanto encontramos lo que buscamos, no
tiene sentido seguir procesando.

```
        ┌────────────────┐
        ▼                │
  ¿condicion?─sí──▶ hacer algo
        │                │
       no                └─ (si no hay break, vuelve)
        │
        ▼ (sale del bucle)
```
"""),

code(r"""
# Buscar el primer producto con stock por debajo del umbral de alerta.
inventario = [
    ("camisas",     320),
    ("pantalones",  85),
    ("zapatos",     12),   # <-- stock crítico
    ("gorras",      200),
]
UMBRAL = 50

for producto, stock in inventario:
    if stock < UMBRAL:
        print("ALERTA: stock critico en '" + producto + "' (" + str(stock) + " unidades)")
        break   # dejamos de buscar, ya encontramos el primero
else:
    print("Todos los productos tienen stock suficiente.")
"""),

md(r"""
### `continue` — saltar al siguiente ciclo

Omite el resto del bloque para la iteración actual y pasa a la siguiente.
Útil para filtrar sin anidar más `if`.

```
for elemento in lista:
    if condicion_de_salto:
        continue       # <- salta al siguiente elemento
    ... procesar elemento ...
```
"""),

code(r"""
# Procesar solo transacciones válidas (ignorar montos negativos o cero).
transacciones = [15000, -200, 89000, 0, 43000, -1500, 120000]

total = 0
invalidas = 0
for t in transacciones:
    if t <= 0:
        invalidas += 1
        continue       # saltar este; no lo sumamos
    total += t

print("Total (transacciones validas): $" + "{:,}".format(total))
print("Transacciones invalidas ignoradas:", invalidas)
"""),

md(r"""
### `else` en bucles — el bloque "si terminé sin break"

El `else` de un bucle se ejecuta **solo si el bucle terminó normalmente** (sin
`break`). Es el mecanismo idiomático de Python para el patrón *"busqué y no
encontré"*.

```python
for elemento in coleccion:
    if condicion:
        break
else:
    # Solo llega aquí si NO hubo break
    print("No se encontró nada")
```
"""),

code(r"""
# Verificar si un número es primo con for...else (patrón elegante).
def es_primo(n):
    if n < 2:
        return False
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0:
            return False   # encontró divisor -> no es primo
    # Si el for termina sin break -> ningún divisor encontrado -> es primo
    return True

for n in [2, 7, 9, 13, 15, 97]:
    estado = "primo" if es_primo(n) else "compuesto"
    print(str(n) + " -> " + estado)
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

1. En el ejemplo de inventario, eliminas el `break`. ¿Cuántos mensajes de alerta
   ves si hay dos productos con stock crítico?
2. ¿Qué imprime el `else` del inventario si **todos** los productos son críticos?
   (pista: nunca llega al `else` porque el `break` se ejecuta en la primera vuelta).
3. ¿Puedes tener un `else` también en un `while`? Sí. ¿Cuándo se ejecutaría?
"""),
]


# ===================================================================== #
# 5. BUCLES ANIDADOS
# ===================================================================== #
C += [
md(r"""
## 5. Bucles anidados: matrices y productos cartesianos

A veces necesitamos recorrer **dos dimensiones**: filas y columnas de una
tabla, pares de elementos, combinaciones de opciones...

### Diagrama

```
PARA CADA fila EN filas HACER
    PARA CADA col EN columnas HACER
        procesar (fila, col)
    FIN_PARA
FIN_PARA
```

El bucle interior se ejecuta **completo** por cada iteración del exterior.
Si el exterior da `n` vueltas y el interior `m`, el total es `n × m` operaciones.

### Complejidad O(n²)

Cuando `n = m` (cuadrícula cuadrada), hablamos de **O(n²)**: cuadrática. Con
100 elementos son 10.000 operaciones; con 1.000 son un millón. Usar bucles
anidados innecesariamente en datasets grandes es un error común y costoso.
"""),

code(r"""
# Generar la tabla de multiplicar de 1 a 5.
print("Tabla de multiplicar (1-5):")
print("     ", end="")
for j in range(1, 6):
    print("{:4}".format(j), end="")
print()
print("    " + "-" * 22)

for i in range(1, 6):
    print("{:3} |".format(i), end="")
    for j in range(1, 6):
        print("{:4}".format(i * j), end="")
    print()
"""),

code(r"""
# Producto cartesiano: generar todas las combinaciones de talla y color.
tallas  = ["S", "M", "L", "XL"]
colores = ["rojo", "azul", "negro"]

variantes = []
for talla in tallas:
    for color in colores:
        variantes.append(talla + "-" + color)

print("Total de variantes:", len(variantes))
print("Primeras 6:", variantes[:6])
print("(", len(tallas), "tallas x", len(colores), "colores =", len(variantes), ")")
"""),

md(r"""
### Trazado del bucle anidado (primeras iteraciones)

Para `tallas = ["S","M"]` y `colores = ["rojo","azul"]`:

| `talla` | `color` | resultado |
|---------|---------|-----------|
| "S" | "rojo" | "S-rojo" |
| "S" | "azul" | "S-azul" |
| "M" | "rojo" | "M-rojo" |
| "M" | "azul" | "M-azul" |

El interior completa su recorrido (rojo, azul) antes de que el exterior avance.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

1. Añades una tercera dimensión: `temporadas = ["verano", "invierno"]`. ¿Cuántas
   variantes habría con 4 tallas, 3 colores y 2 temporadas? ¿Qué complejidad tiene?
2. Un bucle anidado que compara cada elemento de una lista con todos los demás
   es O(n²). ¿Cuándo podría ser inevitable? ¿Cuándo podría evitarse?
"""),
]


# ===================================================================== #
# 6. FUNCIONES: POR QUÉ EXISTEN
# ===================================================================== #
C += [
md(r"""
## 6. Funciones: reutilización, abstracción y pruebas

### ¿Por qué no siempre escribir código "suelto"?

Imagina que calculas el IVA en cinco partes distintas de tu programa:
```python
# Parte 1
precio1 * 0.19
# Parte 2
precio2 * 0.19
# ...
```

Ahora el IVA sube al 21%. Tienes que buscar y cambiar cada aparición. Si te
olvidas una → bug silencioso. Si la lógica fuera más compleja (descuentos,
exenciones), el problema se multiplica.

**Las funciones resuelven esto** empaquetando lógica en una caja con nombre:
```python
def calcular_iva(precio):
    return precio * 0.19
```
Cambias el número en un solo lugar y todo el programa se actualiza.

### Los tres beneficios de las funciones

1. **Reutilización:** define una vez, llama muchas veces.
2. **Abstracción:** quien llama a `calcular_iva(precio)` no necesita saber cómo
   se calcula; solo confía en que funciona.
3. **Pruebas:** puedes comprobar una función aislada antes de integrarla.
"""),

md(r"""
## 7. Definir funciones: `def`, parámetros, `return`, docstrings

### Anatomía de una función

```
def nombre_funcion(param1, param2):
    # docstring: describe que hace, que recibe y que devuelve.
    # cuerpo: los pasos
    resultado = param1 + param2
    return resultado
```

- `def`: palabra clave que inicia la definición.
- `nombre_funcion`: nombre descriptivo (verbos son una buena práctica).
- `param1, param2`: parámetros (las "entradas" de la función).
- `return`: especifica la salida. Sin `return`, la función devuelve `None`.

### La metodología de 6 pasos aplicada a funciones

Cada función que diseñemos seguirá: contexto → intuición → algoritmo →
pseudocódigo → Python → análisis. Empecemos con dos ejemplos completos.
"""),

md(r"""
### Ejemplo A · Validar rango de monto

**1. Contexto:** en el sistema de pagos, los montos deben estar entre $1.000 y
$5.000.000. Necesitamos una función que devuelva `True` si el monto es válido.

**2. Solución intuitiva:** verificar que el monto esté dentro del rango.

**3. Algoritmo:** comparar contra el mínimo y el máximo.

**4. Pseudocódigo:**
```
SI monto >= 1000 Y monto <= 5000000 ENTONCES
    DEVOLVER Verdadero
SINO
    DEVOLVER Falso
```
"""),

code(r"""
# 5. Python
def es_monto_valido(monto, minimo=1000, maximo=5000000):
    # Devuelve True si monto esta dentro del rango [minimo, maximo].
    return minimo <= monto <= maximo  # encadenamiento de comparaciones de Python

# 6. Análisis y pruebas
casos = [500, 1000, 75000, 5000000, 5000001]
for m in casos:
    estado = "VALIDO  " if es_monto_valido(m) else "INVALIDO"
    print(estado + "  $" + "{:,}".format(m))
"""),

md(r"""
### Ejemplo B · Calcular comisión de venta

**1. Contexto:** una empresa paga comisión a sus vendedores:
- Ventas < $500.000: 5%
- Ventas entre $500.000 y $2.000.000: 8%
- Ventas > $2.000.000: 12%

**4. Pseudocódigo:**
```
SI venta < 500000 ENTONCES
    tasa ← 0.05
SINO SI venta <= 2000000 ENTONCES
    tasa ← 0.08
SINO
    tasa ← 0.12
FIN_SI
DEVOLVER venta * tasa
```
"""),

code(r"""
# 5. Python
def calcular_comision(venta):
    # Calcula la comision segun tramo de venta.
    if venta < 500000:
        tasa = 0.05
    elif venta <= 2000000:
        tasa = 0.08
    else:
        tasa = 0.12
    return venta * tasa

# 6. Pruebas
ventas = [200000, 500000, 1000000, 2000000, 3000000]
print("Venta          Comision    Tasa")
print("-" * 38)
for v in ventas:
    c = calcular_comision(v)
    tasa_pct = c / v * 100
    print("${:>12,}  ${:>10,.0f}   {:.0f}%".format(v, c, tasa_pct))
"""),

md(r"""
### Retorno múltiple

Python puede devolver varios valores a la vez (técnicamente devuelve una tupla):

```python
def estadisticas(lista):
    return min(lista), max(lista), sum(lista)/len(lista)

mn, mx, prom = estadisticas([10, 20, 30])
```
"""),

code(r"""
def estadisticas_ventas(montos):
    # Devuelve (minimo, maximo, promedio) de una lista de montos.
    if not montos:
        return None, None, None
    return min(montos), max(montos), sum(montos) / len(montos)

ventas_semana = [320000, 89000, 540000, 210000, 780000]
mn, mx, prom = estadisticas_ventas(ventas_semana)
print("Minimo:   $" + "{:,}".format(mn))
print("Maximo:   $" + "{:,}".format(mx))
print("Promedio: $" + "{:,.0f}".format(prom))
"""),
]


# ===================================================================== #
# 8. PARÁMETROS POR DEFECTO Y ARGS POR NOMBRE
# ===================================================================== #
C += [
md(r"""
## 8. Parámetros por defecto y argumentos por nombre

### Parámetros con valor por defecto

Permiten llamar una función sin especificar todos los argumentos cuando hay un
valor "razonable" de fábrica:

```python
def calcular_iva(precio, tasa=0.19):
    return precio * tasa

calcular_iva(100000)          # usa tasa=0.19
calcular_iva(100000, 0.05)    # usa tasa=0.05
```

> ⚠️ Los parámetros con defecto van **al final** de la lista. `def f(a=1, b)`
> es un error de sintaxis en Python.

### Argumentos por nombre (keyword arguments)

Al llamar una función, puedes especificar los argumentos **por nombre** en
cualquier orden. Esto mejora la legibilidad y evita errores de posición:

```python
def registrar_pedido(producto, cantidad, ciudad, urgente=False):
    ...

# Por posición (frágil: si cambias el orden de parámetros, se rompe):
registrar_pedido("laptop", 2, "Bogota", True)

# Por nombre (robusto y legible):
registrar_pedido(producto="laptop", cantidad=2, ciudad="Bogota", urgente=True)
```
"""),

code(r"""
def formatear_precio(monto, moneda="COP", decimales=0):
    # Formatea un precio con simbolo de moneda y decimales configurables.
    fmt = "{:,." + str(decimales) + "f}"
    return moneda + " " + fmt.format(monto)

# Diferentes formas de llamar la misma función:
print(formatear_precio(125000))                          # COP 125,000
print(formatear_precio(99.99, moneda="USD", decimales=2))  # USD 99.99
print(formatear_precio(1500000, decimales=2))            # COP 1,500,000.00
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

1. Defines `def f(a=1, b=2, c=3)` y llamas `f(10, c=30)`. ¿Qué valores toman
   `a`, `b` y `c`? (Respuesta: a=10, b=2, c=30).
2. Intentas `f(b=20, 10)` — argumento posicional después de uno nombrado.
   ¿Qué ocurre? (Error de sintaxis: los posicionales van antes de los nombrados).
"""),
]


# ===================================================================== #
# 9. SCOPE
# ===================================================================== #
C += [
md(r"""
## 9. Scope (alcance): local vs global

### ¿Por qué las variables "viven" dentro de las funciones?

Cuando defines una variable **dentro** de una función, esa variable es **local**:
solo existe mientras la función se ejecuta y desaparece al terminar. Las
variables **globales** existen en el módulo o notebook.

```
┌─────────────────────────────────────┐
│  Scope GLOBAL (el notebook entero)  │
│                                     │
│  x = 10                             │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Scope LOCAL de calcular()     │  │
│  │                               │  │
│  │  resultado = x * 2  ← puede   │  │
│  │                       leer x  │  │
│  │  y = 5  ← solo existe aquí    │  │
│  └───────────────────────────────┘  │
│                                     │
│  # Fuera: y no existe (NameError)   │
└─────────────────────────────────────┘
```

### La regla LEGB (orden de búsqueda de nombres)
Python busca una variable en este orden:
**L**ocal → **E**nclosing → **G**lobal → **B**uilt-in
"""),

code(r"""
descuento_global = 0.10   # variable global: disponible en todo el notebook

def aplicar_descuento(precio):
    # 'precio' es local; 'descuento_global' se lee del scope global
    precio_final = precio * (1 - descuento_global)
    return precio_final

print(aplicar_descuento(100000))  # 90000.0

# Intentar acceder a una variable local desde afuera -> NameError
try:
    print(precio_final)  # precio_final NO existe fuera de la función
except NameError as e:
    print("Error esperado:", e)
"""),

code(r"""
# ¿Qué pasa si usamos el mismo nombre dentro y fuera?
# Python crea una NUEVA variable local, no modifica la global.

total = 1000   # global

def resetear():
    total = 0  # crea una NUEVA variable local llamada 'total'
    print("  dentro de la funcion, total =", total)

resetear()
print("fuera de la funcion, total =", total)  # sigue siendo 1000
"""),

md(r"""
### La palabra clave `global` (úsala con moderación)

Si **realmente** necesitas modificar una variable global desde una función,
debes declararlo explícitamente con `global`. Pero en buena arquitectura,
las funciones **reciben datos por parámetros y devuelven resultados**: raramente
deberían tocar variables globales.

```python
contador = 0

def incrementar():
    global contador   # avisa que no crearemos una local
    contador += 1
```

> 💡 La regla práctica: **evita `global`**. Si sientes que lo necesitas, probablemente
> la solución sea pasar el valor como parámetro y devolver el nuevo valor.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

```python
x = 5
def f():
    x = 10
    return x
f()
print(x)
```

¿Qué imprime `print(x)`? ¿5 o 10? Traza en papel antes de ejecutar.
"""),

code(r"""
# Verificación del ejercicio anterior:
x = 5
def f():
    x = 10     # esta 'x' es local, NO modifica la global
    return x

resultado = f()
print("Resultado de f():", resultado)
print("x global sigue siendo:", x)   # 5, sin cambiar
"""),
]


# ===================================================================== #
# 10. FUNCIONES COMO VALORES
# ===================================================================== #
C += [
md(r"""
## 10. Funciones como valores: asignar y pasar como argumento

En Python, las funciones son **objetos de primera clase**: puedes asignarlas
a variables, meterlas en listas, y pasarlas como argumentos a otras funciones.
Esta idea es la base de `map()`, `filter()`, y de mucho código funcional.
"""),

code(r"""
# Una funcion es un objeto; puede asignarse a una variable.
def duplicar(x):
    return x * 2

def triplicar(x):
    return x * 3

# 'operacion' apunta al objeto-funcion (sin llamarla: sin parentesis)
operacion = duplicar
print("duplicar(5) =", operacion(5))   # 10

operacion = triplicar
print("triplicar(5) =", operacion(5))  # 15
"""),

code(r"""
# Pasar una función como argumento a otra función.
def aplicar_a_lista(lista, funcion):
    # Aplica funcion a cada elemento de lista y devuelve una nueva lista.
    resultado = []
    for x in lista:
        resultado.append(funcion(x))
    return resultado

precios = [100000, 250000, 89000]
con_iva = aplicar_a_lista(precios, lambda p: p * 1.19)
print("Precios con IVA:", con_iva)

# Pasamos diferentes funciones: el mismo esqueleto, comportamientos distintos.
def con_descuento_10(precio):
    return precio * 0.90

precios_rebajados = aplicar_a_lista(precios, con_descuento_10)
print("Precios con 10% descuento:", precios_rebajados)
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

¿Puedes meter funciones en una lista? Sí. ¿Para qué sirve eso?

```python
operaciones = [duplicar, triplicar, con_descuento_10]
for op in operaciones:
    print(op(50000))
```

Este patrón (lista de funciones) aparece en pipelines de procesamiento de datos:
aplicas una transformación tras otra. Lo verás explícitamente en la Clase 6.
"""),
]


# ===================================================================== #
# 11. LAMBDA, MAP, FILTER
# ===================================================================== #
C += [
md(r"""
## 11. Lambda: funciones anónimas de una línea

### Contexto
A veces necesitas una función muy simple, solo una vez, y ponerle nombre sería
verboso. Para eso existe `lambda`:

```
lambda parametros: expresion
```

Es equivalente a:
```python
def _(parametros):
    return expresion
```

No tiene cuerpo, no tiene nombre propio, no admite varias líneas. **Solo sirve
para transformaciones simples en una línea.**

### Cuándo usar lambda vs def

| Usa `lambda` | Usa `def` |
|---|---|
| Transformación de una línea | Lógica con varios pasos |
| Se usa una sola vez | Se reutiliza o se necesita probar |
| Como argumento de `map`/`filter` | Cualquier función con nombre propio |
"""),

code(r"""
# Lambda básica: calcular el IVA de un precio.
calcular_iva = lambda precio: precio * 0.19

print("IVA de $100.000:", calcular_iva(100000))
print("IVA de $250.000:", calcular_iva(250000))

# Lambda con dos parametros: total de una linea de pedido.
subtotal = lambda precio, cantidad: precio * cantidad

print("Subtotal (5 unidades a $12.000):", subtotal(12000, 5))
"""),

md(r"""
## 12. `map()` y `filter()`: aplicar funciones a colecciones

### `map(funcion, iterable)`

Aplica `funcion` a **cada elemento** del iterable y devuelve un iterador con
los resultados.

```
lista original:  [10, 20, 30]
        |  map(lambda x: x * 2)
        v
resultado:       [20, 40, 60]
```

### `filter(funcion, iterable)`

Devuelve solo los elementos para los cuales `funcion(elemento)` es `True`.

```
lista original:  [15, 200, 85, 500, 3]
        |  filter(lambda x: x > 100)
        v
resultado:       [200, 500]
```

> En Python 3, `map()` y `filter()` devuelven **iteradores** (perezosos, no
> calculan hasta que se piden). Envuelve con `list()` para materializarlos.
"""),

code(r"""
montos = [320000, 89000, 1500000, 43000, 780000, 250000]

# map: calcular el IVA de cada monto
ivas = list(map(lambda m: m * 0.19, montos))
print("Montos originales:", montos)
print("IVAs:             ", [int(i) for i in ivas])

# filter: solo montos que superan $200.000
grandes = list(filter(lambda m: m > 200000, montos))
print("Montos > $200.000:", grandes)
"""),

code(r"""
# Encadenar map y filter: montos grandes, y calcular su IVA.
resultado = list(map(
    lambda m: m * 0.19,
    filter(lambda m: m > 200000, montos)
))
print("IVA de los montos grandes:", [int(r) for r in resultado])

# Equivalente con list comprehension (otra forma valida, más legible para muchos):
resultado2 = [m * 0.19 for m in montos if m > 200000]
print("Con comprehension:        ", [int(r) for r in resultado2])
"""),

md(r"""
### Diagrama: el pipeline map/filter

```
montos = [320000, 89000, 1500000, 43000, 780000, 250000]
    |
    | filter(lambda m: m > 200000)
    v
[320000, 1500000, 780000, 250000]
    |
    | map(lambda m: m * 0.19)
    v
[60800, 285000, 148200, 47500]
```

Cada paso transforma la colección sin modificar la original. Este es el
corazón del **paradigma funcional**: transformaciones inmutables encadenadas.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

1. `filter(lambda x: x % 2 == 0, range(10))` — ¿qué devuelve?
2. `map(len, ["Bogota", "Cali", "Medellin"])` — ¿qué devuelve?
3. ¿Qué ventaja tiene `filter` sobre un bucle `for` con `if`?
   (En términos de código, son equivalentes. `filter` es más declarativo).
"""),
]


# ===================================================================== #
# 13. ERRORES COMUNES
# ===================================================================== #
C += [
md(r"""
## 13. Errores comunes

### Error 1: olvidar `return` (la función devuelve `None` en silencio)

```python
def calcular_total(lista):
    total = sum(lista)
    # Se olvidó el return: la función no devuelve nada explícito

resultado = calcular_total([100, 200])
print(resultado)   # None ← no es el 300 que esperabas
```

**Cura:** si una función debe producir un valor, siempre verifica que todas
las rutas de ejecución tengan un `return`.
"""),

code(r"""
# Demostración del error:
def sin_return(lista):
    total = sum(lista)   # calcula pero no devuelve

def con_return(lista):
    return sum(lista)

print("sin return:", sin_return([1, 2, 3]))   # None
print("con return:", con_return([1, 2, 3]))   # 6
"""),

md(r"""
### Error 2: mutar una lista mientras se recorre

```python
# MALO: modificar la lista que itera -> comportamiento impredecible
numeros = [1, 2, 3, 4, 5]
for n in numeros:
    if n % 2 == 0:
        numeros.remove(n)   # <- NUNCA hagas esto
```

**Cura:** recorre una copia o construye una nueva lista.
"""),

code(r"""
# Incorrecto: se salta elementos porque la lista se encoge mientras se itera.
numeros = [1, 2, 3, 4, 5, 6]
for n in numeros[:]:   # numeros[:] crea una copia
    pass               # iterar sobre la copia es seguro

# Correcto: filtrar con list comprehension o filter.
numeros = [1, 2, 3, 4, 5, 6]
impares = [n for n in numeros if n % 2 != 0]
print("Impares:", impares)
print("Original intacto:", numeros)
"""),

md(r"""
### Error 3: scope confuso — usar una variable antes de asignarla

```python
total = 100

def actualizar():
    total += 50   # Python ve 'total =' y la trata como local,
                  # pero 'total' no tiene valor local aún -> UnboundLocalError
```

**Cura:** pasa `total` como parámetro y devuelve el nuevo valor.

### Error 4: bucle infinito por condición que nunca se vuelve `False`

**Síntoma:** el programa se congela (spinning). **Cura:** siempre asegúrate
de que la variable de la condición cambia dentro del `while`.

### Error 5: `lambda` para lógica compleja

```python
# MALO: difícil de leer, de depurar y de probar
procesar = lambda x: x*0.19 if x > 0 else (0 if x == 0 else -x*0.19)

# BIEN: usa def cuando la lógica tiene ramas
def procesar(x):
    if x > 0:
        return x * 0.19
    elif x == 0:
        return 0
    else:
        return -x * 0.19
```
"""),
]


# ===================================================================== #
# 14. RESUMEN Y QUIZ
# ===================================================================== #
C += [
md(r"""
## 14. Resumen de la clase

| Concepto | En una frase |
|---|---|
| `for` | recorre una secuencia elemento a elemento |
| `while` | repite mientras una condición sea verdadera |
| `break` | sale del bucle inmediatamente |
| `continue` | salta al siguiente ciclo, omitiendo el resto del bloque |
| `else` (bucle) | se ejecuta si el bucle terminó sin `break` |
| Bucles anidados | un bucle dentro de otro; complejidad O(n×m) |
| `def` | define una función; los parámetros son locales |
| `return` | especifica la salida; sin `return` la función devuelve `None` |
| Parámetros por defecto | `def f(x, tasa=0.19)` |
| Argumentos por nombre | `f(precio=100, tasa=0.05)` |
| Scope | las variables locales no escapan de su función |
| Funciones como valores | `op = duplicar; op(5)` |
| `lambda` | función anónima de una línea |
| `map(f, lista)` | aplica `f` a cada elemento |
| `filter(f, lista)` | conserva los elementos donde `f` es `True` |
"""),

md(r"""
## Quiz de autoevaluación

Responde mentalmente antes de ejecutar la celda.

1. ¿Cuál es la diferencia entre `for` y `while`?
2. ¿Cuándo se ejecuta el bloque `else` de un bucle?
3. ¿Qué devuelve una función sin `return`?
4. ¿Qué hace `map(lambda x: x**2, [1,2,3,4])`?
5. ¿Por qué no puedes usar una variable local de `f()` fuera de `f()`?
"""),

code(r"""
respuestas = {
    1: ("'for' recorre una secuencia conocida; 'while' repite mientras "
        "una condicion sea True (numero de vueltas desconocido al inicio)."),
    2: ("El bloque 'else' de un bucle se ejecuta si el bucle termino "
        "normalmente (sin que se ejecutara un 'break')."),
    3: "None (Python devuelve None implicitamente si no hay return).",
    4: ("Devuelve un iterador con [1, 4, 9, 16]. "
        "Envuelve con list() para materializarlo."),
    5: ("Porque las variables locales tienen scope local: existen solo "
        "durante la ejecucion de la funcion y desaparecen al terminar."),
}
for k, v in respuestas.items():
    print(str(k) + ". " + v + "\n")
"""),

md(r"""
## Glosario de la Clase 3

| Término | Definición |
|---|---|
| **Bucle `for`** | estructura que recorre elemento a elemento una secuencia |
| **Bucle `while`** | estructura que repite un bloque mientras una condición sea True |
| **`break`** | sale del bucle actual inmediatamente |
| **`continue`** | salta a la siguiente iteración del bucle |
| **`else` de bucle** | bloque que se ejecuta si el bucle termina sin `break` |
| **Bucle anidado** | un bucle dentro de otro; complejidad multiplicativa |
| **Función** | bloque de código con nombre que recibe parámetros y devuelve un valor |
| **Parámetro** | variable local de la función que recibe un argumento |
| **`return`** | termina la función y entrega un valor al llamador |
| **Docstring** | cadena de documentación al inicio de una función |
| **Parámetro por defecto** | parámetro con valor preestablecido (`def f(x, n=5)`) |
| **Argumento por nombre** | argumento especificado como `f(x=10)` |
| **Scope local** | variables que solo existen dentro de una función |
| **Scope global** | variables del módulo/notebook, accesibles desde todas partes |
| **Lambda** | función anónima de una línea (`lambda x: x*2`) |
| **`map()`** | aplica una función a cada elemento de un iterable |
| **`filter()`** | conserva los elementos de un iterable que cumplen una condición |
| **Primera clase** | las funciones son objetos que se pueden asignar y pasar |

## Retos para practicar

1. **FizzBuzz extendido:** imprime 1..50, "Fizz" si divisible por 3, "Buzz" si
   por 5, "FizzBuzz" si por ambos, y "¡Premio!" si divisible por 7.
2. **Pipeline funcional:** dada una lista de precios, usa `filter` para quedarte
   con los que superan $100.000, luego `map` para aplicarles un descuento del 15%.
3. **Función recursiva (adelanto):** escribe `suma_recursiva(n)` que calcule
   1+2+…+n sin bucles. ¿Cuándo es mejor que el bucle?

---

➡️ **Siguiente paso**
- **practice01.ipynb** — 10 ejercicios de bucles y funciones.
- **practice02.ipynb** — pipeline de procesamiento de transacciones.
- **homework01.ipynb** y **homework02.ipynb** — tareas autocalificables.
"""),
]


# ===================================================================== #
# CELDAS ADICIONALES — insertar_despues para profundizar y alcanzar 80+ celdas
# ===================================================================== #

def insertar_despues(celdas, marcador_texto, nuevas):
    """Inserta 'nuevas' justo después de la primera celda cuyo source contiene 'marcador_texto'."""
    for i, c in enumerate(celdas):
        if marcador_texto in c.source:
            return celdas[: i + 1] + nuevas + celdas[i + 1 :]
    return celdas + nuevas


# --- Ampliación MOTIVACIÓN: contexto logístico completo --------------------
EXTRA_MOTIVACION = [
md(r"""
### Automatización real: procesar un lote de pedidos

Antes del bucle, una empresa de e-commerce necesitaba que alguien **manualmente**
actualizara el estado de cada pedido. Con 50 pedidos al día, eso son 50 copias
del mismo proceso. El bucle cambia radicalmente la escala posible.
"""),
code(r"""
pedidos = [
    {"id": "P001", "ciudad": "Bogota",      "monto": 320000, "estado": "pendiente"},
    {"id": "P002", "ciudad": "Medellin",    "monto": 89000,  "estado": "pendiente"},
    {"id": "P003", "ciudad": "Cali",        "monto": 540000, "estado": "pendiente"},
    {"id": "P004", "ciudad": "Barranquilla","monto": 43000,  "estado": "pendiente"},
]
ENVIO_GRATIS = 100000

for p in pedidos:
    iva = int(p["monto"] * 0.19)
    envio = 0 if p["monto"] >= ENVIO_GRATIS else 15000
    total = p["monto"] + iva + envio
    p["estado"] = "procesado"
    print("Pedido " + p["id"] + " | " + p["ciudad"].ljust(13) +
          " | Total: $" + "{:,}".format(total) + " | " + p["estado"])
"""),
]

# --- Ampliación FOR: iterar sobre pares con zip -----------------------------
EXTRA_FOR_ZIP = [
md(r"""
### 2.5 Iterar sobre dos listas a la vez: `zip()`

Cuando tienes dos listas relacionadas (como productos y precios), `zip()` las
empareja elemento a elemento. Equivale a "recorrer en paralelo".

```
productos = ["A", "B", "C"]
precios   = [100, 200, 300]
    |
    | zip(productos, precios)
    v
("A", 100), ("B", 200), ("C", 300)
```
"""),
code(r"""
sucursales = ["Bogota", "Medellin", "Cali", "Barranquilla"]
ventas_mes = [4500000, 3200000, 2800000, 1900000]
metas      = [5000000, 3000000, 3000000, 2000000]

print("Desempeno mensual:")
print("-" * 50)
for suc, real, meta in zip(sucursales, ventas_mes, metas):
    pct = real / meta * 100
    estado = "OK" if real >= meta else "BAJO META"
    print("  " + suc.ljust(14) + " {:.1f}%  {}".format(pct, estado))
"""),
]

# --- Ampliación WHILE: algoritmo de Euclides ----------------------------
EXTRA_WHILE_EUCLIDES = [
md(r"""
### El `while` en acción: algoritmo de Euclides (MCD)

El Máximo Común Divisor (MCD) de dos números se calcula con el algoritmo de
Euclides: mientras el segundo número no sea 0, reemplaza `(a, b)` por `(b, a % b)`.

No sabemos cuántas vueltas hará antes de que `b == 0` → `while` es la elección natural.

```
Traza: mcd(48, 18)
  a=48, b=18  →  (18, 48%18=12)
  a=18, b=12  →  (12, 18%12=6)
  a=12, b=6   →  (6,  12%6=0)
  a=6,  b=0   →  FIN, MCD=6
```
"""),
code(r"""
def mcd(a, b):
    # Maximo Comun Divisor por el algoritmo de Euclides.
    while b != 0:
        a, b = b, a % b   # intercambio atomico de Python
    return a

pares = [(48, 18), (100, 75), (13, 7), (252, 105)]
for a, b in pares:
    print("mcd(" + str(a) + ", " + str(b) + ") = " + str(mcd(a, b)))
"""),
]

# --- Ampliación FUNCIONES: docstrings y diseño defensivo -------------------
EXTRA_FUNCIONES_DISENO = [
md(r"""
### Diseño defensivo: validar la entrada en la función

Una función robusta verifica sus precondiciones al inicio. Este patrón evita
que errores silenciosos se propaguen lejos de donde ocurren.

```python
def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b
```

En ciencia de datos, la entrada suele venir de archivos CSV o bases de datos
y puede tener valores inesperados. Validar pronto ahorra depuración larga.
"""),
code(r"""
def tasa_crecimiento(valor_anterior, valor_actual):
    # Calcula la tasa de crecimiento porcentual entre dos valores.
    # Args: valor_anterior (no puede ser cero), valor_actual.
    # Returns: tasa como porcentaje (ej: 15.3 = 15.3%).
    if valor_anterior == 0:
        raise ValueError("valor_anterior no puede ser cero")
    return (valor_actual - valor_anterior) / valor_anterior * 100

ventas = [(800000, 920000), (1200000, 1080000), (500000, 575000)]
for ant, act in ventas:
    tasa = tasa_crecimiento(ant, act)
    signo = "+" if tasa >= 0 else ""
    print("  " + "{:>8,}".format(ant) + " -> " + "{:>8,}".format(act) +
          "   " + signo + "{:.1f}%".format(tasa))
"""),
]

# --- Ampliación LAMBDA: ordenar con key ------------------------------------
EXTRA_LAMBDA_SORT = [
md(r"""
### Lambda como `key` en ordenamiento

Uno de los usos más comunes de `lambda` es como argumento `key` de `sorted()` o
`list.sort()`. Permite ordenar por un criterio personalizado en una sola línea.

```python
# Ordenar por el segundo elemento de cada tupla:
datos = [("Ana", 4.5), ("Luis", 3.0), ("Sara", 4.9)]
sorted(datos, key=lambda par: par[1])
# -> [("Luis", 3.0), ("Ana", 4.5), ("Sara", 4.9)]
```
"""),
code(r"""
productos = [
    ("laptop",    2500000, 15),
    ("teclado",    120000, 80),
    ("monitor",    890000, 22),
    ("mouse",       45000, 120),
    ("ssd",        350000, 40),
]

# Ordenar por precio ascendente
por_precio = sorted(productos, key=lambda p: p[1])
print("Por precio (menor a mayor):")
for nombre, precio, stock in por_precio:
    print("  " + nombre.ljust(10) + " $" + "{:,}".format(precio))

print()

# Ordenar por valor de inventario (precio * stock) descendente
por_valor = sorted(productos, key=lambda p: p[1] * p[2], reverse=True)
print("Por valor de inventario (mayor a menor):")
for nombre, precio, stock in por_valor:
    print("  " + nombre.ljust(10) + " valor: $" + "{:,}".format(precio * stock))
"""),
]

# --- Ampliación: comprehensions vs map/filter comparación ------------------
EXTRA_COMPREHENSION = [
md(r"""
### Comprehensions vs map/filter: ¿cuál elegir?

Las **list comprehensions** y `map`/`filter` son dos formas de hacer lo mismo.
En Python moderno, las comprehensions son generalmente más legibles:

| Tarea | `map`/`filter` | Comprehension |
|---|---|---|
| Transformar | `list(map(f, lst))` | `[f(x) for x in lst]` |
| Filtrar | `list(filter(pred, lst))` | `[x for x in lst if pred(x)]` |
| Ambas | `list(map(f, filter(pred, lst)))` | `[f(x) for x in lst if pred(x)]` |

**Cuándo usar `map`/`filter`:** cuando ya tienes la función definida con nombre
y quieres dejar claro que es una transformación pura. En código funcional o
pipelines, resultan más explícitos.

**Cuándo usar comprehension:** para transformaciones ad-hoc, más legibles para
la mayoría de programadores Python.
"""),
code(r"""
montos = [320000, 89000, 1500000, 43000, 780000, 250000]

# Las tres formas son equivalentes:
# 1. map + filter
r1 = list(map(lambda m: round(m * 0.19), filter(lambda m: m > 200000, montos)))

# 2. comprehension
r2 = [round(m * 0.19) for m in montos if m > 200000]

# 3. bucle for explícito
r3 = []
for m in montos:
    if m > 200000:
        r3.append(round(m * 0.19))

print("map/filter:    ", r1)
print("comprehension: ", r2)
print("bucle for:     ", r3)
print("Son iguales:", r1 == r2 == r3)
"""),
]

# --- Ampliación: funciones de orden superior — patrón pipeline --------------
EXTRA_HOF = [
md(r"""
### Funciones de orden superior: el patrón pipeline de datos

Una **función de orden superior** es aquella que recibe o devuelve funciones.
`map`, `filter`, `sorted` son ejemplos de la biblioteca estándar.

El patrón **pipeline** encadena transformaciones: la salida de una es la entrada
de la siguiente. Es la base de pandas y de muchas bibliotecas de datos.

```
datos_crudos
    |  limpiar (filter)
    v
datos_limpios
    |  transformar (map)
    v
datos_transformados
    |  agregar (sum, max, etc.)
    v
resultado final
```
"""),
code(r"""
# Pipeline completo sobre transacciones de ejemplo.
transacciones = [
    {"ciudad": "Bogota",      "categoria": "tecnologia", "monto": 1500000},
    {"ciudad": "Medellin",    "categoria": "ropa",       "monto": 89000},
    {"ciudad": "Bogota",      "categoria": "tecnologia", "monto": 320000},
    {"ciudad": "Cali",        "categoria": "alimentos",  "monto": 43000},
    {"ciudad": "Bogota",      "categoria": "tecnologia", "monto": 780000},
    {"ciudad": "Barranquilla","categoria": "ropa",       "monto": 0},     # invalida
]

# Paso 1: filtrar invalidas y la ciudad objetivo
bogota_validas = list(filter(
    lambda t: t["ciudad"] == "Bogota" and t["monto"] > 0,
    transacciones
))

# Paso 2: extraer montos
montos_bogota = list(map(lambda t: t["monto"], bogota_validas))

# Paso 3: estadísticas
total = sum(montos_bogota)
promedio = total / len(montos_bogota) if montos_bogota else 0

print("Transacciones de Bogota (validas):", len(montos_bogota))
print("Total:    $" + "{:,}".format(total))
print("Promedio: $" + "{:,.0f}".format(promedio))
"""),
]

# --- Insertar bloques extra en posiciones estratégicas ---
C = insertar_despues(C, "no tiene sentido seguir procesando.", EXTRA_FOR_ZIP)
C = insertar_despues(C, "El bucle es la respuesta.", EXTRA_MOTIVACION)
C = insertar_despues(C, "el bucle infinite", EXTRA_WHILE_EUCLIDES)
C = insertar_despues(C, "Cuántas veces ejecutaría el bucle?", EXTRA_WHILE_EUCLIDES)
C = insertar_despues(C, "El tipo de interés fuera", EXTRA_WHILE_EUCLIDES)
C = insertar_despues(C, "retorno multiple", EXTRA_FUNCIONES_DISENO)
C = insertar_despues(C, "Retorno múltiple", EXTRA_FUNCIONES_DISENO)
C = insertar_despues(C, "lambda` para lógica compleja", EXTRA_LAMBDA_SORT)
C = insertar_despues(C, "lambda` para transformaciones", EXTRA_LAMBDA_SORT)
C = insertar_despues(C, "Son iguales:", EXTRA_HOF)
C = insertar_despues(C, "comprehension son", EXTRA_COMPREHENSION)
C = insertar_despues(C, "Comprehensions vs", EXTRA_COMPREHENSION)


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase03", "lecture.ipynb")
build(os.path.abspath(ruta), C)
