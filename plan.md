# PRD - Curso de Fundamentos de Programación para Ciencia de Datos

## Objetivo
Diseñar un curso universitario de 8 clases (3 horas c/u), inspirado en la metodología de CS50 (aprendizaje basado en problemas), completamente en español y desarrollado exclusivamente mediante notebooks Jupyter.

## Filosofía
- Enseñar a pensar antes de programar.
- Todo problema sigue la secuencia: contexto → solución intuitiva → algoritmo → pseudocódigo → Python → análisis.
- Cada notebook contiene abundante Markdown (60% explicación, 40% código).
- Evitar "Hello World" y ejercicios triviales.
- Cada clase termina con recapitulación, quiz y retos.
## Estructura del repositorio
```text
curso/
 clase01/
   lecture.ipynb
   practice01.ipynb
   practice02.ipynb
   homework01.ipynb
   homework02.ipynb
 clase02/
   lecture.ipynb
   practice01.ipynb
   practice02.ipynb
   homework01.ipynb
   homework02.ipynb
 clase03/
   lecture.ipynb
   practice01.ipynb
   practice02.ipynb
   homework01.ipynb
   homework02.ipynb
 clase04/
   lecture.ipynb
   practice01.ipynb
   practice02.ipynb
   homework01.ipynb
   homework02.ipynb
 clase05/
   lecture.ipynb
   practice01.ipynb
   practice02.ipynb
   homework01.ipynb
   homework02.ipynb
 clase06/
   lecture.ipynb
   practice01.ipynb
   practice02.ipynb
   homework01.ipynb
   homework02.ipynb
 clase07/
   lecture.ipynb
   practice01.ipynb
   practice02.ipynb
   homework01.ipynb
   homework02.ipynb
 clase08/
   lecture.ipynb
   practice01.ipynb
   practice02.ipynb
   homework01.ipynb
   homework02.ipynb
 assets/
 datasets/
 shared/
```

---

# Estado de implementación

| Clase | Tema | Estado |
|-------|------|--------|
| 1 | Pensamiento algorítmico y pseudocódigo | ✅ **Completa y verificada** |
| 2 | Variables, tipos, operadores, condicionales | ⬜ Pendiente (carpeta creada) |
| 3 | Ciclos, funciones y lambdas | ⬜ Pendiente (carpeta creada) |
| 4 | Estructuras de datos Python | ⬜ Pendiente (carpeta creada) |
| 5 | NumPy | ⬜ Pendiente (carpeta creada) |
| 6 | Pandas | ⬜ Pendiente (carpeta creada) |
| 7 | EDA y transformación | ⬜ Pendiente (carpeta creada) |
| 8 | Proyecto integrador | ⬜ Pendiente (carpeta creada) |

**Hecho hasta ahora**
- Andamiaje del repo: `curso/clase01..08/`, `assets/`, `datasets/`, `shared/`.
- `curso/shared/verificador.py`: utilidad de autocalificación (✅/❌) compartida.
- `curso/datasets/transacciones.csv`: dataset sintético determinista (120 filas).
- Clase 1: `lecture` (81 celdas), `practice01`, `practice02`, `homework01`, `homework02`.
- `curso/README.md` con la estructura y modo de uso.
- Generadores reproducibles en `_build/` (usan `nbformat`).

**Pendiente (clases 2–8)** — por cada clase, replicar los 5 notebooks:
`lecture.ipynb` (80–150 celdas), `practice01.ipynb` (10 ejercicios),
`practice02.ipynb` (caso aplicado a ciencia de datos), `homework01.ipynb`
(8 ejercicios autocalificables) y `homework02.ipynb` (mini proyecto).

---

# Convenciones de implementación (establecidas en la Clase 1)

Decisiones acordadas que **toda clase nueva debe respetar** para mantener
coherencia:

1. **Autocalificación basada en `assert`** (no nbgrader). Imita la idea de
   nbgrader (tests visibles + tests ocultos) sin dependencias extra.
   - **practice01 / practice02:** comprobaciones *suaves* con
     `verificador.revisar(...)` / `Reporte`: imprimen ✅/❌ **sin lanzar
     excepción**, de modo que el notebook corre de principio a fin aunque el
     estudiante no haya resuelto. Las soluciones van **ocultas** en bloques
     `<details>` de Markdown.
   - **homework01 / homework02:** celdas plantilla con
     `raise NotImplementedError`, seguidas de celdas de **tests visibles** y
     **tests adicionales (ocultos)** con `assert`.

2. **Compromiso "ejecutable de principio a fin" vs. tareas para resolver.**
   Una tarea recién abierta **no** corre completa a propósito: las celdas de
   `assert` fallan hasta que el estudiante implementa cada función. Eso es el
   comportamiento correcto de un homework. La *corrección* se garantiza así:
   - Las soluciones de referencia se **validan en tiempo de build** (asserts en
     el script generador).
   - Para verificar ejecución de extremo a extremo, el generador puede emitir una
     copia *resuelta* temporal (fuera de `curso/`) que se ejecuta con `nbclient`.
   - `lecture` y ambos `practice` **sí** se ejecutan completos sin error.

3. **Dependencias del proyecto** (en `pyproject.toml`, vía `uv`):
   `numpy`, `pandas`, `matplotlib`, `ipykernel`. Para generar/ejecutar notebooks
   se usan `nbformat` (dependencia) y `nbclient`/`nbconvert` (solo herramientas de
   build, instaladas en el venv, no en `pyproject`).

4. **Generación reproducible.** Los notebooks **no** se escriben a mano: se
   generan con scripts en `_build/` que usan los helpers `nbtools.py`
   (`md`, `code`, `build`) y `hwtools.py` (tareas autocalificables). Regenerar es
   determinista. Los datasets sintéticos usan semilla fija (`random.seed`).

5. **Utilidades compartidas.** Los notebooks añaden `../shared` al `sys.path` e
   importan desde `verificador.py`. Los datasets viven en `../datasets/`.

6. **Pedagogía y estilo** (además de lo ya descrito en el PRD):
   - Secuencia obligatoria por problema: contexto → solución intuitiva →
     algoritmo → pseudocódigo → Python → análisis.
   - Diagramas ASCII, tablas de trazado, bloques **🤔 ¿Qué pasaría si...?**,
     errores comunes, glosario, quiz con respuestas y retos.
   - Ejemplos originales y contextualizados (negocios, logística, finanzas, vida
     cotidiana). Sin "Hello World".
   - `lecture`: densidad objetivo 80–150 celdas (la Clase 1 quedó en 81).
   - Cada librería/estructura se introduce **justificando por qué existe**; los
     reenvíos a clases futuras (p. ej. `set`, `dict`, pandas) se marcan
     explícitamente.

---

# Clase 1  ✅ (implementada)
## Tema
Pensamiento algorítmico y pseudocódigo

### Objetivos
- Comprensión conceptual.
- Resolver problemas antes de escribir código.
- Analizar eficiencia.
### Agenda (180 min)
- 20 min motivación
- 40 min teoría con ejemplos
- 35 min pseudocódigo
- 45 min implementación
- 20 min ejercicios guiados
- 20 min cierre y quiz

### lecture.ipynb
- 80-150 celdas.
- Alternar Markdown y código.
- Diagramas ASCII.
- Visualización de variables.
- Preguntas de reflexión.
- Errores comunes.
- Resumen.

### practice01.ipynb
10 ejercicios crecientes con solución oculta.

### practice02.ipynb
Caso aplicado a ciencia de datos.

### homework01.ipynb
8 ejercicios autocalificables.

### homework02.ipynb
Mini proyecto autocalificable.

### Problemas sugeridos
- Buscar patrones.
- Diseñar algoritmo.
- Escribir pseudocódigo.
- Implementar.
- Analizar complejidad.


# Clase 2
## Tema
Variables, tipos, operadores, condicionales

### Objetivos
- Comprensión conceptual.
- Resolver problemas antes de escribir código.
- Analizar eficiencia.
### Agenda (180 min)
- 20 min motivación
- 40 min teoría con ejemplos
- 35 min pseudocódigo
- 45 min implementación
- 20 min ejercicios guiados
- 20 min cierre y quiz

