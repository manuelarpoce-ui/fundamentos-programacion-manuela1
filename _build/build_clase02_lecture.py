"""Construye curso/clase02/lecture.ipynb — Variables, tipos, operadores, condicionales."""
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
# Clase 2 · Variables, tipos de datos, operadores y condicionales

### Fundamentos de Programación para Ciencia de Datos

> *"Los datos son la materia prima; las variables son las etiquetas que les
> damos para poder trabajar con ellos."*

---

**Duración:** 3 horas · **Modalidad:** notebook interactivo

En la Clase 1 aprendimos a pensar algorítmicamente: a descomponer problemas,
trazar ejecuciones y escribir pseudocódigo. Ahora damos el siguiente paso:
**hacer que Python hable de números, texto y decisiones**.

Hoy aprenderemos qué tipos de datos existen en Python, cómo operarlos y cómo
hacer que nuestro código tome decisiones con `if/elif/else`. Al final de la
clase podrás traducir cualquier pseudocódigo de decisión a Python real.
"""),

md(r"""
## Mapa de la clase

| Bloque | Tiempo | Qué haremos |
|---|---|---|
| 1. Motivación | 15 min | De pseudocódigo a Python: el rol de las variables |
| 2. Tipos primitivos | 30 min | int, float, str, bool — representación en memoria |
| 3. Conversión de tipos | 20 min | int(), float(), str(), bool() — cuándo y por qué |
| 4. Operadores aritméticos | 25 min | +, -, *, /, //, %, ** con ejemplos financieros |
| 5. Operadores relacionales y lógicos | 25 min | ==, !=, <, >, and, or, not, tablas de verdad |
| 6. Precedencia de operadores | 15 min | Orden de evaluación y paréntesis |
| 7. Condicionales if/elif/else | 30 min | Traducción directa del pseudocódigo |
| 8. Operador ternario | 10 min | Expresión condicional en una línea |
| 9. Errores comunes y cierre | 20 min | Quiz, glosario y retos |

> 🧭 **Cómo usar este notebook:** lee cada celda de texto *antes* de ejecutar la
> que le sigue. Detente en cada bloque **🤔 ¿Qué pasaría si...?** e intenta
> responder antes de continuar.
"""),
]


# ===================================================================== #
# 1. MOTIVACIÓN  (15 min)
# ===================================================================== #
C += [
md(r"""
## 1. De pseudocódigo a Python: el rol de las variables

En la Clase 1 usamos variables en pseudocódigo sin pensarlo mucho:

```
precio ← 50000
descuento ← 0.08
precio_final ← precio * (1 - descuento)
MOSTRAR precio_final
```

Ahora vamos a entender qué significa eso *en Python real*, en términos de
memoria y tipos de datos.

**¿Qué es una variable en Python?**

Una variable es un **nombre** que apunta a un **objeto en memoria**. Cuando
escribes `precio = 50000`, Python:
1. Crea un objeto de tipo `int` con el valor `50000` en algún lugar de la memoria.
2. Hace que el nombre `precio` apunte a ese objeto.

```
   nombre          objeto en memoria
   ┌─────────┐        ┌──────────────┐
   │  precio │ ──────▶│  int: 50000  │
   └─────────┘        └──────────────┘
```

Esta distinción importa porque Python es un lenguaje de **tipado dinámico**:
el tipo lo lleva el objeto, no el nombre. La misma variable puede apuntar
a un entero ahora y a un texto después.
"""),

code(r"""
# Tipado dinámico en acción: una misma variable, distintos tipos.
precio = 50000
print(type(precio), precio)   # <class 'int'>

precio = "cincuenta mil"
print(type(precio), precio)   # <class 'str'>

# Esto NO es un error en Python. En Java o C++ sí lo sería.
# Más adelante veremos cuándo esto puede ser un problema.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- ¿Qué pasa si asignas `precio = "50000"` (con comillas) y luego intentas
  calcular `precio * 1.08`? ¿Python lo rechaza o hace algo inesperado?
- ¿Por qué crees que Python permite cambiar el tipo de una variable? ¿Qué
  ventajas y qué riesgos tiene?

Antes de responder, pensemos qué tipos de datos maneja Python.
"""),
]


# ===================================================================== #
# 2. TIPOS PRIMITIVOS  (30 min)
# ===================================================================== #
C += [
md(r"""
## 2. Los cuatro tipos primitivos de Python

Python tiene cuatro tipos de datos *primitivos* o *atómicos*: los que no se
descomponen en partes más simples. Todo lo demás (listas, diccionarios,
objetos) son combinaciones de estos.

| Tipo | Nombre Python | Para qué sirve | Ejemplos |
|---|---|---|---|
| Entero | `int` | contar, indexar, años, cantidades | `0`, `42`, `-3`, `2024` |
| Decimal | `float` | precios, tasas, medidas | `3.14`, `1.5e6`, `-0.001` |
| Texto | `str` | nombres, categorías, mensajes | `"Bogota"`, `'tarjeta'` |
| Booleano | `bool` | flags, condiciones, resultados | `True`, `False` |

> 💡 En ciencia de datos, el tipo más traicionero es `str`: los datos que
> llegan de CSV, bases de datos o APIs vienen *casi siempre* como texto,
> aunque representen números. Veremos cómo convertirlos.
"""),

md(r"""
### 2a. Enteros (`int`)

Los `int` en Python son de **precisión arbitraria**: pueden ser tan grandes
como permita la memoria. No hay desbordamiento como en C.

```
Cómo Python almacena 42 (simplificado):
   ┌────────────────────────────┐
   │  objeto int                │
   │  valor: 42                 │
   │  tipo: int                 │
   └────────────────────────────┘
```
"""),

code(r"""
# Ejemplos de int en finanzas y logística.
precio_unitario = 85000        # precio de un producto (COP)
cantidad        = 12           # unidades en inventario
anio_ingreso    = 2019         # año como entero
codigo_producto = 1047         # ID de producto

total = precio_unitario * cantidad
print("Total del pedido:   $", total)
print("Tipo de 'total':    ", type(total))
print()

# Python maneja enteros muy grandes sin problema:
poblacion_colombia = 51_000_000    # guión bajo como separador visual (Python 3.6+)
print("Población aprox.:", poblacion_colombia)
print("¿Es int?         :", isinstance(poblacion_colombia, int))
"""),

md(r"""
### 2b. Decimales (`float`)

Los `float` usan representación **IEEE 754 de doble precisión** (64 bits).
Esto significa que pueden representar números con hasta ~15 dígitos
significativos, pero con limitaciones de precisión conocidas.

> ⚠️ Un resultado famoso: en Python `0.1 + 0.2` no es exactamente `0.3`. No es
> un bug: es una consecuencia de cómo los decimales se guardan en binario. En
> aplicaciones financieras se usa el módulo `decimal` para dinero exacto.
> Para el curso, `float` es suficiente.
"""),

code(r"""
# Decimales en contexto financiero.
tasa_iva    = 0.19          # 19% de IVA en Colombia
precio_base = 125000.0      # precio sin IVA
tasa_interes = 1.5e-2       # 1.5% mensual (notación científica)

print("IVA (19%):", precio_base * tasa_iva)
print("Precio con IVA:", precio_base * (1 + tasa_iva))
print()

