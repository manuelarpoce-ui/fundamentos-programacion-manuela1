"""Construye curso/clase02/practice02.ipynb — caso aplicado con transacciones.

Análisis de transacciones financieras usando los conceptos de la Clase 2:
tipos de datos, conversión de tipos, operadores y condicionales.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []

C += [
md(r"""
# Clase 2 · Práctica 02 — Análisis de transacciones financieras

### Variables, tipos, operadores y condicionales aplicados a datos reales

En esta sesión analizamos un dataset real de transacciones de una tienda con
sucursales en varias ciudades colombianas. Usaremos exactamente los conceptos
de la Clase 2:

- **Conversión de tipos:** los montos llegan como `str` desde el CSV.
- **Operadores aritméticos:** calcular comisiones, totales, promedios.
- **Operadores relacionales y lógicos:** filtrar transacciones.
- **Condicionales `if/elif/else`:** clasificar y categorizar datos.

> 🎯 **Meta:** al terminar, habrás producido un reporte ejecutivo con las
> métricas clave del negocio.

**Preguntas de negocio que responderemos:**
1. ¿Cuántas transacciones hay por categoría?
2. ¿Cuál es la comisión que cobra el procesador de pagos según el método y el monto?
3. ¿Qué transacciones son de "alto valor" (>200000 COP)?
4. ¿Cómo se distribuye el ingreso por ciudad?
5. **Tu turno:** tres tareas para que implementes tú.
"""),

code(r"""
import csv, os, sys
sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar

ruta = os.path.join("..", "datasets", "transacciones.csv")
with open(ruta, encoding="utf-8") as f:
    filas = list(csv.DictReader(f))

print("Transacciones cargadas:", len(filas))
print("Columnas:", list(filas[0].keys()))
print("Primera fila:", filas[0])
"""),

md(r"""
### Paso 1 · Limpieza y conversión de tipos

Todo llega como `str` desde el CSV. Antes de cualquier cálculo, convertimos
`monto` a `int`. Este es el primer paso en cualquier pipeline de datos.
"""),

code(r"""
# Convertir monto de str a int en cada fila.
# Creamos una lista de diccionarios con el monto ya convertido.
transacciones = []
for fila in filas:
    t = dict(fila)               # copia para no modificar el original
    t["monto"] = int(fila["monto"])   # type casting: str -> int
    transacciones.append(t)

print("Tipo de monto antes de convertir:", type(filas[0]["monto"]))
print("Tipo de monto despues de convertir:", type(transacciones[0]["monto"]))
print()

# Extraer solo los montos para análisis numérico rápido:
montos = [t["monto"] for t in transacciones]
print("Primeros 5 montos:", montos[:5])
print("Rango: ${:,.0f} – ${:,.0f}".format(min(montos), max(montos)))
"""),

md(r"""
### Paso 2 · Estadísticas básicas (operadores aritméticos)

Con los montos ya convertidos, aplicamos los patrones de acumulador y campeón.
"""),

code(r"""
# Acumulador para total; campeón para máximo y mínimo.
total    = sum(montos)
promedio = total / len(montos)
maximo   = max(montos)
minimo   = min(montos)

print("=== Estadisticas generales ===")
print("Transacciones: {:,}".format(len(montos)))
print("Total facturado: ${:,.0f}".format(total))
print("Ticket promedio: ${:,.0f}".format(promedio))
print("Monto maximo:    ${:,.0f}".format(maximo))
print("Monto minimo:    ${:,.0f}".format(minimo))
"""),

md(r"""
### Paso 3 · Clasificar transacciones con condicionales

Aplicamos el esquema de clasificación de la Clase 2: cada transacción recibe
una etiqueta según su monto.
"""),

code(r"""
def clasificar_transaccion(monto):
    """Clasifica el monto: bajo / medio / alto."""
    if monto > 200000:
        return "alto"
    elif monto > 50000:
        return "medio"
    else:
        return "bajo"

# Contar cuántas hay de cada categoría de monto:
conteo = {"bajo": 0, "medio": 0, "alto": 0}
for t in transacciones:
    cat = clasificar_transaccion(t["monto"])
    conteo[cat] += 1

print("=== Clasificacion por monto ===")
for cat, n in conteo.items():
    pct = n / len(transacciones) * 100
    print("  {:6}: {:3} transacciones ({:.1f}%)".format(cat, n, pct))
"""),

md(r"""
### Paso 4 · Calcular comisiones por método de pago

Los procesadores de pago cobran distintas comisiones según el método:

| Método de pago | Comisión |
|---|---|
| efectivo | 0% (sin cargo) |
| tarjeta | 2.5% del monto |
| transferencia | 1.0% del monto, máximo $5000 |

Usaremos `if/elif/else` para aplicar la regla correcta.
"""),

code(r"""
def calcular_comision(monto, metodo_pago):
    """Calcula la comisión del procesador de pagos."""
    if metodo_pago == "efectivo":
        return 0
    elif metodo_pago == "tarjeta":
        return monto * 0.025
    elif metodo_pago == "transferencia":
        comision = monto * 0.01
        return min(comision, 5000)   # tope de 5000 COP
    else:
        return 0   # método desconocido: sin comisión

