"""Construye curso/clase03/practice02.ipynb — pipeline de procesamiento de transacciones.

Tema: normalizar, transformar y resumir datos usando funciones y map/filter
sobre el dataset de transacciones reales del curso.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []

# --------------------------------------------------------------------------- #
# Portada
# --------------------------------------------------------------------------- #
C += [
md(r"""
# Clase 3 · Práctica 02 — Pipeline de procesamiento de transacciones

### Funciones, map y filter aplicados a datos reales

En la clase de hoy aprendiste bucles, funciones y el paradigma funcional
(`lambda`, `map`, `filter`). Ahora los aplicamos a un caso real de negocio:
construir un **pipeline de procesamiento de datos** paso a paso.

**Objetivo del negocio:** a partir de un archivo CSV de transacciones,
queremos producir un reporte limpio que incluya:
1. Normalizar y limpiar los datos (detectar inválidos, convertir tipos).
2. Enriquecer cada transacción: calcular IVA, clasificar por tamaño.
3. Filtrar y resumir: totales por categoría, transacciones grandes, estadísticas.

> 🎯 Todavía no usamos NumPy ni pandas. Todo con listas, funciones y bucles,
> para que entiendas qué hacen esas herramientas por dentro.
"""),

code(r"""
# Cargar dataset y utilidad de comprobación.
import csv, os, sys
sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar

ruta = os.path.join("..", "datasets", "transacciones.csv")
with open(ruta, encoding="utf-8") as f:
    filas_raw = list(csv.DictReader(f))

print("Transacciones cargadas:", len(filas_raw))
print("Columnas:", list(filas_raw[0].keys()))
print("Primera fila:", filas_raw[0])
"""),
]

# --------------------------------------------------------------------------- #
# PASO 1: Normalizar y limpiar
# --------------------------------------------------------------------------- #
C += [
md(r"""
## Paso 1 · Normalizar y limpiar los datos

Al leer un CSV, todo llega como texto (`str`). Antes de cualquier cálculo,
debemos **convertir tipos** y **validar** que los valores tengan sentido.

**Función de normalización:** convertir cada fila en un diccionario con los
tipos correctos y añadir un flag `"valida"`.
"""),

code(r"""
def normalizar_fila(fila):
    # Convierte los tipos de una fila y valida que el monto sea positivo.
    # Devuelve un nuevo dict con id(int), monto(int), valida(bool) + resto sin cambios.
    monto = int(fila["monto"])
    return {
        "id":          int(fila["id"]),
        "fecha":       fila["fecha"],
        "ciudad":      fila["ciudad"],
        "categoria":   fila["categoria"],
        "metodo_pago": fila["metodo_pago"],
        "monto":       monto,
        "valida":      monto > 0,
    }

# Aplicamos la normalización a todas las filas con map.
transacciones = list(map(normalizar_fila, filas_raw))

invalidas = list(filter(lambda t: not t["valida"], transacciones))
validas   = list(filter(lambda t: t["valida"], transacciones))

print("Total filas:       ", len(transacciones))
print("Filas validas:     ", len(validas))
print("Filas invalidas:   ", len(invalidas))
if invalidas:
    print("Ejemplo invalida: id=" + str(invalidas[0]["id"]) +
          " monto=" + str(invalidas[0]["monto"]))
"""),

md(r"""
### ¿Por qué `map(normalizar_fila, filas_raw)`?

Porque tenemos **una función que transforma una fila** y queremos aplicarla a
**todas las filas** — exactamente el caso de uso de `map`. Alternativa equivalente
con comprehension: `[normalizar_fila(f) for f in filas_raw]`.

La diferencia es de estilo: `map` es más declarativo ("aplica esta función"),
la comprehension es más explícita. Ambas son correctas.
"""),
]

# --------------------------------------------------------------------------- #
# PASO 2: Enriquecer cada transacción
# --------------------------------------------------------------------------- #
C += [
md(r"""
## Paso 2 · Enriquecer: calcular IVA y clasificar por tamaño

Definimos funciones puras para cada transformación, luego las aplicamos
con `map`. Trabajamos solo sobre las transacciones válidas.
"""),

code(r"""
def clasificar_monto(monto):
    # Clasifica el monto: 'pequena' (<50k), 'mediana' (<300k), 'grande' (resto).
    if monto < 50000:
        return "pequena"
    elif monto < 300000:
        return "mediana"
    else:
        return "grande"

