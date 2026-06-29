"""Construye curso/clase01/practice02.ipynb — caso aplicado de ciencia de datos.

Analizamos un dataset real-ista de transacciones SOLO con Python puro (sin NumPy
ni pandas todavía), para que el estudiante vea que la ciencia de datos es, en el
fondo, los mismos patrones algorítmicos de hoy aplicados a datos reales.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []

C += [
md(r"""
# Clase 1 · Práctica 02 — Caso aplicado: analizando transacciones

### De los patrones a un problema real de negocio

Hoy aprendimos patrones algorítmicos (acumulador, contador, campeón, búsqueda).
Ahora los usamos sobre **datos reales** de una tienda con sucursales en varias
ciudades de Colombia.

> 🎯 **Importante:** todavía **no** usaremos NumPy ni pandas (vienen en las clases
> 5 y 6). Lo haremos "a mano", con listas y bucles, para que entiendas qué hacen
> esas librerías por dentro. Al final compararás cuánto código te ahorrarán.

**Preguntas de negocio que responderemos:**
1. ¿Cuánto vendió la tienda en total y cuál fue el ticket promedio?
2. ¿Cuál fue la transacción más alta? ¿Y la más baja?
3. ¿Qué ciudad generó más ingresos?
4. ¿Cuántas transacciones superaron los \$200.000 (posibles ventas mayoristas)?
5. ¿Hay valores atípicos (*outliers*) que debamos revisar?
"""),

code(r"""
# Cargamos el dataset con la librería estándar 'csv' (sin pandas).
import csv, os, sys
sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar

ruta = os.path.join("..", "datasets", "transacciones.csv")
with open(ruta, encoding="utf-8") as f:
    filas = list(csv.DictReader(f))   # cada fila es un dict {columna: valor}

print(f"Se cargaron {len(filas)} transacciones.")
print("Primera fila:", filas[0])
"""),

md(r"""
### Paso 1 · Entender la estructura (Entrada)

Cada fila tiene: `id`, `fecha`, `ciudad`, `categoria`, `metodo_pago`, `monto`.

⚠️ Detalle crucial: al leer un CSV, **todo llega como texto** (`str`). El `monto`
`"73078"` es una cadena, no un número. Si intentáramos sumar cadenas obtendríamos
basura. Primer paso de toda limpieza de datos: **convertir los tipos**.
"""),

code(r"""
# Extraemos los montos como ENTEROS (no como texto). Patrón: transformar la entrada.
montos = [int(fila["monto"]) for fila in filas]
print("Tipo del primer monto en el CSV:", type(filas[0]["monto"]).__name__)
print("Tipo tras convertir:            ", type(montos[0]).__name__)
print("Primeros 5 montos:", montos[:5])
"""),

md(r"""
### Pregunta 1 · Total e ingreso promedio (acumulador)

Usamos el patrón **acumulador** para el total, y lo dividimos por la cantidad para
el promedio. Exactamente lo que hicimos en la clase, ahora sobre 120 datos reales.
"""),

code(r"""
total = 0
for m in montos:           # acumulador
    total += m
promedio = total / len(montos)

print(f"Ingreso total:   ${total:,.0f}")
print(f"Ticket promedio: ${promedio:,.0f}")
print(f"Transacciones:   {len(montos)}")
"""),

md(r"""
### Pregunta 2 · Transacción máxima y mínima (patrón campeón)

Dos campeones a la vez en un solo recorrido: uno que busca el mayor y otro el
menor. Recorrer una sola vez para obtener dos respuestas es más eficiente que
recorrer dos veces.
"""),

code(r"""
maximo = montos[0]
minimo = montos[0]
for m in montos:
    if m > maximo:
        maximo = m
    if m < minimo:
        minimo = m

print(f"Transacción más alta: ${maximo:,.0f}")
print(f"Transacción más baja: ${minimo:,.0f}")
# Comprobamos con las funciones incorporadas:
print("¿Coincide max()?", maximo == max(montos), "| ¿min()?", minimo == min(montos))
"""),

md(r"""
### Pregunta 3 · ¿Qué ciudad vendió más? (agrupar sin diccionarios)

