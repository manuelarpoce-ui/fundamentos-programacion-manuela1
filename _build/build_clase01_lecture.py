"""Construye curso/clase01/lecture.ipynb — Pensamiento algorítmico y pseudocódigo."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []  # lista de celdas


# ===================================================================== #
# 0. PORTADA Y MOTIVACIÓN  (20 min)
# ===================================================================== #
C += [
md(r"""
# Clase 1 · Pensamiento algorítmico y pseudocódigo

### Fundamentos de Programación para Ciencia de Datos

> *"La programación no se trata de teclear, se trata de pensar."* — Rich Hickey (parafraseado)

---

**Duración:** 3 horas · **Modalidad:** notebook interactivo

En esta primera clase **casi no vamos a hablar de Python**. Suena raro en un
curso de programación, ¿verdad? Pero hay una razón poderosa: el cuello de
botella de un buen programador rara vez es el lenguaje. Es la **claridad de
pensamiento**. Si sabes *exactamente* qué pasos resuelven un problema, traducirlos
a Python (o a R, o a Java) es casi mecánico. Si no lo sabes, ningún lenguaje te
salvará.

Hoy aprenderemos a **pensar como un algoritmo**: a descomponer un problema, a
escribir la solución en un lenguaje intermedio (pseudocódigo) y solo al final a
implementarla. Y, ya que vamos camino a la ciencia de datos, mediremos cuánto
"cuesta" cada solución.
"""),

md(r"""
## Mapa de la clase

| Bloque | Tiempo | Qué haremos |
|---|---|---|
| 1. Motivación | 20 min | Por qué pensar antes de programar |
| 2. Teoría con ejemplos | 40 min | Qué es un algoritmo, entrada/proceso/salida, las 3 estructuras |
| 3. Pseudocódigo | 35 min | Convenciones, diagramas de flujo, trazado de ejecución |
| 4. Implementación | 45 min | Del pseudocódigo a Python: máximo, búsqueda, conteo |
| 5. Ejercicios guiados | 20 min | Resolvemos juntos |
| 6. Cierre y quiz | 20 min | Errores comunes, resumen, autoevaluación |

> 🧭 **Cómo usar este notebook:** lee cada celda de texto *antes* de ejecutar la
> celda de código que le sigue. Detente en cada bloque **🤔 ¿Qué pasaría si...?**
> e intenta responder mentalmente antes de continuar.
"""),

md(r"""
## 1. Un acertijo para empezar

Imagina que te doy una guía telefónica de papel de 1.000 páginas (sí, eso
existía) y te pido encontrar el número de **"Zuluaga, Andrés"**.

Tienes dos estrategias:

**Estrategia A** — Empiezas en la página 1 y vas pasando hoja por hoja hasta
encontrarlo.

**Estrategia B** — Abres por la mitad. Como "Zuluaga" empieza por Z, sabes que
está en la segunda mitad. Te quedas con esa mitad y la vuelves a partir por la
mitad. Repites.

Las dos estrategias **funcionan**. Las dos te dan la respuesta correcta. Pero su
*costo* es radicalmente distinto. Y esa diferencia, multiplicada por millones de
datos, es la diferencia entre un programa que responde en 1 segundo y uno que
tarda una hora.

Ese es el corazón de esta clase: **un mismo problema admite muchos algoritmos, y
no todos cuestan lo mismo.**
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

- ¿...la guía **no** estuviera ordenada alfabéticamente? ¿Cuál de las dos
  estrategias dejaría de funcionar?
- ¿...buscaras "Aguirre, Ana" en vez de "Zuluaga"? ¿La estrategia A sería rápida
  por casualidad? ¿Eso la hace mejor?

Guarda tus respuestas. Volveremos a este acertijo al final, cuando sepamos
*medir* algoritmos.
"""),
]


# ===================================================================== #
# 2. TEORÍA: QUÉ ES UN ALGORITMO  (40 min)
# ===================================================================== #
C += [
md(r"""
## 2. ¿Qué es un algoritmo, en serio?

Olvida por un momento la palabra "computadora". Un **algoritmo** es simplemente:

> Una **secuencia finita de pasos no ambiguos** que, partiendo de unas
> **entradas**, produce una **salida** y **termina**.

Lo usas todos los días sin darte cuenta:

- Una **receta** de cocina (entrada: ingredientes → salida: un plato).
- Las **instrucciones para llegar** a un lugar (entrada: punto de partida → salida: estar ahí).
- El **procedimiento para pagar** en una tienda.

La palabra viene de *al-Juarismi*, un matemático persa del siglo IX. Mucho antes
de los computadores, la humanidad ya escribía algoritmos.
"""),

md(r"""
### Las cuatro propiedades de un buen algoritmo

No cualquier lista de pasos es un algoritmo. Debe cumplir:

| Propiedad | Significa que... | Ejemplo de violación |
|---|---|---|
| **Finitud** | termina después de un número finito de pasos | "sigue revolviendo para siempre" |
| **Precisión** | cada paso es no ambiguo | "agrega *un poco* de sal" (¿cuánto?) |
| **Entrada definida** | se sabe qué recibe (0 o más entradas) | usar un ingrediente que nunca se mencionó |
| **Salida definida** | produce al menos un resultado | una receta que no dice qué obtienes |

> 💡 La **precisión** es la que más cuesta a los humanos. Estamos acostumbrados a
> instrucciones vagas porque otro humano "rellena los huecos". Una computadora
> **no rellena huecos**: hace exactamente lo que dices, incluso si es absurdo.
"""),

md(r"""
### El modelo Entrada → Proceso → Salida (EPS)

Casi todo programa, por grande que sea, encaja en este esquema mental:

```
        ┌─────────────┐
ENTRADA │             │ SALIDA
───────▶│   PROCESO   │───────▶
 datos  │ (algoritmo) │ resultado
        └─────────────┘
```

- **Entrada:** los datos con los que trabajas (una lista de ventas, una imagen, un texto).
- **Proceso:** las transformaciones que aplicas (sumar, filtrar, ordenar, contar).
- **Salida:** lo que entregas (un promedio, una gráfica, una decisión).

En ciencia de datos lo verás constantemente: *entran* datos crudos y *sale*
conocimiento. Acostúmbrate a preguntarte siempre: **¿cuál es la entrada, cuál es
la salida, y qué proceso las conecta?**
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Para el problema *"calcular el promedio de las notas de un curso"*, identifica:

1. ¿Cuál es la **entrada**?
2. ¿Cuál es la **salida**?
3. ¿Qué pasaría si la lista de notas está **vacía**? ¿El algoritmo sigue siendo
   "finito" y "con salida definida"?

El tercer punto es justo el tipo de "hueco" que los humanos rellenamos sin pensar
y que rompe los programas. Lo retomaremos.
"""),

md(r"""
## La metodología del curso: 6 pasos, siempre

Cada problema que enfrentemos seguirá **la misma secuencia**. No es un capricho:
es la forma de no perderte cuando el problema sea difícil.