def enriquecer(t):
    # Anade campos iva, total_con_iva y clasificacion a una transaccion valida.
    iva = int(t["monto"] * 0.19)
    return {
        **t,
        "iva":          iva,
        "total_con_iva": t["monto"] + iva,
        "clasificacion": clasificar_monto(t["monto"]),
    }

# Enriquecer solo las validas con map.
transacciones_enriquecidas = list(map(enriquecer, validas))

# Ver las primeras 3 para verificar
for t in transacciones_enriquecidas[:3]:
    print("id={id}  monto=${monto:,}  iva=${iva:,}  total=${total_con_iva:,}  ({clasificacion})".format(**t))
"""),

md(r"""
### El operador `**t` (desempaquetado de diccionario)

`{**t, "nuevo_campo": valor}` crea un **nuevo diccionario** que contiene todo lo
que había en `t` más los campos nuevos. No modifica `t` (inmutabilidad):
un principio clave del paradigma funcional.
"""),
]

# --------------------------------------------------------------------------- #
# PASO 3: Análisis y resumen
# --------------------------------------------------------------------------- #
C += [
md(r"""
## Paso 3 · Analizar y resumir

### 3.1 Total de ventas e IVA recaudado
"""),

code(r"""
def suma_campo(lista, campo):
    # Suma el valor del campo indicado en todos los dicts de la lista.
    total = 0
    for t in lista:
        total += t[campo]
    return total

total_ventas = suma_campo(transacciones_enriquecidas, "monto")
total_iva    = suma_campo(transacciones_enriquecidas, "iva")
total_final  = suma_campo(transacciones_enriquecidas, "total_con_iva")

print("Ventas netas:     $" + "{:,}".format(total_ventas))
print("IVA recaudado:    $" + "{:,}".format(total_iva))
print("Total con IVA:    $" + "{:,}".format(total_final))
print("Ticket promedio:  $" + "{:,.0f}".format(total_ventas / len(transacciones_enriquecidas)))
"""),

md(r"""
### 3.2 Transacciones grandes: filter + map
"""),

code(r"""
# Filtrar grandes, extraer su monto con total con IVA.
grandes = list(filter(lambda t: t["clasificacion"] == "grande",
                      transacciones_enriquecidas))

totales_grandes = list(map(lambda t: t["total_con_iva"], grandes))

print("Transacciones grandes:", len(grandes))
print("Total de ventas grandes: $" + "{:,}".format(sum(totales_grandes)))
print("Pct del total: {:.1f}%".format(sum(totales_grandes) / total_final * 100))
"""),

md(r"""
### 3.3 Resumen por ciudad

Usamos el patrón de **dos listas paralelas** (ciudades vistas + acumuladores),
que ya conocemos de la Clase 1, ahora empaquetado en una función reutilizable.
"""),

code(r"""
def agrupar_por(lista, campo_grupo, campo_valor):
    # Agrupa los valores de campo_valor por campo_grupo.
    # Devuelve lista de tuplas (grupo, suma_valor) ordenada por suma desc.
    grupos = []
    totales = []
    for t in lista:
        grupo = t[campo_grupo]
        valor = t[campo_valor]
        if grupo in grupos:
            i = grupos.index(grupo)
            totales[i] += valor
        else:
            grupos.append(grupo)
            totales.append(valor)
    # Ordenar por total descendente con zip y sorted
    pares = list(zip(grupos, totales))
    return sorted(pares, key=lambda p: p[1], reverse=True)

resumen_ciudad = agrupar_por(transacciones_enriquecidas, "ciudad", "monto")
print("Ventas por ciudad:")
print("-" * 35)
for ciudad, total in resumen_ciudad:
    print("  " + ciudad.ljust(15) + " $" + "{:>12,}".format(total))
"""),

code(r"""
resumen_categoria = agrupar_por(transacciones_enriquecidas, "categoria", "monto")
print("Ventas por categoria:")
print("-" * 35)
for cat, total in resumen_categoria:
    pct = total / total_ventas * 100
    print("  " + cat.ljust(12) + " $" + "{:>10,}".format(total) + "  ({:.1f}%)".format(pct))
"""),
]

# --------------------------------------------------------------------------- #
# TU TURNO
# --------------------------------------------------------------------------- #
C += [
md(r"""
---
## Tu turno

Completa las tres tareas siguientes, que amplían el pipeline que acabamos de
construir. Cada una tiene una comprobación automática.
"""),

md(r"""
### Tarea A · Contar transacciones por método de pago

