"""
verificador.py
==============

Pequeña utilidad de autocalificación basada en `assert` para los notebooks del
curso. La idea es imitar el espíritu de nbgrader (tests visibles + tests
ocultos) pero sin dependencias extra: el estudiante simplemente ejecuta la
celda de tests y obtiene retroalimentación inmediata con ✅ / ❌.

Uso típico dentro de un notebook
--------------------------------

    from verificador import revisar, Reporte

    rep = Reporte("Ejercicio 1: suma")
    rep.comprobar("caso simple",  suma(2, 3) == 5)
    rep.comprobar("con ceros",    suma(0, 0) == 0)
    rep.comprobar("negativos",    suma(-2, -3) == -5)
    rep.resumen()

`revisar` es una versión de una sola línea para comprobaciones rápidas.
"""

from __future__ import annotations

from typing import Any, Callable


# --------------------------------------------------------------------------- #
# Comprobación de una sola línea
# --------------------------------------------------------------------------- #
def revisar(nombre: str, condicion: bool, pista: str = "") -> bool:
    """Imprime ✅ o ❌ según `condicion`. Devuelve el booleano para encadenar.

    Parameters
    ----------
    nombre : str
        Descripción legible de lo que se está probando.
    condicion : bool
        Resultado de la comprobación (normalmente una comparación ``==``).
    pista : str, opcional
        Mensaje de ayuda que se muestra solo cuando la prueba falla.
    """
    if condicion:
        print(f"✅ {nombre}")
        return True
    msg = f"❌ {nombre}"
    if pista:
        msg += f"  →  pista: {pista}"
    print(msg)
    return False


# --------------------------------------------------------------------------- #
# Reporte agrupado de varias comprobaciones
# --------------------------------------------------------------------------- #
class Reporte:
    """Agrupa varias comprobaciones y muestra un resumen final.

    Pensado para que cada ejercicio del homework tenga su propio `Reporte`,
    de modo que el estudiante vea cuántos casos pasó de cuántos.
    """

    def __init__(self, titulo: str = "Comprobaciones") -> None:
        self.titulo = titulo
        self.pasadas = 0
        self.total = 0

    def comprobar(self, nombre: str, condicion: bool, pista: str = "") -> "Reporte":
        """Registra una comprobación y la imprime. Devuelve ``self`` para encadenar."""
        self.total += 1
        if revisar(nombre, bool(condicion), pista):
            self.pasadas += 1
        return self

    def comprobar_igual(self, nombre: str, obtenido: Any, esperado: Any) -> "Reporte":
        """Comprueba igualdad mostrando el valor obtenido cuando falla."""
        ok = obtenido == esperado
        pista = "" if ok else f"esperaba {esperado!r}, obtuve {obtenido!r}"
        return self.comprobar(nombre, ok, pista)

    def comprobar_excepcion(
        self, nombre: str, funcion: Callable[[], Any], excepcion: type = Exception
    ) -> "Reporte":
        """Comprueba que ``funcion()`` lance la ``excepcion`` esperada."""
        try:
            funcion()
        except excepcion:
            return self.comprobar(nombre, True)
        except Exception as e:  # noqa: BLE001 - queremos reportar cualquier otra
            return self.comprobar(
                nombre, False, f"lanzó {type(e).__name__} en vez de {excepcion.__name__}"
            )
        return self.comprobar(nombre, False, "no se lanzó ninguna excepción")

    def resumen(self) -> bool:
        """Imprime el marcador final. Devuelve True si pasaron todas."""
        print("─" * 48)
        estado = "🎉 ¡Todo en orden!" if self.pasadas == self.total else "Sigue intentando 💪"
        print(f"{self.titulo}: {self.pasadas}/{self.total} pruebas superadas. {estado}")
        return self.pasadas == self.total