# La famosa sorpresa de los flotantes:
print("0.1 + 0.2 =", 0.1 + 0.2)                  # no es exactamente 0.3
print("0.1 + 0.2 == 0.3 es", 0.1 + 0.2 == 0.3)   # False (!)
print("Diferencia:", (0.1 + 0.2) - 0.3)            # ~5.5e-17 (ruido de precisión)
"""),

md(r"""
### 2c. Cadenas de texto (`str`)

Un `str` es una **secuencia inmutable de caracteres Unicode**. Se puede
definir con comillas simples, dobles o triples. En ciencia de datos es el
tipo que más necesita conversión y limpieza.

```
"Bogota"  →  secuencia de caracteres: B-o-g-o-t-a
posición:                             0-1-2-3-4-5
```
"""),

code(r"""
# Cadenas en contexto de negocio.
ciudad      = "Bogota"
categoria   = 'tecnologia'
descripcion = """Laptop gamer
con 16 GB RAM"""          # str multilínea con triple comilla

print("Ciudad:     ", ciudad)
print("Categoría:  ", categoria)
print("Descripción:", descripcion)
print()

# Operaciones básicas (más en la Clase 4):
print("Largo del nombre:", len(ciudad))                    # longitud
print("En mayúsculas:   ", ciudad.upper())                 # transformar
print("¿Empieza con B?: ", ciudad.startswith("B"))         # buscar
print("Ciudad + país:   ", ciudad + ", Colombia")          # concatenar
"""),

md(r"""
### 2d. Booleanos (`bool`)

`True` y `False` son los únicos valores booleanos. En Python, `bool` es
subclase de `int`: `True == 1` y `False == 0`, lo que da algunos trucos
útiles (y algunas sorpresas).

Los booleanos son el resultado de comparaciones y expresiones lógicas.
Son la **base de todas las decisiones** (`if`, `while`, `and`, `or`).
"""),

code(r"""
# Booleanos: resultados de comparaciones.
monto         = 450000
es_mayorista  = monto > 200000     # True
tiene_descuento = False

print("¿Es venta mayorista?   ", es_mayorista,    type(es_mayorista))
print("¿Tiene descuento?      ", tiene_descuento, type(tiene_descuento))
print()

# Truco: True y False son 1 y 0 (subclase de int).
aprobados = [True, True, False, True, False]
print("Total aprobados (suma de True):", sum(aprobados))   # 3

# Operación con bool como int:
print("True + True =", True + True)     # 2 (!)
print("True * 5    =", True * 5)        # 5
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

1. ¿Cuál es el tipo de `type(True)`? ¿Qué devuelve `isinstance(True, int)`?
2. ¿Qué pasaría si intentas hacer `"100" + 200`? ¿Y `"100" * 3`?
3. ¿Cómo comprobarías que el tipo de una variable es `float`?

Ejecuta la celda siguiente para descubrirlo:
"""),

code(r"""
# Explorando los tipos.
print("type(True)          =", type(True))
print("isinstance(True, int)=", isinstance(True, int))
print()

# Operaciones mixtas: Python es estricto con str + int:
try:
    resultado = "100" + 200
except TypeError as e:
    print("Error al sumar str + int:", e)

# Pero str * int sí funciona (repetición de cadena):
print('"ha" * 3 =', "ha" * 3)     # "hahaha"
print()

# Comprobar si es float:
tasa = 0.19
print("isinstance(tasa, float):", isinstance(tasa, float))
"""),
]


# ===================================================================== #
# 3. CONVERSIÓN DE TIPOS (type casting)  (20 min)
# ===================================================================== #
C += [
md(r"""
## 3. Conversión de tipos (type casting)

En ciencia de datos, los datos casi siempre llegan *con el tipo incorrecto*:
los CSV traen todo como `str`, los formularios web también. Saber convertir
tipos es una habilidad del día a día.

Python ofrece cuatro conversores explícitos:

| Función | Convierte a | Ejemplo | Resultado |
|---|---|---|---|
| `int(x)` | entero | `int("42")` | `42` |
| `float(x)` | decimal | `float("1.5")` | `1.5` |
| `str(x)` | texto | `str(99)` | `"99"` |
| `bool(x)` | booleano | `bool(0)` | `False` |

### ¿Cuándo convertir?

1. **Leer datos de CSV** → convertir texto a número para operar.
2. **Mostrar resultados** → convertir número a texto para concatenar.
3. **Comparar condiciones** → convertir a bool para usarlo en `if`.
"""),

code(r"""
# Caso de uso real: datos de un formulario de venta.
# Todo llega como str (texto), necesitamos operar con ellos.

precio_str   = "85000"      # precio leído de un CSV
cantidad_str = "12"         # cantidad leída de un formulario
tasa_str     = "0.08"       # descuento leído como texto

# Convertimos antes de operar:
precio   = int(precio_str)
cantidad = int(cantidad_str)
tasa     = float(tasa_str)

subtotal  = precio * cantidad
descuento = subtotal * tasa
total     = subtotal - descuento

print("Subtotal:  $" + str(subtotal))
print("Descuento: $" + str(descuento))
print("Total:     $" + str(total))
"""),

md(r"""
### Reglas de `bool()`: qué es "falso" en Python

Python tiene una convención potente: casi cualquier valor se puede evaluar
como booleano. Esta lista se llama **valores falsy**:

| Valor | bool() |
|---|---|
| `0`, `0.0` | `False` |
| `""` (cadena vacía) | `False` |
| `None` | `False` |
| `[]`, `{}`, `()` (colecciones vacías) | `False` |

**Todo lo demás** es `True` (truthy): cualquier número distinto de cero,
cualquier cadena no vacía, cualquier colección no vacía.
"""),

code(r"""
# Demostración de valores falsy:
print("bool(0)    =", bool(0))        # False
print("bool(0.0)  =", bool(0.0))      # False
print("bool('')   =", bool(''))       # False (cadena vacía)
print("bool(None) =", bool(None))     # False
print()
print("bool(1)    =", bool(1))        # True
print("bool(-99)  =", bool(-99))      # True (cualquier no-cero)
print("bool('0')  =", bool('0'))      # True (¡cadena '0' NO es vacía!)
print("bool([])   =", bool([]))       # False (lista vacía)
print("bool([0])  =", bool([0]))      # True (lista con un elemento)
"""),

md(r"""
### Errores comunes de conversión

No toda conversión es posible: si el texto no se puede interpretar como
número, Python lanza `ValueError`.
"""),

code(r"""
# Qué pasa cuando la conversión falla:

# Esto funciona:
print(int("42"))
print(float("3.14"))

# Esto falla con ValueError:
try:
    int("cuarenta y dos")
except ValueError as e:
    print("Error con int('cuarenta y dos'):", e)

try:
    int("3.14")      # un float como str no se puede convertir directo a int
except ValueError as e:
    print("Error con int('3.14'):", e)

# La forma correcta para un float representado como str -> int:
valor = int(float("3.14"))
print("int(float('3.14')) =", valor)   # 3 (trunca)
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

1. ¿Qué devuelve `int(True)` e `int(False)`? ¿Tiene sentido?
2. ¿`float("1e3")` funciona? ¿Cuánto vale?
3. Si tienes `monto = "450 000"` (con espacio), ¿`int(monto)` funciona?
   ¿Cómo lo limpiarías antes? (pista: `.replace(" ", "")`)