Agrupar por ciudad es un problema nuevo. Lo resolvemos con **dos listas
paralelas**: una con los nombres de ciudad y otra con su total acumulado. (En la
Clase 4 verás que un *diccionario* hace esto de forma más elegante; hoy lo hacemos
con las herramientas que ya dominas, para entender la mecánica.)

**Algoritmo:**
1. Por cada transacción, busca su ciudad en la lista de ciudades vistas.
2. Si ya está, súmale el monto en la posición correspondiente.
3. Si es nueva, agrégala con su monto inicial.
"""),

code(r"""
ciudades = []     # nombres únicos de ciudad
totales = []      # total acumulado, alineado por posición con 'ciudades'

for fila in filas:
    ciudad = fila["ciudad"]
    monto = int(fila["monto"])
    # búsqueda lineal de la ciudad entre las ya vistas
    if ciudad in ciudades:
        i = ciudades.index(ciudad)   # posición de la ciudad
        totales[i] += monto
    else:
        ciudades.append(ciudad)
        totales.append(monto)

# Mostramos el resultado y encontramos la ciudad líder (otro 'campeón').
lider = ciudades[0]
mejor_total = totales[0]
for i in range(len(ciudades)):
    print(f"  {ciudades[i]:<14} ${totales[i]:>12,.0f}")
    if totales[i] > mejor_total:
        mejor_total = totales[i]
        lider = ciudades[i]

print(f"\n🏆 Ciudad con más ingresos: {lider} (${mejor_total:,.0f})")
"""),

md(r"""
### Pregunta 4 · Ventas mayoristas (contador con condición)
"""),

code(r"""
UMBRAL = 200000
mayoristas = 0
for m in montos:
    if m > UMBRAL:
        mayoristas += 1
print(f"Transacciones por encima de ${UMBRAL:,}: {mayoristas}")
print(f"Eso es el {mayoristas / len(montos) * 100:.1f}% de las ventas.")
"""),

md(r"""
### Pregunta 5 · Detección de valores atípicos (*outliers*)

En el mundo real, los datos traen errores y rarezas. Una regla simple y común:
marcar como sospechoso todo monto que supere **3 veces el promedio**. No es una
verdad absoluta, pero es un buen primer filtro para *"esto merece una mirada
humana"*.
"""),

code(r"""
limite = 3 * promedio
sospechosos = []
for fila in filas:
    if int(fila["monto"]) > limite:
        sospechosos.append(fila)

print(f"Umbral de sospecha (3x promedio): ${limite:,.0f}")
print(f"Transacciones atípicas encontradas: {len(sospechosos)}")
for s in sospechosos:
    print(f"  id {s['id']} | {s['ciudad']:<13} | ${int(s['monto']):>12,}")
"""),

md(r"""
> 🤔 **¿Qué pasaría si...?** elimináramos los outliers antes de calcular el
> promedio. ¿Subiría o bajaría el ticket promedio? Los valores atípicos altos
> *inflan* el promedio: por eso en estadística a veces se prefiere la **mediana**.
> Lo veremos con detalle más adelante.
""")
,
]


# --------------------------------------------------------------------------- #
# Sección "TU TURNO": 3 mini-tareas con comprobación suave
# --------------------------------------------------------------------------- #
C += [
md(r"""
---
## 🛠️ Tu turno

Ahora resuelve tú. Completa cada función y ejecuta su comprobación.
"""),

md(r"""
### Tarea A · Ingreso por método de pago

Completa `total_por_metodo(filas, metodo)`: la suma de los montos cuyas
transacciones usaron ese `metodo_pago`.

**Ejemplo:** `total_por_metodo(filas, "efectivo")` → suma de todas las compras en
efectivo.
"""),

code(r"""
def total_por_metodo(filas, metodo):
    # ✏️ TU CÓDIGO AQUÍ (acumulador con condición)
    return None

# Comprobación: comparamos contra un cálculo de referencia hecho aparte.
_ref_efectivo = sum(int(f["monto"]) for f in filas if f["metodo_pago"] == "efectivo")
revisar("efectivo", total_por_metodo(filas, "efectivo") == _ref_efectivo)
_ref_tarjeta = sum(int(f["monto"]) for f in filas if f["metodo_pago"] == "tarjeta")
revisar("tarjeta", total_por_metodo(filas, "tarjeta") == _ref_tarjeta)
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def total_por_metodo(filas, metodo):
    total = 0
    for f in filas:
        if f["metodo_pago"] == metodo:
            total += int(f["monto"])
    return total
