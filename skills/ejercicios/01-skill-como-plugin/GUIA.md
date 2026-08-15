# Taller práctico: construir una Skill empaquetada como plugin, desde cero

> Esta guía asume que no se sabe nada todavía. Cada paso crea un archivo nuevo, explica qué contiene línea por línea, y por qué esa línea existe — con una analogía cotidiana antes del detalle técnico, siguiendo el mismo estilo que el resto de este repositorio.
>
> Ya existe una copia completa y funcional de lo que se va a construir en la carpeta [`taller-marketplace/`](./taller-marketplace/) — no es necesario abrirla para seguir esta guía, pero sirve como "solución" para comparar si algo no coincide.

---

## La analogía general de todo el taller

Construir una Skill empaquetada en un plugin es como armar, desde cero, un pequeño libro de cocina de una sola receta:

1. Primero se necesita una **carpeta** para el libro — el lugar físico donde va a vivir.
2. Adentro va la **portada** — un archivo que dice el nombre del libro y de qué trata (`plugin.json`).
3. Adentro también va la **receta en sí** — la página con los pasos a seguir (`SKILL.md`).
4. Recién ahí se puede **abrir el libro y probar la receta** (probarlo en Claude Code).
5. Si más adelante se quiere que otras personas también tengan ese libro, se necesita un **catálogo de biblioteca** que diga dónde encontrarlo (`marketplace.json`).

Cada paso de esta guía construye una de esas piezas, en ese orden.

---

## Antes de empezar

Se necesita tener Claude Code instalado en la computadora (no alcanza con este entorno de chat — los comandos de esta guía se corren en una terminal real, fuera de esta conversación). Todo lo demás se explica sobre la marcha.

---

## Paso 1 — Crear la carpeta del plugin

Un plugin es, ante todo, **una carpeta**. No existe ningún comando especial para "crear un plugin" — se crea la carpeta a mano, como cualquier otra.

```bash
mkdir mi-plugin-practica
```

> **Analogía:** este es el paso de conseguir la carpeta física vacía donde va a vivir el libro de cocina. Todavía no tiene nada adentro — es solo el contenedor.

---

## Paso 2 — Crear el manifiesto (`plugin.json`)

El manifiesto es el archivo que le dice a Claude Code "esto de aquí es un plugin, y así se llama". Vive en una subcarpeta especial llamada `.claude-plugin/` — ese nombre exacto, con el punto adelante, no es opcional.

```bash
mkdir mi-plugin-practica/.claude-plugin
```

Ahora, adentro de esa carpeta, se crea el archivo `plugin.json` con este contenido exacto:

```json
{
  "name": "mi-plugin-practica",
  "description": "Plugin de practica para aprender a empaquetar una skill",
  "version": "0.1.0"
}
```

### Qué hace cada línea

| Línea | Qué significa | Obligatorio |
|---|---|---|
| `"name"` | El identificador único del plugin. Este valor es el que va a aparecer como prefijo de la skill más adelante (`mi-plugin-practica:algo`) | Sí |
| `"description"` | Una frase corta que describe qué hace el plugin. Se muestra cuando alguien lo está buscando para instalar | Sí |
| `"version"` | Un número de versión. Sirve para que, si el plugin se distribuye, la gente sepa cuándo hay una actualización | No — se puede omitir, pero conviene tenerlo desde el principio |

> **Analogía:** este archivo es la portada y la ficha del libro — el título, un resumen de una línea, y la edición ("versión 0.1.0", como diría "primera edición, borrador"). Nadie necesita abrir el libro entero para saber de qué trata: alcanza con leer la portada.

En este punto, la carpeta se ve así:

```
mi-plugin-practica/
└── .claude-plugin/
    └── plugin.json
```

---

## Paso 3 — Crear la skill (`SKILL.md`)

Este es el contenido real: la receta. Las skills de un plugin viven en una carpeta llamada `skills/`, y cada skill tiene su propia subcarpeta.

```bash
mkdir -p mi-plugin-practica/skills/generador-mensaje-commit
```

El nombre de esa subcarpeta (`generador-mensaje-commit`) es importante: **ese nombre de carpeta es el nombre de la skill**. No hace falta repetirlo dentro del archivo.

Ahora se crea el archivo `SKILL.md` adentro de esa carpeta:

