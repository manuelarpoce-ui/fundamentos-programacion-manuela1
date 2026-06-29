"""Construye curso/clase04/homework02.ipynb — mini proyecto autocalificable.

Proyecto: "Motor de búsqueda de inventario"
El estudiante construye, pieza a pieza, un sistema que indexa un catálogo de
productos y permite búsquedas multi-filtro eficientes.

Ejercicios se construyen sobre los anteriores (compartir_ns=True).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

# Catálogo de productos compartido en el enunciado
CATALOGO_STR = (
    "CATALOGO = [\n"
    "    {'id': 'P001', 'nombre': 'laptop',    'categoria': 'tecnologia', 'precio': 2_500_000, 'stock': 15},\n"
    "    {'id': 'P002', 'nombre': 'teclado',   'categoria': 'tecnologia', 'precio':   120_000, 'stock': 45},\n"
    "    {'id': 'P003', 'nombre': 'monitor',   'categoria': 'tecnologia', 'precio':   800_000, 'stock':  8},\n"
    "    {'id': 'P004', 'nombre': 'silla',     'categoria': 'hogar',      'precio':   450_000, 'stock': 20},\n"
    "    {'id': 'P005', 'nombre': 'escritorio','categoria': 'hogar',      'precio':   900_000, 'stock':  5},\n"
    "    {'id': 'P006', 'nombre': 'arroz',     'categoria': 'alimentos',  'precio':     5_000, 'stock': 200},\n"
    "    {'id': 'P007', 'nombre': 'aceite',    'categoria': 'alimentos',  'precio':    18_000, 'stock': 150},\n"
    "    {'id': 'P008', 'nombre': 'mouse',     'categoria': 'tecnologia', 'precio':    80_000, 'stock': 60},\n"
    "    {'id': 'P009', 'nombre': 'lampara',   'categoria': 'hogar',      'precio':    75_000, 'stock': 30},\n"
    "    {'id': 'P010', 'nombre': 'cafe',      'categoria': 'alimentos',  'precio':    25_000, 'stock': 80},\n"
    "]"
)

ejercicios = [
    {
        "n": 1,
        "titulo": "Cargar el catálogo",
        "enunciado": (
            "El catálogo de productos ya está definido en la celda de identificación "
            "como la variable `CATALOGO` (lista de dicts). Implementa `ids_por_categoria(catalogo)` "
            "que devuelva un dict `{categoria: set_de_ids}`.\n\n"
            "**Ejemplo:**\n"
            "```\n"
            "ids_por_categoria(CATALOGO)['tecnologia']\n"
            "# -> {'P001', 'P002', 'P003', 'P008'}\n"
            "```\n\n"
            "Esta es la estructura de **índice por categoría** que permite recuperar "
            "todos los productos de una categoría en O(1)."
        ),
        "plantilla": "def ids_por_categoria(catalogo):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            CATALOGO_STR + "\n\n"
            "def ids_por_categoria(catalogo):\n"
            "    indice = {}\n"
            "    for p in catalogo:\n"
            "        indice.setdefault(p['categoria'], set()).add(p['id'])\n"
            "    return indice"
        ),
        "visibles": [
            "assert ids_por_categoria(CATALOGO)['tecnologia'] == {'P001', 'P002', 'P003', 'P008'}",
            "assert ids_por_categoria(CATALOGO)['hogar'] == {'P004', 'P005', 'P009'}",
        ],
        "ocultos": [
            "assert ids_por_categoria(CATALOGO)['alimentos'] == {'P006', 'P007', 'P010'}",
            "assert set(ids_por_categoria(CATALOGO).keys()) == {'tecnologia', 'hogar', 'alimentos'}",
            "assert ids_por_categoria([]) == {}",
        ],
    },
    {
        "n": 2,
        "titulo": "Índice id → producto",
        "enunciado": (
            "Implementa `indice_por_id(catalogo)` que devuelva un dict `{id: producto}` "
            "donde `producto` es el dict completo del producto.\n\n"
            "Este índice permite recuperar todos los datos de un producto por su id en O(1),\n"
            "en vez de recorrer el catálogo completo cada vez.\n\n"
            "**Ejemplo:**\n"
            "`indice_por_id(CATALOGO)['P003']['nombre']` → `'monitor'`"
        ),
        "plantilla": "def indice_por_id(catalogo):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def indice_por_id(catalogo):\n"
            "    return {p['id']: p for p in catalogo}"
        ),
        "visibles": [
            "assert indice_por_id(CATALOGO)['P003']['nombre'] == 'monitor'",
            "assert indice_por_id(CATALOGO)['P006']['precio'] == 5_000",
        ],
        "ocultos": [
            "assert set(indice_por_id(CATALOGO).keys()) == {p['id'] for p in CATALOGO}",
            "assert indice_por_id(CATALOGO)['P001']['stock'] == 15",
            "assert indice_por_id([]) == {}",
        ],
    },
    {
        "n": 3,
        "titulo": "Buscar por categoría",
        "enunciado": (
            "Implementa `buscar_categoria(catalogo, categoria)` que devuelva una "
            "**lista de dicts** con todos los productos de esa categoría.\n\n"
            "Usa las funciones `ids_por_categoria` e `indice_por_id` que ya implementaste.\n\n"
            "El resultado debe estar **ordenado por precio ascendente**.\n\n"
            "Si la categoría no existe, devuelve lista vacía."
        ),
        "plantilla": (
            "def buscar_categoria(catalogo, categoria):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    # Pista: usa ids_por_categoria e indice_por_id\n"
            "    " + NI
        ),
        "solucion": (
            "def buscar_categoria(catalogo, categoria):\n"
            "    indice_cat = ids_por_categoria(catalogo)\n"
            "    indice_id  = indice_por_id(catalogo)\n"
            "    ids = indice_cat.get(categoria, set())\n"
            "    productos = [indice_id[i] for i in ids]\n"
            "    return sorted(productos, key=lambda p: p['precio'])"
        ),
        "visibles": [
            "_alim = buscar_categoria(CATALOGO, 'alimentos')",
            "assert len(_alim) == 3",
            "assert _alim[0]['nombre'] == 'arroz'",
            "assert _alim[-1]['nombre'] == 'cafe'",
        ],
        "ocultos": [
            "_tec = buscar_categoria(CATALOGO, 'tecnologia')",
            "assert [p['id'] for p in _tec] == ['P008', 'P002', 'P003', 'P001']",
            "assert buscar_categoria(CATALOGO, 'deportes') == []",
        ],
    },
    {
        "n": 4,
        "titulo": "Buscar por rango de precio",
        "enunciado": (
            "Implementa `buscar_rango_precio(catalogo, precio_min, precio_max)` que "
            "devuelva una **lista de dicts** con los productos cuyo precio esté entre "
            "`precio_min` y `precio_max` (inclusive).\n\n"
            "El resultado debe estar ordenado por precio ascendente."
        ),
        "plantilla": "def buscar_rango_precio(catalogo, precio_min, precio_max):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def buscar_rango_precio(catalogo, precio_min, precio_max):\n"
            "    filtrados = [p for p in catalogo\n"
            "                 if precio_min <= p['precio'] <= precio_max]\n"
            "    return sorted(filtrados, key=lambda p: p['precio'])"
        ),
        "visibles": [
            "_rango = buscar_rango_precio(CATALOGO, 50_000, 200_000)",
            "assert len(_rango) == 3",
            "assert _rango[0]['nombre'] == 'lampara'",
        ],
        "ocultos": [
            "assert buscar_rango_precio(CATALOGO, 0, 1_000) == []",
            "_exacto = buscar_rango_precio(CATALOGO, 120_000, 120_000)",
            "assert len(_exacto) == 1 and _exacto[0]['id'] == 'P002'",
            "assert len(buscar_rango_precio(CATALOGO, 0, 9_999_999)) == len(CATALOGO)",
        ],
    },
    {
        "n": 5,
        "titulo": "Búsqueda multi-filtro",
        "enunciado": (
            "Implementa `buscar(catalogo, categoria=None, precio_min=None, precio_max=None, "
            "en_stock=False)` que aplique **todos** los filtros que no sean `None`:\n\n"
            "- `categoria`: si se especifica, solo productos de esa categoría.\n"
            "- `precio_min`: si se especifica, precio >= precio_min.\n"
            "- `precio_max`: si se especifica, precio <= precio_max.\n"
            "- `en_stock=True`: solo productos con stock > 0.\n\n"
            "Devuelve lista de dicts ordenada por precio ascendente.\n\n"
            "Usa las funciones anteriores como bloques de construcción o filtra directamente."
        ),
        "plantilla": (
            "def buscar(catalogo, categoria=None, precio_min=None, precio_max=None, en_stock=False):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    " + NI
        ),
        "solucion": (
            "def buscar(catalogo, categoria=None, precio_min=None, precio_max=None, en_stock=False):\n"
            "    resultado = list(catalogo)\n"
            "    if categoria is not None:\n"
            "        resultado = [p for p in resultado if p['categoria'] == categoria]\n"
            "    if precio_min is not None:\n"
            "        resultado = [p for p in resultado if p['precio'] >= precio_min]\n"
            "    if precio_max is not None:\n"
            "        resultado = [p for p in resultado if p['precio'] <= precio_max]\n"
            "    if en_stock:\n"
            "        resultado = [p for p in resultado if p['stock'] > 0]\n"
            "    return sorted(resultado, key=lambda p: p['precio'])"
        ),
        "visibles": [
            "_r1 = buscar(CATALOGO, categoria='hogar')",
            "assert len(_r1) == 3",
            "_r2 = buscar(CATALOGO, precio_min=100_000, precio_max=500_000)",
            "assert all(100_000 <= p['precio'] <= 500_000 for p in _r2)",
        ],
        "ocultos": [
            "_r3 = buscar(CATALOGO, categoria='tecnologia', precio_max=200_000)",
            "assert set(p['id'] for p in _r3) == {'P002', 'P008'}",
            "_r4 = buscar(CATALOGO, en_stock=True)",
            "assert all(p['stock'] > 0 for p in _r4)",
            "assert buscar(CATALOGO, categoria='deportes') == []",
        ],
    },
    {
        "n": 6,
        "titulo": "Resumen del catálogo",
        "enunciado": (
            "Implementa `resumen_catalogo(catalogo)` que devuelva un dict con el\n"
            "resumen estadístico del catálogo, **reutilizando las funciones anteriores**:\n\n"
            "```python\n"
            "{\n"
            "  'total_productos': int,\n"
            "  'categorias': set,                # conjunto de categorías únicas\n"
            "  'precio_min': int,                # precio del producto más barato\n"
            "  'precio_max': int,                # precio del producto más caro\n"
            "  'producto_mas_barato': str,       # nombre del producto de menor precio\n"
            "  'productos_en_stock': int,        # cantidad con stock > 0\n"
            "}\n"
            "```\n\n"
            "Si el catálogo está vacío, devuelve el dict con 0, set vacío, None donde corresponda."
        ),
        "plantilla": "def resumen_catalogo(catalogo):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def resumen_catalogo(catalogo):\n"
            "    if not catalogo:\n"
            "        return {\n"
            "            'total_productos': 0,\n"
            "            'categorias': set(),\n"
            "            'precio_min': None,\n"
            "            'precio_max': None,\n"
            "            'producto_mas_barato': None,\n"
            "            'productos_en_stock': 0,\n"
            "        }\n"
            "    precios = [p['precio'] for p in catalogo]\n"
            "    pmin = min(precios)\n"
            "    pmax = max(precios)\n"
            "    mas_barato = next(p['nombre'] for p in catalogo if p['precio'] == pmin)\n"
            "    return {\n"
            "        'total_productos': len(catalogo),\n"
            "        'categorias': {p['categoria'] for p in catalogo},\n"
            "        'precio_min': pmin,\n"
            "        'precio_max': pmax,\n"
            "        'producto_mas_barato': mas_barato,\n"
            "        'productos_en_stock': sum(1 for p in catalogo if p['stock'] > 0),\n"
            "    }"
        ),
        "visibles": [
            "_res = resumen_catalogo(CATALOGO)",
            "assert _res['total_productos'] == 10",
            "assert _res['categorias'] == {'tecnologia', 'hogar', 'alimentos'}",
            "assert _res['producto_mas_barato'] == 'arroz'",
        ],
        "ocultos": [
            "assert _res['precio_min'] == 5_000",
            "assert _res['precio_max'] == 2_500_000",
            "assert _res['productos_en_stock'] == 10",
            "_res_vacio = resumen_catalogo([])",
            "assert _res_vacio['total_productos'] == 0",
            "assert _res_vacio['categorias'] == set()",
        ],
    },
]

meta = {
    "intro_md": (
        "# Clase 4 · Tarea 02 — Mini proyecto: motor de búsqueda de inventario\n\n"
        "### Estructuras de datos aplicadas\n\n"
        "En esta tarea construirás, **pieza a pieza**, un motor de búsqueda simple\n"
        "para el inventario de una tienda. El motor indexa el catálogo y permite\n"
        "búsquedas por categoría, rango de precio y disponibilidad de stock.\n\n"
        "```\n"
        "  CATALOGO              tu motor                   resultados\n"
        " [lista de dicts]  -->  indexar + buscar  -->  [productos filtrados]\n"
        "```\n\n"
        "**Instrucciones**\n\n"
        "1. Implementa cada función reemplazando `raise NotImplementedError`.\n"
        "2. **No cambies nombres ni parámetros**: las funciones se llaman entre sí.\n"
        "3. Resuélvelas **en orden**: las partes 3-6 usan las anteriores.\n"
        "4. Ejecuta los tests de cada parte hasta ver ✅.\n\n"
        "> 🧠 Antes de programar, decide qué estructura de datos usará cada función.\n\n"
        + CATALOGO_STR
    ),
    "cierre_md": r"""
