"""Construye curso/clase04/practice02.ipynb — caso aplicado: análisis de transacciones
con diccionarios, índice invertido y conjuntos.

El estudiante construye paso a paso:
  1. Índice invertido ciudad → lista de transacciones
  2. Resumen por categoría usando dict
  3. Clientes únicos por ciudad con set
Luego hay tres "Tu turno" con comprobación suave.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []

C += [
md(r"""
# Clase 4 · Práctica 02 — Análisis de transacciones con diccionarios

### Del dataset a la inteligencia de negocio

En la clase aprendimos las cuatro estructuras de datos de Python y sus patrones.
Ahora las aplicamos a un dataset real de transacciones para responder preguntas
de negocio concretas.

**Lo que construiremos:**
1. **Índice invertido** `ciudad → [transacciones]` para consultas rápidas.
2. **Resumen por categoría** usando dict (total, promedio, conteo).
3. **Clientes únicos por ciudad** usando set.

> 🎯 Al final, habrás implementado, en Python puro, algo muy parecido a lo que
> hace `pandas.groupby()` internamente.
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
### Limpieza previa: convertir tipos

Al cargar un CSV, todo llega como texto. Convertimos los tipos necesarios
una sola vez para no hacerlo en cada operación.
"""),

code(r"""
# Convertir monto a entero en todas las filas
for f in filas:
    f["monto"] = int(f["monto"])

print("Tipo de monto tras conversion:", type(filas[0]["monto"]).__name__)
print("Ciudades presentes:", sorted({f["ciudad"] for f in filas}))
print("Categorias presentes:", sorted({f["categoria"] for f in filas}))
print("Metodos de pago:", sorted({f["metodo_pago"] for f in filas}))
"""),
]


# --------------------------------------------------------------------- #
# PARTE 1: Índice invertido ciudad → transacciones
# --------------------------------------------------------------------- #
C += [
md(r"""
## Parte 1 · Índice invertido: ciudad → transacciones

Un **índice invertido** mapea un valor (ciudad) a todos los registros que
lo contienen. Es exactamente como un índice de libro: en vez de leer todo
el libro, vas directo a la página.

**Antes del índice:** para obtener transacciones de Bogotá hay que recorrer
las 120 filas cada vez → O(n) por consulta.

**Con el índice:** la lista de transacciones de Bogotá está precalculada →
O(1) para acceder, O(n) para construir (una sola vez).

### Algoritmo
```
indice = {}
PARA CADA fila EN filas HACER
    ciudad = fila["ciudad"]
    SI ciudad NO está en indice ENTONCES
        indice[ciudad] = []
    FIN_SI
    indice[ciudad].append(fila)
FIN_PARA
```
"""),

code(r"""
# Construir el indice ciudad -> [filas]
indice_ciudad = {}
for f in filas:
    ciudad = f["ciudad"]
    if ciudad not in indice_ciudad:
        indice_ciudad[ciudad] = []
    indice_ciudad[ciudad].append(f)

# Resumen del indice
print("Indice construido. Transacciones por ciudad:")
for ciudad in sorted(indice_ciudad.keys()):
    n = len(indice_ciudad[ciudad])
    total = sum(f["monto"] for f in indice_ciudad[ciudad])
    print("  {:<15} {:>4} transacciones   total ${:>12,}".format(ciudad, n, total))
"""),

code(r"""
# Consulta rapida: top 3 transacciones de Medellin por monto
tx_medellin = indice_ciudad.get("Medellin", [])
top3 = sorted(tx_medellin, key=lambda f: f["monto"], reverse=True)[:3]
print("Top 3 transacciones en Medellin:")
for t in top3:
    print("  id={} | {} | ${:,}".format(t["id"], t["categoria"], t["monto"]))
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

El índice usa listas porque una ciudad puede tener muchas transacciones.
¿Qué estructura usarías si cada ciudad tuviera **exactamente una** transacción
y necesitaras acceder por ciudad? ¿Qué estructura si solo necesitas saber
*si una ciudad tiene transacciones* (sin acceder a los datos)?
"""),
]


# --------------------------------------------------------------------- #
# PARTE 2: Resumen por categoría
# --------------------------------------------------------------------- #
C += [
md(r"""
## Parte 2 · Resumen por categoría con dict

Queremos, para cada categoría:
- Número total de transacciones.
- Suma de montos.
- Promedio de monto.

Usaremos un **dict de dicts**: `{categoria: {"total": ..., "suma": ..., "n": ...}}`.
"""),

code(r"""
# Resumen por categoria: {cat: {"n": conteo, "suma": total}}
resumen_cat = {}
for f in filas:
    cat = f["categoria"]
    if cat not in resumen_cat:
        resumen_cat[cat] = {"n": 0, "suma": 0}
    resumen_cat[cat]["n"] += 1
    resumen_cat[cat]["suma"] += f["monto"]

# Calcular promedio y mostrar
print("{:<15} {:>8} {:>14} {:>14}".format("Categoria", "N", "Total", "Promedio"))
print("-" * 55)
for cat in sorted(resumen_cat.keys()):
    r = resumen_cat[cat]
    promedio = r["suma"] / r["n"]
    print("{:<15} {:>8} {:>14,} {:>14,.0f}".format(cat, r["n"], r["suma"], promedio))