```
  1. CONTEXTO            ¿Qué me están pidiendo, en palabras?
        │
        ▼
  2. SOLUCIÓN INTUITIVA  ¿Cómo lo resolvería yo, a mano?
        │
        ▼
  3. ALGORITMO           Los pasos, ordenados y sin ambigüedad
        │
        ▼
  4. PSEUDOCÓDIGO        Esos pasos en un formato semi-formal
        │
        ▼
  5. PYTHON              La traducción a código ejecutable
        │
        ▼
  6. ANÁLISIS            ¿Es correcto? ¿Cuánto cuesta? ¿Se puede mejorar?
```

> Los principiantes saltan directo al paso 5. Por eso se atascan. Nosotros
> haremos los 6 pasos, una y otra vez, hasta que se vuelva un reflejo.
"""),
]


# ===================================================================== #
# 3. PSEUDOCÓDIGO  (35 min)
# ===================================================================== #
C += [
md(r"""
## 3. Pseudocódigo: el puente entre la idea y el código

El **pseudocódigo** es una forma de escribir un algoritmo a medio camino entre el
español y un lenguaje de programación. No tiene reglas oficiales estrictas: la
única regla real es que **cualquier programador lo pueda leer y traducir a su
lenguaje favorito**.

¿Por qué molestarnos en escribirlo si al final usaremos Python?

- Te obliga a **pensar la lógica** sin pelear con la sintaxis (los `:`, los
  paréntesis, la indentación...).
- Es **independiente del lenguaje**: el mismo pseudocódigo sirve para Python, Java o R.
- Es la forma en que los equipos **discuten** soluciones en una pizarra.
"""),

md(r"""
### Convenciones que usaremos en el curso

No memorices una sintaxis rígida; usa estas palabras clave con sentido común:

| Intención | Pseudocódigo |
|---|---|
| Asignar un valor | `x ← 5`  (la flecha significa "guarda 5 en x") |
| Leer / recibir | `LEER edad` |
| Mostrar / entregar | `MOSTRAR resultado` |
| Decisión | `SI condicion ENTONCES ... SINO ... FIN_SI` |
| Repetición conocida | `PARA i DESDE 1 HASTA n HACER ... FIN_PARA` |
| Repetición condicional | `MIENTRAS condicion HACER ... FIN_MIENTRAS` |
| Recorrer una colección | `PARA CADA elemento EN lista HACER ... FIN_PARA` |

> ✍️ Usaremos **MAYÚSCULAS** para las palabras clave y **sangría** para mostrar
> qué pasos están "dentro" de un SI o de un PARA. La sangría no es decorativa:
> comunica estructura.
"""),

md(r"""
### Las tres estructuras de control (y solo tres)

Un teorema precioso de la informática (Böhm–Jacopini, 1966) dice que **cualquier
algoritmo imaginable** se puede construir combinando solo tres formas de
organizar los pasos:

**1. Secuencia** — un paso tras otro, de arriba a abajo.

```
paso A
paso B
paso C
```

**2. Decisión (selección)** — elegir un camino según una condición.

```
        ┌─ ¿condición? ─┐
       sí               no
        │                │
     hacer X          hacer Y
        └──────┬─────────┘
               ▼
```

**3. Repetición (iteración)** — repetir pasos mientras se cumpla algo.

```
   ┌──────────────┐
   ▼              │
 ¿seguir? ──sí──▶ hacer algo
   │
   no
   ▼
```

Todo lo demás —por complejo que parezca un programa— son estas tres piezas
anidadas y combinadas. Hoy las veremos a nivel conceptual; en las clases 2 y 3
las escribiremos en Python con todo detalle.
"""),

md(r"""
### Diagramas de flujo

Un **diagrama de flujo** dibuja el algoritmo. Símbolos básicos:

```
  ╭─────────╮     inicio / fin
  ╰─────────╯

  ┌─────────┐     proceso (un paso, una acción)
  └─────────┘

  ◇─────────◇     decisión (pregunta sí/no)

  ▱─────────▱     entrada / salida de datos
```

Ejemplo — *"¿el número es par o impar?"*:

```
        ╭────────╮
        │ INICIO │
        ╰────┬───╯
             ▼
       ▱ LEER n ▱
             ▼
     ◇ n % 2 == 0 ◇
        sí │   │ no
     ┌─────▼┐ ┌▼──────┐
     │ "par"│ │"impar"│
     └─────┬┘ └┬──────┘
           ▼   ▼
        ╭────────╮
        │  FIN   │
        ╰────────╯
```

> `n % 2` es el **residuo** de dividir `n` entre 2. Si es 0, el número es par.
> El operador `%` lo veremos a fondo en la Clase 2.
"""),

md(r"""
### Trazado de ejecución (*trace table*)

Antes de ejecutar código en la máquina, los buenos programadores lo **ejecutan en
papel**. Se llama *trazar* el algoritmo: ir anotando, paso a paso, cómo cambian
las variables. Es la mejor herramienta para entender (y depurar) lógica.

Tracemos este algoritmo que suma los números del 1 al 4:

```
suma ← 0
PARA i DESDE 1 HASTA 4 HACER
    suma ← suma + i
FIN_PARA
MOSTRAR suma
```

| Paso | `i` | `suma` antes | operación | `suma` después |
|------|-----|--------------|-----------|----------------|
| inicio | — | — | suma ← 0 | 0 |
| 1 | 1 | 0 | 0 + 1 | 1 |
| 2 | 2 | 1 | 1 + 2 | 3 |
| 3 | 3 | 3 | 3 + 3 | 6 |
| 4 | 4 | 6 | 6 + 4 | 10 |

Salida final: **10**. Lo verificaremos con código en un momento.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

En el trazado anterior, ¿qué valor final tendría `suma` si el bucle fuera
`DESDE 1 HASTA 5`? Haz la tabla mentalmente **antes** de ejecutar la celda
siguiente.
"""),

code(r"""
# Verificamos el trazado con Python real.
# (Si la sintaxis te resulta nueva, no te preocupes: es el tema de la Clase 3.
#  Por ahora, fíjate en que el código IMITA exactamente el pseudocódigo.)

suma = 0                  # suma ← 0
for i in range(1, 5):     # PARA i DESDE 1 HASTA 4  (range(1,5) = 1,2,3,4)
    suma = suma + i       #     suma ← suma + i
    print(f"  i={i}  ->  suma={suma}")   # ver cómo cambia, igual que en la tabla
print("Resultado final:", suma)
"""),

md(r"""
¡La columna `suma después` de nuestra tabla coincide con lo que imprime Python!

Esto ilustra la idea central de hoy: **si el pseudocódigo es correcto, el código
casi se escribe solo**. Y si trazas bien en papel, no necesitas "adivinar" qué
hace tu programa.
"""),
]


# ===================================================================== #
# 4. IMPLEMENTACIÓN: 3 EJEMPLOS COMPLETOS  (45 min)
# ===================================================================== #
C += [
md(r"""
## 4. Tres problemas, los 6 pasos cada uno

