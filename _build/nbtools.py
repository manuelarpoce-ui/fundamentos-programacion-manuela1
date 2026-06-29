"""Helpers mínimos para construir notebooks .ipynb con nbformat.

    from nbtools import md, code, build
    build("salida.ipynb", [md("# Titulo"), code("print('hola')")])
"""
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell


def md(texto: str):
    """Celda Markdown. Se hace dedent ligero: se quitan los saltos de línea
    iniciales/finales para que el contenido quede limpio."""
    return new_markdown_cell(texto.strip("\n"))


def code(texto: str):
    """Celda de código."""
    return new_code_cell(texto.strip("\n"))


def build(path: str, cells, kernel: str = "python3"):
    nb = new_notebook(cells=cells)
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3 (fundamentos)",
            "language": "python",
            "name": kernel,
        },
        "language_info": {"name": "python", "version": "3.11"},
    }
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    n_md = sum(1 for c in cells if c.cell_type == "markdown")
    n_code = sum(1 for c in cells if c.cell_type == "code")
    print(f"{path}: {len(cells)} celdas ({n_md} md, {n_code} code)")