### lecture.ipynb
- 80-150 celdas.
- Alternar Markdown y código.
- Diagramas ASCII.
- Visualización de variables.
- Preguntas de reflexión.
- Errores comunes.
- Resumen.

### practice01.ipynb
10 ejercicios crecientes con solución oculta.

### practice02.ipynb
Caso aplicado a ciencia de datos.

### homework01.ipynb
8 ejercicios autocalificables.

### homework02.ipynb
Mini proyecto autocalificable.

### Problemas sugeridos
- Buscar patrones.
- Diseñar algoritmo.
- Escribir pseudocódigo.
- Implementar.
- Analizar complejidad.


# Clase 3
## Tema
Ciclos, funciones y lambdas

### Objetivos
- Comprensión conceptual.
- Resolver problemas antes de escribir código.
- Analizar eficiencia.
### Agenda (180 min)
- 20 min motivación
- 40 min teoría con ejemplos
- 35 min pseudocódigo
- 45 min implementación
- 20 min ejercicios guiados
- 20 min cierre y quiz

### lecture.ipynb
- 80-150 celdas.
- Alternar Markdown y código.
- Diagramas ASCII.
- Visualización de variables.
- Preguntas de reflexión.
- Errores comunes.
- Resumen.

### practice01.ipynb
10 ejercicios crecientes con solución oculta.

### practice02.ipynb
Caso aplicado a ciencia de datos.

### homework01.ipynb
8 ejercicios autocalificables.

### homework02.ipynb
Mini proyecto autocalificable.

### Problemas sugeridos
- Buscar patrones.
- Diseñar algoritmo.
- Escribir pseudocódigo.
- Implementar.
- Analizar complejidad.


# Clase 4
## Tema
Estructuras de datos Python

### Objetivos
- Comprensión conceptual.
- Resolver problemas antes de escribir código.
- Analizar eficiencia.
### Agenda (180 min)
- 20 min motivación
- 40 min teoría con ejemplos
- 35 min pseudocódigo
- 45 min implementación
- 20 min ejercicios guiados
- 20 min cierre y quiz

### lecture.ipynb
- 80-150 celdas.
- Alternar Markdown y código.
- Diagramas ASCII.
- Visualización de variables.
- Preguntas de reflexión.
- Errores comunes.
- Resumen.

### practice01.ipynb
10 ejercicios crecientes con solución oculta.

### practice02.ipynb
Caso aplicado a ciencia de datos.

### homework01.ipynb
8 ejercicios autocalificables.

### homework02.ipynb
Mini proyecto autocalificable.

### Problemas sugeridos
- Buscar patrones.
- Diseñar algoritmo.
- Escribir pseudocódigo.
- Implementar.
- Analizar complejidad.


# Clase 5
## Tema
NumPy

### Objetivos
- Comprensión conceptual.
- Resolver problemas antes de escribir código.
- Analizar eficiencia.
### Agenda (180 min)
- 20 min motivación
- 40 min teoría con ejemplos
- 35 min pseudocódigo
- 45 min implementación
- 20 min ejercicios guiados
- 20 min cierre y quiz

### lecture.ipynb
- 80-150 celdas.
- Alternar Markdown y código.
- Diagramas ASCII.
- Visualización de variables.
- Preguntas de reflexión.
- Errores comunes.
- Resumen.

### practice01.ipynb
10 ejercicios crecientes con solución oculta.

### practice02.ipynb
Caso aplicado a ciencia de datos.

### homework01.ipynb
8 ejercicios autocalificables.

### homework02.ipynb
Mini proyecto autocalificable.

### Problemas sugeridos
- Buscar patrones.
- Diseñar algoritmo.
- Escribir pseudocódigo.
- Implementar.
- Analizar complejidad.


# Clase 6
## Tema
Pandas

### Objetivos
- Comprensión conceptual.
- Resolver problemas antes de escribir código.
- Analizar eficiencia.
### Agenda (180 min)
- 20 min motivación
- 40 min teoría con ejemplos
- 35 min pseudocódigo
- 45 min implementación
- 20 min ejercicios guiados
- 20 min cierre y quiz