Ahora aplicamos la metodología completa a problemas reales. Estos tres patrones
—**encontrar un máximo**, **buscar un elemento** y **acumular/contar**— aparecen
una y otra vez en ciencia de datos.
"""),

# ---- Ejemplo A: máximo ------------------------------------------------
md(r"""
## Ejemplo A · El cliente que más compró

### 1. Contexto
Una tienda tiene una lista con el monto total gastado por cada cliente en el mes.
El gerente quiere saber **cuál fue la compra más alta** para premiar a ese cliente.

### 2. Solución intuitiva
Si tuvieras los recibos en la mano, los irías revisando uno por uno y te
quedarías con *"el más grande que he visto hasta ahora"*. Al terminar la pila, ese
es el máximo. **Esa frase entre comillas es la clave del algoritmo.**

### 3. Algoritmo
1. Supón que el primer monto es el mayor (tu "campeón" provisional).
2. Recorre los demás montos uno por uno.
3. Si encuentras uno mayor que el campeón, ese pasa a ser el nuevo campeón.
4. Al terminar, el campeón es el máximo.
"""),

md(r"""
### 4. Pseudocódigo

```
LEER montos          # una lista de números, no vacía
maximo ← montos[0]   # el primero es el campeón provisional
PARA CADA m EN montos HACER
    SI m > maximo ENTONCES
        maximo ← m
    FIN_SI
FIN_PARA
MOSTRAR maximo
```

Observa el patrón **"acumulador campeón"**: una variable (`maximo`) que recuerda
el mejor valor visto hasta ahora y se actualiza cuando aparece algo mejor.
"""),

code(r"""
# 5. Python  (traducción casi literal del pseudocódigo)

montos = [120000, 89000, 240000, 240000, 56000, 310000, 99000]

maximo = montos[0]              # campeón provisional
for m in montos:                # PARA CADA m EN montos
    if m > maximo:              # SI m > maximo
        maximo = m              # nuevo campeón
print("La compra más alta fue:", maximo)
"""),

md(r"""
### Trazado (para convencernos de que es correcto)

| `m` | `maximo` antes | ¿`m > maximo`? | `maximo` después |
|-----|----------------|----------------|------------------|
| 120000 | 120000 | no (igual) | 120000 |
| 89000  | 120000 | no | 120000 |
| 240000 | 120000 | **sí** | 240000 |
| 240000 | 240000 | no | 240000 |
| 56000  | 240000 | no | 240000 |
| 310000 | 240000 | **sí** | 310000 |
| 99000  | 310000 | no | 310000 |

Resultado: **310000**. ✔️
"""),

md(r"""
### 6. Análisis
- **¿Es correcto?** Sí: para cuando terminamos, hemos comparado el campeón contra
  *todos* los montos, así que ninguno puede ser mayor.
- **¿Cuánto cuesta?** Hacemos **una comparación por cada elemento**. Si hay `n`
  montos, son `n` comparaciones. Decimos que el costo *crece de forma lineal* con
  `n`. Lo formalizaremos al final como **O(n)**.
- **¿Se puede mejorar?** Para encontrar el máximo, **no**: es imposible saber cuál
  es el mayor sin mirar todos al menos una vez. Algunas tareas tienen un costo
  mínimo inevitable.

> 🐍 Python ya trae `max(montos)`. Pero entender *cómo* funciona por dentro es lo
> que te convierte en programador y no en alguien que copia funciones.
"""),

code(r"""
# Comparamos nuestra versión con la función incorporada: deben coincidir.
print("Nuestra versión:", maximo)
print("Función max():  ", max(montos))
print("¿Coinciden?    ", maximo == max(montos))
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

1. ...la lista `montos` estuviera **vacía**? La línea `maximo = montos[0]` fallaría
   (no hay posición 0). Este es un *caso borde* que un buen algoritmo debe
   considerar. ¿Cómo lo manejarías?
2. ...quisieras el cliente que **menos** compró? ¿Qué única cosa cambiarías en el
   pseudocódigo?
"""),

code(r"""
# Demostración del caso borde: descomenta la última línea para ver el error real.
montos_vacios = []
# maximo = montos_vacios[0]   # IndexError: list index out of range
print("Una lista vacía no tiene 'primer elemento'. Hay que decidir qué hacer:")
print("  - ¿devolver None?  - ¿lanzar un aviso?  - ¿asumir 0?")
print("Esa decisión es DISEÑO, y es tan importante como el algoritmo.")
"""),

# ---- Ejemplo B: búsqueda lineal --------------------------------------
md(r"""
## Ejemplo B · ¿Está este cliente en la lista? (búsqueda lineal)

### 1. Contexto
Tenemos los identificadores de los clientes que ya pagaron. Llega un cliente con
su id y queremos saber **si está** en la lista (para no cobrarle dos veces).

### 2. Solución intuitiva
Revisas la lista de arriba a abajo. Si en algún punto encuentras el id, respondes
"sí" y **dejas de buscar** (no tiene sentido seguir). Si llegas al final sin
encontrarlo, respondes "no".

### 3. Algoritmo
1. Recorre la lista elemento por elemento.
2. Si el elemento actual es el buscado → responde "encontrado" y termina.
3. Si terminas el recorrido sin éxito → responde "no encontrado".
"""),

md(r"""
### 4. Pseudocódigo

```
LEER lista, objetivo
PARA CADA elemento EN lista HACER
    SI elemento == objetivo ENTONCES
        DEVOLVER Verdadero        # ¡lo encontré, salgo ya!
    FIN_SI
FIN_PARA
DEVOLVER Falso                    # recorrí todo y no estaba
```

> 🔑 El detalle fino: devolver en cuanto encontramos evita trabajo inútil. A esto
> se le llama **salida temprana** (*early return*).
"""),

code(r"""
# 5. Python

def esta_en(lista, objetivo):
    # Devuelve True si 'objetivo' aparece en 'lista'; False si no.
    # Implementa una búsqueda lineal: revisa elemento por elemento y se
    # detiene en cuanto encuentra una coincidencia.
    for elemento in lista:          # PARA CADA elemento EN lista
        if elemento == objetivo:    # SI elemento == objetivo
            return True             # DEVOLVER Verdadero (salida temprana)
    return False                    # DEVOLVER Falso

clientes_pagaron = [1004, 1079, 1067, 1063, 1105]
print("¿Pagó el 1067?", esta_en(clientes_pagaron, 1067))   # True
print("¿Pagó el 9999?", esta_en(clientes_pagaron, 9999))   # False
"""),

md(r"""
### 6. Análisis: el mejor, el peor y el caso promedio

Aquí el costo **depende de los datos**, no solo de su cantidad:

