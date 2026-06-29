"""Utilidades para construir tareas (homework) autocalificables con asserts.

Cada ejercicio se describe con un diccionario y produce, en el notebook lanzado:
  - Markdown: enunciado + casos de ejemplo.
  - Celda PLANTILLA protegida: el estudiante implementa (por defecto NotImplementedError).
  - Celda de TESTS VISIBLES (asserts que el estudiante puede leer).
  - Celda de TESTS OCULTOS / adicionales (asserts con casos extra).

Además genera una copia "resuelta" (sustituyendo la plantilla por la solución de
referencia) para poder verificar, fuera de curso/, que todo ejecuta sin error.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402


def _tests_block(titulo, asserts, cierre):
    cuerpo = "\n".join(asserts)
    return code(f'''
# === {titulo} ===
{cuerpo}
print("{cierre}")
''')


def construir_homework(meta, ejercicios, ruta_release, ruta_solved):
    """meta: dict(titulo, intro_md, cierre_md).
    ejercicios: lista de dicts con claves:
        n, titulo, enunciado, plantilla, solucion, visibles[], ocultos[]
    """
    release = []
    solved = []

    portada = [
        md(meta["intro_md"]),
        code('''
# Identifícate (esto ayuda si entregas el notebook).
NOMBRE = ""   # ✏️ escribe tu nombre completo
print("Tarea lista para resolver. Ejecuta cada bloque de tests tras implementar.")
'''),
    ]
    release += portada
    solved += portada

    for ej in ejercicios:
        enunciado = md(
            f"## Ejercicio {ej['n']} · {ej['titulo']}\n\n{ej['enunciado']}"
        )
        plantilla = code(ej["plantilla"])
        solucion = code(ej["solucion"])
        visibles = _tests_block(
            f"Tests visibles · Ejercicio {ej['n']}",
            ej["visibles"],
            f"✅ Ejercicio {ej['n']}: tests visibles superados.",
        )
        ocultos = _tests_block(
            f"Tests adicionales (ocultos) · Ejercicio {ej['n']}",
            ej["ocultos"],
            f"✅ Ejercicio {ej['n']}: tests adicionales superados.",
        )
        # release: enunciado, plantilla(vacía), tests visibles, tests ocultos
        release += [enunciado, plantilla, visibles, ocultos]
        # solved: enunciado, solución, tests visibles, tests ocultos
        solved += [enunciado, solucion, visibles, ocultos]

    cierre = md(meta["cierre_md"])
    release.append(cierre)
    solved.append(cierre)

    build(os.path.abspath(ruta_release), release)
    if ruta_solved:
        os.makedirs(os.path.dirname(os.path.abspath(ruta_solved)), exist_ok=True)
        build(os.path.abspath(ruta_solved), solved)


def validar(ejercicios, compartir_ns=False):
    """Ejecuta solución + (visibles + ocultos) de cada ejercicio y comprueba asserts.

    Si compartir_ns=True, todas las soluciones se acumulan en un mismo namespace
    (necesario para proyectos donde una función usa otra). Si False, cada
    ejercicio se valida aislado.
    """
    ns_global = {}
    for ej in ejercicios:
        ns = ns_global if compartir_ns else {}
        exec(ej["solucion"], ns)
        for linea in ej["visibles"] + ej["ocultos"]:
            exec(linea, ns)
    print(f"✔ {len(ejercicios)} ejercicios: soluciones de referencia validadas.")