---
## ¡Proyecto terminado!

Si todos los tests pasan, construiste un motor de búsqueda funcional usando
las estructuras de datos de la clase:

| Parte | Estructura clave | Patrón |
|---|---|---|
| 1 Índice por categoría | `dict` de `sets` | agrupar por clave |
| 2 Índice por id | `dict` | comprensión `{k: v for ...}` |
| 3 Buscar categoría | `set` + `dict` | consulta sobre índice |
| 4 Buscar por precio | `list` + comprensión | filtro con condición |
| 5 Búsqueda multi-filtro | composición de filtros | encadenamiento |
| 6 Resumen | `set`, `list`, `dict` | **integración** |

### Reto opcional (sin calificar)
- Añade un índice de búsqueda por **rango de precio** preconstruido para que
  `buscar_rango_precio` no recorra todo el catálogo. ¿Qué estructura usarías?
- Extiende `buscar` para que acepte un parámetro `orden` (`"precio"`, `"nombre"`,
  `"stock"`) y ordene por ese campo.
- ¿Cómo cambiaría el código si el catálogo tuviera 1 millón de productos?
  ¿Qué índice pre-construirías? ¿Qué operación sería el cuello de botella?

> 💡 Los motores de búsqueda reales (Elasticsearch, Solr) construyen exactamente
> estos índices invertidos, pero sobre texto y con algoritmos de ranking.
> Hoy entiendes el principio fundamental detrás de ellos.
""",
}

validar(ejercicios, compartir_ns=True)
construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase04", "homework02.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "clase04_homework02_solved.ipynb"),
)
