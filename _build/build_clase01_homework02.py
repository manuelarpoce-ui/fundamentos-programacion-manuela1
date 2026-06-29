"""Construye curso/clase01/homework02.ipynb — mini proyecto autocalificable.

Proyecto: "Mini-analizador de notas de un curso". El estudiante construye, parte
por parte, un pequeño sistema que recibe las notas como texto y produce un
resumen. Cada parte se apoya en las anteriores (integración), y todas las partes
son autocalificables con asserts.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    {
        "n": 1,
        "titulo": "Parsear las notas (de texto a datos)",
        "enunciado": (
            "Las notas llegan como un texto: `\"Ana:4.5,Luis:3.0,Sara:2.5\"`.\n\n"
            "Implementa `parsear(texto)` que devuelva una **lista de tuplas** "
            "`(nombre, nota)` donde el nombre es texto y la nota es `float`.\n\n"
            "**Ejemplo:** `parsear(\"Ana:4.5,Luis:3.0\")` → `[('Ana', 4.5), ('Luis', 3.0)]`.\n\n"
            "Pista: `texto.split(\",\")` separa por comas; `parte.split(\":\")` separa "
            "nombre y nota; `float(...)` convierte a número."
        ),
        "plantilla": f"def parsear(texto):\n    # ✏️ TU CÓDIGO AQUÍ\n    {NI}",
        "solucion": (
            "def parsear(texto):\n"
            "    resultado = []\n"
            "    for parte in texto.split(','):\n"
            "        nombre, nota = parte.split(':')\n"
            "        resultado.append((nombre, float(nota)))\n"
            "    return resultado"
        ),
        "visibles": [
            "assert parsear('Ana:4.5,Luis:3.0') == [('Ana', 4.5), ('Luis', 3.0)]",
        ],
        "ocultos": [
            "assert parsear('Sara:2.5') == [('Sara', 2.5)]",
            "assert parsear('A:5.0,B:0.0,C:3.3') == [('A', 5.0), ('B', 0.0), ('C', 3.3)]",
        ],
    },
    {
        "n": 2,
        "titulo": "Promedio del curso (acumulador)",
        "enunciado": (
            "Implementa `promedio(notas)` que reciba una lista de tuplas "
            "`(nombre, nota)` y devuelva el promedio de las notas como `float`. "
            "Si la lista está vacía, devuelve `None`.\n\n"
            "**Ejemplo:** `promedio([('Ana', 4.0), ('Luis', 2.0)])` → `3.0`."
        ),
        "plantilla": f"def promedio(notas):\n    # ✏️ TU CÓDIGO AQUÍ\n    {NI}",
        "solucion": (
            "def promedio(notas):\n"
            "    if len(notas) == 0:\n"
            "        return None\n"
            "    total = 0.0\n"
            "    for nombre, nota in notas:\n"
            "        total += nota\n"
            "    return total / len(notas)"
        ),
        "visibles": [
            "assert promedio([('Ana', 4.0), ('Luis', 2.0)]) == 3.0",
            "assert promedio([]) is None",
        ],
        "ocultos": [
            "assert promedio([('X', 5.0)]) == 5.0",
            "assert abs(promedio([('A', 3.0), ('B', 4.0), ('C', 5.0)]) - 4.0) < 1e-9",
        ],
    },
    {
        "n": 3,
        "titulo": "El mejor estudiante (patrón campeón)",
        "enunciado": (
            "Implementa `mejor(notas)` que devuelva el **nombre** del estudiante con "
            "la nota más alta. En caso de empate, el primero que aparece.\n\n"
            "**Ejemplo:** `mejor([('Ana', 4.5), ('Luis', 3.0)])` → `'Ana'`."
        ),
        "plantilla": f"def mejor(notas):\n    # ✏️ TU CÓDIGO AQUÍ\n    {NI}",
        "solucion": (
            "def mejor(notas):\n"
            "    nombre_top, nota_top = notas[0]\n"
            "    for nombre, nota in notas:\n"
            "        if nota > nota_top:\n"
            "            nota_top = nota\n"
            "            nombre_top = nombre\n"
            "    return nombre_top"
        ),
        "visibles": [
            "assert mejor([('Ana', 4.5), ('Luis', 3.0)]) == 'Ana'",
        ],
        "ocultos": [
            "assert mejor([('A', 2.0), ('B', 4.0), ('C', 4.0)]) == 'B'",
            "assert mejor([('Solo', 1.0)]) == 'Solo'",
        ],
    },
    {
        "n": 4,
        "titulo": "Cuántos aprobaron (contador con umbral)",
        "enunciado": (
            "Implementa `aprobados(notas, umbral=3.0)` que cuente cuántos estudiantes "
            "tienen nota **mayor o igual** al umbral.\n\n"
            "**Ejemplo:** `aprobados([('A', 3.0), ('B', 2.9), ('C', 4.0)])` → `2`."
        ),
        "plantilla": f"def aprobados(notas, umbral=3.0):\n    # ✏️ TU CÓDIGO AQUÍ\n    {NI}",
        "solucion": (
            "def aprobados(notas, umbral=3.0):\n"
            "    cuenta = 0\n"
            "    for nombre, nota in notas:\n"
            "        if nota >= umbral:\n"
            "            cuenta += 1\n"
            "    return cuenta"
        ),
        "visibles": [
            "assert aprobados([('A', 3.0), ('B', 2.9), ('C', 4.0)]) == 2",
        ],
        "ocultos": [
            "assert aprobados([('A', 1.0), ('B', 2.0)]) == 0",
            "assert aprobados([('A', 4.0), ('B', 5.0)], umbral=4.5) == 1",
        ],
    },
    {
        "n": 5,
        "titulo": "Distribución por bandas (varios contadores + decisión)",
        "enunciado": (
            "Implementa `distribucion(notas)` que devuelva una tupla "
            "`(reprobados, regulares, buenos)` contando:\n"
            "- **reprobados:** nota < 3.0\n"
            "- **regulares:** 3.0 <= nota < 4.0\n"
            "- **buenos:** nota >= 4.0\n\n"
            "**Ejemplo:** `distribucion([('A', 2.0), ('B', 3.5), ('C', 4.8)])` → `(1, 1, 1)`."
        ),
        "plantilla": f"def distribucion(notas):\n    # ✏️ TU CÓDIGO AQUÍ\n    {NI}",
        "solucion": (
            "def distribucion(notas):\n"
            "    reprobados = regulares = buenos = 0\n"
            "    for nombre, nota in notas:\n"
            "        if nota < 3.0:\n"
            "            reprobados += 1\n"
            "        elif nota < 4.0:\n"
            "            regulares += 1\n"
            "        else:\n"
            "            buenos += 1\n"
            "    return (reprobados, regulares, buenos)"
        ),
        "visibles": [
            "assert distribucion([('A', 2.0), ('B', 3.5), ('C', 4.8)]) == (1, 1, 1)",
        ],
        "ocultos": [
            "assert distribucion([]) == (0, 0, 0)",
            "assert distribucion([('A', 2.9), ('B', 3.0), ('C', 3.9), ('D', 4.0)]) == (1, 2, 1)",
        ],
    },
    {
        "n": 6,
        "titulo": "Integración: resumen del curso",
        "enunciado": (
            "¡La pieza final! Implementa `resumen(texto)` que reciba el texto crudo de "
            "notas y devuelva una tupla con cuatro valores, **reutilizando tus "
            "funciones anteriores**:\n\n"
            "`(cantidad_estudiantes, promedio_curso, mejor_estudiante, num_aprobados)`\n\n"
            "**Ejemplo:** `resumen(\"Ana:4.0,Luis:2.0,Sara:5.0\")` → `(3, 3.6666..., 'Sara', 2)`.\n\n"
            "Esto demuestra el poder de **descomponer**: ya tienes todas las piezas; "
            "solo las combinas."
        ),
        "plantilla": f"def resumen(texto):\n    # ✏️ TU CÓDIGO AQUÍ (usa parsear, promedio, mejor, aprobados)\n    {NI}",
        "solucion": (
            "def resumen(texto):\n"
            "    notas = parsear(texto)\n"
            "    return (len(notas), promedio(notas), mejor(notas), aprobados(notas))"
        ),
        "visibles": [
            "_r = resumen('Ana:4.0,Luis:2.0,Sara:5.0')",
            "assert _r[0] == 3",
            "assert abs(_r[1] - 11.0/3) < 1e-9",
            "assert _r[2] == 'Sara'",
            "assert _r[3] == 2",
        ],
        "ocultos": [
            "_r2 = resumen('A:1.0,B:1.5')",
            "assert _r2 == (2, 1.25, 'B', 0)",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 1 · Tarea 02 — Mini proyecto: analizador de notas

### Pensamiento algorítmico aplicado

En esta tarea construirás, **pieza por pieza**, un pequeño analizador de las notas
de un curso. Recibirás las notas como un texto y producirás un resumen útil.

```
  texto crudo            tu analizador               resumen
"Ana:4.5,Luis:3.0"  ──▶  parsear → calcular  ──▶  (cantidad, promedio,
                                                    mejor, aprobados)
```

Es un proyecto de **integración**: cada parte resuelve un subproblema pequeño
(parsear, promediar, encontrar el mejor, contar...) y la última parte las combina.
Así trabaja de verdad un científico de datos: descomponiendo un problema grande en
piezas conocidas.

**Instrucciones**

1. Implementa cada función reemplazando `raise NotImplementedError`.
2. **No cambies nombres ni parámetros**: las partes se llaman entre sí.
3. Resuélvelas **en orden**: la Parte 6 usa las anteriores.
4. Ejecuta los tests de cada parte hasta ver ✅.

> 🧠 Escribe el pseudocódigo de cada parte antes de programarla.
""",
    "cierre_md": r"""
---
## ¡Proyecto terminado! 🏗️

Si todos los tests pasan, construiste un analizador funcional combinando los
patrones de la clase:

| Parte | Patrón |
|---|---|
| 1 Parsear | transformar la entrada (texto → datos) |
| 2 Promedio | acumulador + caso borde |
| 3 Mejor | campeón |
| 4 Aprobados | contador con umbral |
| 5 Distribución | varios contadores + decisión escalonada |
| 6 Resumen | **integración** (descomposición) |

### Reto opcional (sin calificar)
- Añade una función `peor(notas)` que devuelva el estudiante con la nota más baja.
- Modifica `resumen` para que también informe la `distribucion`.
- ¿Qué pasaría si el texto trae un espacio extra, como `"Ana : 4.5"`? ¿Cómo lo
  limpiarías? (pista: `.strip()`).

> 💡 En la Clase 6, con pandas, todo este analizador cabría en unas pocas líneas.
> Pero hoy entiendes **cada paso** de lo que esa magia hace por dentro.
""",
}

validar(ejercicios, compartir_ns=True)
construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase01", "homework02.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "homework02_solved.ipynb"),
)
