# Taller práctico: una Skill que incluye un script, desde cero

> Esta guía construye una Skill nueva, distinta de la del taller anterior, para responder una pregunta puntual: ¿qué más puede llevar una Skill además de instrucciones en texto? La respuesta concreta de este taller es un **script real que Claude ejecuta**, no solo lee. Ya existe una copia terminada en [`auditor-skill-md/`](./auditor-skill-md/) — sirve como solución para comparar, no hace falta abrirla para seguir la guía.

---

## La analogía general

Hasta ahora, toda skill de este repositorio fue solo texto: instrucciones que Claude lee y sigue con su propio criterio. Un script adentro de una skill es distinto — es como darle a un asistente, además del manual de procedimientos, **una calculadora ya programada** para un cálculo puntual. El asistente no tiene que "hacer cuentas mentalmente" siguiendo una receta en prosa: aprieta un botón, la calculadora hace exactamente lo mismo todas las veces, y el asistente solo interpreta el resultado. Eso es un script dentro de una skill: la parte determinista y repetible se delega a código real, no a instrucciones que el modelo interpreta cada vez.

---

## Qué se va a construir

Una skill llamada `auditor-skill-md`, que recibe la ruta a un archivo `SKILL.md` cualquiera (por ejemplo, uno de los que ya existen en `skills/notas/` de este mismo repositorio) y reporta:

- si tiene un bloque de frontmatter válido,
- si le falta el campo `description` (el más importante, según ya se documentó en [¿Qué son las Skills de una IA?](../../notas/que-son-las-skills.md)),
- si supera las 500 líneas que la documentación oficial recomienda como máximo para un `SKILL.md`.

---

## Antes de empezar

Se necesita tener Python 3 instalado en la computadora donde se va a probar esto (no en este entorno de chat). Se puede confirmar con:

```bash
python --version
```

---

## Paso 1 — Crear la carpeta de la skill y la carpeta de scripts

```bash
mkdir -p auditor-skill-md/scripts
```

> **Analogía:** `scripts/` es el cajón donde va la calculadora — separado de la carpeta general de la skill, para que quede claro que ahí adentro hay algo que se **ejecuta**, no algo que Claude simplemente lee como si fuera parte de las instrucciones.

---

## Paso 2 — Escribir el script (`scripts/revisar_skill.py`)

El script se escribe en tres partes. Cada una resuelve un problema puntual.

### 2.1 — Separar el frontmatter del resto del archivo

```python
def leer_frontmatter(lineas):
    """Separa el bloque de frontmatter (entre '---' y '---') del resto del archivo."""
    if not lineas or lineas[0].strip() != "---":
        return None, lineas

    fin = None
    for i in range(1, len(lineas)):
        if lineas[i].strip() == "---":
            fin = i
            break

    if fin is None:
        return None, lineas

    return lineas[1:fin], lineas[fin + 1:]
```

Esta función recibe todas las líneas del archivo. Si la primera línea no es `---`, no hay frontmatter y se avisa devolviendo `None`. Si sí empieza con `---`, busca la **segunda** aparición de `---` para saber dónde termina el bloque, y devuelve dos cosas: las líneas de adentro del frontmatter, y todo lo que viene después (el cuerpo de instrucciones).

> **Analogía:** es como separar la ficha de préstamo pegada afuera de una carpeta del resto de los papeles que tiene adentro — primero hay que encontrar dónde termina la ficha para poder leerla aparte del contenido.

### 2.2 — Buscar un campo puntual dentro del frontmatter

```python
def buscar_campo(frontmatter, nombre):
    """Busca un campo simple tipo 'nombre: valor' dentro del frontmatter."""
    for linea in frontmatter:
        if linea.strip().startswith(f"{nombre}:"):
            return linea.split(":", 1)[1].strip()
    return None
```

Recorre las líneas del frontmatter buscando una que empiece con, por ejemplo, `"description:"`, y devuelve lo que hay después de los dos puntos. Si no encuentra nada, devuelve `None`.

### 2.3 — La función principal: leer el archivo, revisar, e informar

```python
def main():
    if len(sys.argv) != 2:
        print("Uso: python revisar_skill.py <ruta-al-SKILL.md>")
        sys.exit(1)

    ruta = Path(sys.argv[1])
    if not ruta.is_file():
        print(f"No se encontro el archivo: {ruta}")
        sys.exit(1)

    lineas = ruta.read_text(encoding="utf-8").splitlines()
    frontmatter, _cuerpo = leer_frontmatter(lineas)

    problemas = []
    avisos = []

    if frontmatter is None:
        problemas.append("No se encontro un bloque de frontmatter valido (debe empezar y terminar con '---').")
    else:
        description = buscar_campo(frontmatter, "description")
        if not description:
            problemas.append("Falta el campo 'description' (o esta vacio) - sin el, Claude no sabe cuando usar esta skill.")
        elif len(description) < 20:
            avisos.append(f"El 'description' es muy corto ({len(description)} caracteres) - puede no alcanzar para que Claude decida activarla.")

    if len(lineas) > LIMITE_LINEAS:
        avisos.append(f"El archivo tiene {len(lineas)} lineas, por encima de las {LIMITE_LINEAS} recomendadas. Conviene mover detalle a archivos de referencia aparte.")

    ...
```

Qué hace cada parte:

| Bloque | Qué revisa |
|---|---|
| `if len(sys.argv) != 2` | Que se haya pasado exactamente una ruta como argumento al correr el script |
| `if not ruta.is_file()` | Que el archivo realmente exista antes de intentar leerlo |
| `leer_frontmatter(lineas)` | Separa frontmatter del cuerpo, usando la función del paso 2.1 |
| `if frontmatter is None` | Si no hay frontmatter en absoluto, es un **problema** (no un aviso menor) |
| `if not description` | Si el frontmatter existe pero no tiene `description`, también es un problema |
| `elif len(description) < 20` | Si tiene `description` pero es muy corta, es solo un **aviso** — no impide que la skill funcione, pero puede activarse peor |
| `if len(lineas) > LIMITE_LINEAS` | Compara contra el límite de 500 líneas recomendado por la documentación oficial |

El resto de la función (`print(...)` y `sys.exit(...)`) simplemente arma el reporte final y usa el código de salida (`0` sin problemas, `1` si hay algo grave) — una convención estándar para que cualquier script de terminal indique si algo salió mal.

> **Analogía:** esto es la lógica de un control de calidad en una línea de producción — algunas fallas paran la línea (`problemas`), otras solo quedan anotadas para revisar después sin detener nada (`avisos`).

El archivo completo ya está armado en [`auditor-skill-md/scripts/revisar_skill.py`](./auditor-skill-md/scripts/revisar_skill.py) para copiar tal cual.

---

## Paso 3 — Escribir el `SKILL.md` que usa el script

```yaml
---
description: Audita un archivo SKILL.md y reporta si tiene frontmatter valido, si falta el campo description, o si supera las 500 lineas recomendadas. Usar esta skill cuando el usuario pida revisar, auditar o validar una skill propia.
argument-hint: [ruta-al-SKILL.md]
allowed-tools: Bash(python ${CLAUDE_SKILL_DIR}/scripts/revisar_skill.py *)
---

# Auditor de SKILL.md

Cuando el usuario pida auditar un archivo `SKILL.md`:

1. Correr `python ${CLAUDE_SKILL_DIR}/scripts/revisar_skill.py $ARGUMENTS`, donde `$ARGUMENTS` es la ruta al archivo que se quiere revisar.
2. Mostrar el resultado del script, explicando en una frase cada problema o aviso que haya encontrado.
3. Si el script no encuentra nada, confirmarlo brevemente sin agregar mas.
```

### Qué hace cada línea nueva (respecto a las skills anteriores de este repo)

| Línea | Qué significa |
|---|---|
| `argument-hint: [ruta-al-SKILL.md]` | Un texto de ayuda que aparece en el autocompletado al escribir `/auditor-skill-md` — no cambia el comportamiento, solo orienta a quien la usa |
| `allowed-tools: Bash(python ${CLAUDE_SKILL_DIR}/scripts/revisar_skill.py *)` | Le da permiso a Claude para correr **exactamente ese comando** sin preguntar cada vez. `${CLAUDE_SKILL_DIR}` se reemplaza automáticamente por la carpeta real donde vive esta skill, sin importar si está instalada en `.claude/skills/` o en `~/.claude/skills/` |
| `$ARGUMENTS` (en el cuerpo) | Lo que la persona escriba después del nombre de la skill se inserta ahí. Por ejemplo, `/auditor-skill-md ./skills/notas/que-son-las-skills.md` hace que `$ARGUMENTS` se convierta en esa ruta |

> **Analogía:** `allowed-tools` es como dejarle una llave al asistente, pero solo para una puerta puntual (correr ese script exacto) — no le está dando acceso a toda la casa, solo a ese cajón con la calculadora del Paso 2.

---

## Paso 4 — Instalar y probar

Se copia la carpeta completa `auditor-skill-md/` a `~/.claude/skills/` (disponible en todos los proyectos) o a `.claude/skills/` de un proyecto puntual:

```bash
cp -r auditor-skill-md ~/.claude/skills/
```

Se abre una sesión de Claude Code en cualquier carpeta:

```bash
claude
```

Y se prueba de dos formas:

**Invocación directa**, pasando la ruta a un `SKILL.md` real como argumento:

```
/auditor-skill-md ./skills/notas/que-son-las-skills.md
```

**Dejar que Claude la active sola**, con un pedido natural:

> "¿Podés auditar el SKILL.md que está en tal ruta?"

En ambos casos, Claude debería correr el script y mostrar el reporte, sin pedir permiso para ejecutar el comando (gracias al `allowed-tools` del Paso 3).

- [ ] 🧪 Pendiente de correr en una instalación real con Python instalado — este entorno de trabajo no tiene Python disponible, así que el script no se pudo ejecutar todavía para confirmarlo en la práctica.

---

## Resumen de qué archivo hace qué

| Archivo | Su función | Analogía |
|---|---|---|
| `scripts/revisar_skill.py` | Hace el trabajo determinista: leer, separar, comparar contra reglas fijas | La calculadora ya programada |
| `SKILL.md` | Le dice a Claude cuándo usar la skill y qué comando correr | El manual que indica cuándo sacar la calculadora del cajón y cómo usarla |
| `allowed-tools` en el frontmatter | Da permiso previo para correr ese comando exacto | La llave de un cajón puntual, no de toda la casa |

---

## Por qué esto importa

Esto muestra la diferencia real entre una skill que es solo texto y una que además ejecuta código: cuando una tarea tiene una regla fija y repetible (¿tiene `description` o no?, ¿supera 500 líneas o no?), conviene resolverla con un script en vez de pedirle al modelo que "cuente las líneas mentalmente" cada vez — es más rápido, y el resultado es exactamente el mismo todas las veces. Esta misma skill, además, es la primera herramienta de este repositorio que podría usarse para revisar las propias notas ya escritas — cerrando, aunque sea parcialmente, el punto pendiente del roadmap sobre "cómo evaluar rigurosamente que una skill funciona bien".