| Escenario | Comparaciones | Nombre |
|---|---|---|
| El objetivo es el **primero** | 1 | mejor caso |
| El objetivo es el **último** o **no está** | `n` | peor caso |
| El objetivo está en una posición cualquiera | ~`n/2` en promedio | caso promedio |

Cuando analizamos algoritmos, casi siempre nos importa el **peor caso**: la
garantía de "nunca tardará más que esto". La búsqueda lineal es **O(n)** en el
peor caso.

> Recuerda el acertijo de la guía telefónica: la Estrategia A *era* una búsqueda
> lineal. Pronto veremos por qué la Estrategia B es muchísimo mejor.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

¿Qué pasaría si la lista tuviera el id repetido tres veces? ¿Cuántas veces lo
encontraría nuestra función antes de devolver `True`? ¿Cambia eso la respuesta?
"""),

# ---- Ejemplo C: contar/acumular --------------------------------------
md(r"""
## Ejemplo C · Contar y promediar (el patrón acumulador)

### 1. Contexto
De la lista de montos del mes, el gerente quiere dos cifras: **cuántas** ventas
superaron los \$100.000 y el **promedio** de todas las ventas.

### 2. Solución intuitiva
Llevas dos "contadores mentales": uno que suma todos los montos (para el
promedio) y otro que cuenta cuántos pasan el umbral. Recorres una sola vez.

### 3 y 4. Algoritmo + Pseudocódigo

```
total ← 0           # acumulador de suma
cuantos ← 0         # contador de ventas grandes
n ← cantidad de montos
PARA CADA m EN montos HACER
    total ← total + m
    SI m > 100000 ENTONCES
        cuantos ← cuantos + 1
    FIN_SI
FIN_PARA
promedio ← total / n
MOSTRAR cuantos, promedio
```

> Fíjate: **un solo recorrido** calcula las dos cosas. Recorrer la lista dos
> veces daría el mismo resultado pero costaría el doble. Pensar en eficiencia es
> pensar en *cuántas veces tocas los datos*.
"""),

code(r"""
# 5. Python

montos = [120000, 89000, 240000, 240000, 56000, 310000, 99000]

total = 0
cuantos = 0
for m in montos:
    total = total + m                 # acumulador de suma
    if m > 100000:
        cuantos = cuantos + 1         # contador condicional

promedio = total / len(montos)        # len() = cantidad de elementos
print(f"Ventas mayores a $100.000: {cuantos}")
print(f"Promedio de ventas: ${promedio:,.0f}")
"""),

md(r"""
### 6. Análisis
- **Acumulador** (`total`) y **contador** (`cuantos`) son los dos patrones más
  reutilizables de toda la programación. Memorízalos como conceptos, no como código.
- Un solo recorrido ⇒ costo **O(n)**.
- En la Clase 5 veremos que **NumPy** hace esto mismo, pero a velocidad de C y en
  una sola línea: `montos.mean()`. Hoy entendemos qué ocurre por debajo.
"""),
]


# ===================================================================== #
# 5. VISUALIZACIÓN + EFICIENCIA  (parte del bloque de implementación/cierre)
# ===================================================================== #
C += [
md(r"""
## 5. Midamos la eficiencia: la gran idea de "Big-O"

Volvamos al acertijo de la guía telefónica con números. La pregunta no es
*"¿cuántos segundos tarda?"* (eso depende de tu computador), sino
**"¿cómo crece el trabajo cuando crecen los datos?"**.

- **Búsqueda lineal (Estrategia A):** en el peor caso, revisa los `n` nombres. Si
  duplicas la guía, duplicas el trabajo. → crecimiento **lineal**, `O(n)`.
- **Búsqueda binaria (Estrategia B):** cada paso *descarta la mitad*. Con 1.000
  páginas tardas ~10 pasos; con 2.000, solo ~11. → crecimiento **logarítmico**, `O(log n)`.

Esa diferencia es brutal a gran escala. Veámoslo con una tabla y una gráfica.
"""),

code(r"""
import math

print(f"{'n datos':>12} | {'lineal O(n)':>14} | {'binaria O(log n)':>16}")
print("-" * 50)
for n in [10, 100, 1_000, 1_000_000, 1_000_000_000]:
    pasos_lineal = n
    pasos_binaria = math.ceil(math.log2(n))
    print(f"{n:>12,} | {pasos_lineal:>14,} | {pasos_binaria:>16,}")
"""),

md(r"""
Lee la última fila con calma: para **mil millones** de datos, la búsqueda lineal
haría mil millones de comparaciones; la binaria, **30**. No es que un computador
sea más rápido: es que el *algoritmo* es fundamentalmente mejor. **Elegir el
algoritmo correcto vence a cualquier hardware.**
"""),

code(r"""
import numpy as np
import matplotlib.pyplot as plt

n = np.arange(1, 101)                 # tamaños de entrada de 1 a 100
plt.figure(figsize=(8, 5))
plt.plot(n, n,              label="O(n)  — lineal")
plt.plot(n, n**2,          label="O(n²) — cuadrático")
plt.plot(n, np.log2(n),    label="O(log n) — logarítmico")
plt.xlabel("tamaño de la entrada (n)")
plt.ylabel("operaciones (aprox.)")
plt.title("Cómo crece el trabajo según el algoritmo")
plt.ylim(0, 120)
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
"""),

md(r"""
### Cómo leer la gráfica

- La curva **logarítmica** (abajo) casi no sube: duplicar los datos apenas añade
  trabajo. Es el ideal cuando se puede lograr.
- La **lineal** sube de forma constante: aceptable y muy común.
- La **cuadrática** `O(n²)` se dispara. Aparece, por ejemplo, cuando comparas cada
  elemento con todos los demás (dos bucles anidados). Funciona con datos pequeños,
  pero "explota" con datos grandes.

> 🧠 Por ahora basta con la **intuición**: ¿el trabajo crece igual, más rápido o
> más lento que los datos? La notación formal la profundizaremos a lo largo del
> curso.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Tienes un algoritmo `O(n²)` que tarda **1 segundo** con 1.000 datos.
Aproximadamente, ¿cuánto tardaría con 10.000 datos (10× más)?

<details>
<summary>👉 Pista (ábrela tras pensar)</summary>

En `O(n²)`, multiplicar los datos por 10 multiplica el trabajo por 10² = **100**.
Pasaría de 1 segundo a ~**100 segundos**. Por eso `O(n²)` asusta.
</details>
"""),
]


# ===================================================================== #
# 6. ERRORES COMUNES + REFLEXIÓN
# ===================================================================== #
C += [
md(r"""
## 6. Errores comunes (y cómo evitarlos)

Estos tropiezos le pasan a todo el mundo al empezar. Reconocerlos vale oro.

**1. Saltar directo al código.** Escribir Python sin haber pensado el algoritmo.
Síntoma: borras y reescribes sin rumbo. *Cura:* pseudocódigo primero, siempre.

**2. Instrucciones ambiguas.** "Ordena los datos" — ¿ascendente o descendente?
¿por qué columna? La máquina no adivina. *Cura:* precisión en cada paso.

