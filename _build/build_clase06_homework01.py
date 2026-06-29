"""Construye curso/clase06/homework01.ipynb — 8 ejercicios autocalificables de pandas."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    # ---- 1 ---------------------------------------------------------------- #
    {
        "n": 1,
        "titulo": "Porcentaje de participación por ciudad en ventas totales",
        "enunciado": (
            "Implementa `participacion_ciudades(df)` que reciba el DataFrame de\n"
            "transacciones y devuelva un **DataFrame** con columnas:\n"
            "- `'ciudad'`: nombre de la ciudad\n"
            "- `'total'`: suma de montos de esa ciudad\n"
            "- `'pct'`: porcentaje del total global, redondeado a 2 decimales\n\n"
            "Ordenado de mayor a menor `'pct'`.\n\n"
            "**Ejemplo:** si Bogota tiene el 25% de las ventas, `pct` = 25.0"
        ),
        "plantilla": (
            "def participacion_ciudades(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "def participacion_ciudades(df):\n"
            "    res = df.groupby('ciudad')['monto'].sum().reset_index()\n"
            "    res.columns = ['ciudad', 'total']\n"
            "    res['pct'] = (res['total'] / res['total'].sum() * 100).round(2)\n"
            "    return res.sort_values('pct', ascending=False).reset_index(drop=True)"
        ),
        "visibles": [
            "import os, pandas as pd",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = pd.read_csv(ruta)",
            "_res = participacion_ciudades(_df)",
            "assert 'ciudad' in _res.columns",
            "assert 'total' in _res.columns",
            "assert 'pct' in _res.columns",
            "assert len(_res) == 5",
            "assert abs(_res['pct'].sum() - 100.0) < 0.1",
        ],
        "ocultos": [
            "assert _res.iloc[0]['pct'] >= _res.iloc[-1]['pct']",
            "assert (_res['pct'] > 0).all()",
            "assert abs(_res['total'].sum() - _df['monto'].sum()) < 1",
        ],
    },
    # ---- 2 ---------------------------------------------------------------- #
    {
        "n": 2,
        "titulo": "Categoría con mayor variabilidad (desviación estándar) de precios",
        "enunciado": (
            "Implementa `categoria_mas_variable(df)` que devuelva el **nombre**\n"
            "(str) de la categoría con mayor desviación estándar de montos.\n\n"
            "**Ejemplo:** devuelve algo como `'tecnologia'` (el nombre exacto\n"
            "depende del dataset)."
        ),
        "plantilla": (
            "def categoria_mas_variable(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "def categoria_mas_variable(df):\n"
            "    stds = df.groupby('categoria')['monto'].std()\n"
            "    return stds.idxmax()"
        ),
        "visibles": [
            "import os, pandas as pd",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = pd.read_csv(ruta)",
            "_cat = categoria_mas_variable(_df)",
            "assert isinstance(_cat, str)",
            "assert _cat in _df['categoria'].unique()",
        ],
        "ocultos": [
            "# El resultado debe ser la categoría con std máximo",
            "_stds = _df.groupby('categoria')['monto'].std()",
            "assert _cat == _stds.idxmax()",
        ],
    },
    # ---- 3 ---------------------------------------------------------------- #
    {
        "n": 3,
        "titulo": "Función resumen_ciudad(df, ciudad) que devuelva métricas clave",
        "enunciado": (
            "Implementa `resumen_ciudad(df, ciudad)` que devuelva una **Series**\n"
            "con las siguientes métricas para la ciudad indicada:\n"
            "- `'n_transacciones'`: número de transacciones\n"
            "- `'total'`: suma de montos\n"
            "- `'promedio'`: promedio de monto (float)\n"
            "- `'maximo'`: monto máximo\n"
            "- `'minimo'`: monto mínimo\n\n"
            "**Ejemplo:** `resumen_ciudad(df, 'Bogota')['n_transacciones']` → número entero."
        ),
        "plantilla": (
            "def resumen_ciudad(df, ciudad):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "def resumen_ciudad(df, ciudad):\n"
            "    sub = df[df['ciudad'] == ciudad]['monto']\n"
            "    return pd.Series({\n"
            "        'n_transacciones': len(sub),\n"
            "        'total': sub.sum(),\n"
            "        'promedio': sub.mean(),\n"
            "        'maximo': sub.max(),\n"
            "        'minimo': sub.min(),\n"
            "    })"
        ),
        "visibles": [
            "import os, pandas as pd",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = pd.read_csv(ruta)",
            "_s = resumen_ciudad(_df, 'Bogota')",
            "assert hasattr(_s, 'index')  # es una Series",
            "assert 'n_transacciones' in _s.index",
            "assert 'total' in _s.index",
            "assert 'promedio' in _s.index",
        ],
        "ocultos": [
            "assert _s['n_transacciones'] == len(_df[_df['ciudad'] == 'Bogota'])",
            "assert _s['total'] == _df[_df['ciudad'] == 'Bogota']['monto'].sum()",
            "assert _s['minimo'] <= _s['promedio'] <= _s['maximo']",
        ],
    },
    # ---- 4 ---------------------------------------------------------------- #
    {
        "n": 4,
        "titulo": "Detectar y eliminar transacciones duplicadas por id",
        "enunciado": (
            "Implementa `eliminar_duplicados(df)` que devuelva una **copia** del\n"
            "DataFrame sin filas con `id` duplicado. Si hay duplicados, se conserva\n"
            "la **primera** aparición.\n\n"
            "La función debe devolver el DataFrame limpio (sin modificar el original)."
        ),
        "plantilla": (
            "def eliminar_duplicados(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "def eliminar_duplicados(df):\n"
            "    return df.drop_duplicates(subset='id', keep='first').reset_index(drop=True)"
        ),
        "visibles": [
            "import os, pandas as pd",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = pd.read_csv(ruta)",
            "# Crear duplicado artificial",
            "_df_dup = pd.concat([_df, _df.head(3)], ignore_index=True)",
            "_df_limpio = eliminar_duplicados(_df_dup)",
            "assert len(_df_limpio) == len(_df)",
            "assert _df_limpio['id'].nunique() == len(_df_limpio)",
        ],
        "ocultos": [
            "# El original no debe modificarse",
            "assert len(_df_dup) == len(_df) + 3",
            "# Primera aparición conservada",
            "assert list(_df_limpio['id'][:3]) == list(_df['id'][:3])",
        ],
    },
    # ---- 5 ---------------------------------------------------------------- #
    {
        "n": 5,
        "titulo": "Ventas acumuladas (cumsum) ordenadas por fecha",
        "enunciado": (
            "Implementa `ventas_acumuladas(df)` que devuelva una **copia** del\n"
            "DataFrame, ordenada por fecha (ascendente), con una columna adicional\n"
            "`'acumulado'` que contenga la suma acumulada de monto.\n\n"
            "El índice del resultado debe ser 0, 1, 2, ... (reset_index)."
        ),
        "plantilla": (
            "def ventas_acumuladas(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "def ventas_acumuladas(df):\n"
            "    copia = df.sort_values('fecha').reset_index(drop=True).copy()\n"
            "    copia['acumulado'] = copia['monto'].cumsum()\n"
            "    return copia"
        ),
        "visibles": [
            "import os, pandas as pd",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = pd.read_csv(ruta, parse_dates=['fecha'])",
            "_dfac = ventas_acumuladas(_df)",
            "assert 'acumulado' in _dfac.columns",
            "assert len(_dfac) == len(_df)",
            "assert _dfac['acumulado'].iloc[-1] == _df['monto'].sum()",
        ],
        "ocultos": [
            "# Debe estar ordenado por fecha",
            "assert (_dfac['fecha'].diff().dropna() >= pd.Timedelta(0)).all()",
            "# El acumulado es monotónico creciente",
            "assert (_dfac['acumulado'].diff().dropna() >= 0).all()",
        ],
    },
    # ---- 6 ---------------------------------------------------------------- #
    {
        "n": 6,
        "titulo": "Comparar medianas por método de pago con groupby + agg",
        "enunciado": (
            "Implementa `comparar_medianas(df)` que devuelva un **DataFrame** con\n"
            "columnas `'metodo_pago'`, `'mediana'` y `'promedio'` (redondeados a\n"
            "2 decimales), ordenado de mayor a menor `'mediana'`."
        ),
        "plantilla": (
            "def comparar_medianas(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "def comparar_medianas(df):\n"
            "    return (\n"
            "        df.groupby('metodo_pago')['monto']\n"
            "          .agg(\n"
            "              mediana=lambda x: round(x.median(), 2),\n"
            "              promedio=lambda x: round(x.mean(), 2)\n"
            "          )\n"
            "          .reset_index()\n"
            "          .sort_values('mediana', ascending=False)\n"
            "          .reset_index(drop=True)\n"
            "    )"
        ),
        "visibles": [
            "import os, pandas as pd",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = pd.read_csv(ruta)",
            "_res = comparar_medianas(_df)",
            "assert 'metodo_pago' in _res.columns",
            "assert 'mediana' in _res.columns",
            "assert 'promedio' in _res.columns",
            "assert len(_res) == 3",
        ],
        "ocultos": [
            "assert _res.iloc[0]['mediana'] >= _res.iloc[-1]['mediana']",
            "assert (_res['mediana'] > 0).all()",
            "assert (_res['promedio'] > 0).all()",
        ],
    },
    # ---- 7 ---------------------------------------------------------------- #
    {
        "n": 7,
        "titulo": "Filtrar y exportar transacciones atípicas (z-score > 2)",
        "enunciado": (
            "Implementa `exportar_atipicos(df, ruta_salida)` que:\n"
            "1. Calcule el z-score de la columna `monto`:\n"
            "   `z = (monto - monto.mean()) / monto.std()`\n"
            "2. Filtre las filas donde `abs(z) > 2`.\n"
            "3. Exporte esas filas a `ruta_salida` como CSV (sin índice).\n"
            "4. Devuelva el número de filas exportadas.\n\n"
            "**Ejemplo:** devuelve un entero con el número de outliers encontrados."
        ),
        "plantilla": (
            "def exportar_atipicos(df, ruta_salida):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "def exportar_atipicos(df, ruta_salida):\n"
            "    z = (df['monto'] - df['monto'].mean()) / df['monto'].std()\n"
            "    atipicos = df[z.abs() > 2]\n"
            "    atipicos.to_csv(ruta_salida, index=False)\n"
            "    return len(atipicos)"
        ),
        "visibles": [
            "import os, pandas as pd, tempfile",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = pd.read_csv(ruta)",
            "with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as _f:",
            "    _ruta_tmp = _f.name",
            "_n = exportar_atipicos(_df, _ruta_tmp)",
            "assert isinstance(_n, int)",
            "assert _n >= 0",
        ],
        "ocultos": [
            "_df_out = pd.read_csv(_ruta_tmp)",
            "assert len(_df_out) == _n",
            "# Verificar que son realmente atípicos",
            "_z = (_df['monto'] - _df['monto'].mean()) / _df['monto'].std()",
            "_expected = int((_z.abs() > 2).sum())",
            "assert _n == _expected",
            "import os; os.unlink(_ruta_tmp)",
        ],
    },
    # ---- 8 ---------------------------------------------------------------- #
    {
        "n": 8,
        "titulo": "Crear columna 'trimestre' a partir de fecha y agrupar",
        "enunciado": (
            "Implementa `ventas_por_trimestre(df)` que:\n"
            "1. Agregue una columna `'trimestre'` con el trimestre del año (1, 2, 3 o 4),\n"
            "   calculado como `((mes - 1) // 3) + 1` donde `mes = fecha.dt.month`.\n"
            "2. Devuelva un **DataFrame** con columnas `'trimestre'` y `'total'`\n"
            "   (suma de montos por trimestre), ordenado por trimestre.\n\n"
            "**Ejemplo:** `trimestre=1` es enero-marzo, `trimestre=2` es abril-junio, etc."
        ),
        "plantilla": (
            "def ventas_por_trimestre(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "def ventas_por_trimestre(df):\n"
            "    copia = df.copy()\n"
            "    copia['trimestre'] = ((copia['fecha'].dt.month - 1) // 3) + 1\n"
            "    return (\n"
            "        copia.groupby('trimestre')['monto']\n"
            "             .sum()\n"
            "             .reset_index()\n"
            "             .rename(columns={'monto': 'total'})\n"
            "             .sort_values('trimestre')\n"
            "             .reset_index(drop=True)\n"
            "    )"
        ),
        "visibles": [
            "import os, pandas as pd",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = pd.read_csv(ruta, parse_dates=['fecha'])",
            "_res = ventas_por_trimestre(_df)",
            "assert 'trimestre' in _res.columns",
            "assert 'total' in _res.columns",
            "assert len(_res) >= 1",
        ],
        "ocultos": [
            "# Los trimestres deben ser valores válidos (1, 2, 3 o 4)",
            "assert _res['trimestre'].between(1, 4).all()",
            "# El total debe sumar el monto global",
            "assert abs(_res['total'].sum() - _df['monto'].sum()) < 1",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 6 · Tarea 01 — 8 ejercicios autocalificables de pandas

### Series, DataFrames, filtrado, groupby y más

**Instrucciones**

1. Implementa cada función reemplazando `raise NotImplementedError`.
2. **No cambies el nombre ni los parámetros** de las funciones.
3. Ejecuta las celdas de **tests visibles** y **tests adicionales**. Si una función
   está bien, verás ✅; si no, saltará un `AssertionError`.
4. Tu objetivo: que **todas** las celdas de tests pasen sin error.

> 🗂️ Todos los ejercicios usan el dataset `../datasets/transacciones.csv`.
> Cada ejercicio lo carga por su cuenta — no necesitas cargar el dataset antes.

> ⚠️ Recién abierta, esta tarea **no** corre de principio a fin: las celdas de tests
> fallarán hasta que implementes cada función. ¡Eso es lo que vas a arreglar!
""",
    "cierre_md": r"""
---
## Entrega

Cuando **todas** las celdas de tests muestren ✅, has completado la tarea.

Repaso de conceptos ejercitados:

| Ejercicio | Concepto pandas |
|---|---|
| 1 Participación por ciudad | `groupby` + porcentaje |
| 2 Categoría más variable | `groupby` + `std` + `idxmax` |
| 3 Resumen de ciudad | filtrado + `pd.Series` manual |
| 4 Eliminar duplicados | `drop_duplicates` |
| 5 Ventas acumuladas | `sort_values` + `cumsum` |
| 6 Comparar medianas | `groupby` + `agg` con lambda |
| 7 Exportar atípicos | z-score + filtrado + `to_csv` |
| 8 Agrupar por trimestre | `dt.month` + `groupby` |

> 💭 **Reflexión:** el z-score del ejercicio 7 es una técnica estadística simple
> pero poderosa. En machine learning se usa para normalizar features. ¿Puedes
> pensarlo en términos del patrón "acumulador + transformación vectorizada"?
""",
}

validar(ejercicios)
construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase06", "homework01.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "clase06_homework01_solved.ipynb"),
)