# Verificar con ejemplos puntuales:
print("Comision tarjeta $100,000:     ${:.0f}".format(calcular_comision(100000, "tarjeta")))
print("Comision transferencia $100k:  ${:.0f}".format(calcular_comision(100000, "transferencia")))
print("Comision transferencia $800k:  ${:.0f}".format(calcular_comision(800000, "transferencia")))
print("Comision efectivo:             ${:.0f}".format(calcular_comision(200000, "efectivo")))
print()

# Aplicar a todas las transacciones:
total_comisiones = 0
for t in transacciones:
    comision = calcular_comision(t["monto"], t["metodo_pago"])
    total_comisiones += comision

print("Total comisiones del periodo: ${:,.0f}".format(total_comisiones))
"""),

md(r"""
### Paso 5 · Transacciones de alto valor

Filtramos las transacciones con monto > 200000 para análisis especial.
Estas requieren revisión adicional o condiciones comerciales distintas.
"""),

code(r"""
alto_valor = [t for t in transacciones if t["monto"] > 200000]

print("Transacciones de alto valor (> $200,000): {}".format(len(alto_valor)))
print()
print("{:<6} {:<14} {:<12} {:>12}".format("ID", "Ciudad", "Categoria", "Monto"))
print("-" * 48)
for t in alto_valor[:10]:   # mostrar primeras 10
    print("{:<6} {:<14} {:<12} {:>12,.0f}".format(
        t["id"], t["ciudad"], t["categoria"], t["monto"]))
if len(alto_valor) > 10:
    print("  ... y {} mas".format(len(alto_valor) - 10))
"""),

md(r"""
### Paso 6 · Ingreso por ciudad

Agrupamos el total facturado por ciudad usando un diccionario de contadores.
"""),

code(r"""
# Acumular monto por ciudad.
totales_ciudad = {}
for t in transacciones:
    ciudad = t["ciudad"]
    if ciudad not in totales_ciudad:
        totales_ciudad[ciudad] = 0
    totales_ciudad[ciudad] += t["monto"]

# Ordenar de mayor a menor (usando sorted con key):
ciudades_ord = sorted(totales_ciudad.items(), key=lambda x: x[1], reverse=True)

print("=== Ingreso por ciudad ===")
print("{:<14} {:>14} {:>10}".format("Ciudad", "Total ($)", "% del total"))
print("-" * 42)
for ciudad, total_c in ciudades_ord:
    pct = total_c / total * 100
    print("{:<14} {:>14,.0f} {:>9.1f}%".format(ciudad, total_c, pct))
"""),
]


# --------------------------------------------------------------------------- #
# Sección "Tu turno"
# --------------------------------------------------------------------------- #
C += [
md(r"""
---
## Tu turno

Ahora implementa tú. Completa cada función y ejecuta su comprobación.
"""),

md(r"""
### Tarea A · Monto neto (monto menos comisión)

Completa `monto_neto(monto, metodo_pago)` que devuelva el monto **después**
de descontar la comisión del procesador. Reutiliza `calcular_comision`.

**Ejemplo:** `monto_neto(100000, "tarjeta")` → `97500.0`
(100000 - 2500 de comisión al 2.5%).
"""),

code(r"""
def monto_neto(monto, metodo_pago):
    # ✏️ TU CÓDIGO AQUÍ — usa calcular_comision()
    return None

_ref_tarjeta = 100000 - calcular_comision(100000, "tarjeta")
revisar("100k tarjeta neto = 97500", monto_neto(100000, "tarjeta") == _ref_tarjeta)
_ref_efectivo = 80000 - calcular_comision(80000, "efectivo")
revisar("80k efectivo neto = 80000", monto_neto(80000, "efectivo") == _ref_efectivo)
_ref_trans = 500000 - calcular_comision(500000, "transferencia")
revisar("500k transferencia neto", monto_neto(500000, "transferencia") == _ref_trans)
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def monto_neto(monto, metodo_pago):
    return monto - calcular_comision(monto, metodo_pago)
```
Al reutilizar `calcular_comision`, toda la lógica de comisiones está en
un solo lugar. Si cambian las tasas, solo actualizas esa función.
</details>
"""),

md(r"""
### Tarea B · Contar transacciones por método de pago

Completa `contar_por_metodo(transacciones, metodo)` que devuelva cuántas
transacciones usan ese método de pago.

**Ejemplo:** `contar_por_metodo(transacciones, "efectivo")` → entero >= 0.
"""),

code(r"""
def contar_por_metodo(transacciones, metodo):
    # ✏️ TU CÓDIGO AQUÍ
    return None

_ref_ef  = sum(1 for t in transacciones if t["metodo_pago"] == "efectivo")
_ref_tc  = sum(1 for t in transacciones if t["metodo_pago"] == "tarjeta")
_ref_tr  = sum(1 for t in transacciones if t["metodo_pago"] == "transferencia")

revisar("efectivo count correcto",      contar_por_metodo(transacciones, "efectivo") == _ref_ef)
revisar("tarjeta count correcto",       contar_por_metodo(transacciones, "tarjeta") == _ref_tc)
revisar("transferencia count correcto", contar_por_metodo(transacciones, "transferencia") == _ref_tr)
revisar("metodo inexistente = 0",       contar_por_metodo(transacciones, "criptomoneda") == 0)
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def contar_por_metodo(transacciones, metodo):
    cuenta = 0
    for t in transacciones:
        if t["metodo_pago"] == metodo:
            cuenta += 1
    return cuenta
```
**Versión compacta:**
```python
def contar_por_metodo(transacciones, metodo):
    return sum(1 for t in transacciones if t["metodo_pago"] == metodo)
```
</details>
"""),

md(r"""
### Tarea C · Promedio de monto por categoría de producto