**3. Olvidar los casos borde.** La lista vacía, el cero, el valor negativo, el
dato repetido. *Cura:* pregúntate siempre "¿y si la entrada es rara?".

**4. Confundir el `=` de asignación con la igualdad.** En pseudocódigo usamos `←`
para asignar y `==` para comparar precisamente para no confundirlos.

**5. Errores de borde en bucles (*off-by-one*).** ¿El bucle va hasta `n` o hasta
`n-1`? ¿Incluye el último elemento? *Cura:* traza con un ejemplo pequeño.

**6. Ignorar la eficiencia hasta que es tarde.** El código "funciona" con 10
datos y colapsa con 10 millones. *Cura:* piensa en `n` desde el diseño.
"""),

code(r"""
# Ilustración del error #4 y del #5 con un caso concreto.
# Queremos los números del 1 al 5. ¿range(1, 5) o range(1, 6)?

print("range(1, 5) produce:", list(range(1, 5)))   # ¡le falta el 5! (off-by-one)
print("range(1, 6) produce:", list(range(1, 6)))   # correcto

# En Python, range(a, b) llega hasta b-1. Trazarlo en papel evita este error.
"""),

md(r"""
### Una reflexión antes de cerrar

A lo largo de tu carrera escribirás miles de algoritmos, pero todos serán
combinaciones de muy pocas ideas: **secuencia, decisión, repetición**;
**acumular, contar, buscar, comparar**. La maestría no consiste en saber muchas
cosas distintas, sino en reconocer *cuál de estos patrones encaja* en el problema
que tienes enfrente.

La ciencia de datos es, en el fondo, esto mismo a gran escala: entran datos
crudos, se acumulan, se filtran, se cuentan, se comparan — y sale conocimiento.
"""),
]


# ===================================================================== #
# 7. RESUMEN + QUIZ
# ===================================================================== #
C += [
md(r"""
## 7. Resumen de la clase

| Concepto | En una frase |
|---|---|
| **Algoritmo** | pasos finitos, precisos, con entrada y salida |
| **Modelo EPS** | todo programa es Entrada → Proceso → Salida |
| **Metodología (6 pasos)** | contexto → intuición → algoritmo → pseudocódigo → Python → análisis |
| **Pseudocódigo** | puente legible entre la idea y el código |
| **3 estructuras** | secuencia, decisión, repetición (¡y nada más!) |
| **Trazado** | ejecutar el algoritmo en papel para verificarlo |
| **Patrones clave** | campeón (máx/mín), búsqueda lineal, acumulador, contador |
| **Eficiencia (Big-O)** | cómo crece el trabajo cuando crecen los datos |

### Lo más importante que te llevas
> **Piensa primero, codifica después.** Un buen pseudocódigo y un buen trazado
> hacen que el código sea casi una formalidad — y te permiten elegir el algoritmo
> *eficiente*, no solo uno que funcione.
"""),

md(r"""
## 8. Quiz de autoevaluación

Responde mentalmente y luego ejecuta la celda para comprobar.

1. ¿Cuáles son las **tres** estructuras de control con las que se construye
   cualquier algoritmo?
2. Un algoritmo revisa todos los `n` elementos exactamente una vez. ¿Cuál es su
   complejidad: `O(1)`, `O(log n)`, `O(n)` u `O(n²)`?
3. En `range(2, 7)`, ¿qué números genera Python?
4. ¿Por qué la búsqueda binaria (Estrategia B) es mejor que la lineal en una guía
   *ordenada*?
"""),

code(r"""
respuestas = {
    1: "Secuencia, decisión (selección) e iteración (repetición).",
    2: "O(n): el trabajo crece de forma lineal con la cantidad de datos.",
    3: "Los enteros 2, 3, 4, 5, 6  (range llega hasta b-1).",
    4: ("Porque en cada paso descarta la MITAD de los datos restantes, "
        "así que el trabajo crece como O(log n) en vez de O(n). "
        "Requiere que los datos estén ordenados."),
}
for k, v in respuestas.items():
    print(f"{k}. {v}\n")
"""),

md(r"""
## 9. Retos para practicar

Antes de pasar a los notebooks de práctica, intenta estos en papel (pseudocódigo
+ trazado):

1. **Patrón.** Dada una lista de temperaturas, encuentra cuántas veces la
   temperatura **subió** respecto al día anterior.
2. **Diseño.** Escribe el algoritmo para decidir si una palabra es un *palíndromo*
   (se lee igual al derecho y al revés, como "reconocer").
3. **Análisis.** Tienes dos algoritmos para la misma tarea: uno `O(n)` y otro
   `O(n²)`. ¿En qué situación podría convenir el `O(n²)`? (pista: piensa en `n`
   muy pequeño y en simplicidad del código).

---

### ➡️ Siguiente paso

- **practice01.ipynb** — 10 ejercicios graduales con solución oculta.
- **practice02.ipynb** — un caso aplicado de ciencia de datos con datos reales.
- **homework01.ipynb** y **homework02.ipynb** — tareas autocalificables.

¡Nos vemos en la práctica! 🚀
"""),
]


# ===================================================================== #
# CELDAS ADICIONALES — se intercalan para profundizar y alcanzar densidad
# pedagógica (80-150 celdas). Se insertan en puntos estratégicos.
# ===================================================================== #

# --- Ampliación del bloque de MOTIVACIÓN: un algoritmo cotidiano ------------
EXTRA_MOTIVACION = [
md(r"""
### Tú ya eres un algoritmo andante

Antes de seguir, hagamos visible algo que haces sin pensar. Describe el
algoritmo de *"preparar una taza de café instantáneo"*. Un primer intento suele
ser:

```
1. Calentar agua
2. Servir el café
3. Revolver
```

Suena bien... hasta que un robot lo intenta y se queda congelado en el paso 1:
*¿cuánta* agua? ¿caliente *cuánto*? ¿servir el café **en** qué? El robot no
rellena huecos. Reescribámoslo con **precisión**:

```
1. Verter 250 ml de agua en la jarra eléctrica
2. Encender la jarra y esperar hasta que el agua hierva
3. Poner 2 cucharaditas de café en una taza
4. Verter el agua caliente en la taza hasta 2 cm del borde
5. Revolver durante 10 segundos
```

Esa diferencia —de lo vago a lo preciso— es exactamente el salto mental que
practicaremos toda la clase.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

En el algoritmo del café, ¿qué pasaría si intercambiamos los pasos 3 y 4 (verter
el agua *antes* de poner el café)? ¿El resultado es el mismo? Este pequeño
ejercicio muestra que en un algoritmo **el orden importa**: es una *secuencia*,
no un conjunto de pasos sueltos.
"""),
]

# --- Ampliación TEORÍA: decisión ejecutable + variables como cajas ----------
EXTRA_TEORIA = [
md(r"""
### Una decisión, en vivo