Escribe `contar_por_metodo(transacciones)` que devuelva una **lista de tuplas**
`(metodo_pago, cantidad)` ordenada de mayor a menor cantidad.

**Pista:** usa el mismo patrón de `agrupar_por`, pero acumula un contador (1)
en lugar del monto.
"""),

code(r"""
def contar_por_metodo(lista):
    # ✏️ TU CÓDIGO AQUÍ
    return None

conteo = contar_por_metodo(transacciones_enriquecidas)

# Comprobaciones
_ref = sorted(
    {t["metodo_pago"] for t in transacciones_enriquecidas},
    key=lambda m: sum(1 for t in transacciones_enriquecidas if t["metodo_pago"] == m),
    reverse=True
)
revisar("devuelve lista",     conteo is not None and isinstance(conteo, list))
revisar("3 metodos de pago",  conteo is not None and len(conteo) == 3)
revisar("suma total correcta", conteo is not None and sum(c for _, c in conteo) == len(transacciones_enriquecidas))
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def contar_por_metodo(lista):
    metodos = []
    conteos = []
    for t in lista:
        m = t["metodo_pago"]
        if m in metodos:
            conteos[metodos.index(m)] += 1
        else:
            metodos.append(m)
            conteos.append(1)
    pares = list(zip(metodos, conteos))
    return sorted(pares, key=lambda p: p[1], reverse=True)
```
</details>
"""),

md(r"""
### Tarea B · Promedio por clasificación usando map/filter

Escribe `promedio_por_clasificacion(transacciones)` que devuelva un diccionario
`{clasificacion: promedio_monto}` para cada una de las tres clasificaciones
("pequena", "mediana", "grande").

**Pista:** para cada clasificación, usa `filter` para obtener esas transacciones,
luego `map` para extraer los montos, luego calcula el promedio.
"""),

code(r"""
def promedio_por_clasificacion(lista):
    # ✏️ TU CÓDIGO AQUÍ
    return None

promedios = promedio_por_clasificacion(transacciones_enriquecidas)

# Comprobaciones
revisar("devuelve dict",          promedios is not None and isinstance(promedios, dict))
revisar("tiene 3 claves",         promedios is not None and len(promedios) == 3)
revisar("pequenas < medianas",    promedios is not None and promedios.get("pequena", 0) < promedios.get("mediana", 0))
revisar("medianas < grandes",     promedios is not None and promedios.get("mediana", 0) < promedios.get("grande", 0))
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def promedio_por_clasificacion(lista):
    resultado = {}
    for clf in ["pequena", "mediana", "grande"]:
        montos = list(map(
            lambda t: t["monto"],
            filter(lambda t: t["clasificacion"] == clf, lista)
        ))
        resultado[clf] = sum(montos) / len(montos) if montos else 0
    return resultado
```
</details>
"""),

md(r"""
### Tarea C · Función de reporte completo

Escribe `generar_reporte(transacciones)` que use las funciones anteriores y
devuelva un diccionario con:
- `"total_ventas"`: suma de todos los montos
- `"n_validas"`: número de transacciones
- `"ciudad_top"`: ciudad con más ventas (string)
- `"n_grandes"`: número de transacciones grandes

Demuestra la **descomposición**: esta función llama a las que ya tienes.
"""),

code(r"""
def generar_reporte(lista):
    # ✏️ TU CÓDIGO AQUÍ (usa sum, agrupar_por, filter que ya definimos arriba)
    return None

reporte = generar_reporte(transacciones_enriquecidas)

revisar("total_ventas > 0",   reporte is not None and reporte.get("total_ventas", 0) > 0)
revisar("n_validas correcto",  reporte is not None and reporte.get("n_validas") == len(transacciones_enriquecidas))
revisar("ciudad_top es string", reporte is not None and isinstance(reporte.get("ciudad_top"), str))
revisar("n_grandes > 0",       reporte is not None and reporte.get("n_grandes", 0) > 0)
"""),

md(r"""
<details><summary>💡 Ver solución</summary>

```python
def generar_reporte(lista):
    total = sum(t["monto"] for t in lista)
    ciudad_top = agrupar_por(lista, "ciudad", "monto")[0][0]   # primera ciudad ordenada
    n_grandes  = len(list(filter(lambda t: t["clasificacion"] == "grande", lista)))
    return {
        "total_ventas": total,
        "n_validas":    len(lista),
        "ciudad_top":   ciudad_top,
        "n_grandes":    n_grandes,
    }
```
</details>
"""),
]

C += [
md(r"""
---
## Reflexión final: el pipeline funcional vs pandas

