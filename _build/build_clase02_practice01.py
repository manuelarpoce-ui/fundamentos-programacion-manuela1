"""Construye curso/clase02/practice01.ipynb — 10 ejercicios graduales.

Clase 2: Variables, tipos de datos, operadores y condicionales.
Contexto: finanzas, negocios y ciencia de datos.

Patrón por ejercicio:
  1. Markdown con enunciado + ejemplo.
  2. Celda plantilla (el estudiante escribe aquí).
  3. Celda de comprobación SUAVE (revisar()).
  4. Markdown <details> con la solución comentada (oculta).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []

# --------------------------------------------------------------------------- #
# Portada + bootstrap
# --------------------------------------------------------------------------- #
C += [
md(r"""
# Clase 2 · Práctica 01 — 10 ejercicios graduales

### Variables, tipos, operadores y condicionales

Estos 10 ejercicios van **de menor a mayor dificultad**. Para cada uno:

1. Lee el enunciado y el ejemplo.
2. Escribe tu solución en la celda `# ✏️ TU CÓDIGO AQUÍ`.
3. Ejecuta la celda de **comprobación**: verás ✅ o ❌ por cada caso.
4. ¿Atascado? Despliega **💡 Ver solución** al final de cada ejercicio.

> 🧠 **Antes de teclear**, escribe el pseudocódigo y traza un ejemplo.
> El objetivo es entender la lógica, no solo pasar las comprobaciones.

> ⚙️ Las comprobaciones son *suaves*: si tu función aún no está lista,
> verás ❌ pero el notebook seguirá ejecutándose sin romperse.
"""),

code(r"""
import os, sys
sys.path.append(os.path.abspath(os.path.join("..", "shared")))
from verificador import revisar
print("Listo. Usa revisar(descripcion, condicion) para comprobar tus respuestas.")
"""),
]


# --------------------------------------------------------------------------- #
# Helper para construir ejercicios
# --------------------------------------------------------------------------- #
def ejercicio(numero, titulo, enunciado_md, plantilla, check_code, solucion_md):
    C.append(md("## Ejercicio {} · {}\n\n{}".format(numero, titulo, enunciado_md)))
    C.append(code(plantilla))
    C.append(code(check_code))
    C.append(md(solucion_md))


# ---- 1: Clasificar monto ---------------------------------------------------
ejercicio(
    1, "Clasificar monto de venta",
    r"""Escribe `clasificar_monto(monto)` que devuelva:
- `"alto"` si `monto > 100000`
- `"medio"` si `monto > 30000` (y <= 100000)
- `"bajo"` si `monto <= 30000`

**Ejemplo:** `clasificar_monto(150000)` → `"alto"`;
`clasificar_monto(50000)` → `"medio"`;
`clasificar_monto(20000)` → `"bajo"`.""",
    r"""
def clasificar_monto(monto):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("150000 -> alto",  clasificar_monto(150000) == "alto")
revisar("50000  -> medio", clasificar_monto(50000)  == "medio")
revisar("20000  -> bajo",  clasificar_monto(20000)  == "bajo")
revisar("100000 -> medio", clasificar_monto(100000) == "medio")
revisar("100001 -> alto",  clasificar_monto(100001) == "alto")
revisar("30000  -> bajo",  clasificar_monto(30000)  == "bajo")
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def clasificar_monto(monto):
    if monto > 100000:
        return "alto"
    elif monto > 30000:
        return "medio"
    else:
        return "bajo"
```
Patrón de **decisión escalonada**: las condiciones se evalúan de mayor a
menor. El `elif` garantiza que si ya pasó la primera condición, no se
evalúan las siguientes.
</details>
""",
)

# ---- 2: Calcular IVA -------------------------------------------------------
ejercicio(
    2, "Calcular IVA",
    r"""Escribe `calcular_iva(precio_sin_iva, tasa)` que devuelva una **tupla**
`(precio_sin_iva, iva, precio_con_iva)` donde:
- `iva = precio_sin_iva * tasa`
- `precio_con_iva = precio_sin_iva + iva`

**Ejemplo:** `calcular_iva(100000, 0.19)` → `(100000, 19000.0, 119000.0)`.""",
    r"""
def calcular_iva(precio_sin_iva, tasa):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
resultado = calcular_iva(100000, 0.19)
revisar("precio sin iva",  resultado[0] == 100000)
revisar("iva calculado",   resultado[1] == 19000.0)
revisar("precio con iva",  resultado[2] == 119000.0)
resultado2 = calcular_iva(50000, 0.08)
revisar("tasa 8%: precio_con_iva", resultado2[2] == 54000.0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def calcular_iva(precio_sin_iva, tasa):
    iva = precio_sin_iva * tasa
    precio_con_iva = precio_sin_iva + iva
    return (precio_sin_iva, iva, precio_con_iva)
```
Una función puede devolver **múltiples valores** empaquetándolos en una
tupla. El que llama la función puede desempacar:
`base, iva, total = calcular_iva(100000, 0.19)`.
</details>
""",
)

# ---- 3: Validar contraseña ------------------------------------------------
ejercicio(
    3, "Validar contraseña simple",
    r"""Escribe `contrasena_valida(contrasena)` que devuelva `True` si:
- La longitud es >= 8 caracteres, **Y**
- Contiene al menos un dígito (0-9).

Si cualquiera de las dos condiciones falla, devuelve `False`.

**Ejemplo:** `contrasena_valida("abc12345")` → `True`;
`contrasena_valida("abcdefgh")` → `False` (sin dígito);
`contrasena_valida("abc1")` → `False` (muy corta).

**Pista:** para recorrer la contraseña carácter por carácter y verificar si
es dígito: `c.isdigit()`.""",
    r"""
def contrasena_valida(contrasena):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("abc12345 -> True",  contrasena_valida("abc12345") is True)
revisar("abcdefgh -> False", contrasena_valida("abcdefgh") is False)
revisar("abc1 -> False",     contrasena_valida("abc1") is False)
revisar("12345678 -> True",  contrasena_valida("12345678") is True)
revisar("pass1234 -> True",  contrasena_valida("pass1234") is True)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def contrasena_valida(contrasena):
    if len(contrasena) < 8:
        return False
    tiene_digito = False
    for c in contrasena:
        if c.isdigit():
            tiene_digito = True
            break
    return tiene_digito
```
**Versión compacta** con `any()`:
```python
def contrasena_valida(contrasena):
    return len(contrasena) >= 8 and any(c.isdigit() for c in contrasena)
```
`any()` devuelve `True` si al menos un elemento del iterable es `True`.
</details>
""",
)

# ---- 4: Categoría de temperatura ------------------------------------------
ejercicio(
    4, "Categoría de temperatura",
    r"""Escribe `categoria_temperatura(grados)` que devuelva:
- `"frio"` si `grados < 10`
- `"templado"` si `10 <= grados <= 25`
- `"calor"` si `grados > 25`

**Ejemplo:** `categoria_temperatura(5)` → `"frio"`;
`categoria_temperatura(20)` → `"templado"`;
`categoria_temperatura(30)` → `"calor"`.""",
    r"""
def categoria_temperatura(grados):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("5  -> frio",     categoria_temperatura(5)  == "frio")
revisar("10 -> templado", categoria_temperatura(10) == "templado")
revisar("25 -> templado", categoria_temperatura(25) == "templado")
revisar("30 -> calor",    categoria_temperatura(30) == "calor")
revisar("-5 -> frio",     categoria_temperatura(-5) == "frio")
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def categoria_temperatura(grados):
    if grados < 10:
        return "frio"
    elif grados <= 25:
        return "templado"
    else:
        return "calor"
```
Nótese el uso de la comparación encadenada implícita: si ya pasó `< 10`,
sabemos que `grados >= 10`, así que `elif grados <= 25` cubre el rango
`[10, 25]` sin escribir `10 <= grados <= 25`.
</details>
""",
)

# ---- 5: Año bisiesto -------------------------------------------------------
ejercicio(
    5, "Año bisiesto",
    r"""Escribe `es_bisiesto(anio)` que devuelva `True` si el año es bisiesto.

**Regla del calendario gregoriano:**
- Es bisiesto si es divisible por 4, **EXCEPTO** si es divisible por 100,
  a menos que también sea divisible por 400.

**Ejemplos:**
- `es_bisiesto(2024)` → `True` (div. por 4, no por 100)
- `es_bisiesto(1900)` → `False` (div. por 100, no por 400)
- `es_bisiesto(2000)` → `True` (div. por 400)
- `es_bisiesto(2023)` → `False`""",
    r"""