Veamos la estructura de **decisión** funcionando. El siguiente código clasifica
una transacción según su monto. Lee primero el pseudocódigo:

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
def clasificar(monto):
    # Traduce el pseudocódigo de decisión escalonada (if / elif / else).
    if monto > 200000:
        return "alta"
    elif monto > 50000:
        return "media"
    else:
        return "baja"

for m in [310000, 89000, 12000]:
    print(f"${m:>7,}  ->  categoria {clasificar(m)!r}")
"""),

md(r"""
### Variables como cajas etiquetadas

Una **variable** es una caja con una etiqueta (su nombre) que guarda un valor. La
asignación `x ← 5` significa *"mete el 5 en la caja llamada x"*. Cuando haces
`x ← x + 1`, lees lo que hay en la caja, le sumas 1, y vuelves a guardarlo:

```
   antes            después de  x ← x + 1
  ┌─────┐                ┌─────┐
x │  5  │            x   │  6  │
  └─────┘                └─────┘
```

Entender esto evita el error clásico de creer que `x = x + 1` es una ecuación
"imposible". No es una ecuación: es una **orden de actualizar la caja**.
"""),

code(r"""
# Visualicemos el contenido de las 'cajas' paso a paso.
x = 5
print(f"x empieza valiendo {x}")
x = x + 1          # lee 5, suma 1, guarda 6
print(f"tras x = x + 1, ahora x vale {x}")

# Intercambiar dos cajas: un clásico que conviene tener claro.
a, b = "izquierda", "derecha"
print(f"\nantes:    a={a!r}, b={b!r}")
a, b = b, a        # Python intercambia en una línea
print(f"después:  a={a!r}, b={b!r}")
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Para intercambiar `a` y `b` en lenguajes sin la magia de `a, b = b, a`, se usa una
**caja auxiliar**:

```
temp ← a
a ← b
b ← temp
```

¿Qué pasaría si **omites** la variable `temp` y escribes directo `a ← b` y luego
`b ← a`? Traza en papel con `a=1, b=2` y descubre por qué se pierde un valor.
"""),
]

# --- Ampliación IMPLEMENTACIÓN: el cajero (algoritmo voraz) -----------------
EXTRA_CAJERO = [
md(r"""
## Ejemplo D · El cajero que da el vuelto (algoritmo voraz)

### 1. Contexto
Un cajero automático debe entregar un monto usando la **menor cantidad de
billetes** posible. Disponibles: \$50.000, \$20.000, \$10.000, \$5.000, \$1.000.

### 2. Solución intuitiva
Como cualquier cajero humano: empieza por el billete **más grande** que quepa,
entrega tantos como puedas, y continúa con el siguiente. Esta táctica de
"agarra siempre lo más grande disponible" se llama **algoritmo voraz** (*greedy*).

### 3. Algoritmo
1. Ordena los billetes de mayor a menor.
2. Para cada billete: entrega `monto // billete` unidades y reduce el monto al
   residuo `monto % billete`.
3. Repite hasta que el monto llegue a 0.
"""),

md(r"""
### 4. Pseudocódigo

```
LEER monto
billetes ← [50000, 20000, 10000, 5000, 1000]   # ya ordenados de mayor a menor
PARA CADA b EN billetes HACER
    cantidad ← monto DIV b        # división entera: ¿cuántos caben?
    SI cantidad > 0 ENTONCES
        MOSTRAR cantidad, "billetes de", b
    FIN_SI
    monto ← monto MOD b           # lo que queda por entregar
FIN_PARA
```

> `DIV` (`//` en Python) es la división entera; `MOD` (`%`) es el residuo. Son dos
> operaciones que usarás muchísimo. Las formalizamos en la Clase 2.
"""),

code(r"""
# 5. Python

def dar_vuelto(monto):
    # Entrega 'monto' usando la menor cantidad de billetes (estrategia voraz).
    billetes = [50000, 20000, 10000, 5000, 1000]   # de mayor a menor
    print(f"Entregar ${monto:,}:")
    for b in billetes:
        cantidad = monto // b            # cuántos billetes de 'b' caben
        if cantidad > 0:
            print(f"  {cantidad} x ${b:,}")
        monto = monto % b                # lo que falta por entregar
    if monto > 0:
        print(f"  (no se puede entregar el resto: ${monto:,})")

dar_vuelto(87000)
"""),

md(r"""
### 6. Análisis
- **Correcto** para este conjunto de billetes porque cada uno es múltiplo de los
  menores. ¡Ojo! El método voraz **no siempre da el óptimo** con cualquier conjunto
  de denominaciones (ese es un resultado famoso). Reconocer *cuándo* una estrategia
  funciona es parte del análisis.
- **Costo:** recorremos una vez la lista de billetes ⇒ es proporcional a la
  cantidad de denominaciones, no al monto. Muy eficiente.

### 🤔 ¿Qué pasaría si...?
¿Qué pasaría si existiera un billete de \$30.000 y quisieras dar \$60.000? El
voraz tomaría uno de \$50.000 y luego \$10.000 (2 billetes), cuando dos de
\$30.000 también suman \$60.000 (2 billetes). Empatan aquí, pero hay conjuntos
donde el voraz pierde. **Una estrategia intuitiva no es prueba de optimalidad.**
"""),
]

# --- Ampliación: búsqueda binaria ejecutable (cierra el acertijo) -----------
EXTRA_BINARIA = [
md(r"""
## Cerrando el acertijo: la búsqueda binaria en código

Prometimos volver a la guía telefónica. La **Estrategia B** (partir por la mitad)
se llama **búsqueda binaria** y solo funciona si los datos están **ordenados**.

### Pseudocódigo

```
LEER lista_ordenada, objetivo
inicio ← 0
fin ← longitud(lista) - 1
MIENTRAS inicio <= fin HACER
    medio ← (inicio + fin) DIV 2
    SI lista[medio] == objetivo ENTONCES
        DEVOLVER medio                 # encontrado
    SINO SI lista[medio] < objetivo ENTONCES
        inicio ← medio + 1             # descarta la mitad izquierda
    SINO
        fin ← medio - 1                # descarta la mitad derecha
    FIN_SI
FIN_MIENTRAS
DEVOLVER -1                            # no está
```
"""),

code(r"""
def busqueda_binaria(lista_ordenada, objetivo):
    # Devuelve la posición de 'objetivo' o -1 si no está.
    # Cuenta cuántos pasos da, para comparar con la búsqueda lineal.
    inicio, fin = 0, len(lista_ordenada) - 1
    pasos = 0
    while inicio <= fin:
        pasos += 1
        medio = (inicio + fin) // 2
        if lista_ordenada[medio] == objetivo:
            print(f"  encontrado en la posición {medio} tras {pasos} paso(s)")
            return medio
        elif lista_ordenada[medio] < objetivo:
            inicio = medio + 1           # mira la mitad derecha
        else:
            fin = medio - 1              # mira la mitad izquierda
    print(f"  no está (tras {pasos} pasos)")
    return -1