```
</details>
"""),

md(r"""
### Tarea B · Contar transacciones de una ciudad

Completa `contar_ciudad(filas, ciudad)`: cuántas transacciones ocurrieron en esa
ciudad.
"""),

code(r"""
def contar_ciudad(filas, ciudad):
    # ✏️ TU CÓDIGO AQUÍ (contador con condición)
    return None

_ref_bogota = sum(1 for f in filas if f["ciudad"] == "Bogota")
revisar("Bogota", contar_ciudad(filas, "Bogota") == _ref_bogota)
_ref_cali = sum(1 for f in filas if f["ciudad"] == "Cali")
revisar("Cali", contar_ciudad(filas, "Cali") == _ref_cali)
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def contar_ciudad(filas, ciudad):
    cuenta = 0
    for f in filas:
        if f["ciudad"] == ciudad:
            cuenta += 1
    return cuenta
```
</details>
"""),

md(r"""
### Tarea C · Promedio de una categoría

Completa `promedio_categoria(filas, categoria)`: el promedio de los montos de esa
categoría. Si no hay ninguna transacción de esa categoría, devuelve `None`
(¡caso borde!).
"""),

code(r"""
def promedio_categoria(filas, categoria):
    # ✏️ TU CÓDIGO AQUÍ (acumulador + contador + validar división)
    return None

_montos_tec = [int(f["monto"]) for f in filas if f["categoria"] == "tecnologia"]
_ref_tec = sum(_montos_tec) / len(_montos_tec)
revisar("tecnologia", promedio_categoria(filas, "tecnologia") == _ref_tec)
revisar("categoría inexistente -> None", promedio_categoria(filas, "no_existe") is None)
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def promedio_categoria(filas, categoria):
    total = 0
    cuenta = 0
    for f in filas:
        if f["categoria"] == categoria:
            total += int(f["monto"])
            cuenta += 1
    if cuenta == 0:
        return None
    return total / cuenta
```
</details>
"""),

md(r"""
---
## Reflexión final: eficiencia y lo que viene

Fíjate en algo: para responder 5 preguntas recorrimos la lista de transacciones
**varias veces** (una por pregunta). Con 120 filas no importa, pero con 50 millones
de filas, cada recorrido cuesta. Parte del oficio es decidir *cuándo* combinar
trabajo en un solo recorrido y *cuándo* separar por claridad.

También notaste cuánto código hizo falta para agrupar por ciudad "a mano". En la
**Clase 6** harás exactamente esto con pandas en **una sola línea**:

```python
df.groupby("ciudad")["monto"].sum()
```

Pero ahora **sabes qué hace esa línea por dentro** — y esa comprensión es lo que
separa a quien usa una herramienta de quien la domina.

➡️ Sigue con **homework01.ipynb** y **homework02.ipynb** para afianzar lo aprendido.
"""),
]


# ===================================================================== #
# VALIDACIÓN en construcción: las soluciones de referencia funcionan sobre el CSV
# ===================================================================== #
def _validar():
    import csv
    ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "datasets", "transacciones.csv")
    with open(os.path.abspath(ruta), encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    def total_por_metodo(filas, metodo):
        return sum(int(x["monto"]) for x in filas if x["metodo_pago"] == metodo)

    def contar_ciudad(filas, ciudad):
        return sum(1 for x in filas if x["ciudad"] == ciudad)

    def promedio_categoria(filas, categoria):
        m = [int(x["monto"]) for x in filas if x["categoria"] == categoria]
        return None if not m else sum(m) / len(m)

    assert total_por_metodo(filas, "efectivo") > 0
    assert contar_ciudad(filas, "Bogota") >= 0
    assert promedio_categoria(filas, "no_existe") is None
    assert promedio_categoria(filas, "tecnologia") > 0
    print("✔ Las soluciones de referencia de practice02 funcionan sobre el dataset.")

_validar()


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase01", "practice02.ipynb")
build(os.path.abspath(ruta), C)
