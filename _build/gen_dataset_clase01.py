"""Genera un dataset sintético y determinista para la Clase 1.

Salida: curso/datasets/transacciones.csv
Tema: transacciones de una pequeña tienda en varias ciudades de Colombia.
Solo usa la librería estándar para que el dataset sea reproducible sin pandas.
"""
import csv
import os
import random
from datetime import date, timedelta

random.seed(42)  # determinista: siempre se genera el mismo archivo

CIUDADES = ["Bogota", "Medellin", "Cali", "Barranquilla", "Bucaramanga"]
METODOS = ["efectivo", "tarjeta", "transferencia"]
CATEGORIAS = ["alimentos", "aseo", "tecnologia", "papeleria", "hogar"]

inicio = date(2024, 1, 1)
filas = []
for i in range(120):
    dia = inicio + timedelta(days=random.randint(0, 89))
    ciudad = random.choice(CIUDADES)
    categoria = random.choice(CATEGORIAS)
    metodo = random.choice(METODOS)
    # montos con un par de valores atípicos para que haya algo que "limpiar"
    monto = round(random.uniform(5_000, 250_000), 0)
    if random.random() < 0.04:
        monto = round(monto * 10, 0)  # outlier ocasional
    filas.append(
        {
            "id": 1000 + i,
            "fecha": dia.isoformat(),
            "ciudad": ciudad,
            "categoria": categoria,
            "metodo_pago": metodo,
            "monto": int(monto),
        }
    )

filas.sort(key=lambda f: f["fecha"])

aqui = os.path.dirname(os.path.abspath(__file__))
destino = os.path.join(aqui, "..", "curso", "datasets", "transacciones.csv")
destino = os.path.abspath(destino)

with open(destino, "w", newline="", encoding="utf-8") as f:
    campos = ["id", "fecha", "ciudad", "categoria", "metodo_pago", "monto"]
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    writer.writerows(filas)

print(f"Escritas {len(filas)} filas en {destino}")