"""),

code(r"""
# Respuestas a los retos anteriores:
print("int(True)  =", int(True))    # 1
print("int(False) =", int(False))   # 0
print()
print("float('1e3') =", float("1e3"))   # 1000.0
print()
monto_sucio = "450 000"
monto_limpio = int(monto_sucio.replace(" ", ""))
print("Monto limpiado:", monto_limpio)
"""),
]


# ===================================================================== #
# 4. OPERADORES ARITMÉTICOS  (25 min)
# ===================================================================== #
C += [
md(r"""
## 4. Operadores aritméticos

Python hereda la aritmética estándar y añade dos operadores muy usados en
programación:

| Operador | Nombre | Ejemplo | Resultado |
|---|---|---|---|
| `+` | suma | `1000 + 200` | `1200` |
| `-` | resta | `5000 - 800` | `4200` |
| `*` | multiplicación | `3 * 50000` | `150000` |
| `/` | división real | `7 / 2` | `3.5` (siempre float) |
| `//` | división entera | `7 // 2` | `3` (trunca) |
| `%` | módulo (residuo) | `7 % 2` | `1` |
| `**` | potencia | `2 ** 10` | `1024` |

Los dos más novedosos son `//` (división entera) y `%` (módulo). Los viste
en el algoritmo del cajero en la Clase 1; hoy los entendemos a fondo.
"""),

code(r"""
# Aritmetica básica con contexto financiero.
precio_base = 350000
cantidad    = 3
tasa_iva    = 0.19
tasa_desc   = 0.05

subtotal       = precio_base * cantidad
descuento      = subtotal * tasa_desc
base_gravable  = subtotal - descuento
iva            = base_gravable * tasa_iva
total          = base_gravable + iva

print("Subtotal:      ${:,.0f}".format(subtotal))
print("Descuento (5%): ${:,.0f}".format(descuento))
print("Base gravable: ${:,.0f}".format(base_gravable))
print("IVA (19%):     ${:,.0f}".format(iva))
print("TOTAL:         ${:,.0f}".format(total))
"""),

md(r"""
### División entera `//` y módulo `%`

Estos dos operadores son complementarios: juntos descomponen una división
en su cociente y residuo.

```
dividendo = divisor * cociente + residuo
   7       =    2   *    3     +    1

   Python:  7 // 2 = 3  (cociente)
            7 % 2  = 1  (residuo)
```

**Usos prácticos en finanzas y negocios:**
- `//` → convertir totales a unidades mayores (segundos a horas, pesos a billetes)
- `%` → saber el sobrante, detectar paridad, calcular ciclos
"""),

code(r"""
# Uso 1: descomponer un tiempo en horas, minutos y segundos.
segundos_totales = 9753

horas   = segundos_totales // 3600
resto   = segundos_totales % 3600
minutos = resto // 60
segs    = resto % 60

print("{} segundos = {}h {}m {}s".format(segundos_totales, horas, minutos, segs))

print()

# Uso 2: repartir unidades en cajas (un problema de logística).
unidades_pedido = 250
por_caja = 12

cajas_completas = unidades_pedido // por_caja
sobrante        = unidades_pedido % por_caja

print("Pedido de {} unidades en cajas de {}:".format(unidades_pedido, por_caja))
print("  {} cajas completas + {} unidades sueltas".format(cajas_completas, sobrante))

print()

# Uso 3: ¿es un número par? (el más clásico)
for n in [4, 7, 100, 33]:
    paridad = "par" if n % 2 == 0 else "impar"
    print("{}  ->  {}".format(n, paridad))
"""),

md(r"""
### Potencia `**` e interés compuesto

El operador `**` calcula potencias. En finanzas tiene una aplicación directa:
el cálculo de **interés compuesto**.

```
Capital final = Capital inicial × (1 + tasa)^periodos
```
"""),

code(r"""
# Interés compuesto: cuánto crece un capital con el tiempo.
capital_inicial = 1_000_000    # 1 millón de pesos
tasa_mensual    = 0.015        # 1.5% mensual
periodos        = 12           # 12 meses

capital_final = capital_inicial * (1 + tasa_mensual) ** periodos
ganancia      = capital_final - capital_inicial

print("Capital inicial:  ${:,.0f}".format(capital_inicial))
print("Tasa mensual:      {:.1%}".format(tasa_mensual))
print("Periodos:          {} meses".format(periodos))
print("Capital final:    ${:,.0f}".format(capital_final))
print("Ganancia:         ${:,.0f}".format(ganancia))
print("Rendimiento total: {:.2%}".format(ganancia / capital_inicial))
"""),

md(r"""
### Trazado de ejecución — verificando la aritmética

Antes de confiar en un cálculo complejo, traza los valores intermedios.
Practiquemos con el cálculo de precio con IVA y descuento:

```
precio_base = 120000
descuento   = precio_base * 0.10  = 12000
neto        = precio_base - descuento = 108000
iva         = neto * 0.19          = 20520
total       = neto + iva           = 128520
```

| Paso | Variable | Operación | Valor |
|---|---|---|---|
| 1 | `precio_base` | — | 120000 |
| 2 | `descuento` | 120000 × 0.10 | 12000.0 |
| 3 | `neto` | 120000 − 12000 | 108000.0 |
| 4 | `iva` | 108000 × 0.19 | 20520.0 |
| 5 | `total` | 108000 + 20520 | 128520.0 |
"""),

code(r"""
# Verificamos el trazado:
precio_base = 120000
descuento   = precio_base * 0.10
neto        = precio_base - descuento
iva         = neto * 0.19
total       = neto + iva

print("precio_base =", precio_base)
print("descuento   =", descuento)
print("neto        =", neto)
print("iva         =", iva)
print("total       =", total)
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

1. ¿Cuánto es `10 / 3` vs `10 // 3` vs `10 % 3`? Traza cada uno.
2. ¿`-7 // 2` es `-3` o `-4`? Python redondea hacia **abajo** (hacia −∞),
   no hacia cero. Verifica y reflexiona.