### lecture.ipynb
- 80-150 celdas.
- Alternar Markdown y código.
- Diagramas ASCII.
- Visualización de variables.
- Preguntas de reflexión.
- Errores comunes.
- Resumen.

### practice01.ipynb
10 ejercicios crecientes con solución oculta.

### practice02.ipynb
Caso aplicado a ciencia de datos.

### homework01.ipynb
8 ejercicios autocalificables.

### homework02.ipynb
Mini proyecto autocalificable.

### Problemas sugeridos
- Buscar patrones.
- Diseñar algoritmo.
- Escribir pseudocódigo.
- Implementar.
- Analizar complejidad.


# Clase 7
## Tema
EDA y transformación

### Objetivos
- Comprensión conceptual.
- Resolver problemas antes de escribir código.
- Analizar eficiencia.
### Agenda (180 min)
- 20 min motivación
- 40 min teoría con ejemplos
- 35 min pseudocódigo
- 45 min implementación
- 20 min ejercicios guiados
- 20 min cierre y quiz

### lecture.ipynb
- 80-150 celdas.
- Alternar Markdown y código.
- Diagramas ASCII.
- Visualización de variables.
- Preguntas de reflexión.
- Errores comunes.
- Resumen.

### practice01.ipynb
10 ejercicios crecientes con solución oculta.

### practice02.ipynb
Caso aplicado a ciencia de datos.

### homework01.ipynb
8 ejercicios autocalificables.

### homework02.ipynb
Mini proyecto autocalificable.

### Problemas sugeridos
- Buscar patrones.
- Diseñar algoritmo.
- Escribir pseudocódigo.
- Implementar.
- Analizar complejidad.


# Clase 8
## Tema
Proyecto integrador

### Objetivos
- Comprensión conceptual.
- Resolver problemas antes de escribir código.
- Analizar eficiencia.
### Agenda (180 min)
- 20 min motivación
- 40 min teoría con ejemplos
- 35 min pseudocódigo
- 45 min implementación
- 20 min ejercicios guiados
- 20 min cierre y quiz

### lecture.ipynb
- 80-150 celdas.
- Alternar Markdown y código.
- Diagramas ASCII.
- Visualización de variables.
- Preguntas de reflexión.
- Errores comunes.
- Resumen.

### practice01.ipynb
10 ejercicios crecientes con solución oculta.

### practice02.ipynb
Caso aplicado a ciencia de datos.

### homework01.ipynb
8 ejercicios autocalificables.

### homework02.ipynb
Mini proyecto autocalificable.

### Problemas sugeridos
- Buscar patrones.
- Diseñar algoritmo.
- Escribir pseudocódigo.
- Implementar.
- Analizar complejidad.


# Requisitos para notebooks
- Usar Markdown extensivamente.
- Explicar cada bloque de código.
- Incluir tablas, listas y diagramas.
- Nunca introducir una estructura sin justificar por qué existe.
- Todas las funciones deben documentarse.
- Añadir preguntas "¿Qué pasaría si...?"

# Autocalificación
Preferir nbgrader.
Cada tarea:
- Enunciado
- Casos de ejemplo
- Celdas protegidas
- Tests visibles
- Tests ocultos

# Estilo
Inspiración: CS50, pero contenido completamente original.
Tono conversacional, profundo y riguroso.

# Proyecto final
Analizar un dataset real:
1. Carga.
2. Limpieza.
3. Transformación.
4. NumPy.
5. Pandas.
6. Responder preguntas.
7. Conclusiones.
8. Reflexión sobre eficiencia.

# Instrucciones para Claude Code/Codex
Genera todos los notebooks completos.
No dejes secciones vacías.
Incluye datasets sintéticos cuando sea necesario.
Cada notebook debe ser ejecutable de principio a fin.
Prioriza claridad pedagógica sobre brevedad.

- Generar ejemplos originales, contextualizados en problemas reales de negocios, ciencia de datos, logística, finanzas y vida cotidiana; comenzar siempre con lógica, continuar con pseudocódigo y finalizar con implementación comentada.