"""),

code(r"""
# Encontrar la categoria con mayor promedio de monto (patron campeon sobre dict)
mejor_cat = None
mejor_prom = 0
for cat, r in resumen_cat.items():
    prom = r["suma"] / r["n"]
    if prom > mejor_prom:
        mejor_prom = prom
        mejor_cat = cat

print("Categoria con mayor promedio de monto: {} (${:,.0f})".format(mejor_cat, mejor_prom))
"""),

md(r"""
### Comprensión de dict para el resumen

El mismo resultado usando comprensión — más conciso, mismo resultado:
"""),

code(r"""
# Resumen con comprension (equivalente al bucle anterior)
categorias = sorted({f["categoria"] for f in filas})

resumen_comp = {
    cat: {
        "n":    sum(1 for f in filas if f["categoria"] == cat),
        "suma": sum(f["monto"] for f in filas if f["categoria"] == cat),
    }
    for cat in categorias
}

# Verificar que son iguales
for cat in categorias:
    assert resumen_comp[cat]["n"]    == resumen_cat[cat]["n"],    "conteo difiere en " + cat
    assert resumen_comp[cat]["suma"] == resumen_cat[cat]["suma"], "suma difiere en " + cat
print("Ambas implementaciones producen el mismo resultado.")
print("Nota: la version con bucle es O(n); la comprension es O(n*k) donde k=nro categorias.")
"""),
]


# --------------------------------------------------------------------- #
# PARTE 3: Clientes únicos por ciudad
# --------------------------------------------------------------------- #
C += [
md(r"""
## Parte 3 · Clientes únicos por ciudad con set

El campo `id` identifica cada transacción (no al cliente), pero podemos
simular "clientes únicos" como los ids de transacción distintos por ciudad.

Aquí usamos **dict de sets**: `{ciudad: set_de_ids}`.
Los sets eliminan duplicados automáticamente y la operación `|` (unión)
nos da los ids que compraron en *alguna* ciudad.
"""),

code(r"""
# Construir {ciudad: set de ids de transaccion}
ids_por_ciudad = {}
for f in filas:
    ciudad = f["ciudad"]
    ids_por_ciudad.setdefault(ciudad, set()).add(f["id"])

print("IDs unicos por ciudad:")
for ciudad in sorted(ids_por_ciudad.keys()):
    print("  {:<15} {} ids".format(ciudad, len(ids_por_ciudad[ciudad])))

# Como cada id es unico en el dataset, el set coincide con el conteo por lista
# pero la estructura de set permite operaciones de conjunto directamente
"""),

code(r"""
# Operaciones de conjunto entre ciudades
ids_bogota = ids_por_ciudad.get("Bogota", set())
ids_cali   = ids_por_ciudad.get("Cali",   set())

# (En este dataset cada id es unico, pero el patron es util cuando hay ids repetidos)
solo_bogota  = ids_bogota - ids_cali
solo_cali    = ids_cali - ids_bogota
en_ambas     = ids_bogota & ids_cali
en_cualquiera = ids_bogota | ids_cali

print("Solo en Bogota:   {} transacciones".format(len(solo_bogota)))
print("Solo en Cali:     {} transacciones".format(len(solo_cali)))
print("En ambas:         {} transacciones".format(len(en_ambas)))
print("En alguna:        {} transacciones".format(len(en_cualquiera)))
"""),
]


# --------------------------------------------------------------------- #
# TU TURNO: 3 tareas con comprobación
# --------------------------------------------------------------------- #
C += [
md(r"""
---
## Tu turno

Completa cada función y ejecuta su comprobación.
"""),

md(r"""
### Tarea A · Top-3 categorías por ingreso total

Completa `top3_categorias(filas)` que devuelva una **lista** con las 3
categorías de mayor ingreso total, ordenadas de mayor a menor.

**Resultado esperado:** una lista de 3 strings con nombres de categoría.
"""),

code(r"""
def top3_categorias(filas):
    # ✏️ TU CÓDIGO AQUÍ
    # Pista: construye {cat: total} y luego ordena por valor desc.
    return None

# Comprobacion
resultado = top3_categorias(filas)
_totales_ref = {}
for f in filas:
    _totales_ref[f["categoria"]] = _totales_ref.get(f["categoria"], 0) + f["monto"]
_top3_ref = sorted(_totales_ref, key=_totales_ref.get, reverse=True)[:3]

revisar("devuelve 3 categorias", isinstance(resultado, list) and len(resultado) == 3)
revisar("coincide con referencia", resultado == _top3_ref)
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def top3_categorias(filas):
    totales = {}
    for f in filas:
        totales[f["categoria"]] = totales.get(f["categoria"], 0) + f["monto"]
    return sorted(totales, key=totales.get, reverse=True)[:3]