3. ¿Qué pasaría si divides `5 / 0`? ¿Y `5 // 0`?
"""),

code(r"""
# División y sus variantes:
print("10 / 3  =", 10 / 3)    # 3.333...
print("10 // 3 =", 10 // 3)   # 3 (piso)
print("10 % 3  =", 10 % 3)    # 1

print()
# División entera con negativos:
print("-7 // 2 =", -7 // 2)   # -4 (no -3): Python redondea hacia -inf
print("-7 % 2  =", -7 % 2)    # 1  (residuo siempre >= 0 con divisor positivo)

print()
# División por cero:
try:
    resultado = 5 / 0
except ZeroDivisionError as e:
    print("ZeroDivisionError:", e)
"""),
]


# ===================================================================== #
# 5. OPERADORES RELACIONALES Y LÓGICOS  (25 min)
# ===================================================================== #
C += [
md(r"""
## 5. Operadores relacionales y lógicos

### 5a. Operadores relacionales

Comparan dos valores y devuelven `True` o `False`. Son la **base de toda
decisión** en programación.

| Operador | Significado | Ejemplo | Resultado |
|---|---|---|---|
| `==` | igual a | `5 == 5` | `True` |
| `!=` | distinto de | `5 != 3` | `True` |
| `<` | menor que | `3 < 5` | `True` |
| `>` | mayor que | `3 > 5` | `False` |
| `<=` | menor o igual | `5 <= 5` | `True` |
| `>=` | mayor o igual | `6 >= 5` | `True` |

> ⚠️ **Error clásico:** confundir `=` (asignación) con `==` (comparación).
> `precio = 50000` guarda el valor. `precio == 50000` pregunta si es igual.
"""),

code(r"""
# Comparaciones en contexto de negocio.
monto_venta  = 350000
umbral_mayor = 200000
umbral_desc  = 150000
stock_actual = 0

# Comparaciones que generan True o False:
es_venta_grande  = monto_venta > umbral_mayor
aplica_descuento = monto_venta >= umbral_desc
sin_stock        = stock_actual == 0
stock_normal     = stock_actual != 0

print("¿Es venta grande?    ", es_venta_grande)
print("¿Aplica descuento?   ", aplica_descuento)
print("¿Sin stock?          ", sin_stock)
print("¿Stock normal?       ", stock_normal)
"""),

md(r"""
### 5b. Operadores lógicos: `and`, `or`, `not`

Combinan condiciones booleanas para formar expresiones más complejas.

| Operador | Descripción | Ejemplo | Resultado |
|---|---|---|---|
| `and` | verdadero si **ambas** son True | `True and False` | `False` |
| `or` | verdadero si **al menos una** es True | `True or False` | `True` |
| `not` | invierte el valor | `not True` | `False` |

### Tablas de verdad

```
  A       B      A and B    A or B    not A
─────   ─────   ─────────  ────────  ──────
True    True     True       True      False
True    False    False      True      False
False   True     False      True      True
False   False    False      False     True
```
"""),

code(r"""
# Lógica combinada en un sistema de crédito simplificado.
ingresos_mensuales = 3_500_000
score_crediticio   = 720
deuda_existente    = False
monto_solicitado   = 10_000_000

# Condiciones individuales:
ingreso_suficiente = ingresos_mensuales >= 2_000_000
buen_score         = score_crediticio >= 700
sin_deuda          = not deuda_existente
monto_razonable    = monto_solicitado <= ingresos_mensuales * 5

# Decisión combinada:
aprobado = ingreso_suficiente and buen_score and sin_deuda and monto_razonable

print("Ingresos suficientes: ", ingreso_suficiente)
print("Buen score:           ", buen_score)
print("Sin deuda:            ", sin_deuda)
print("Monto razonable:      ", monto_razonable)
print()
print("Credito APROBADO:", aprobado)
"""),

md(r"""
### Cortocircuito: Python no evalúa más de lo necesario

Con `and`, si la primera condición es `False`, Python **no evalúa** la segunda
(porque el resultado ya es `False` pase lo que pase).

Con `or`, si la primera condición es `True`, Python **no evalúa** la segunda.

Esto se llama **evaluación perezosa** o **cortocircuito** (*short-circuit*).
Es importante cuando la segunda condición es costosa o puede fallar.

```
Cortocircuito con and:
  False and (cualquier_cosa)  →  False  (no evalúa el segundo)

Cortocircuito con or:
  True  or  (cualquier_cosa)  →  True   (no evalúa el segundo)
```
"""),

code(r"""
# Demostración de cortocircuito.
# La función division_peligrosa lanza un error si denominador es 0.
def division_peligrosa(a, b):
    return a / b   # ZeroDivisionError si b == 0

denominador = 0

# SIN cortocircuito (evaluaría ambos lados):
# if True and division_peligrosa(10, denominador):   # fallaría

# CON cortocircuito (and): si la izquierda es False, no se evalúa la derecha:
if denominador != 0 and division_peligrosa(10, denominador) > 1:
    print("Resultado positivo")
else:
    print("Denominador es cero; division_peligrosa NO fue llamada (cortocircuito).")

# CON cortocircuito (or): si la izquierda es True, no se evalúa la derecha:
ciudad_valida = True
if ciudad_valida or division_peligrosa(10, denominador) > 0:
    print("Condicion satisfecha sin evaluar el segundo operando.")
"""),

md(r"""
### Comparaciones encadenadas

Python permite comparaciones encadenadas, muy legibles:

```python
10 <= edad < 65   # equivale a: 10 <= edad and edad < 65
```

Esto es idiomático en Python y más claro que dos condiciones separadas.
"""),

code(r"""
# Comparaciones encadenadas: rangos de forma natural.
def clasificar_temperatura(grados):
    if grados < 0:
        return "congelacion"
    elif 0 <= grados < 10:
        return "muy frio"
    elif 10 <= grados < 20:
        return "frio"
    elif 20 <= grados < 30:
        return "templado"
    else:
        return "calor"

for t in [-5, 5, 15, 25, 35]:
    print("{}°C  ->  {}".format(t, clasificar_temperatura(t)))
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

1. ¿Qué devuelve `"a" == "A"`? ¿Las comparaciones de cadenas son sensibles
   a mayúsculas?
2. ¿Qué devuelve `1 == True`? ¿Y `0 == False`? (recuerda que `bool` es
   subclase de `int`).
3. ¿`None == False`? ¿`None == 0`? ¿Cómo se compara correctamente con `None`?
"""),

code(r"""
# Comparaciones sorprendentes:
print('"a" == "A":', "a" == "A")     # False (sensible a mayúsculas)
print('"a" == "a":', "a" == "a")     # True

print()
print("1 == True: ", 1 == True)      # True  (True es 1)
print("0 == False:", 0 == False)     # True  (False es 0)
print("2 == True: ", 2 == True)      # False (True solo es 1)

print()
print("None == False:", None == False)   # False
print("None == 0:    ", None == 0)       # False
print("None is None: ", None is None)    # True  (la forma correcta)
# 'is' compara identidad (mismo objeto en memoria), no igualdad de valor.
"""),
]


# ===================================================================== #
# 6. PRECEDENCIA DE OPERADORES  (15 min)
# ===================================================================== #
C += [
md(r"""
## 6. Precedencia de operadores

Cuando una expresión mezcla varios operadores, Python sigue un orden de
evaluación (como las matemáticas con "primero multiplicación que suma").

**Orden de mayor a menor precedencia (simplificado):**

```
1. Paréntesis          ()
2. Potencia            **
3. Signo unario        -x, +x
4. Multiplicación      *, /, //, %
5. Suma y resta        +, -
6. Comparaciones       ==, !=, <, >, <=, >=
7. not
8. and
9. or
```

**Regla práctica:** cuando tengas dudas, usa **paréntesis**. Son gratuitos
en términos de rendimiento y hacen el código más claro.
"""),

code(r"""
# Precedencia en acción: mismos números, distintos resultados.
print("2 + 3 * 4    =", 2 + 3 * 4)     # 14 (no 20): * antes que +
print("(2 + 3) * 4  =", (2 + 3) * 4)   # 20: paréntesis primero
print()

# Error clásico: calcular el promedio de dos precios.
precio_a = 80000
precio_b = 120000

# MAL: la división ocurre antes que la suma.
promedio_mal = precio_a + precio_b / 2
# BIEN: paréntesis fuerzan la suma primero.
promedio_ok  = (precio_a + precio_b) / 2

print("Promedio MAL:", promedio_mal)   # 140000 (incorrecto)
print("Promedio OK: ", promedio_ok)    # 100000 (correcto)
print()

# Precedencia con lógica:
monto = 180000
tiene_tarjeta = True

# ¿Se aplica descuento? (>150000 Y tiene tarjeta) O (>300000)
aplica_1 = monto > 150000 and tiene_tarjeta or monto > 300000  # ambiguo
aplica_2 = (monto > 150000 and tiene_tarjeta) or monto > 300000  # explícito
print("Con paréntesis explícitos:", aplica_2)
"""),

md(r"""
### Reglas de oro para expresiones complejas

1. **Usa paréntesis** cuando la precedencia no sea obvia.
2. **Divide expresiones largas** en varias variables intermedias.
3. **Traza** la expresión si no estás seguro del orden.

```python
# En lugar de esto:
total = precio * cantidad * (1 - descuento) * (1 + iva)

# Esto es más trazable:
subtotal      = precio * cantidad
neto          = subtotal * (1 - descuento)
total         = neto * (1 + iva)
```
"""),

code(r"""
# Demostración: una sola línea vs. variables intermedias.
precio    = 50000
cantidad  = 5
descuento = 0.10
iva       = 0.19

# Una línea (difícil de depurar):
total_linea = precio * cantidad * (1 - descuento) * (1 + iva)

# Con variables intermedias (fácil de trazar):
subtotal = precio * cantidad
neto     = subtotal * (1 - descuento)
total_v  = neto * (1 + iva)

print("Total en una linea:   ${:,.2f}".format(total_linea))
print("Total con variables:  ${:,.2f}".format(total_v))
print("Son iguales:          ", abs(total_linea - total_v) < 0.01)
"""),
]


# ===================================================================== #
# 7. CONDICIONALES if/elif/else  (30 min)
# ===================================================================== #
C += [
md(r"""
## 7. Condicionales `if / elif / else`

El `if` de Python es la traducción directa del `SI ... ENTONCES ... SINO`
del pseudocódigo. Es la estructura que permite a un programa **elegir un
camino** según los datos.

### Sintaxis

```python
if condicion_1:
    # bloque si condicion_1 es True
elif condicion_2:
    # bloque si condicion_1 es False Y condicion_2 es True
else:
    # bloque si ninguna condicion anterior fue True
```

> 📐 En Python la **indentación** (sangría) define los bloques. El estándar
> es **4 espacios**. No hay `FIN_SI` ni llaves: el fin del bloque lo marca
> que dejamos de indentar.
"""),

md(r"""
### Ejemplo completo: clasificación de ventas

Apliquemos la metodología de los 6 pasos.

**1. Contexto:** una tienda quiere etiquetar cada venta como "baja", "media"
o "alta" para reportes.

**2. Solución intuitiva:** según el monto, elegimos la etiqueta.

**3. Algoritmo:**
1. Si monto > 200000 → etiqueta "alta"
2. Si no, pero monto > 50000 → etiqueta "media"
3. Si no → etiqueta "baja"

**4. Pseudocódigo:**
```
SI monto > 200000 ENTONCES
    categoria ← "alta"
SINO SI monto > 50000 ENTONCES
    categoria ← "media"
SINO
    categoria ← "baja"
FIN_SI
```
"""),

code(r"""
# 5. Python: traducción directa del pseudocódigo.

def clasificar_venta(monto):
    """Clasifica una venta por su monto en COP."""
    if monto > 200000:
        return "alta"
    elif monto > 50000:
        return "media"
    else:
        return "baja"

# Prueba con varios montos:
montos_prueba = [310000, 89000, 12000, 200000, 200001]
for m in montos_prueba:
    print("${:>8,}  ->  {}".format(m, clasificar_venta(m)))
"""),

md(r"""
### Trazado de la función `clasificar_venta`

| monto | ¿m > 200000? | ¿m > 50000? | Resultado |
|---|---|---|---|
| 310000 | True | — | "alta" |
| 89000 | False | True | "media" |
| 12000 | False | False | "baja" |
| 200000 | False (200000 no es > 200000) | True | "media" |
| 200001 | True | — | "alta" |

> 🔎 Nota el caso borde: `200000` cae en "media" porque la condición es
> estrictamente mayor (`>`). Si quisieras que `200000` fuera "alta", usarías
> `monto >= 200000`.
"""),

code(r"""
# 6. Análisis: verificamos con los 5 casos del trazado.
assert clasificar_venta(310000) == "alta"
assert clasificar_venta(89000)  == "media"
assert clasificar_venta(12000)  == "baja"
assert clasificar_venta(200000) == "media"   # borde estricto
assert clasificar_venta(200001) == "alta"
print("Todos los casos del trazado son correctos.")
"""),

md(r"""
### Ejemplo 2: descuento escalonado

En muchos comercios el descuento **aumenta con el monto**. Este patrón
de decisiones escalonadas se llama **branching en cascada**.

**Reglas de negocio:**
- monto > 500000 → descuento del 15%
- monto > 200000 → descuento del 8%
- monto > 100000 → descuento del 3%
- monto <= 100000 → sin descuento
"""),

code(r"""
def calcular_precio_final(precio_original):
    """Aplica descuento escalonado según el monto."""
    if precio_original > 500000:
        pct = 0.15
    elif precio_original > 200000:
        pct = 0.08
    elif precio_original > 100000:
        pct = 0.03
    else:
        pct = 0.00

    descuento = precio_original * pct
    precio_final = precio_original - descuento
    return precio_original, pct, descuento, precio_final

# Tabla de resultados:
print("{:<12} {:>8} {:>12} {:>12}".format("Original", "Descuento", "Valor desc.", "Final"))
print("-" * 50)
for monto in [80000, 150000, 250000, 600000]:
    orig, pct, desc, final = calcular_precio_final(monto)
    print("${:<10,} {:>7.0%} {:>12,.0f} {:>12,.0f}".format(orig, pct, desc, final))
"""),

md(r"""
### Ejemplo 3: año bisiesto

Un caso clásico de lógica anidada con `and` y `or`.

**Regla:** un año es bisiesto si:
- Es divisible por 4, **Y**
- Si es divisible por 100, **también** debe ser divisible por 400.

Esto cubre los casos especiales: 1900 (divisible por 100 pero no por 400 →
no bisiesto) y 2000 (divisible por 400 → bisiesto).
"""),

code(r"""
def es_bisiesto(anio):
    """Determina si un año es bisiesto según las reglas del calendario gregoriano."""
    if anio % 400 == 0:
        return True
    elif anio % 100 == 0:
        return False
    elif anio % 4 == 0:
        return True
    else:
        return False

# Casos de prueba con explicación:
casos = [(2000, True), (1900, False), (2024, True), (2023, False), (2100, False)]
for anio, esperado in casos:
    resultado = es_bisiesto(anio)
    marca = "OK" if resultado == esperado else "ERROR"
    print("{}: {}  [{}]".format(anio, resultado, marca))
"""),

md(r"""
### Diagrama de flujo para `es_bisiesto`

```
        ╭─────────╮
        │  INICIO │
        ╰────┬────╯
             ▼
      ◇ anio % 400 == 0 ◇
        sí │       │ no
           ▼       ▼
        True    ◇ anio % 100 == 0 ◇
                  sí │       │ no
                     ▼       ▼
                   False  ◇ anio % 4 == 0 ◇
                            sí │    │ no
                               ▼    ▼
                            True  False
```

Este diagrama muestra por qué el orden de las condiciones **importa**: si
revisáramos `% 4` antes que `% 100`, el año 1900 erróneamente sería
"bisiesto".
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

1. ¿Qué devuelve `clasificar_venta(0)`? ¿Y `clasificar_venta(-500)`? ¿Tiene
   sentido que montos negativos sean "bajos"?
2. En la función de descuento, ¿qué pasa si cambias todos los `elif` por
   `if`? ¿Cambia el resultado? ¿Por qué?
3. ¿Puedes reescribir `es_bisiesto` usando una sola expresión booleana con
   `and` y `or`?
"""),

code(r"""
# Reto 3: es_bisiesto en una línea.
def es_bisiesto_v2(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

# Verificamos que da los mismos resultados:
casos = [2000, 1900, 2024, 2023, 2100, 1600]
for a in casos:
    assert es_bisiesto(a) == es_bisiesto_v2(a)
print("Ambas versiones coinciden en todos los casos.")
"""),
]


# ===================================================================== #
# 8. OPERADOR TERNARIO  (10 min)
# ===================================================================== #
C += [
md(r"""
## 8. Operador ternario (expresión condicional)

Python tiene una forma compacta de escribir un `if/else` simple en una sola
línea, cuando el resultado es una expresión (no un bloque de código):

```python
valor_si_true if condicion else valor_si_false
```

Este es el **operador ternario** o **expresión condicional**. Es equivalente
a:

```python
if condicion:
    resultado = valor_si_true
else:
    resultado = valor_si_false
```

> ✅ Úsalo para asignaciones simples. Si el bloque tiene más de una línea o
> la lógica es compleja, prefiere el `if/else` tradicional: es más legible.
"""),

code(r"""
# Ternario: asignar una etiqueta según una condición.
monto = 350000

# Versión if/else:
if monto > 200000:
    etiqueta = "mayorista"
else:
    etiqueta = "minorista"

# Versión ternaria (equivalente):
etiqueta2 = "mayorista" if monto > 200000 else "minorista"

print("Con if/else:   ", etiqueta)
print("Con ternario:  ", etiqueta2)
print("Son iguales:   ", etiqueta == etiqueta2)

# Otro ejemplo: calcular comisión del agente de ventas.
ventas = 5_200_000
comision = ventas * 0.05 if ventas >= 5_000_000 else ventas * 0.03
print()
print("Ventas: ${:,.0f}  -> Comision: ${:,.0f}".format(ventas, comision))
"""),

code(r"""
# Ternario encadenado (con moderación: puede volverse ilegible).
nota = 3.7

# Tres posibilidades: reprobado, aprobado, excelente.
estado = "excelente" if nota >= 4.5 else ("aprobado" if nota >= 3.0 else "reprobado")
print("Nota {}: {}".format(nota, estado))

# Comparar con if/elif/else para ver la diferencia de legibilidad:
if nota >= 4.5:
    estado2 = "excelente"
elif nota >= 3.0:
    estado2 = "aprobado"
else:
    estado2 = "reprobado"

print("Mismo resultado:", estado == estado2)
print("Para 3 ramas, el if/elif/else suele ser mas legible.")
"""),
]


# ===================================================================== #
# 9. ERRORES COMUNES  (parte del cierre)
# ===================================================================== #
C += [
md(r"""
## 9. Errores comunes con variables, tipos y condicionales

Estos errores le ocurren a todos al empezar (y a veces a los veteranos).
Reconocerlos vale más que memorizarlos.

**1. Usar `=` en lugar de `==` en una condición**

```python
if precio = 50000:   # SyntaxError: no es posible asignar dentro de if
    ...
```

Python protege de este error con un `SyntaxError`.

**2. Comparar tipos incompatibles**

```python
"50000" > 40000   # TypeError en Python 3
```

Siempre convierte antes de comparar.

**3. Dividir entre cero sin validar**

```python
promedio = total / n   # ZeroDivisionError si n == 0
```

Siempre valida el denominador antes de dividir.

**4. Olvidar que `//` trunca hacia abajo (no hacia cero) con negativos**

**5. Confiar en la precisión exacta de los `float`**

Para dinero exacto: usa `round()` o el módulo `decimal`.
"""),

code(r"""
# Demostraciones de los errores comunes:

# Error 2: comparar str con int:
try:
    resultado = "50000" > 40000
except TypeError as e:
    print("TypeError:", e)

# Error 3: división por cero:
try:
    promedio = 0 / 0
except ZeroDivisionError as e:
    print("ZeroDivisionError:", e)

# Error 4: // con negativos (ya lo vimos, pero vale repetir):
print()
print("Truncamiento de //:  7 // 2 =", 7 // 2)    # 3
print("Hacia -inf con neg: -7 // 2 =", -7 // 2)   # -4 (no -3)

# Error 5: imprecision de float:
total_factura = 0.1 + 0.1 + 0.1
print()
print("0.1 * 3 exacto?  : 0.1+0.1+0.1 =", total_factura)
print("round(total, 10) =", round(total_factura, 10))   # 0.3 tras redondear
"""),
]


# ===================================================================== #
# 10. RESUMEN + QUIZ + RETOS
# ===================================================================== #
C += [
md(r"""
## 10. Resumen de la clase

| Concepto | En una frase |
|---|---|
| **int, float, str, bool** | los cuatro tipos primitivos; cada uno tiene su representación en memoria |
| **Tipado dinámico** | el tipo lo lleva el objeto, no la variable; puede cambiar |
| **Type casting** | `int()`, `float()`, `str()`, `bool()` convierten entre tipos |
| **Operadores aritméticos** | `+`, `-`, `*`, `/`, `//`, `%`, `**`; cuidado con `/` vs `//` |
| **Módulo `%`** | residuo de la división entera; clave para paridad y ciclos |
| **Operadores relacionales** | producen `True/False`; la base de toda decisión |
| **Operadores lógicos** | `and`, `or`, `not`; tablas de verdad; cortocircuito |
| **Precedencia** | `**` > `*/%` > `+-` > comparaciones > `not` > `and` > `or` |
| **if / elif / else** | traducción directa del pseudocódigo; la indentación es el bloque |
| **Operador ternario** | `x if cond else y`; para asignaciones simples de dos caminos |

### Lo más importante que te llevas

> **Convierte antes de operar, valida antes de dividir, y usa paréntesis
> cuando la precedencia no sea obvia.**
"""),

md(r"""
## Quiz de autoevaluación

Responde mentalmente y ejecuta la celda para comprobar.

1. ¿Cuánto vale `7 // 2` y `7 % 2`?
2. ¿Por qué `0.1 + 0.2 != 0.3` en Python?
3. ¿Qué devuelve `bool("")`? ¿Y `bool("False")`?
4. ¿Cuál es la diferencia entre `=` y `==`?
5. En `a and b`, si `a` es `False`, ¿Python evalúa `b`? ¿Por qué?
"""),

code(r"""
respuestas = {
    1: "7 // 2 = 3 (division entera, trunca hacia abajo); 7 % 2 = 1 (residuo).",
    2: ("Los float usan IEEE 754 binario: 0.1 no tiene representacion exacta. "
        "El resultado tiene un error de ~5.5e-17."),
    3: ("bool('') = False (cadena vacia es falsy). "
        "bool('False') = True (la cadena 'False' NO es vacia; cualquier str no vacio es truthy)."),
    4: ("'=' es asignacion: guarda un valor en una variable. "
        "'==' es comparacion: devuelve True si los valores son iguales."),
    5: ("No evalua 'b' (cortocircuito/evaluacion perezosa): "
        "si 'a' es False, 'a and b' ya es False sin importar 'b'."),
}
for k, v in respuestas.items():
    print("{}. {}".format(k, v))
    print()
"""),

md(r"""
## Retos para practicar

Antes de los notebooks de práctica, intenta estos en papel:

1. **Tipos.** ¿Cuál es el tipo de `type(3 + 2.0)`? ¿Por qué Python "promovió"
   el resultado a `float`?
2. **Operadores.** Escribe una expresión que calcule cuántos días faltan para
   que un contrato de `n` meses llegue a 1 año. Usa solo aritmética.
3. **Condicionales.** Escribe el pseudocódigo y luego el Python para: dada
   una nota de 0 a 5, devolver `"reprobado"` si < 3.0, `"aprobado"` si
   3.0 ≤ nota < 4.0, `"bueno"` si 4.0 ≤ nota < 4.5, `"excelente"` si >= 4.5.
4. **Borde.** En el ejercicio anterior, ¿qué devuelve tu función con `-1` o
   con `6.0`? ¿Debería validarse la entrada?

---

### ➡️ Siguiente paso

- **practice01.ipynb** — 10 ejercicios graduales sobre tipos, operadores y condicionales.
- **practice02.ipynb** — análisis de un dataset de transacciones financieras.
- **homework01.ipynb** y **homework02.ipynb** — tareas autocalificables.
"""),
]


# ===================================================================== #
# CELDAS ADICIONALES — insertar_despues para alcanzar 80+ celdas
# ===================================================================== #

def insertar_despues(celdas, marcador_texto, nuevas):
    """Inserta 'nuevas' justo después de la primera celda que contiene 'marcador_texto'."""
    for i, c in enumerate(celdas):
        if marcador_texto in c.source:
            return celdas[: i + 1] + nuevas + celdas[i + 1 :]
    return celdas + nuevas


# --- Extra: representación en memoria de los tipos ---
EXTRA_MEMORIA = [
md(r"""
### Cómo Python representa los tipos en memoria

Aunque no necesitamos gestionar la memoria manualmente, entender cómo
Python organiza los objetos ayuda a evitar sorpresas.

```
  Tipo    | Ejemplo     | Tamaño en memoria (aprox.)
  --------|-------------|-----------------------------
  int     | 42          | 28 bytes (objeto Python base)
  float   | 3.14        | 24 bytes
  bool    | True        | 28 bytes (es subclase de int)
  str     | "hola"      | 49 + 1 byte por carácter
```

En Python, **todo es un objeto**. Incluso un simple `42` es un objeto con
su tipo, su contador de referencias y su valor. Esto hace que Python sea
flexible pero más lento que C (donde `42` ocupa solo 4 bytes).

Para conjuntos grandes de datos numéricos, **NumPy** usa arreglos de C
por dentro, ganando velocidad y eficiencia. Lo veremos en la Clase 5.
"""),

code(r"""
import sys

# Cuanto 'pesa' cada tipo en Python:
print("sys.getsizeof(42):      ", sys.getsizeof(42), "bytes")
print("sys.getsizeof(3.14):   ", sys.getsizeof(3.14), "bytes")
print("sys.getsizeof(True):   ", sys.getsizeof(True), "bytes")
print("sys.getsizeof('hola'): ", sys.getsizeof('hola'), "bytes")
print("sys.getsizeof(''):     ", sys.getsizeof(''), "bytes")
print()
# Un int en Python pesa ~28 bytes; en C pestaría 4 u 8 bytes.
# Por eso, para millones de numeros, NumPy es hasta 10x mas eficiente.
print("¿Por que NumPy? Porque un entero Python es ~7x mas grande que en C.")
"""),
]

# --- Extra: asignación múltiple y convenciones de nombres ---
EXTRA_ASIGNACION = [
md(r"""
### Asignación múltiple y convenciones de nombres

Python ofrece formas convenientes de asignar varias variables a la vez:

```python
# Asignación múltiple en una línea:
a, b, c = 1, 2, 3

# Intercambio sin variable auxiliar (¡muy idiomático!):
a, b = b, a

# Asignar el mismo valor a varias variables:
x = y = z = 0
```

**Convenciones de nombres (PEP 8):**

| Caso | Convención | Ejemplo |
|---|---|---|
| Variables y funciones | snake_case | `precio_base`, `calcular_iva` |
| Constantes | MAYÚSCULAS | `TASA_IVA`, `MAX_INTENTOS` |
| Clases | PascalCase | `ProductoFinanciero` |

El nombre importa: `p = 120000` dice poco; `precio_base = 120000` dice todo.
"""),

code(r"""
# Asignacion multiple en contexto de negocio.
precio_cop, tasa_usd, tasa_eur = 120000, 4200.0, 4600.0

precio_usd = precio_cop / tasa_usd
precio_eur = precio_cop / tasa_eur

print("Precio COP: ${:,.0f}".format(precio_cop))
print("Precio USD: ${:,.2f}".format(precio_usd))
print("Precio EUR: €{:,.2f}".format(precio_eur))

print()

# Intercambio de valores: caso clásico en algoritmos de ordenamiento.
stock_tienda_a = 150
stock_tienda_b = 80

print("Antes:  A={}, B={}".format(stock_tienda_a, stock_tienda_b))
stock_tienda_a, stock_tienda_b = stock_tienda_b, stock_tienda_a
print("Despues: A={}, B={}".format(stock_tienda_a, stock_tienda_b))
"""),
]

# --- Extra: cadenas de texto avanzadas (formato) ---
EXTRA_FORMAT = [
md(r"""
### Formatear cadenas: del `+` al `.format()` al f-string

Python tiene varias formas de combinar texto con variables. En el curso
usamos principalmente **f-strings** (Python 3.6+), que son los más legibles:

```python
nombre = "Bogota"
ventas = 1350000

# Concatenación clásica (incómoda, requiere str()):
"Ventas en " + nombre + ": $" + str(ventas)

# .format() (compatible con versiones antiguas):
"Ventas en {}: ${}".format(nombre, ventas)

# f-string (recomendado):
f"Ventas en {nombre}: ${ventas:,.0f}"
```

Los **especificadores de formato** controlan cómo se muestra el número:
- `{:,.0f}` → separador de miles, sin decimales
- `{:.2%}` → porcentaje con 2 decimales
- `{:>10}` → alineado a la derecha en 10 caracteres
"""),

code(r"""
# Comparacion de estilos de formateo.
ciudad  = "Medellin"
ventas  = 2_350_000
tasa    = 0.192

# Los tres estilos producen el mismo resultado:
s1 = "Ventas en " + ciudad + ": $" + str(ventas)
s2 = "Ventas en {}: ${}".format(ciudad, ventas)
s3 = "Ventas en {}: ${:,.0f}".format(ciudad, ventas)

print(s1)
print(s2)
print(s3)
print()

# Tabla formateada con especificadores:
datos = [("Bogota", 3_200_000), ("Medellin", 2_350_000), ("Cali", 1_870_000)]
print("{:<12} {:>14}".format("Ciudad", "Ventas (COP)"))
print("-" * 28)
for c, v in datos:
    print("{:<12} {:>14,.0f}".format(c, v))
"""),
]

# --- Extra: operadores de asignación compuesta ---
EXTRA_COMPUESTA = [
md(r"""
### Operadores de asignación compuesta

Python tiene atajos para actualizar variables:

| Operador | Equivale a | Ejemplo |
|---|---|---|
| `x += n` | `x = x + n` | `total += precio` |
| `x -= n` | `x = x - n` | `stock -= cantidad` |
| `x *= n` | `x = x * n` | `capital *= (1 + tasa)` |
| `x /= n` | `x = x / n` | `precio /= 2` |
| `x //= n` | `x = x // n` | `horas //= 60` |
| `x %= n` | `x = x % n` | `resto %= divisor` |
| `x **= n` | `x = x ** n` | `base **= exponente` |

Son exactamente equivalentes a la forma larga; son solo una convención.
"""),

code(r"""
# Operadores compuestos en un ciclo de ventas del mes.
inventario  = 500
ventas_dia  = [12, 8, 15, 20, 5, 18, 9]
ingreso_total = 0
precio_unidad = 35000

for v in ventas_dia:
    inventario    -= v              # descontar del inventario
    ingreso_total += v * precio_unidad   # acumular ingreso

print("Ventas del mes:", sum(ventas_dia), "unidades")
print("Inventario restante:", inventario)
print("Ingreso total: ${:,.0f}".format(ingreso_total))
"""),
]

# --- Extra: None y la ausencia de valor ---
EXTRA_NONE = [
md(r"""
### `None`: la ausencia de valor

`None` es el objeto especial de Python que representa **"ningún valor"** o
**"aún no definido"**. Es de tipo `NoneType` y es único (hay un solo `None`
en memoria).

**Cuándo aparece `None`:**
- Cuando una función no tiene `return` explícito.
- Como valor por defecto para indicar "no aplica".
- Para inicializar variables antes de asignarles un valor real.

**Cómo comparar con `None`:**

```python
# Forma correcta: usar 'is' o 'is not'
if resultado is None:
    ...

# Evitar '==' con None (funciona pero es menos idiomático):
if resultado == None:   # funciona, pero PEP 8 prefiere 'is'
    ...
```
"""),

code(r"""
# None en el contexto de una función que puede fallar.

def dividir_seguro(a, b):
    """Devuelve a/b, o None si b es cero."""
    if b == 0:
        return None    # señal explícita de 'no se puede calcular'
    return a / b

resultados = [(10, 2), (5, 0), (100, 4)]
for a, b in resultados:
    r = dividir_seguro(a, b)
    if r is None:
        print("{}/{} = [indefinido: division por cero]".format(a, b))
    else:
        print("{}/{} = {:.2f}".format(a, b, r))
"""),
]

# --- Extra: glosario clase 2 ---
EXTRA_GLOSARIO = [
md(r"""
## Glosario de la Clase 2

| Término | Definición breve |
|---|---|
| **Tipo de dato** | categoría que define qué valores puede tomar una variable y qué operaciones admite |
| **int** | entero de precisión arbitraria; para contar y operar sin decimales |
| **float** | número decimal IEEE 754; para medidas, tasas y precios aproximados |
| **str** | cadena de texto unicode; para nombres, categorías y mensajes |
| **bool** | `True` o `False`; resultado de comparaciones; subclase de `int` |
| **Tipado dinámico** | el tipo lo lleva el objeto, no la variable; puede cambiar |
| **Type casting** | conversión explícita entre tipos con `int()`, `float()`, `str()`, `bool()` |
| **Falsy** | valores que Python evalúa como `False`: `0`, `0.0`, `""`, `None`, colecciones vacías |
| **Módulo (`%`)** | residuo de la división entera; `7 % 2 = 1` |
| **División entera (`//`)** | cociente entero, trunca hacia abajo; `7 // 2 = 3` |
| **Cortocircuito** | `and` no evalúa el segundo si el primero es `False`; `or` no evalúa si el primero es `True` |
| **Precedencia** | orden en que Python evalúa operadores; los paréntesis la anulan |
| **if / elif / else** | estructura condicional; la indentación define los bloques |
| **Operador ternario** | `x if cond else y`; asignación condicional en una línea |
| **None** | ausencia de valor; único objeto de tipo `NoneType`; comparar con `is` |
"""),
]

# Insertar bloques extra en posiciones estratégicas:
C = insertar_despues(C, "La misma variable puede apuntar", EXTRA_ASIGNACION)
C = insertar_despues(C, "cinco tipos de datos primitivos", EXTRA_MEMORIA)
C = insertar_despues(C, "La forma correcta para un float", EXTRA_NONE)
C = insertar_despues(C, "Operaciones básicas (más en la Clase 4):", EXTRA_FORMAT)
C = insertar_despues(C, "Operadores de asignación compuesta", EXTRA_COMPUESTA)


# --- Extra: más ejemplos de condicionales con contexto real ---
EXTRA_COND_REAL = [
md(r"""
### Ejemplo adicional: clasificar IMC

El **Índice de Masa Corporal** (IMC) es un indicador de salud usado en
medicina, seguros y app de bienestar.

```
IMC = peso_kg / altura_m²

< 18.5 → "bajo peso"
18.5 - 24.99 → "normal"
25 - 29.99 → "sobrepeso"
>= 30 → "obesidad"
```
"""),

code(r"""
def clasificar_imc(peso_kg, altura_m):
    """Calcula e interpreta el IMC."""
    if altura_m <= 0:
        return None, "Error: altura debe ser positiva"
    imc = peso_kg / (altura_m ** 2)

    if imc < 18.5:
        categoria = "bajo peso"
    elif imc < 25:
        categoria = "normal"
    elif imc < 30:
        categoria = "sobrepeso"
    else:
        categoria = "obesidad"

    return round(imc, 1), categoria

# Prueba con varios perfiles:
perfiles = [(55, 1.70), (80, 1.75), (90, 1.65), (120, 1.72)]
print("{:<6} {:<8} {:>6} {:<12}".format("Peso", "Altura", "IMC", "Categoria"))
print("-" * 36)
for peso, altura in perfiles:
    imc, cat = clasificar_imc(peso, altura)
    print("{:<6} {:<8} {:>6} {:<12}".format(peso, altura, imc, cat))
"""),

md(r"""
### Ejemplo adicional: conversión de temperatura

Las conversiones entre escalas son ejercicios clásicos de operadores
aritméticos y tipos numéricos.

```
Celsius a Fahrenheit:  F = C × (9/5) + 32
Celsius a Kelvin:      K = C + 273.15
```
"""),

code(r"""
def convertir_temperatura(celsius):
    """Convierte Celsius a Fahrenheit y Kelvin."""
    fahrenheit = celsius * (9 / 5) + 32
    kelvin     = celsius + 273.15
    return fahrenheit, kelvin

# Tabla de conversiones:
print("{:>8} {:>12} {:>10}".format("Celsius", "Fahrenheit", "Kelvin"))
print("-" * 34)
for c in [-10, 0, 20, 37, 100]:
    f, k = convertir_temperatura(c)
    print("{:>8.1f} {:>12.1f} {:>10.2f}".format(c, f, k))
"""),
]

C = insertar_despues(C, "Ambas versiones coinciden en todos los casos.", EXTRA_COND_REAL)
C = insertar_despues(C, "Para 3 ramas, el if/elif/else suele ser mas legible.", EXTRA_GLOSARIO)


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase02", "lecture.ipynb")
build(os.path.abspath(ruta), C)