datos = list(range(1, 1001))             # 1..1000, ya ordenados
print("Buscar 999 con búsqueda binaria:")
busqueda_binaria(datos, 999)
print("Una búsqueda lineal habría hecho 999 comparaciones para llegar al 999.")
"""),

md(r"""
La búsqueda binaria encontró el 999 en **~10 pasos**, frente a **999** de la
lineal. Esa es, por fin, la respuesta cuantitativa a nuestro acertijo inicial: la
Estrategia B no es "un poco" mejor, es exponencialmente mejor a medida que crecen
los datos.

> ⚠️ Pero recuerda su requisito: **los datos deben estar ordenados**. Si no lo
> están, primero habría que ordenarlos (lo cual tiene su propio costo). Elegir el
> algoritmo correcto siempre depende del contexto.
"""),
]

# --- Ampliación: descomposición de problemas --------------------------------
EXTRA_DESCOMP = [
md(r"""
## Una habilidad transversal: descomponer

Cuando un problema es grande, la táctica universal es **descomponerlo** en
subproblemas más pequeños que ya sepamos resolver. A esto se le llama
*divide y vencerás* a nivel de diseño.

Ejemplo: *"generar el reporte mensual de ventas"* da miedo como un todo, pero se
descompone en piezas familiares:

```
generar_reporte:
    1. cargar las ventas            (entrada)
    2. limpiar datos inválidos      (filtrado)
    3. calcular total y promedio    (acumulador)
    4. encontrar la venta máxima    (campeón)
    5. contar ventas por ciudad     (contador)
    6. mostrar el resumen           (salida)
```

¡Cada pieza es uno de los patrones que ya practicamos hoy! Programar a gran escala
es, en buena medida, **reconocer subproblemas conocidos** dentro de uno nuevo.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Toma el problema *"corregir las notas de un examen y publicar el promedio del
curso"* y descompónlo en 4 o 5 subproblemas, etiquetando cada uno con el patrón
que usa (acumulador, contador, búsqueda, campeón...). No escribas código: solo la
descomposición. Esta es, literalmente, la forma de pensar de un científico de
datos frente a un dataset nuevo.
"""),
]

# Ensamblar: insertamos los bloques extra en posiciones que conservan el hilo.
# (Se reconstruye C intercalando; los índices se eligen por contenido.)
def insertar_despues(celdas, marcador_texto, nuevas):
    """Inserta 'nuevas' justo después de la primera celda cuyo source contiene 'marcador_texto'."""
    for i, c in enumerate(celdas):
        if marcador_texto in c.source:
            return celdas[: i + 1] + nuevas + celdas[i + 1 :]
    return celdas + nuevas  # si no se encuentra, al final

# --- Primer ejemplo COMPLETO con los 6 pasos (par o impar) ------------------
EXTRA_PRIMER_EJEMPLO = [
md(r"""
## Nuestro primer recorrido por los 6 pasos

Antes de los ejemplos grandes, hagamos uno diminuto pero **completo**, para sentir
el ritmo de la metodología.

### 1. Contexto
Dado un número entero, decidir si es **par** o **impar**.

### 2. Solución intuitiva
Un número es par si se puede repartir en dos grupos iguales sin que sobre nada;
es decir, si al dividirlo entre 2 **no sobra** nada.

### 3. Algoritmo
1. Calcular el residuo de dividir el número entre 2.
2. Si el residuo es 0 → es par; si no → es impar.
"""),

md(r"""
### 4. Pseudocódigo

```
LEER n
SI n MOD 2 == 0 ENTONCES
    MOSTRAR "par"
SINO
    MOSTRAR "impar"
FIN_SI
```

Repasa el diagrama de flujo que vimos en la sección de pseudocódigo: ¡es
exactamente este algoritmo!
"""),

code(r"""
# 5. Python

def par_o_impar(n):
    # El operador % da el residuo de la división entera.
    if n % 2 == 0:
        return "par"
    else:
        return "impar"

for n in [0, 7, 10, -3]:
    print(f"{n:>3}  es  {par_o_impar(n)}")
"""),

md(r"""
### 6. Análisis
- **Correcto:** cubre todos los enteros, incluido el 0 (que es par) y los
  negativos.
- **Costo:** una sola operación, sin importar el tamaño de `n`. Esto es lo más
  barato posible: **O(1)**, costo *constante*.

### 🤔 ¿Qué pasaría si...?
¿Qué pasaría si `n` fuera un número con decimales, como `7.5`? ¿Tiene sentido la
pregunta "par o impar"? Este es otro recordatorio de validar *qué tipo* de entrada
esperamos — algo que formalizaremos en la Clase 2.
"""),
]

C = insertar_despues(C, "Por eso se atascan.", EXTRA_PRIMER_EJEMPLO)
C = insertar_despues(C, "Guarda tus respuestas. Volveremos", EXTRA_MOTIVACION)
C = insertar_despues(C, "Los principiantes saltan directo", EXTRA_TEORIA)
C = insertar_despues(C, "¡La columna `suma después`", EXTRA_CAJERO)
C = insertar_despues(C, "¿Cambia eso la respuesta?", EXTRA_BINARIA)
# --- Correcto vs eficiente: detección de duplicados O(n^2) vs O(n) ----------
EXTRA_CORRECTO_EFICIENTE = [
md(r"""
## "Funciona" no es lo mismo que "es bueno"

Un algoritmo puede ser **correcto** (da la respuesta bien) y aun así ser
**ineficiente**. Veámoslo con un problema real: *¿hay ids de cliente repetidos en
la lista?* (un duplicado podría significar un cobro doble).

### Idea ingenua (correcta, pero costosa)
Comparar **cada elemento con todos los demás**. Dos bucles anidados:

```
PARA CADA i EN posiciones HACER
    PARA CADA j EN posiciones DESPUÉS DE i HACER
        SI lista[i] == lista[j] ENTONCES
            DEVOLVER Verdadero
```

Con `n` elementos, esto hace del orden de `n²/2` comparaciones. Para 100 ids son
~5.000; para 100.000 ids son ~5.000 millones. **Explota.**
"""),

code(r"""
def hay_duplicados_lento(lista):
    # O(n^2): compara cada par. Correcto pero costoso.
    comparaciones = 0
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            comparaciones += 1
            if lista[i] == lista[j]:
                print(f"  duplicado: {lista[i]}  (tras {comparaciones} comparaciones)")
                return True
    print(f"  sin duplicados (tras {comparaciones} comparaciones)")
    return False

ids = [1004, 1079, 1067, 1063, 1105, 1067]   # el 1067 está repetido
print("Versión lenta O(n^2):")
hay_duplicados_lento(ids)
"""),

md(r"""
### Idea mejor (correcta y eficiente)
Recorre **una sola vez** y ve guardando lo que ya viste en un "conjunto". Preguntar
si algo ya está en un conjunto es casi instantáneo. Costo: **O(n)**.