```markdown
---
description: Genera un mensaje de commit en espanol, en minuscula y en modo imperativo, a partir de los cambios que el usuario describe. Usar esta skill cuando el usuario pida ayuda para escribir el mensaje de un commit de git.
---

# Generador de mensaje de commit

Cuando el usuario describa los cambios que acaba de hacer y pida ayuda con el mensaje del commit:

1. Resumir el cambio en una sola linea, en espanol, en minuscula, en modo imperativo (por ejemplo "agregar", "corregir", "actualizar"), sin punto final.
2. Si el cambio tiene mas de un aspecto relevante, agregar un cuerpo de una o dos lineas debajo del titulo.
3. No inventar detalles que el usuario no haya mencionado.
```

### Qué hace cada parte

| Parte | Qué significa |
|---|---|
| Las líneas entre `---` y `---` (arriba de todo) | Se llama **frontmatter** — es la ficha técnica de la skill, escrita en un formato llamado YAML |
| `description:` dentro del frontmatter | Lo más importante de todo el archivo. Claude decide **cuándo usar esta skill** leyendo esta línea. Si es vaga, la skill existe pero nunca se activa cuando debería |
| El nombre de la carpeta (`generador-mensaje-commit`) | Funciona como el nombre de la skill — no se declara con un campo `name` adentro del archivo |
| Todo lo que va después del segundo `---` | Las instrucciones reales, en Markdown normal, que Claude sigue cuando la skill se activa |

> **Analogía:** el frontmatter es la ficha de préstamo pegada afuera de la carpeta del expediente — dice de qué se trata sin tener que abrir la carpeta. El `description` en particular es el índice de la biblioteca: si no dice claramente "usar esto cuando pase X", el bibliotecario (Claude) nunca va a saber cuándo ir a buscarlo. El cuerpo de abajo, en cambio, es el contenido real del expediente — los pasos que se siguen una vez que ya se decidió abrirlo.

En este punto, la carpeta completa se ve así:

```
mi-plugin-practica/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── generador-mensaje-commit/
        └── SKILL.md
```

Esto ya es un plugin completo y funcional — con una sola skill adentro. No hace falta nada más para probarlo.

---

## Paso 4 — Probar el plugin (sin necesidad de distribuirlo todavía)

Desde la terminal, parado en la carpeta que **contiene** a `mi-plugin-practica` (no adentro de ella):

```bash
claude --plugin-dir ./mi-plugin-practica
```

Esto abre una sesión de Claude Code cargando ese plugin directamente desde la carpeta local, sin instalarlo en ningún lado.

Adentro de esa sesión:

```
/help
```

y revisar la pestaña **Custom commands** — debería aparecer `mi-plugin-practica:generador-mensaje-commit`. Ese nombre con dos puntos (`:`) es la confirmación de que el plugin cargó bien: `nombre-del-plugin:nombre-de-la-skill`.

Después, probarla con un pedido real:

> "Acabo de agregar un ejercicio nuevo al repo sobre plugins, ayudame con el mensaje de commit"

Si todo salió bien, la respuesta debería llegar en el formato que se definió en el `SKILL.md`: una línea en minúscula, en imperativo, sin punto final.

Si se edita el `SKILL.md` mientras la sesión sigue abierta, se corre `/reload-plugins` para que el cambio se refleje sin reiniciar.

- [ ] 🧪 Pendiente de correr en una instalación real de Claude Code CLI.

> **Analogía:** este paso es como probar la receta en la propia cocina antes de publicar el libro — se cocina una sola vez, en casa, para confirmar que funciona, sin necesidad de imprimir y distribuir nada todavía.

---

## Paso 5 (opcional) — Empaquetar el plugin para que otros lo puedan instalar

Todo lo anterior alcanza para uso personal. Este paso es solo necesario si se quiere que **otra persona** pueda instalar el plugin con un comando, en vez de copiar la carpeta a mano.

Para eso se necesita un **marketplace**: un catálogo que dice dónde está cada plugin disponible.

### 5.1 — Crear la carpeta del marketplace

El marketplace es, otra vez, una carpeta — pero distinta de la del plugin. Por convención, adentro tiene una subcarpeta `plugins/` donde vive (una copia o el original de) cada plugin que ofrece.

```bash
mkdir -p mi-marketplace-practica/.claude-plugin
mkdir -p mi-marketplace-practica/plugins
```

Y se mueve (o copia) el plugin ya armado adentro:

```bash
cp -r mi-plugin-practica mi-marketplace-practica/plugins/mi-plugin-practica
```

### 5.2 — Crear el catálogo (`marketplace.json`)

Adentro de `mi-marketplace-practica/.claude-plugin/`, se crea `marketplace.json`:

```json
{
  "name": "mi-marketplace-practica",
  "owner": {
    "name": "Tu nombre"
  },
  "plugins": [
    {
      "name": "mi-plugin-practica",
      "source": "./plugins/mi-plugin-practica",
      "description": "Plugin de practica para aprender a empaquetar una skill"
    }
  ]
}
```

### Qué hace cada línea

| Línea | Qué significa | Obligatorio |
|---|---|---|
| `"name"` (la de arriba, del marketplace) | El identificador del catálogo completo. Es el nombre que se usa al instalar (`plugin@este-nombre`) | Sí |
| `"owner"` → `"name"` | Quién mantiene este marketplace | Sí |
| `"plugins"` | La lista de plugins que ofrece este catálogo — puede tener uno o varios | Sí |
| `"name"` (la de adentro de cada plugin) | El identificador de ese plugin específico dentro del catálogo | Sí |
| `"source"` | Dónde encontrar los archivos reales del plugin. Acá es una ruta relativa (`./plugins/...`) porque vive en la misma carpeta del marketplace — también puede apuntar a un repositorio de GitHub, una URL, o un paquete de npm | Sí |
| `"description"` (la de adentro de cada plugin) | Descripción de ese plugin puntual, para cuando alguien está buscando en el catálogo | No |

> **Analogía:** si `plugin.json` era la ficha de un libro, `marketplace.json` es el catálogo entero de la biblioteca — la lista de todos los libros disponibles y en qué estante físico está cada uno (`source`). El nombre del marketplace es el nombre de la biblioteca misma; el nombre de cada plugin adentro es el título de cada libro puntual que esa biblioteca ofrece.

En este punto, la estructura completa se ve así:

```
mi-marketplace-practica/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── mi-plugin-practica/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            └── generador-mensaje-commit/
                └── SKILL.md
```

---

## Paso 6 (opcional) — Instalar el plugin desde el marketplace

Desde la terminal, parado en la carpeta que contiene a `mi-marketplace-practica`, abrir Claude Code normalmente (sin `--plugin-dir` esta vez):

```bash
claude
```

Adentro de la sesión, agregar el marketplace:

```
/plugin marketplace add ./mi-marketplace-practica
```

Después, instalar el plugin desde ese marketplace:

```
/plugin install mi-plugin-practica@mi-marketplace-practica
```

Si el resumen de instalación dice `Run /reload-plugins to activate.`, correr ese comando. Después, probar la skill igual que en el Paso 4.

- [ ] 🧪 Pendiente de correr en una instalación real de Claude Code CLI.

> **Analogía:** esto es lo que hace alguien que nunca vio la receta antes — no copia la carpeta a mano, sino que "pide" el libro al catálogo de la biblioteca (`/plugin marketplace add`) y después lo "retira" (`/plugin install`). Es el mismo contenido que en el Paso 4, pero llegando por el camino que usaría cualquier otra persona, no quien lo escribió.

---

## Resumen de qué archivo hace qué

| Archivo | Dónde vive | Su función | Analogía |
|---|---|---|---|
| `plugin.json` | `<plugin>/.claude-plugin/` | Identifica el plugin: nombre, descripción, versión | La portada del libro |
| `SKILL.md` | `<plugin>/skills/<nombre-skill>/` | Define qué hace la skill y cuándo activarse | La receta en sí, con su ficha de catálogo (`description`) pegada arriba |
| `marketplace.json` | `<marketplace>/.claude-plugin/` | Lista qué plugins ofrece el catálogo y dónde encontrarlos | El catálogo completo de la biblioteca |

---

## Si algo no coincide

La carpeta [`taller-marketplace/`](./taller-marketplace/) de este mismo ejercicio ya tiene la versión terminada de todo esto (con el mismo plugin, ya armado). Sirve para comparar archivo por archivo si algo en el propio intento no funciona como se esperaba.

---

## Por qué esto importa

Entender el orden exacto — primero la carpeta, después el manifiesto, después la skill, y solo al final (si hace falta) el marketplace — evita el error más común de empezar por el lugar equivocado: escribir el `marketplace.json` sin tener todavía un plugin real que catalogar, o mezclar las carpetas `skills/`, `agents/` y `hooks/` dentro de `.claude-plugin/` cuando en realidad solo `plugin.json` va ahí. Una vez que este flujo queda claro con un ejemplo mínimo como este, agregar más piezas a un plugin (agentes, hooks, conexiones MCP) es repetir el mismo patrón con una carpeta más, no aprender algo nuevo desde cero.
