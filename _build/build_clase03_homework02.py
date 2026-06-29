"""Construye curso/clase03/homework02.ipynb — mini proyecto autocalificable.

Mini proyecto: procesador de pedidos — dada una lista de productos con precio y
cantidad, aplica descuentos por volumen, calcula subtotales con map/lambda,
filtra pedidos nulos e imprime la factura.

Los ejercicios se apoyan entre sí (compartir_ns=True).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    # ------------------------------------------------------------------ #
    # Parte 1: parsear la lista de pedidos
    # ------------------------------------------------------------------ #
    {
        "n": 1,
        "titulo": "Parsear la lista de pedidos",
        "enunciado": (
            "Los pedidos llegan como una lista de cadenas con el formato "
            "`\"producto:precio_unitario:cantidad\"`. Por ejemplo:\n"
            "`[\"laptop:2500000:2\", \"mouse:45000:5\", \"cargador:80000:0\"]`\n\n"
            "Implementa `parsear_pedidos(raw)` que devuelva una **lista de "
            "diccionarios** con claves `producto` (str), `precio` (int) y "
            "`cantidad` (int).\n\n"
            "**Ejemplo:**\n"
            "`parsear_pedidos([\"laptop:2500000:2\"])` → "
            "`[{'producto': 'laptop', 'precio': 2500000, 'cantidad': 2}]`"
        ),
        "plantilla": "def parsear_pedidos(raw):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def parsear_pedidos(raw):\n"
            "    resultado = []\n"
            "    for linea in raw:\n"
            "        partes = linea.split(':')\n"
            "        resultado.append({\n"
            "            'producto': partes[0],\n"
            "            'precio':   int(partes[1]),\n"
            "            'cantidad': int(partes[2]),\n"
            "        })\n"
            "    return resultado"
        ),
        "visibles": [
            "_p = parsear_pedidos(['laptop:2500000:2'])",
            "assert _p == [{'producto': 'laptop', 'precio': 2500000, 'cantidad': 2}]",
        ],
        "ocultos": [
            "_p2 = parsear_pedidos(['mouse:45000:5', 'cargador:80000:0'])",
            "assert _p2[0]['producto'] == 'mouse'",
            "assert _p2[1]['cantidad'] == 0",
            "assert parsear_pedidos([]) == []",
        ],
    },
    # ------------------------------------------------------------------ #
    # Parte 2: filtrar pedidos nulos
    # ------------------------------------------------------------------ #
    {
        "n": 2,
        "titulo": "Filtrar pedidos nulos",
        "enunciado": (
            "Un pedido 'nulo' es aquel con `cantidad == 0`. Implementa "
            "`filtrar_nulos(pedidos)` que devuelva una **nueva lista** sin "
            "los pedidos nulos, usando `filter` y `lambda`.\n\n"
            "**Ejemplo:** dado `[{'producto': 'a', 'precio': 100, 'cantidad': 2}, "
            "{'producto': 'b', 'precio': 50, 'cantidad': 0}]`, devuelve solo el "
            "primer elemento."
        ),
        "plantilla": "def filtrar_nulos(pedidos):\n    # ✏️ TU CÓDIGO AQUÍ (usa filter + lambda)\n    " + NI,
        "solucion": (
            "def filtrar_nulos(pedidos):\n"
            "    return list(filter(lambda p: p['cantidad'] > 0, pedidos))"
        ),
        "visibles": [
            "_raw = ['laptop:2500000:2', 'mouse:45000:5', 'cargador:80000:0']",
            "_pedidos = parsear_pedidos(_raw)",
            "_activos = filtrar_nulos(_pedidos)",
            "assert len(_activos) == 2",
            "assert all(p['cantidad'] > 0 for p in _activos)",
        ],
        "ocultos": [
            "assert filtrar_nulos([]) == []",
            "_todos_nulos = [{'producto': 'x', 'precio': 10, 'cantidad': 0}]",
            "assert filtrar_nulos(_todos_nulos) == []",
        ],
    },
    # ------------------------------------------------------------------ #
    # Parte 3: aplicar descuento por volumen
    # ------------------------------------------------------------------ #
    {
        "n": 3,
        "titulo": "Aplicar descuento por volumen",
        "enunciado": (
            "Los descuentos por volumen se aplican sobre el **precio unitario**:\n"
            "- cantidad >= 10 → 15% de descuento\n"
            "- cantidad >= 5  → 10% de descuento\n"
            "- cantidad < 5   → sin descuento\n\n"
            "Implementa `aplicar_descuento_volumen(pedido)` que reciba un "
            "**diccionario de pedido** y devuelva un **nuevo diccionario** con "
            "los mismos campos más `'precio_con_descuento'` (int) y "
            "`'descuento_pct'` (float, ej: 0.10).\n\n"
            "**Ejemplo:** `{'producto': 'mouse', 'precio': 45000, 'cantidad': 5}` → "
            "añade `precio_con_descuento: 40500, descuento_pct: 0.10`."
        ),
        "plantilla": "def aplicar_descuento_volumen(pedido):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def aplicar_descuento_volumen(pedido):\n"
            "    cantidad = pedido['cantidad']\n"
            "    if cantidad >= 10:\n"
            "        tasa = 0.15\n"
            "    elif cantidad >= 5:\n"
            "        tasa = 0.10\n"
            "    else:\n"
            "        tasa = 0.0\n"
            "    precio_desc = int(pedido['precio'] * (1 - tasa))\n"
            "    return {**pedido, 'precio_con_descuento': precio_desc, 'descuento_pct': tasa}"
        ),
        "visibles": [
            "_m = aplicar_descuento_volumen({'producto': 'mouse', 'precio': 45000, 'cantidad': 5})",
            "assert _m['precio_con_descuento'] == 40500",
            "assert _m['descuento_pct'] == 0.10",
        ],
        "ocultos": [
            "_l = aplicar_descuento_volumen({'producto': 'laptop', 'precio': 2500000, 'cantidad': 10})",
            "assert _l['precio_con_descuento'] == 2125000",
            "assert _l['descuento_pct'] == 0.15",
            "_c = aplicar_descuento_volumen({'producto': 'cable', 'precio': 20000, 'cantidad': 2})",
            "assert _c['descuento_pct'] == 0.0",
            "assert _c['precio_con_descuento'] == 20000",
        ],
    },
    # ------------------------------------------------------------------ #
    # Parte 4: calcular subtotales con map + lambda
    # ------------------------------------------------------------------ #
    {
        "n": 4,
        "titulo": "Calcular subtotales con map y lambda",
        "enunciado": (
            "Implementa `calcular_subtotales(pedidos_con_descuento)` que reciba "
            "la lista de pedidos ya enriquecidos (con `precio_con_descuento`) y "
            "devuelva una **nueva lista** con un campo adicional `'subtotal'` = "
            "`precio_con_descuento * cantidad`.\n\n"
            "Usa `map` y `lambda`.\n\n"
            "**Ejemplo:** `{'precio_con_descuento': 40500, 'cantidad': 5}` → "
            "añade `subtotal: 202500`."
        ),
        "plantilla": "def calcular_subtotales(pedidos_con_descuento):\n    # ✏️ TU CÓDIGO AQUÍ (usa map + lambda)\n    " + NI,
        "solucion": (
            "def calcular_subtotales(pedidos_con_descuento):\n"
            "    return list(map(\n"
            "        lambda p: {**p, 'subtotal': p['precio_con_descuento'] * p['cantidad']},\n"
            "        pedidos_con_descuento\n"
            "    ))"
        ),
        "visibles": [
            "_pd = [{'producto': 'mouse', 'precio': 45000, 'cantidad': 5, 'precio_con_descuento': 40500, 'descuento_pct': 0.10}]",
            "_st = calcular_subtotales(_pd)",
            "assert _st[0]['subtotal'] == 202500",
        ],
        "ocultos": [
            "_pd2 = [{'producto': 'a', 'precio': 100, 'cantidad': 3, 'precio_con_descuento': 100, 'descuento_pct': 0.0}]",
            "assert calcular_subtotales(_pd2)[0]['subtotal'] == 300",
            "assert calcular_subtotales([])==[]",
        ],
    },
    # ------------------------------------------------------------------ #
    # Parte 5: generar la factura
    # ------------------------------------------------------------------ #
    {
        "n": 5,
        "titulo": "Generar resumen de factura",
        "enunciado": (
            "Implementa `resumen_factura(pedidos_finales)` que reciba la lista "
            "de pedidos con todos los campos calculados y devuelva un diccionario:\n"
            "- `'lineas'`: número de líneas de pedido\n"
            "- `'subtotal_neto'`: suma de todos los subtotales\n"
            "- `'iva'`: int, 19% del subtotal_neto\n"
            "- `'total'`: int, subtotal_neto + iva\n"
            "- `'ahorro_total'`: suma de lo que se ahorra en cada línea "
            "= `(precio_original - precio_con_descuento) * cantidad`\n\n"
            "**Usa funciones anteriores** `parsear_pedidos`, `filtrar_nulos`, "
            "`aplicar_descuento_volumen` y `calcular_subtotales` en el pipeline.\n\n"
            "No necesitas llamarlas aquí; solo usas la lista ya procesada."
        ),
        "plantilla": "def resumen_factura(pedidos_finales):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def resumen_factura(pedidos_finales):\n"
            "    subtotal_neto = sum(p['subtotal'] for p in pedidos_finales)\n"
            "    iva = int(subtotal_neto * 0.19)\n"
            "    ahorro = sum(\n"
            "        (p['precio'] - p['precio_con_descuento']) * p['cantidad']\n"
            "        for p in pedidos_finales\n"
            "    )\n"
            "    return {\n"
            "        'lineas':        len(pedidos_finales),\n"
            "        'subtotal_neto': subtotal_neto,\n"
            "        'iva':           iva,\n"
            "        'total':         subtotal_neto + iva,\n"
            "        'ahorro_total':  ahorro,\n"
            "    }"
        ),
        "visibles": [
            "_raw = ['laptop:2500000:2', 'mouse:45000:5', 'cargador:80000:0', 'teclado:120000:10']",
            "_pedidos = parsear_pedidos(_raw)",
            "_activos = filtrar_nulos(_pedidos)",
            "_desc = list(map(aplicar_descuento_volumen, _activos))",
            "_finales = calcular_subtotales(_desc)",
            "_fac = resumen_factura(_finales)",
            "assert _fac['lineas'] == 3",
            "assert _fac['total'] == _fac['subtotal_neto'] + _fac['iva']",
        ],
        "ocultos": [
            "assert _fac['ahorro_total'] >= 0",
            "assert _fac['subtotal_neto'] > 0",
            "_fac2 = resumen_factura([])",
            "assert _fac2['lineas'] == 0",
            "assert _fac2['total'] == 0",
        ],
    },
    # ------------------------------------------------------------------ #
    # Parte 6: imprimir la factura
    # ------------------------------------------------------------------ #
    {
        "n": 6,
        "titulo": "Imprimir factura formateada (pipeline completo)",
        "enunciado": (
            "Implementa `imprimir_factura(raw)` que reciba la lista de cadenas "
            "crudas (como en la Parte 1) y:\n"
            "1. Llame a `parsear_pedidos` → `filtrar_nulos` → `map(aplicar_descuento_volumen)` "
            "→ `calcular_subtotales` → `resumen_factura`.\n"
            "2. Imprima cada línea de pedido con formato:\n"
            "   `[producto] x[cantidad] @ $[precio_desc] = $[subtotal]  (descuento X%)`\n"
            "3. Imprima el resumen al final:\n"
            "   `Subtotal: $... | IVA: $... | TOTAL: $... | Ahorro: $...`\n"
            "4. Devuelva el diccionario de `resumen_factura` (para los tests).\n\n"
            "Esta función integra **todas** las piezas anteriores."
        ),
        "plantilla": "def imprimir_factura(raw):\n    # ✏️ TU CÓDIGO AQUÍ (integra todo el pipeline)\n    " + NI,
        "solucion": (
            "def imprimir_factura(raw):\n"
            "    pedidos  = parsear_pedidos(raw)\n"
            "    activos  = filtrar_nulos(pedidos)\n"
            "    desc     = list(map(aplicar_descuento_volumen, activos))\n"
            "    finales  = calcular_subtotales(desc)\n"
            "    resumen  = resumen_factura(finales)\n"
            "    print('=' * 60)\n"
            "    print('FACTURA')\n"
            "    print('=' * 60)\n"
            "    for p in finales:\n"
            "        pct = int(p['descuento_pct'] * 100)\n"
            "        linea = (p['producto'].ljust(12) +\n"
            "                 ' x' + str(p['cantidad']) +\n"
            "                 ' @ $' + '{:,}'.format(p['precio_con_descuento']) +\n"
            "                 ' = $' + '{:,}'.format(p['subtotal']))\n"
            "        if pct > 0:\n"
            "            linea += '  (descuento ' + str(pct) + '%)'\n"
            "        print(linea)\n"
            "    print('-' * 60)\n"
            "    print('Subtotal: $' + '{:,}'.format(resumen['subtotal_neto']) +\n"
            "          ' | IVA: $' + '{:,}'.format(resumen['iva']) +\n"
            "          ' | TOTAL: $' + '{:,}'.format(resumen['total']) +\n"
            "          ' | Ahorro: $' + '{:,}'.format(resumen['ahorro_total']))\n"
            "    return resumen"
        ),
        "visibles": [
            "_raw = ['laptop:2500000:2', 'mouse:45000:5', 'cargador:80000:0', 'teclado:120000:10']",
            "_resultado = imprimir_factura(_raw)",
            "assert _resultado['lineas'] == 3",
            "assert _resultado['total'] > 0",
        ],
        "ocultos": [
            "assert _resultado['iva'] == int(_resultado['subtotal_neto'] * 0.19)",
            "assert _resultado['ahorro_total'] >= 0",
            "_r2 = imprimir_factura(['item:100:0'])",
            "assert _r2['lineas'] == 0",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 3 · Tarea 02 — Mini proyecto: procesador de pedidos

### Ciclos, funciones y lambdas integradas

En esta tarea construirás **pieza por pieza** un procesador de pedidos
que toma una lista de cadenas crudas y produce una factura formateada.

```
  raw = ["laptop:2500000:2", "mouse:45000:5", "cargador:80000:0"]
    │
    │ parsear_pedidos
    ▼
  [{"producto": "laptop", "precio": 2500000, "cantidad": 2}, ...]
    │
    │ filtrar_nulos
    ▼
  [pedidos con cantidad > 0]
    │
    │ map(aplicar_descuento_volumen)
    ▼
  [pedidos + precio_con_descuento + descuento_pct]
    │
    │ calcular_subtotales
    ▼
  [pedidos + subtotal]
    │
    │ resumen_factura
    ▼
  {lineas, subtotal_neto, iva, total, ahorro_total}
    │
    │ imprimir_factura (todo el pipeline)
    ▼
  FACTURA impresa en pantalla
```

**Instrucciones**

1. Implementa cada función en orden (cada parte usa las anteriores).
2. **No cambies los nombres** de las funciones ni de los campos de los dicts.
3. Ejecuta los tests de cada parte hasta ver ✅.
4. La Parte 6 integra todo: pasa si y solo si las partes 1-5 son correctas.

> 🧠 Antes de programar cada función, lee su enunciado con atención al
> contrato: qué recibe, qué devuelve, qué campos añade.
""",
    "cierre_md": r"""
---
## ¡Proyecto terminado!

Si todos los tests pasan, construiste un procesador de pedidos funcional
que integra todos los conceptos de la clase:

| Parte | Concepto principal |
|---|---|
| 1 Parsear | bucle + split + conversión de tipos |
| 2 Filtrar nulos | `filter` + `lambda` |
| 3 Descuento por volumen | función con lógica de tramos + `{**dict}` |
| 4 Subtotales | `map` + `lambda` |
| 5 Resumen | `sum()` con comprehension, acumuladores |
| 6 Imprimir factura | **integración completa del pipeline** |

### Reto opcional (sin calificar)

- Añade soporte para `categoria` en cada pedido y calcula el total por
  categoría usando `agrupar_por` de la Práctica 02.
- Modifica `imprimir_factura` para que ordene las líneas por subtotal
  descendente antes de imprimir.
- ¿Qué pasaría si el precio unitario fuera 0? Añade validación.

> 💡 En la Clase 6, con pandas, este pipeline completo cabrá en menos de
> 10 líneas. Pero ahora entiendes cada transformación que pandas hace por
> dentro — y eso te convierte en un usuario que también puede depurar.
""",
}

validar(ejercicios, compartir_ns=True)
construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase03", "homework02.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "clase03_homework02_solved.ipynb"),
)