def es_bisiesto(anio):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("2024 -> True",  es_bisiesto(2024) is True)
revisar("1900 -> False", es_bisiesto(1900) is False)
revisar("2000 -> True",  es_bisiesto(2000) is True)
revisar("2023 -> False", es_bisiesto(2023) is False)
revisar("2100 -> False", es_bisiesto(2100) is False)
revisar("1600 -> True",  es_bisiesto(1600) is True)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def es_bisiesto(anio):
    if anio % 400 == 0:
        return True
    elif anio % 100 == 0:
        return False
    elif anio % 4 == 0:
        return True
    else:
        return False
```
**Versión en una línea:**
```python
def es_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)
```
El orden importa: verificamos `% 400` antes que `% 100` para que los
siglos-bisiestos (2000, 2400…) no sean capturados por la rama `% 100`.
</details>
""",
)

# ---- 6: Calcular descuento ------------------------------------------------
ejercicio(
    6, "Calcular descuento escalonado",
    r"""Escribe `calcular_descuento(monto)` que devuelva el porcentaje de descuento
aplicable:
- `0.15` si `monto > 500000`
- `0.08` si `monto > 200000` (y <= 500000)
- `0.00` en cualquier otro caso

**Ejemplo:** `calcular_descuento(600000)` → `0.15`;
`calcular_descuento(300000)` → `0.08`;
`calcular_descuento(100000)` → `0.0`.""",
    r"""
def calcular_descuento(monto):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("600000 -> 0.15", calcular_descuento(600000) == 0.15)
revisar("300000 -> 0.08", calcular_descuento(300000) == 0.08)
revisar("100000 -> 0.00", calcular_descuento(100000) == 0.0)
revisar("500000 -> 0.08", calcular_descuento(500000) == 0.08)
revisar("500001 -> 0.15", calcular_descuento(500001) == 0.15)
revisar("0      -> 0.00", calcular_descuento(0)      == 0.0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def calcular_descuento(monto):
    if monto > 500000:
        return 0.15
    elif monto > 200000:
        return 0.08
    else:
        return 0.0
```
Presta atención a los bordes: `500000` cae en `elif monto > 200000` porque
`500000 > 500000` es `False`. Si el negocio quisiera que `500000` también
tenga el 15%, la condición sería `monto >= 500000`.
</details>
""",
)

# ---- 7: Paridad de suma ---------------------------------------------------
ejercicio(
    7, "Paridad de suma",
    r"""Escribe `paridad_suma(a, b)` que devuelva `"par"` si la suma de `a` y `b`
es par, o `"impar"` si es impar.

**Ejemplo:** `paridad_suma(3, 5)` → `"par"` (3+5=8);
`paridad_suma(2, 3)` → `"impar"` (2+3=5).

**Pista:** usa el operador `%` (módulo).""",
    r"""
def paridad_suma(a, b):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
revisar("3+5=8 -> par",   paridad_suma(3, 5) == "par")
revisar("2+3=5 -> impar", paridad_suma(2, 3) == "impar")
revisar("0+0=0 -> par",   paridad_suma(0, 0) == "par")
revisar("1+1=2 -> par",   paridad_suma(1, 1) == "par")
revisar("1+2=3 -> impar", paridad_suma(1, 2) == "impar")
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def paridad_suma(a, b):
    if (a + b) % 2 == 0:
        return "par"
    else:
        return "impar"
```
**Versión ternaria:**
```python
def paridad_suma(a, b):
    return "par" if (a + b) % 2 == 0 else "impar"