```
`sorted(dict, key=dict.get, reverse=True)` ordena las claves por su valor
descendente. `[:3]` toma los tres primeros.
</details>
"""),

md(r"""
### Tarea B · Ciudades con más de N transacciones (set + comprensión)

Completa `ciudades_activas(filas, min_tx)` que devuelva un **set** con las
ciudades que tienen al menos `min_tx` transacciones.
"""),

code(r"""
def ciudades_activas(filas, min_tx):
    # ✏️ TU CÓDIGO AQUÍ
    # Pista: construye {ciudad: conteo}, luego filtra.
    return None

# Comprobacion
_conteo_ref = {}
for f in filas:
    _conteo_ref[f["ciudad"]] = _conteo_ref.get(f["ciudad"], 0) + 1
_activas_20 = {c for c, n in _conteo_ref.items() if n >= 20}
_activas_50 = {c for c, n in _conteo_ref.items() if n >= 50}

revisar("min_tx=20", ciudades_activas(filas, 20) == _activas_20)
revisar("min_tx=50", ciudades_activas(filas, 50) == _activas_50)
revisar("min_tx=999 -> vacio", ciudades_activas(filas, 999) == set())
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def ciudades_activas(filas, min_tx):
    conteo = {}
    for f in filas:
        conteo[f["ciudad"]] = conteo.get(f["ciudad"], 0) + 1
    return {ciudad for ciudad, n in conteo.items() if n >= min_tx}
```
</details>
"""),

md(r"""
### Tarea C · Índice de búsqueda: método de pago → set de ciudades

Completa `indice_metodo_ciudades(filas)` que devuelva un dict
`{metodo_pago: set_de_ciudades}` indicando en qué ciudades se usó ese
método de pago.

**Ejemplo de estructura:**
```python
{
  "efectivo":      {"Bogota", "Cali", "Medellin", ...},
  "tarjeta":       {"Bogota", "Barranquilla", ...},
  "transferencia": {...},
}
```
"""),

code(r"""
def indice_metodo_ciudades(filas):
    # ✏️ TU CÓDIGO AQUÍ
    return None

# Comprobacion
indice_ref = {}
for f in filas:
    indice_ref.setdefault(f["metodo_pago"], set()).add(f["ciudad"])

resultado_c = indice_metodo_ciudades(filas)
metodos = ["efectivo", "tarjeta", "transferencia"]

revisar("tiene los 3 metodos", set(resultado_c.keys()) == set(metodos))
for m in metodos:
    revisar("{} ciudades correctas".format(m),
            resultado_c.get(m, set()) == indice_ref.get(m, set()))
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def indice_metodo_ciudades(filas):
    indice = {}
    for f in filas:
        indice.setdefault(f["metodo_pago"], set()).add(f["ciudad"])
    return indice
```
`setdefault(k, set()).add(v)` inicializa el set si la clave no existe
y agrega el elemento en una sola expresión.
</details>
"""),

md(r"""
---
## Reflexión final

Hoy construiste, en Python puro:

| Lo que hiciste | Equivalente en pandas |
|---|---|
| Índice ciudad→filas | `df.groupby("ciudad")` |
| Resumen por categoría | `df.groupby("categoria")["monto"].agg(["count","sum","mean"])` |
| Set de ciudades únicas | `df["ciudad"].nunique()` |
| Top 3 por ingreso | `df.groupby("categoria")["monto"].sum().nlargest(3)` |

La diferencia: pandas ejecuta estas operaciones en C, con vectores, para
millones de filas en milisegundos. Pero **sabes exactamente qué hace cada
operación**, y eso es lo que te convierte en un usuario que entiende y no
solo copia.

➡️ Sigue con **homework01.ipynb** y **homework02.ipynb** para afianzar.
"""),
]


# ===================================================================== #
# VALIDACIÓN EN TIEMPO DE CONSTRUCCIÓN
# ===================================================================== #
def _validar():
    import csv
    ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "datasets", "transacciones.csv")
    with open(os.path.abspath(ruta), encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    for row in filas:
        row["monto"] = int(row["monto"])

    def top3_categorias(filas):
        totales = {}
        for f in filas:
            totales[f["categoria"]] = totales.get(f["categoria"], 0) + f["monto"]
        return sorted(totales, key=totales.get, reverse=True)[:3]

    def ciudades_activas(filas, min_tx):
        conteo = {}
        for f in filas:
            conteo[f["ciudad"]] = conteo.get(f["ciudad"], 0) + 1
        return {c for c, n in conteo.items() if n >= min_tx}

    def indice_metodo_ciudades(filas):
        indice = {}
        for f in filas:
            indice.setdefault(f["metodo_pago"], set()).add(f["ciudad"])
        return indice

    top3 = top3_categorias(filas)
    assert isinstance(top3, list) and len(top3) == 3

    activas = ciudades_activas(filas, 1)
    assert len(activas) > 0
    assert ciudades_activas(filas, 999) == set()

    indice = indice_metodo_ciudades(filas)
    assert set(indice.keys()) == {"efectivo", "tarjeta", "transferencia"}
    for v in indice.values():
        assert isinstance(v, set)

    print("✔ Las soluciones de referencia de practice02 (clase04) funcionan sobre el dataset.")

_validar()


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase04", "practice02.ipynb")
build(os.path.abspath(ruta), C)