> Los **conjuntos** (`set`) son tema de la Clase 4; aquí solo los usamos para
> mostrar la idea de cambiar un `O(n²)` por un `O(n)`. Fíjate en el contraste de
> comparaciones.
"""),

code(r"""
def hay_duplicados_rapido(lista):
    # O(n): un solo recorrido, recordando lo ya visto.
    vistos = set()
    pasos = 0
    for x in lista:
        pasos += 1
        if x in vistos:
            print(f"  duplicado: {x}  (tras {pasos} pasos)")
            return True
        vistos.add(x)
    print(f"  sin duplicados (tras {pasos} pasos)")
    return False

print("Versión rápida O(n):")
hay_duplicados_rapido(ids)
"""),

md(r"""
Ambas funciones dan la **misma respuesta**, pero la segunda hace mucho menos
trabajo. Esta es la esencia del **análisis** (paso 6 de la metodología): una vez
que algo funciona, preguntar *"¿se puede hacer con menos trabajo?"*. En ciencia
de datos, donde `n` puede ser de millones, esta pregunta decide si tu análisis
corre en segundos o nunca termina.
"""),
]

# --- Validación de entradas + glosario --------------------------------------
EXTRA_GLOSARIO = [
md(r"""
## Validar la entrada: la defensa del programador

Vimos varios "huecos" peligrosos: listas vacías, decimales donde se esperaban
enteros, datos repetidos. Un algoritmo robusto **valida su entrada antes de
confiar en ella**. En pseudocódigo:

```
SI lista está vacía ENTONCES
    DEVOLVER "no hay datos"   # o un valor especial, o un aviso
FIN_SI
... continuar con el algoritmo normal ...
```

No se trata de paranoia: en datos reales, lo raro **siempre** ocurre. Un buen
hábito desde hoy: por cada algoritmo, escribe una línea preguntándote *"¿cuál es
la entrada más extraña que podría llegar?"*.
"""),

code(r"""
def promedio_seguro(numeros):
    # Valida ANTES de dividir, para no romperse con una lista vacía.
    if len(numeros) == 0:
        return None                  # señal clara de "no se puede calcular"
    return sum(numeros) / len(numeros)

print("promedio de [4, 5, 6] =", promedio_seguro([4, 5, 6]))
print("promedio de []        =", promedio_seguro([]))   # None, sin error
"""),

md(r"""
## Glosario de la Clase 1

| Término | Definición breve |
|---|---|
| **Algoritmo** | secuencia finita y precisa de pasos que resuelve un problema |
| **Pseudocódigo** | descripción semi-formal del algoritmo, independiente del lenguaje |
| **Variable** | "caja" con nombre que guarda un valor |
| **Asignación** (`←`) | guardar un valor en una variable |
| **Secuencia / Decisión / Iteración** | las tres estructuras de control |
| **Trazado** | ejecutar el algoritmo a mano para verificarlo |
| **Acumulador** | variable que va sumando/juntando a lo largo de un recorrido |
| **Contador** | variable que cuenta cuántas veces ocurre algo |
| **Búsqueda lineal / binaria** | revisar uno por uno / partir por la mitad (ordenado) |
| **Algoritmo voraz** | el que en cada paso toma la opción localmente mejor |
| **Caso borde** | entrada extrema o inusual (vacío, cero, negativo, repetido) |
| **Big-O** | cómo crece el trabajo cuando crece el tamaño de la entrada `n` |
| **O(1) / O(log n) / O(n) / O(n²)** | constante / logarítmico / lineal / cuadrático |
"""),
]

C = insertar_despues(C, "siempre depende del contexto.", EXTRA_CORRECTO_EFICIENTE)
C = insertar_despues(C, "salga conocimiento.", EXTRA_DESCOMP)
# --- Ejercicio guiado en clase: tendencia de temperaturas -------------------
EXTRA_GUIADO = [
md(r"""
## Ejercicio guiado: ¿cuántos días subió la temperatura?

Resolvámoslo **juntos**, en vivo, aplicando la metodología. (Es el reto #1 de la
clase; lo desarrollamos aquí como ejemplo guiado).

### Contexto e intuición
Tenemos las temperaturas máximas de varios días seguidos. Queremos contar en
cuántos días la temperatura fue **mayor que la del día anterior**. Intuición:
caminamos por la lista comparando *cada día con el anterior* y llevamos un
**contador**.

### Pseudocódigo
```
subidas ← 0
PARA i DESDE 1 HASTA longitud(temps) - 1 HACER
    SI temps[i] > temps[i-1] ENTONCES
        subidas ← subidas + 1
    FIN_SI
FIN_PARA
MOSTRAR subidas
```

> 🔎 Ojo al detalle: empezamos en `i = 1`, no en `0`, porque el día 0 no tiene
> "día anterior" con el cual compararse. Ese es un *caso borde* resuelto desde el
> diseño.
"""),

code(r"""
temps = [21, 23, 22, 25, 26, 24, 24, 28]

subidas = 0
for i in range(1, len(temps)):          # desde el segundo día
    if temps[i] > temps[i - 1]:         # ¿más caliente que ayer?
        subidas += 1
        print(f"  dia {i}: {temps[i-1]}° -> {temps[i]}°  (subio)")
print("Total de dias que subio la temperatura:", subidas)
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?
- ¿Qué cambiarías para contar los días que **bajó**? (pista: invierte la
  comparación).
- ¿Y si dos días seguidos tienen la **misma** temperatura? Con `>` no cuentan como
  subida. ¿Es eso lo que queremos? Definir esto es **precisión**, el corazón del
  paso de algoritmo.
"""),

md(r"""
### Resolviendo el "¿y si quiero el mínimo?"

En el Ejemplo A preguntamos qué cambiarías para hallar el cliente que **menos**
compró. La respuesta: el patrón "campeón" es el mismo, solo se invierte la
comparación (`<` en vez de `>`). Compruébalo:
"""),

code(r"""
montos = [120000, 89000, 240000, 240000, 56000, 310000, 99000]

minimo = montos[0]
for m in montos:
    if m < minimo:          # ÚNICO cambio respecto al máximo: '<' en vez de '>'
        minimo = m
print("Compra mínima:", minimo, "| comprobación con min():", min(montos))
print("¿Coinciden?", minimo == min(montos))
"""),

md(r"""
> 💡 Lección de diseño: **máximo y mínimo son el mismo algoritmo** con una
> comparación distinta. Reconocer que dos problemas comparten esqueleto te ahorra
> reinventar la rueda. Gran parte de "saber programar" es ver estos parecidos.
"""),
]

C = insertar_despues(C, "Hoy entendemos qué ocurre por debajo.", EXTRA_GUIADO)
C = insertar_despues(C, "frente a un dataset nuevo.", EXTRA_GLOSARIO)


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase01", "lecture.ipynb")
build(os.path.abspath(ruta), C)