```
Curiosidad: la suma de dos enteros es par si **ambos** son pares o
**ambos** son impares. Se puede verificar como `a % 2 == b % 2`.
</details>
""",
)

# ---- 8: IMC ---------------------------------------------------------------
ejercicio(
    8, "Índice de Masa Corporal (IMC)",
    r"""Escribe `interpretar_imc(peso_kg, altura_m)` que devuelva una **tupla**
`(imc, categoria)` donde:
- `imc = peso_kg / altura_m²` (redondeado a 1 decimal)
- `categoria`:
  - `"bajo peso"` si `imc < 18.5`
  - `"normal"` si `18.5 <= imc < 25`
  - `"sobrepeso"` si `25 <= imc < 30`
  - `"obesidad"` si `imc >= 30`

**Ejemplo:** `interpretar_imc(70, 1.75)` → `(22.9, "normal")`.""",
    r"""
def interpretar_imc(peso_kg, altura_m):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
imc, cat = interpretar_imc(70, 1.75)
revisar("IMC 70/1.75 = 22.9",     imc == 22.9)
revisar("categoria normal",        cat == "normal")
imc2, cat2 = interpretar_imc(50, 1.70)
revisar("IMC 50/1.70 = 17.3",     imc2 == 17.3)
revisar("categoria bajo peso",     cat2 == "bajo peso")
imc3, cat3 = interpretar_imc(90, 1.70)
revisar("categoria sobrepeso",     cat3 == "sobrepeso")
imc4, cat4 = interpretar_imc(110, 1.70)
revisar("categoria obesidad",      cat4 == "obesidad")
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def interpretar_imc(peso_kg, altura_m):
    imc = round(peso_kg / (altura_m ** 2), 1)
    if imc < 18.5:
        categoria = "bajo peso"
    elif imc < 25:
        categoria = "normal"
    elif imc < 30:
        categoria = "sobrepeso"
    else:
        categoria = "obesidad"
    return (imc, categoria)
```
`round(valor, n)` redondea a `n` decimales. La cadena de `elif` es el
patrón de **decisión escalonada** que usamos a lo largo de la clase.
</details>
""",
)

# ---- 9: Conversión de temperatura -----------------------------------------
ejercicio(
    9, "Conversión de temperatura",
    r"""Escribe `convertir_celsius(grados_c)` que devuelva una **tupla**
`(fahrenheit, kelvin)` con las conversiones:
- `fahrenheit = grados_c * (9 / 5) + 32`
- `kelvin = grados_c + 273.15`

Redondea ambos a 2 decimales.

**Ejemplo:** `convertir_celsius(0)` → `(32.0, 273.15)`;
`convertir_celsius(100)` → `(212.0, 373.15)`.""",
    r"""
def convertir_celsius(grados_c):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
f, k = convertir_celsius(0)
revisar("0C -> 32F",     f == 32.0)
revisar("0C -> 273.15K", k == 273.15)
f2, k2 = convertir_celsius(100)
revisar("100C -> 212F",  f2 == 212.0)
revisar("100C -> 373.15K", k2 == 373.15)
f3, k3 = convertir_celsius(-40)
revisar("-40C -> -40F",  f3 == -40.0)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def convertir_celsius(grados_c):
    fahrenheit = round(grados_c * (9 / 5) + 32, 2)
    kelvin     = round(grados_c + 273.15, 2)
    return (fahrenheit, kelvin)
```
Un dato curioso: -40°C es exactamente -40°F. Es el único punto en que
las dos escalas coinciden.
</details>
""",
)

# ---- 10: Conversión de moneda ----------------------------------------------
ejercicio(
    10, "Precio en distintas monedas",
    r"""Escribe `convertir_moneda(precio_cop, tasa_usd, tasa_eur)` que devuelva
una **tupla** `(precio_usd, precio_eur)` con el precio convertido.
- `precio_usd = precio_cop / tasa_usd`
- `precio_eur = precio_cop / tasa_eur`

Redondea ambos a 2 decimales.

**Ejemplo:** `convertir_moneda(420000, 4200.0, 4600.0)` →
`(100.0, 91.3)`.

**Caso borde:** si alguna tasa es `<= 0`, devuelve `(None, None)`.""",
    r"""
def convertir_moneda(precio_cop, tasa_usd, tasa_eur):
    # ✏️ TU CÓDIGO AQUÍ
    return None
""",
    r"""
usd, eur = convertir_moneda(420000, 4200.0, 4600.0)
revisar("420000 COP = 100.0 USD", usd == 100.0)
revisar("420000 COP ~= 91.3 EUR", eur == 91.3)
result_inv = convertir_moneda(100000, 0, 4600.0)
revisar("tasa 0 -> None", result_inv == (None, None))
usd2, eur2 = convertir_moneda(1000000, 4100.0, 4500.0)
revisar("1000000/4100 ~ 243.9", usd2 == 243.9)
""",
    r"""
<details><summary>💡 Ver solución</summary>

```python
def convertir_moneda(precio_cop, tasa_usd, tasa_eur):
    if tasa_usd <= 0 or tasa_eur <= 0:
        return (None, None)
    precio_usd = round(precio_cop / tasa_usd, 2)
    precio_eur = round(precio_cop / tasa_eur, 2)
    return (precio_usd, precio_eur)
