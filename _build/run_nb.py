"""Ejecuta uno o más notebooks de principio a fin y reporta si fallan.

    python _build/run_nb.py curso/clase01/lecture.ipynb [...]
"""
import sys
import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


def ejecutar(path: str) -> bool:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=120,
        kernel_name="fundamentos",
        resources={"metadata": {"path": "/".join(path.split("/")[:-1]) or "."}},
    )
    try:
        client.execute()
        print(f"✅ OK   {path}")
        return True
    except CellExecutionError as e:
        print(f"❌ FALLA {path}\n{e}")
        return False


if __name__ == "__main__":
    ok = all(ejecutar(p) for p in sys.argv[1:])
    sys.exit(0 if ok else 1)