En esta práctica construiste un pipeline que:
1. **Normaliza** (convierte tipos, valida) con `map`.
2. **Enriquece** (añade campos calculados) con `map`.
3. **Filtra** (transacciones grandes, por ciudad) con `filter`.
4. **Agrupa** (totales por ciudad/categoría) con bucles + funciones.
5. **Resume** componiendo funciones.

En la **Clase 6**, con pandas, los pasos 1-5 quedarán en unas pocas líneas:
```python
df = pd.read_csv("transacciones.csv")
df["iva"] = df["monto"] * 0.19
df.groupby("ciudad")["monto"].sum().sort_values(ascending=False)
```

Pero ahora **sabes exactamente qué hace pandas por dentro**, y cuando algo falle
podrás depurarlo porque entiendes la mecánica. Esa comprensión es lo que separa
al usuario de la herramienta del que la domina.

➡️ Sigue con **homework01.ipynb** y **homework02.ipynb** para afianzar lo aprendido.
"""),
]


# ===================================================================== #
# VALIDACIÓN EN CONSTRUCCIÓN
# ===================================================================== #
def _validar():
    import csv as _csv
    ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "datasets", "transacciones.csv")
    with open(os.path.abspath(ruta), encoding="utf-8") as f:
        filas_raw = list(_csv.DictReader(f))

    def normalizar_fila(fila):
        monto = int(fila["monto"])
        return {
            "id": int(fila["id"]),
            "fecha": fila["fecha"],
            "ciudad": fila["ciudad"],
            "categoria": fila["categoria"],
            "metodo_pago": fila["metodo_pago"],
            "monto": monto,
            "valida": monto > 0,
        }

    def clasificar_monto(monto):
        if monto < 50000:
            return "pequena"
        elif monto < 300000:
            return "mediana"
        else:
            return "grande"

    def enriquecer(t):
        iva = int(t["monto"] * 0.19)
        return {**t, "iva": iva, "total_con_iva": t["monto"] + iva,
                "clasificacion": clasificar_monto(t["monto"])}

    transacciones = list(map(normalizar_fila, filas_raw))
    validas = list(filter(lambda t: t["valida"], transacciones))
    te = list(map(enriquecer, validas))

    assert len(te) > 0, "No hay transacciones validas"

    def agrupar_por(lista, campo_grupo, campo_valor):
        grupos = []
        totales = []
        for t in lista:
            g = t[campo_grupo]
            v = t[campo_valor]
            if g in grupos:
                totales[grupos.index(g)] += v
            else:
                grupos.append(g)
                totales.append(v)
        return sorted(zip(grupos, totales), key=lambda p: p[1], reverse=True)

    resumen = dict(agrupar_por(te, "ciudad", "monto"))
    assert len(resumen) > 0

    def contar_por_metodo(lista):
        metodos = []
        conteos = []
        for t in lista:
            m = t["metodo_pago"]
            if m in metodos:
                conteos[metodos.index(m)] += 1
            else:
                metodos.append(m)
                conteos.append(1)
        return sorted(zip(metodos, conteos), key=lambda p: p[1], reverse=True)

    conteo = contar_por_metodo(te)
    assert len(conteo) == 3
    assert sum(c for _, c in conteo) == len(te)

    def promedio_por_clasificacion(lista):
        resultado = {}
        for clf in ["pequena", "mediana", "grande"]:
            montos = [t["monto"] for t in lista if t["clasificacion"] == clf]
            resultado[clf] = sum(montos) / len(montos) if montos else 0
        return resultado

    promedios = promedio_por_clasificacion(te)
    assert promedios["pequena"] < promedios["mediana"] < promedios["grande"]

    def generar_reporte(lista):
        total = sum(t["monto"] for t in lista)
        ciudad_top = list(agrupar_por(lista, "ciudad", "monto"))[0][0]
        n_grandes = len([t for t in lista if t["clasificacion"] == "grande"])
        return {"total_ventas": total, "n_validas": len(lista),
                "ciudad_top": ciudad_top, "n_grandes": n_grandes}

    reporte = generar_reporte(te)
    assert reporte["total_ventas"] > 0
    assert reporte["n_validas"] == len(te)
    assert isinstance(reporte["ciudad_top"], str)

    print("OK Soluciones de referencia de practice02 (clase03) validadas sobre el dataset.")

_validar()


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase03", "practice02.ipynb")
build(os.path.abspath(ruta), C)