```
Validar primero que las tasas sean positivas evita `ZeroDivisionError`.
Este patrón de "validar antes de operar" lo usaremos siempre.
</details>
""",
)

C.append(md(r"""
---
## ¡Terminaste la práctica 01!

Si todas las comprobaciones muestran ✅, dominas los fundamentos de la clase:
**tipos primitivos, operadores aritméticos, relacionales y lógicos, y
condicionales if/elif/else**.

➡️ Continúa con **practice02.ipynb**, donde aplicaremos estas ideas a un
análisis de datos reales de transacciones financieras.
"""))


# ===================================================================== #
# VALIDACIÓN EN TIEMPO DE CONSTRUCCIÓN
# ===================================================================== #
def _validar():
    def clasificar_monto(monto):
        if monto > 100000:
            return "alto"
        elif monto > 30000:
            return "medio"
        else:
            return "bajo"
    assert clasificar_monto(150000) == "alto"
    assert clasificar_monto(50000)  == "medio"
    assert clasificar_monto(20000)  == "bajo"
    assert clasificar_monto(100000) == "medio"
    assert clasificar_monto(30000)  == "bajo"

    def calcular_iva(precio_sin_iva, tasa):
        iva = precio_sin_iva * tasa
        return (precio_sin_iva, iva, precio_sin_iva + iva)
    assert calcular_iva(100000, 0.19) == (100000, 19000.0, 119000.0)
    assert calcular_iva(50000, 0.08)[2] == 54000.0

    def contrasena_valida(contrasena):
        return len(contrasena) >= 8 and any(c.isdigit() for c in contrasena)
    assert contrasena_valida("abc12345") is True
    assert contrasena_valida("abcdefgh") is False
    assert contrasena_valida("abc1")     is False

    def categoria_temperatura(grados):
        if grados < 10:
            return "frio"
        elif grados <= 25:
            return "templado"
        else:
            return "calor"
    assert categoria_temperatura(5)  == "frio"
    assert categoria_temperatura(10) == "templado"
    assert categoria_temperatura(25) == "templado"
    assert categoria_temperatura(30) == "calor"

    def es_bisiesto(anio):
        return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)
    assert es_bisiesto(2024) is True
    assert es_bisiesto(1900) is False
    assert es_bisiesto(2000) is True
    assert es_bisiesto(2023) is False
    assert es_bisiesto(2100) is False

    def calcular_descuento(monto):
        if monto > 500000:
            return 0.15
        elif monto > 200000:
            return 0.08
        else:
            return 0.0
    assert calcular_descuento(600000) == 0.15
    assert calcular_descuento(300000) == 0.08
    assert calcular_descuento(100000) == 0.0
    assert calcular_descuento(500000) == 0.08

    def paridad_suma(a, b):
        return "par" if (a + b) % 2 == 0 else "impar"
    assert paridad_suma(3, 5) == "par"
    assert paridad_suma(2, 3) == "impar"
    assert paridad_suma(0, 0) == "par"

    def interpretar_imc(peso_kg, altura_m):
        imc = round(peso_kg / (altura_m ** 2), 1)
        if imc < 18.5:
            cat = "bajo peso"
        elif imc < 25:
            cat = "normal"
        elif imc < 30:
            cat = "sobrepeso"
        else:
            cat = "obesidad"
        return (imc, cat)
    assert interpretar_imc(70, 1.75) == (22.9, "normal")
    assert interpretar_imc(50, 1.70)[1] == "bajo peso"
    assert interpretar_imc(90, 1.70)[1] == "sobrepeso"
    assert interpretar_imc(110, 1.70)[1] == "obesidad"

    def convertir_celsius(grados_c):
        return (round(grados_c * (9 / 5) + 32, 2), round(grados_c + 273.15, 2))
    assert convertir_celsius(0)   == (32.0, 273.15)
    assert convertir_celsius(100) == (212.0, 373.15)
    assert convertir_celsius(-40)[0] == -40.0

    def convertir_moneda(precio_cop, tasa_usd, tasa_eur):
        if tasa_usd <= 0 or tasa_eur <= 0:
            return (None, None)
        return (round(precio_cop / tasa_usd, 2), round(precio_cop / tasa_eur, 2))
    assert convertir_moneda(420000, 4200.0, 4600.0) == (100.0, 91.3)
    assert convertir_moneda(100000, 0, 4600.0) == (None, None)

    print("✔ Todas las soluciones de referencia de practice01 pasan sus pruebas.")

_validar()


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase02", "practice01.ipynb")
build(os.path.abspath(ruta), C)