Completa `promedio_categoria(transacciones, categoria)` que devuelva el
promedio del monto para esa categoría. Si no hay transacciones de esa
categoría, devuelve `None`.

**Categorías disponibles:** `tecnologia`, `alimentos`, `hogar`, `aseo`, `papeleria`.
"""),

code(r"""
def promedio_categoria(transacciones, categoria):
    # ✏️ TU CÓDIGO AQUÍ
    return None

_montos_tec = [t["monto"] for t in transacciones if t["categoria"] == "tecnologia"]
_ref_tec    = sum(_montos_tec) / len(_montos_tec)

revisar("tecnologia promedio correcto",  promedio_categoria(transacciones, "tecnologia") == _ref_tec)
revisar("categoria inexistente -> None", promedio_categoria(transacciones, "muebles") is None)

_montos_ali = [t["monto"] for t in transacciones if t["categoria"] == "alimentos"]
_ref_ali    = sum(_montos_ali) / len(_montos_ali)
revisar("alimentos promedio correcto",   promedio_categoria(transacciones, "alimentos") == _ref_ali)
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def promedio_categoria(transacciones, categoria):
    montos = [t["monto"] for t in transacciones if t["categoria"] == categoria]
    if len(montos) == 0:
        return None
    return sum(montos) / len(montos)
```
Validar antes de dividir (`len == 0 → return None`) evita el
`ZeroDivisionError` en el caso borde de una categoría sin transacciones.
</details>
"""),

md(r"""
---
## Reporte ejecutivo final

Unamos todo en un reporte compacto.
"""),

code(r"""
print("=" * 55)
print("     REPORTE EJECUTIVO DE TRANSACCIONES")
print("=" * 55)
print()
print("VOLUMEN")
print("  Transacciones:          {:>8,}".format(len(transacciones)))
print("  Total facturado:        {:>12,.0f} COP".format(total))
print("  Ticket promedio:        {:>12,.0f} COP".format(promedio))
print("  Total comisiones:       {:>12,.0f} COP".format(total_comisiones))
print()
print("TRANSACCIONES ALTO VALOR (> $200,000)")
print("  Cantidad:               {:>8,}".format(len(alto_valor)))
print("  % del total:            {:>7.1f}%".format(len(alto_valor) / len(transacciones) * 100))
print()
print("CLASIFICACION POR MONTO")
for cat, n in conteo.items():
    print("  {:6}: {:>3} ({:.0f}%)".format(cat, n, n / len(transacciones) * 100))
print()
print("CIUDAD LIDER:", ciudades_ord[0][0],
      "  ${:,.0f}".format(ciudades_ord[0][1]))
print("=" * 55)
"""),
]


# ===================================================================== #
# VALIDACIÓN en construcción
# ===================================================================== #
def _validar():
    import csv
    ruta = os.path.join(
        os.path.dirname(__file__), "..", "curso", "datasets", "transacciones.csv"
    )
    with open(os.path.abspath(ruta), encoding="utf-8") as f:
        filas = list(csv.DictReader(f))

    transacciones = []
    for fila in filas:
        t = dict(fila)
        t["monto"] = int(fila["monto"])
        transacciones.append(t)

    def calcular_comision(monto, metodo_pago):
        if metodo_pago == "efectivo":
            return 0
        elif metodo_pago == "tarjeta":
            return monto * 0.025
        elif metodo_pago == "transferencia":
            return min(monto * 0.01, 5000)
        else:
            return 0

    def monto_neto(monto, metodo_pago):
        return monto - calcular_comision(monto, metodo_pago)

    def contar_por_metodo(transacciones, metodo):
        return sum(1 for t in transacciones if t["metodo_pago"] == metodo)

    def promedio_categoria(transacciones, categoria):
        montos = [t["monto"] for t in transacciones if t["categoria"] == categoria]
        return None if not montos else sum(montos) / len(montos)

    # Assertions:
    assert monto_neto(100000, "tarjeta") == 97500.0
    assert monto_neto(80000, "efectivo") == 80000
    assert contar_por_metodo(transacciones, "efectivo") > 0
    assert contar_por_metodo(transacciones, "criptomoneda") == 0
    assert promedio_categoria(transacciones, "tecnologia") > 0
    assert promedio_categoria(transacciones, "muebles") is None

    print("✔ Las soluciones de referencia de practice02 funcionan sobre el dataset.")

_validar()


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase02", "practice02.ipynb")
build(os.path.abspath(ruta), C)
