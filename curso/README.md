# Curso de Fundamentos de Programación para Ciencia de Datos

Curso universitario de 8 clases (3 h c/u), en español, inspirado en la metodología
de CS50 (aprendizaje basado en problemas). Todo el contenido vive en notebooks
Jupyter, con énfasis en *pensar antes de programar*:
**contexto → solución intuitiva → algoritmo → pseudocódigo → Python → análisis**.

## Estructura

```
curso/
  claseNN/
    lecture.ipynb      teoría con ejemplos, diagramas y quiz
    practice01.ipynb   10 ejercicios graduales con solución oculta
    practice02.ipynb   caso aplicado a ciencia de datos
    homework01.ipynb   8 ejercicios autocalificables
    homework02.ipynb   mini proyecto autocalificable
  assets/              imágenes y recursos
  datasets/            datos (sintéticos y reales) usados en las clases
  shared/              utilidades compartidas (p. ej. verificador.py)
```

| Clase | Tema |
|-------|------|
| 1 | Pensamiento algorítmico y pseudocódigo ✅ |
| 2 | Variables, tipos, operadores, condicionales |
| 3 | Ciclos, funciones y lambdas |
| 4 | Estructuras de datos de Python |
| 5 | NumPy |
| 6 | Pandas |
| 7 | EDA y transformación |
| 8 | Proyecto integrador |

> **Estado:** la **Clase 1** está completa. Las carpetas `clase02`–`clase08`
> están creadas como andamiaje y se desarrollarán en iteraciones siguientes.

## Cómo ejecutar

El proyecto usa [`uv`](https://github.com/astral-sh/uv). Dependencias en
`pyproject.toml` (numpy, pandas, matplotlib, ipykernel).

```bash
uv sync
uv run jupyter lab        # o abre los .ipynb en VS Code / Jupyter
```

## Autocalificación

Las tareas usan comprobaciones basadas en `assert` (sin dependencias extra):

- **practice01 / practice02:** comprobaciones *suaves* (`verificador.revisar`)
  que imprimen ✅/❌ sin interrumpir la ejecución.
- **homework01 / homework02:** celdas de *tests visibles* y *tests adicionales*
  con `assert`. Una tarea recién abierta **no** corre completa: las celdas de
  tests fallan hasta que implementas cada función (ese es el trabajo del
  estudiante).

La utilidad compartida está en [`shared/verificador.py`](shared/verificador.py).

## Generación de notebooks

Los notebooks se generan de forma reproducible con los scripts de `../_build/`
(que usan `nbformat`). Para regenerar la Clase 1:

```bash
.venv/bin/python _build/gen_dataset_clase01.py
.venv/bin/python _build/build_clase01_lecture.py
.venv/bin/python _build/build_clase01_practice01.py
.venv/bin/python _build/build_clase01_practice02.py
.venv/bin/python _build/build_clase01_homework01.py
.venv/bin/python _build/build_clase01_homework02.py
```
