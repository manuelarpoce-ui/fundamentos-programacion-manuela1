"""Construye curso/clase02/homework02.ipynb — mini proyecto autocalificable.

Mini proyecto: Simulador de caja registradora.
El estudiante construye, parte por parte, un sistema que calcula el total
de una compra con IVA, descuentos según método de pago y cambio.

Las funciones se usan entre sí, por eso se usa compartir_ns=True.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    {
        "n": 1,
        "titulo": "Calcular subtotal",
        "enunciado": (
            "Implementa `calcular_subtotal(precio_unitario, cantidad)` que devuelva "
            "el producto de precio por cantidad.\n\n"
            "Si `precio_unitario <= 0` o `cantidad <= 0`, devuelve `None`.\n\n"
            "**Ejemplo:** `calcular_subtotal(25000, 4)` → `100000`;\n"
            "`calcular_subtotal(0, 5)` → `None`."
        ),
        "plantilla": "def calcular_subtotal(precio_unitario, cantidad):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def calcular_subtotal(precio_unitario, cantidad):\n"
            "    if precio_unitario <= 0 or cantidad <= 0:\n"
            "        return None\n"
            "    return precio_unitario * cantidad"
        ),
        "visibles": [
            "assert calcular_subtotal(25000, 4) == 100000",
            "assert calcular_subtotal(0, 5) is None",
        ],
        "ocultos": [
            "assert calcular_subtotal(50000, 1) == 50000",
            "assert calcular_subtotal(-100, 3) is None",
            "assert calcular_subtotal(1000, 0) is None",
        ],
    },
    {
        "n": 2,
        "titulo": "Aplicar descuento por método de pago",
        "enunciado": (
            "Implementa `descuento_metodo(subtotal, metodo_pago)` que devuelva el "
            "porcentaje de descuento según el método:\n"
            "- `'efectivo'` → 5% (0.05) de descuento\n"
            "- `'tarjeta'` → 2% (0.02) de descuento\n"
            "- `'transferencia'` → 3% (0.03) de descuento\n"
            "- cualquier otro → 0% de descuento\n\n"
            "La función devuelve el **monto del descuento** (no el porcentaje).\n"
            "Redondea a 2 decimales.\n\n"
            "**Ejemplo:** `descuento_metodo(100000, 'efectivo')` → `5000.0`;\n"
            "`descuento_metodo(80000, 'tarjeta')` → `1600.0`."
        ),
        "plantilla": "def descuento_metodo(subtotal, metodo_pago):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def descuento_metodo(subtotal, metodo_pago):\n"
            "    if metodo_pago == 'efectivo':\n"
            "        pct = 0.05\n"
            "    elif metodo_pago == 'tarjeta':\n"
            "        pct = 0.02\n"
            "    elif metodo_pago == 'transferencia':\n"
            "        pct = 0.03\n"
            "    else:\n"
            "        pct = 0.0\n"
            "    return round(subtotal * pct, 2)"
        ),
        "visibles": [
            "assert descuento_metodo(100000, 'efectivo') == 5000.0",
            "assert descuento_metodo(80000, 'tarjeta') == 1600.0",
        ],
        "ocultos": [
            "assert descuento_metodo(100000, 'transferencia') == 3000.0",
            "assert descuento_metodo(200000, 'criptomoneda') == 0.0",
            "assert descuento_metodo(0, 'efectivo') == 0.0",
        ],
    },
    {
        "n": 3,
        "titulo": "Calcular IVA sobre base gravable",
        "enunciado": (
            "Implementa `calcular_iva_base(base_gravable, tasa_iva=0.19)` que devuelva "
            "el monto del IVA sobre la `base_gravable`.\n"
            "Redondea a 2 decimales.\n\n"
            "Si `base_gravable < 0` o `tasa_iva < 0`, devuelve `None`.\n\n"
            "**Ejemplo:** `calcular_iva_base(95000)` → `18050.0`;\n"
            "`calcular_iva_base(50000, 0.08)` → `4000.0`."
        ),
        "plantilla": "def calcular_iva_base(base_gravable, tasa_iva=0.19):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def calcular_iva_base(base_gravable, tasa_iva=0.19):\n"
            "    if base_gravable < 0 or tasa_iva < 0:\n"
            "        return None\n"
            "    return round(base_gravable * tasa_iva, 2)"
        ),
        "visibles": [
            "assert calcular_iva_base(95000) == 18050.0",
            "assert calcular_iva_base(50000, 0.08) == 4000.0",
        ],
        "ocultos": [
            "assert calcular_iva_base(0) == 0.0",
            "assert calcular_iva_base(-100) is None",
            "assert calcular_iva_base(100000, 0) == 0.0",
        ],
    },
    {
        "n": 4,
        "titulo": "Total de la compra",
        "enunciado": (
            "Implementa `total_compra(precio_unitario, cantidad, metodo_pago, tasa_iva=0.19)` "
            "que devuelva una tupla `(subtotal, descuento, base_gravable, iva, total)` "
            "usando las funciones anteriores:\n\n"
            "1. `subtotal = calcular_subtotal(precio_unitario, cantidad)`\n"
            "2. `descuento = descuento_metodo(subtotal, metodo_pago)`\n"
            "3. `base_gravable = subtotal - descuento`\n"
            "4. `iva = calcular_iva_base(base_gravable, tasa_iva)`\n"
            "5. `total = base_gravable + iva`\n\n"
            "Si `calcular_subtotal` devuelve `None`, toda la tupla es `None`.\n\n"
            "**Ejemplo:** `total_compra(25000, 4, 'efectivo')` →\n"
            "`(100000, 5000.0, 95000.0, 18050.0, 113050.0)`"
        ),
        "plantilla": "def total_compra(precio_unitario, cantidad, metodo_pago, tasa_iva=0.19):\n    # ✏️ TU CÓDIGO AQUÍ (usa calcular_subtotal, descuento_metodo, calcular_iva_base)\n    " + NI,
        "solucion": (
            "def total_compra(precio_unitario, cantidad, metodo_pago, tasa_iva=0.19):\n"
            "    subtotal = calcular_subtotal(precio_unitario, cantidad)\n"
            "    if subtotal is None:\n"
            "        return None\n"
            "    descuento = descuento_metodo(subtotal, metodo_pago)\n"
            "    base_gravable = subtotal - descuento\n"
            "    iva = calcular_iva_base(base_gravable, tasa_iva)\n"
            "    total = base_gravable + iva\n"
            "    return (subtotal, descuento, base_gravable, iva, total)"
        ),
        "visibles": [
            "_r = total_compra(25000, 4, 'efectivo')",
            "assert _r == (100000, 5000.0, 95000.0, 18050.0, 113050.0)",
        ],
        "ocultos": [
            "_r2 = total_compra(50000, 2, 'tarjeta')",
            "assert _r2[0] == 100000",
            "assert _r2[1] == 2000.0",
            "assert _r2[4] == 116620.0",
            "assert total_compra(0, 5, 'efectivo') is None",
        ],
    },
    {
        "n": 5,
        "titulo": "Calcular cambio",
        "enunciado": (
            "Implementa `calcular_cambio(total_a_pagar, monto_pagado)` que devuelva "
            "el **cambio** que se le debe al cliente.\n\n"
            "- Si `monto_pagado >= total_a_pagar`, devuelve `monto_pagado - total_a_pagar` "
            "(redondeado a 2 decimales).\n"
            "- Si `monto_pagado < total_a_pagar`, devuelve `None` "
            "(pago insuficiente).\n\n"
            "**Ejemplos:** `calcular_cambio(113050.0, 150000)` → `36950.0`;\n"
            "`calcular_cambio(113050.0, 100000)` → `None` (no alcanza)."
        ),
        "plantilla": "def calcular_cambio(total_a_pagar, monto_pagado):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def calcular_cambio(total_a_pagar, monto_pagado):\n"
            "    if monto_pagado < total_a_pagar:\n"
            "        return None\n"
            "    return round(monto_pagado - total_a_pagar, 2)"
        ),
        "visibles": [
            "assert calcular_cambio(113050.0, 150000) == 36950.0",
            "assert calcular_cambio(113050.0, 100000) is None",
        ],
        "ocultos": [
            "assert calcular_cambio(50000, 50000) == 0.0",
            "assert calcular_cambio(99999.99, 100000) == 0.01",
        ],
    },
    {
        "n": 6,
        "titulo": "Simulador completo de caja registradora",
        "enunciado": (
            "Implementa `caja_registradora(precio_unitario, cantidad, metodo_pago, monto_pagado)` "
            "que integra todo el flujo y devuelve un **diccionario** con claves:\n"
            "`subtotal`, `descuento`, `base_gravable`, `iva`, `total`, `cambio`.\n\n"
            "Usa `total_compra` y `calcular_cambio`. Si `total_compra` devuelve `None` "
            "o el pago es insuficiente, el campo `cambio` es `None`.\n\n"
            "**Ejemplo:**\n"
            "```\n"
            "caja_registradora(25000, 4, 'efectivo', 150000) ->\n"
            "{\n"
            "  'subtotal': 100000, 'descuento': 5000.0,\n"
            "  'base_gravable': 95000.0, 'iva': 18050.0,\n"
            "  'total': 113050.0, 'cambio': 36950.0\n"
            "}\n"
            "```"
        ),
        "plantilla": (
            "def caja_registradora(precio_unitario, cantidad, metodo_pago, monto_pagado):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    # usa total_compra() y calcular_cambio()\n"
            "    " + NI
        ),
        "solucion": (
            "def caja_registradora(precio_unitario, cantidad, metodo_pago, monto_pagado):\n"
            "    resultado = total_compra(precio_unitario, cantidad, metodo_pago)\n"
            "    if resultado is None:\n"
            "        return {'subtotal': None, 'descuento': None, 'base_gravable': None,\n"
            "                'iva': None, 'total': None, 'cambio': None}\n"
            "    subtotal, descuento, base_gravable, iva, total = resultado\n"
            "    cambio = calcular_cambio(total, monto_pagado)\n"
            "    return {\n"
            "        'subtotal':      subtotal,\n"
            "        'descuento':     descuento,\n"
            "        'base_gravable': base_gravable,\n"
            "        'iva':           iva,\n"
            "        'total':         total,\n"
            "        'cambio':        cambio,\n"
            "    }"
        ),
        "visibles": [
            "_ticket = caja_registradora(25000, 4, 'efectivo', 150000)",
            "assert _ticket['total'] == 113050.0",
            "assert _ticket['cambio'] == 36950.0",
        ],
        "ocultos": [
            "_ticket2 = caja_registradora(50000, 2, 'tarjeta', 110000)",
            "assert _ticket2['subtotal'] == 100000",
            "assert _ticket2['cambio'] is None",   # 110000 < 116620
            "_ticket3 = caja_registradora(0, 2, 'efectivo', 50000)",
            "assert _ticket3['total'] is None",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 2 · Tarea 02 — Mini proyecto: Simulador de caja registradora

### Variables, tipos, operadores y condicionales aplicados a un caso real

En esta tarea construirás **pieza por pieza** un simulador de caja registradora.
El cliente presenta un producto, una cantidad y un método de pago; la caja
calcula el total con descuento e IVA, y devuelve el cambio.

```
  Entrada                      Tu caja registradora              Ticket
precio_unitario ──┐
cantidad        ──┼──▶  subtotal → descuento → IVA → total  ──▶  { desglose
metodo_pago     ──┤                                                  cambio }
monto_pagado    ──┘
```

Cada parte es un subproblema pequeño; la última las integra todas.

**Instrucciones**

1. Implementa cada función reemplazando `raise NotImplementedError`.
2. Resuélvelas **en orden**: las partes 4, 5 y 6 dependen de las anteriores.
3. Ejecuta los tests de cada parte hasta ver ✅.

> 🧠 Traza un ejemplo completo antes de programar cada parte.
""",
    "cierre_md": r"""
---
## ¡Proyecto terminado!

Si todos los tests pasan, construiste un simulador funcional combinando
los conceptos de la Clase 2:

| Parte | Concepto principal |
|---|---|
| 1 Subtotal | multiplicación, validación de entradas |
| 2 Descuento por método | `if/elif/else`, operadores aritméticos |
| 3 IVA | porcentaje, valor por defecto en parámetro |
| 4 Total compra | integración, descomposición en funciones |
| 5 Calcular cambio | comparación, condicional simple |
| 6 Caja registradora | **integración total**, diccionario como resultado |

### Reto opcional (sin calificar)

- Modifica `caja_registradora` para que acepte un parámetro opcional
  `tasa_iva` y lo pase a `total_compra`.
- Añade una condición: si el subtotal supera $500000, aplica además un
  descuento adicional del 3% antes del IVA.
- ¿Cómo mostrarías el ticket en pantalla de forma bonita usando `.format()`?

> 💡 En la Clase 3 añadiremos bucles para que la caja pueda procesar
> múltiples productos en una misma compra.
""",
}

validar(ejercicios, compartir_ns=True)
construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase02", "homework02.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "clase02_homework02_solved.ipynb"),
)
