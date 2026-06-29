"""Construye curso/clase07/homework01.ipynb — 8 ejercicios autocalificables de EDA."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    {
        "n": 1,
        "titulo": "perfil_columna(serie)",
        "enunciado": (
            "Implementa `perfil_columna(serie)` que reciba una `pd.Series` numérica "
            "y devuelva un **diccionario** con las siguientes claves:\n\n"
            "- `media`: promedio\n"
            "- `mediana`: valor central\n"
            "- `std`: desviación estándar\n"
            "- `nulos`: cantidad de valores nulos\n"
            "- `minimo`: valor mínimo\n"
            "- `maximo`: valor máximo\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "import numpy as np, pandas as pd\n"
            "s = pd.Series([1.0, 2.0, np.nan, 4.0])\n"
            "r = perfil_columna(s)\n"
            "# r['nulos'] == 1, r['media'] == 7/3, r['minimo'] == 1.0\n"
            "```"
        ),
        "plantilla": (
            "import numpy as np\nimport pandas as pd\n\n"
            "def perfil_columna(serie):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import numpy as np\nimport pandas as pd\n\n"
            "def perfil_columna(serie):\n"
            "    return {\n"
            "        'media':   serie.mean(),\n"
            "        'mediana': serie.median(),\n"
            "        'std':     serie.std(),\n"
            "        'nulos':   int(serie.isnull().sum()),\n"
            "        'minimo':  serie.min(),\n"
            "        'maximo':  serie.max(),\n"
            "    }"
        ),
        "visibles": [
            "import numpy as np, pandas as pd",
            "_s = pd.Series([1.0, 2.0, np.nan, 4.0])",
            "_r = perfil_columna(_s)",
            "assert _r['nulos'] == 1",
            "assert abs(_r['minimo'] - 1.0) < 1e-9",
            "assert abs(_r['maximo'] - 4.0) < 1e-9",
        ],
        "ocultos": [
            "_s2 = pd.Series([10.0, 20.0, 30.0])",
            "_r2 = perfil_columna(_s2)",
            "assert abs(_r2['media'] - 20.0) < 1e-9",
            "assert abs(_r2['mediana'] - 20.0) < 1e-9",
            "assert _r2['nulos'] == 0",
            "_s3 = pd.Series([5.0])",
            "_r3 = perfil_columna(_s3)",
            "assert _r3['minimo'] == _r3['maximo'] == 5.0",
        ],
    },
    {
        "n": 2,
        "titulo": "columnas_con_muchos_nulos(df, umbral_pct)",
        "enunciado": (
            "Implementa `columnas_con_muchos_nulos(df, umbral_pct=20)` que devuelva "
            "una **lista** con los nombres de las columnas cuyo porcentaje de nulos "
            "supera el `umbral_pct`.\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "import numpy as np, pandas as pd\n"
            "df = pd.DataFrame({\n"
            "    'a': [1.0, np.nan, np.nan],   # 66.7% nulos\n"
            "    'b': [1.0, 2.0, np.nan],       # 33.3% nulos\n"
            "    'c': [1.0, 2.0, 3.0],           # 0% nulos\n"
            "})\n"
            "columnas_con_muchos_nulos(df, 20)  # ['a', 'b']\n"
            "```"
        ),
        "plantilla": (
            "import numpy as np\nimport pandas as pd\n\n"
            "def columnas_con_muchos_nulos(df, umbral_pct=20):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import numpy as np\nimport pandas as pd\n\n"
            "def columnas_con_muchos_nulos(df, umbral_pct=20):\n"
            "    pct = df.isnull().mean() * 100\n"
            "    return pct[pct > umbral_pct].index.tolist()"
        ),
        "visibles": [
            "import numpy as np, pandas as pd",
            "_df = pd.DataFrame({'a': [1.0, np.nan, np.nan], 'b': [1.0, 2.0, np.nan], 'c': [1.0, 2.0, 3.0]})",
            "_r = columnas_con_muchos_nulos(_df, 20)",
            "assert set(_r) == {'a', 'b'}",
            "assert 'c' not in _r",
        ],
        "ocultos": [
            "_df2 = pd.DataFrame({'x': [1.0, 2.0, 3.0], 'y': [1.0, 2.0, 3.0]})",
            "assert columnas_con_muchos_nulos(_df2) == []",
            "_df3 = pd.DataFrame({'z': [np.nan, np.nan, np.nan, np.nan, 1.0]})",
            "assert 'z' in columnas_con_muchos_nulos(_df3, 50)",
        ],
    },
    {
        "n": 3,
        "titulo": "outliers_iqr(serie)",
        "enunciado": (
            "Implementa `outliers_iqr(serie)` que devuelva una `pd.Series` con los "
            "**valores atípicos** de `serie` según el método IQR de Tukey:\n\n"
            "```\n"
            "límite inferior = Q1 - 1.5 * IQR\n"
            "límite superior = Q3 + 1.5 * IQR\n"
            "```\n\n"
            "Devuelve los valores que caen **fuera** de esos límites "
            "(puede ser una Series vacía si no hay outliers).\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "s = pd.Series([10, 11, 12, 10, 11, 500])\n"
            "outliers_iqr(s)  # Series con solo el 500\n"
            "```"
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def outliers_iqr(serie):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\n\n"
            "def outliers_iqr(serie):\n"
            "    q1 = serie.quantile(0.25)\n"
            "    q3 = serie.quantile(0.75)\n"
            "    iqr = q3 - q1\n"
            "    lim_inf = q1 - 1.5 * iqr\n"
            "    lim_sup = q3 + 1.5 * iqr\n"
            "    return serie[(serie < lim_inf) | (serie > lim_sup)]"
        ),
        "visibles": [
            "import pandas as pd",
            "_s = pd.Series([10, 11, 12, 10, 11, 500])",
            "_r = outliers_iqr(_s)",
            "assert isinstance(_r, pd.Series)",
            "assert 500 in _r.values",
            "assert len(_r) == 1",
        ],
        "ocultos": [
            "_s2 = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])",
            "assert len(outliers_iqr(_s2)) == 0",
            "_s3 = pd.Series([-1000.0, 10.0, 11.0, 12.0, 10.0])",
            "assert -1000.0 in outliers_iqr(_s3).values",
        ],
    },
    {
        "n": 4,
        "titulo": "normalizar_todas_numericas(df)",
        "enunciado": (
            "Implementa `normalizar_todas_numericas(df)` que devuelva un **nuevo "
            "DataFrame** donde **todas las columnas numéricas** han sido normalizadas "
            "a `[0, 1]` usando min-max. Las columnas no numéricas permanecen sin cambios.\n\n"
            "Si una columna numérica tiene todos los valores iguales (max == min), "
            "rellenala con `0.0`.\n\n"
            "**No modifiques el DataFrame original.**"
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def normalizar_todas_numericas(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\n\n"
            "def normalizar_todas_numericas(df):\n"
            "    df_out = df.copy()\n"
            "    for col in df_out.select_dtypes(include='number').columns:\n"
            "        mn, mx = df_out[col].min(), df_out[col].max()\n"
            "        if mx != mn:\n"
            "            df_out[col] = (df_out[col] - mn) / (mx - mn)\n"
            "        else:\n"
            "            df_out[col] = 0.0\n"
            "    return df_out"
        ),
        "visibles": [
            "import pandas as pd",
            "_df = pd.DataFrame({'ciudad': ['Bogota','Cali'], 'monto': [100.0, 200.0]})",
            "_r = normalizar_todas_numericas(_df)",
            "assert abs(_r['monto'].min() - 0.0) < 1e-9",
            "assert abs(_r['monto'].max() - 1.0) < 1e-9",
            "assert list(_r['ciudad']) == ['Bogota', 'Cali']",
        ],
        "ocultos": [
            "_df2 = pd.DataFrame({'a': [5.0, 5.0, 5.0]})",
            "_r2 = normalizar_todas_numericas(_df2)",
            "assert (_r2['a'] == 0.0).all()",
            "_df3 = pd.DataFrame({'x': [0.0, 50.0, 100.0], 'y': [1.0, 1.0, 1.0]})",
            "_r3 = normalizar_todas_numericas(_df3)",
            "assert abs(_r3['x'].iloc[1] - 0.5) < 1e-9",
        ],
    },
    {
        "n": 5,
        "titulo": "correlacion_pearson_manual(x, y)",
        "enunciado": (
            "Implementa `correlacion_pearson_manual(x, y)` que calcule la correlación "
            "de Pearson entre dos `pd.Series` **sin usar** `.corr()` ni `np.corrcoef()`.\n\n"
            "Fórmula:\n"
            "```\n"
            "       Σ((xi - x̄)(yi - ȳ))\n"
            "r = ──────────────────────────────────\n"
            "    sqrt(Σ(xi-x̄)²) * sqrt(Σ(yi-ȳ)²)\n"
            "```\n\n"
            "Devuelve un `float` redondeado a 6 decimales. Si el denominador es 0, devuelve `0.0`."
        ),
        "plantilla": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def correlacion_pearson_manual(x, y):\n"
            "    # ✏️ TU CÓDIGO AQUÍ (sin usar .corr() ni np.corrcoef)\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def correlacion_pearson_manual(x, y):\n"
            "    xc = x - x.mean()\n"
            "    yc = y - y.mean()\n"
            "    numerador = (xc * yc).sum()\n"
            "    denominador = ((xc ** 2).sum() ** 0.5) * ((yc ** 2).sum() ** 0.5)\n"
            "    if denominador == 0:\n"
            "        return 0.0\n"
            "    return round(float(numerador / denominador), 6)"
        ),
        "visibles": [
            "import pandas as pd",
            "_x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])",
            "_y = pd.Series([2.0, 4.0, 6.0, 8.0, 10.0])",
            "assert abs(correlacion_pearson_manual(_x, _y) - 1.0) < 1e-4",
            "_y2 = pd.Series([10.0, 8.0, 6.0, 4.0, 2.0])",
            "assert abs(correlacion_pearson_manual(_x, _y2) + 1.0) < 1e-4",
        ],
        "ocultos": [
            "_x2 = pd.Series([1.0, 2.0, 3.0])",
            "_y3 = pd.Series([1.0, 2.0, 3.0])",
            "assert abs(correlacion_pearson_manual(_x2, _y3) - _x2.corr(_y3)) < 1e-4",
            "_c = pd.Series([3.0, 3.0, 3.0])",
            "assert correlacion_pearson_manual(_x2, _c) == 0.0",
        ],
    },
    {
        "n": 6,
        "titulo": "binning_uniforme(serie, n)",
        "enunciado": (
            "Implementa `binning_uniforme(serie, n)` que use `pd.cut` para dividir "
            "`serie` en `n` intervalos de **igual ancho** y devuelva un **diccionario** "
            "con la forma `{etiqueta_intervalo: conteo}` para cada bin.\n\n"
            "**Pista:** `pd.cut` devuelve una Serie de categorías; usa `.value_counts()` "
            "para obtener los conteos, luego conviértelo a dict. Incluye bins con conteo 0.\n\n"
            "**Ejemplo:** `binning_uniforme(pd.Series([1,2,3,4,5,6,7,8,9,10]), n=2)` "
            "devuelve un dict con 2 claves (los 2 intervalos)."
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def binning_uniforme(serie, n):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\n\n"
            "def binning_uniforme(serie, n):\n"
            "    bins = pd.cut(serie, bins=n)\n"
            "    return bins.value_counts(sort=False).to_dict()"
        ),
        "visibles": [
            "import pandas as pd",
            "_s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])",
            "_r = binning_uniforme(_s, 2)",
            "assert isinstance(_r, dict)",
            "assert len(_r) == 2",
            "assert sum(_r.values()) == 10",
        ],
        "ocultos": [
            "_r2 = binning_uniforme(_s, 5)",
            "assert len(_r2) == 5",
            "assert sum(_r2.values()) == 10",
        ],
    },
    {
        "n": 7,
        "titulo": "frecuencias_relativas(serie)",
        "enunciado": (
            "Implementa `frecuencias_relativas(serie)` que devuelva un **diccionario** "
            "con la frecuencia relativa (como porcentaje, redondeado a 2 decimales) "
            "de cada valor único en `serie`.\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "s = pd.Series(['A', 'B', 'A', 'A', 'B'])\n"
            "frecuencias_relativas(s)\n"
            "# {'A': 60.0, 'B': 40.0}\n"
            "```"
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def frecuencias_relativas(serie):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\n\n"
            "def frecuencias_relativas(serie):\n"
            "    vc = serie.value_counts(normalize=True) * 100\n"
            "    return vc.round(2).to_dict()"
        ),
        "visibles": [
            "import pandas as pd",
            "_s = pd.Series(['A', 'B', 'A', 'A', 'B'])",
            "_r = frecuencias_relativas(_s)",
            "assert isinstance(_r, dict)",
            "assert abs(_r['A'] - 60.0) < 0.1",
            "assert abs(_r['B'] - 40.0) < 0.1",
        ],
        "ocultos": [
            "assert abs(sum(frecuencias_relativas(_s).values()) - 100.0) < 0.1",
            "_s2 = pd.Series(['X', 'X', 'X'])",
            "assert abs(frecuencias_relativas(_s2)['X'] - 100.0) < 0.1",
        ],
    },
    {
        "n": 8,
        "titulo": "imputar_numerico(df, estrategia)",
        "enunciado": (
            "Implementa `imputar_numerico(df, estrategia='mediana')` que devuelva "
            "un **nuevo DataFrame** donde todos los nulos en columnas numéricas han "
            "sido reemplazados según la estrategia:\n\n"
            "- `'media'`: rellena con la media de cada columna.\n"
            "- `'mediana'`: rellena con la mediana de cada columna.\n\n"
            "Las columnas no numéricas no se modifican.\n\n"
            "**No modifiques el DataFrame original.**"
        ),
        "plantilla": (
            "import numpy as np\nimport pandas as pd\n\n"
            "def imputar_numerico(df, estrategia='mediana'):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import numpy as np\nimport pandas as pd\n\n"
            "def imputar_numerico(df, estrategia='mediana'):\n"
            "    df_out = df.copy()\n"
            "    for col in df_out.select_dtypes(include='number').columns:\n"
            "        if estrategia == 'media':\n"
            "            df_out[col] = df_out[col].fillna(df_out[col].mean())\n"
            "        else:\n"
            "            df_out[col] = df_out[col].fillna(df_out[col].median())\n"
            "    return df_out"
        ),
        "visibles": [
            "import numpy as np, pandas as pd",
            "_df = pd.DataFrame({'ciudad': ['Bogota', 'Cali', 'Medellin'], 'monto': [100.0, np.nan, 300.0]})",
            "_r = imputar_numerico(_df, 'mediana')",
            "assert _r['monto'].isnull().sum() == 0",
            "assert abs(_r['monto'].iloc[1] - 200.0) < 1e-9",
        ],
        "ocultos": [
            "_r2 = imputar_numerico(_df, 'media')",
            "assert abs(_r2['monto'].iloc[1] - 200.0) < 1e-9",
            "assert list(_r2['ciudad']) == ['Bogota', 'Cali', 'Medellin']",
            "_original_nulo = _df['monto'].isnull().sum()",
            "assert _original_nulo == 1",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 7 · Tarea 01 — 8 ejercicios autocalificables

### EDA y transformación de datos

**Instrucciones**

1. Implementa cada función en la celda que dice `# ✏️ TU CÓDIGO AQUÍ`
   (reemplaza la línea `raise NotImplementedError`).
2. **No cambies el nombre ni los parámetros** de las funciones.
3. Ejecuta las celdas de tests. Si la función está bien, verás ✅; si no,
   saltará un `AssertionError` señalando el caso que falla.
4. Objetivo: que **todas** las celdas de tests pasen sin error.

> Antes de programar cada función, piensa en el algoritmo: ¿qué pandas/numpy
> necesito? ¿Hay casos borde (serie vacía, todos iguales, sin nulos)?
""",
    "cierre_md": r"""
---
## Entrega

Cuando **todas** las celdas de tests muestren ✅, has completado la tarea.

| Ejercicio | Concepto |
|---|---|
| 1 perfil_columna | estadísticas descriptivas básicas |
| 2 columnas_con_muchos_nulos | diagnóstico de calidad de datos |
| 3 outliers_iqr | detección robusta de atípicos |
| 4 normalizar_todas_numericas | escalado min-max en bloque |
| 5 correlacion_pearson_manual | correlación desde cero |
| 6 binning_uniforme | discretización con pd.cut |
| 7 frecuencias_relativas | análisis de categóricas |
| 8 imputar_numerico | imputación con media o mediana |

> Reflexión: el ejercicio 5 implementa desde cero lo que `.corr()` hace en una
> línea. Eso es lo que da intuición sobre qué mide realmente la correlación.
""",
}

validar(ejercicios)
construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase07", "homework01.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "clase07_homework01_solved.ipynb"),
)
