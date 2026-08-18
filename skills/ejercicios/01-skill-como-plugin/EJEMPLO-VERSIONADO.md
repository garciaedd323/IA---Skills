# Ejemplo paso a paso: cambiar la versión de una Skill empaquetada en un plugin

> Esta es la contraparte práctica de [Cómo versionar una Skill en el tiempo](../../notas/versionar-una-skill-en-el-tiempo.md). Esa nota explicó que una skill suelta no tiene ningún campo de versión real, y que un plugin sí. Este archivo muestra ese mecanismo funcionando de verdad, sobre el mismo plugin ya construido en este taller: [`mi-primer-plugin`](./taller-marketplace/plugins/mi-primer-plugin/).

---

## Paso 0 — Estado inicial (versión `0.1.0`)

Antes del cambio, el plugin tenía esta versión declarada en su manifiesto:

```json
{
  "name": "mi-primer-plugin",
  "description": "Plugin de practica: empaqueta una skill que genera mensajes de commit en espanol, siguiendo el estilo ya usado en este repositorio",
  "version": "0.1.0"
}
```

Y la skill `generador-mensaje-commit` solo sabía generar un resumen simple en minúscula e imperativo — sin ningún soporte para el formato de [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, etc.).

---

## Paso 1 — Decidir el cambio real de comportamiento

Se agrega una instrucción nueva a la skill: si el usuario menciona que el proyecto usa Conventional Commits, la skill debe anteponer el prefijo correspondiente al resumen.

Este es el punto clave antes de tocar ningún número de versión: primero se decide **qué** cambia en el comportamiento, y **después** se decide cómo se refleja eso en la versión — no al revés.

---

## Paso 2 — Editar el `SKILL.md`

**Antes:**

```markdown
1. Resumir el cambio en una sola linea, en espanol, en minuscula, en modo imperativo (por ejemplo "agregar", "corregir", "actualizar", "eliminar"), sin punto final.
2. Si el cambio tiene mas de un aspecto relevante, agregar un cuerpo de una o dos lineas debajo del titulo, separado por una linea en blanco.
3. No inventar detalles que el usuario no haya mencionado explicitamente.
```

**Después:**

```markdown
1. Resumir el cambio en una sola linea, en espanol, en minuscula, en modo imperativo (por ejemplo "agregar", "corregir", "actualizar", "eliminar"), sin punto final.
2. Si el usuario menciona que el proyecto usa Conventional Commits, anteponer el prefijo correspondiente (`feat:`, `fix:`, `docs:`, `refactor:`) antes del resumen en minuscula.
3. Si el cambio tiene mas de un aspecto relevante, agregar un cuerpo de una o dos lineas debajo del titulo, separado por una linea en blanco.
4. No inventar detalles que el usuario no haya mencionado explicitamente.
```

Es un cambio **aditivo**: quien no mencione Conventional Commits sigue recibiendo exactamente el mismo comportamiento de antes. Este detalle importa para el paso siguiente.

---

## Paso 3 — Decidir el número de versión nuevo

`plugin.json` no impone ningún formato de versión — acepta cualquier string. Por convención (la misma que usa npm, la mayoría de los plugins de Claude Code, y prácticamente todo el ecosistema), se usa [versionado semántico](https://semver.org/): `MAJOR.MINOR.PATCH`.

| Parte | Se incrementa cuando... | ¿Aplica a este cambio? |
|---|---|---|
| `MAJOR` | Se rompe compatibilidad — algo que ya funcionaba deja de funcionar igual | No — el comportamiento anterior sigue intacto |
| `MINOR` | Se agrega funcionalidad nueva, sin romper nada existente | **Sí — es exactamente este caso** |
| `PATCH` | Se corrige un error, sin cambiar el comportamiento intencional | No |

Por eso la versión pasa de `0.1.0` a **`0.2.0`** — no a `1.0.0` (no rompe nada) ni a `0.1.1` (no es una corrección, es una capacidad nueva).

---

## Paso 4 — Editar el `plugin.json`

**Antes:**

```json
{
  "name": "mi-primer-plugin",
  "description": "Plugin de practica: empaqueta una skill que genera mensajes de commit en espanol, siguiendo el estilo ya usado en este repositorio",
  "version": "0.1.0"
}
```

**Después:**

```json
{
  "name": "mi-primer-plugin",
  "description": "Plugin de practica: empaqueta una skill que genera mensajes de commit en espanol, siguiendo el estilo ya usado en este repositorio",
  "version": "0.2.0"
}
```

Un solo carácter cambió (`1` → `2`), pero ese carácter es la totalidad del mecanismo de actualización de un plugin — según ya se documentó en [Cómo distribuir un marketplace entre computadoras distintas](../../notas/distribuir-marketplace-entre-pcs.md), Claude Code resuelve la versión de un plugin leyendo primero este campo.

---

## Paso 5 — Qué pasa del lado de quien ya lo tenía instalado

Alguien que instaló `mi-primer-plugin@taller-marketplace` cuando todavía era la versión `0.1.0` **no recibe este cambio automáticamente** solo porque el archivo cambió en el repositorio. Necesita, según cómo esté configurado ese marketplace:

- Que el auto-update en background esté habilitado para ese marketplace (deshabilitado por defecto para marketplaces de terceros y locales, como ya se documentó en la nota de distribución), o
- Correr manualmente:

  ```
  /plugin marketplace update taller-marketplace
  /plugin update mi-primer-plugin@taller-marketplace
  ```

Recién en ese momento Claude Code compara la versión que tiene cacheada (`0.1.0`) contra la que ahora declara el `plugin.json` (`0.2.0`), ve que son distintas, y descarga la copia nueva.

---

## El error más común: olvidar bumpear la versión

Si el Paso 2 se hiciera solo — editar el `SKILL.md` con el soporte de Conventional Commits, pero **sin** tocar el `version` del Paso 4 — el resultado sería que Claude Code sigue viendo `"version": "0.1.0"` en ambos lados, los considera iguales, y **nadie que ya lo tenía instalado recibe el cambio nunca**, sin ningún error ni aviso. El archivo fuente cambió; lo que la gente tiene instalado, no. Esto es exactamente la advertencia que ya dejó la documentación oficial citada en la nota de versionado: bumpear el campo en cada release, o el cambio queda invisible para quien ya instaló una versión anterior.

---

## Resumen de comandos usados en este ejemplo

| Comando | Para qué |
|---|---|
| `/plugin marketplace update taller-marketplace` | Refresca el catálogo del marketplace para ver la nueva versión declarada |
| `/plugin update mi-primer-plugin@taller-marketplace` | Descarga la nueva versión si el número de versión cambió |

- [ ] 🧪 Pendiente de correr en una instalación real de Claude Code CLI — los archivos de este repositorio ya reflejan el cambio (versión `0.2.0`), pero el comando `/plugin update` en sí no se ejecutó todavía desde una instalación real.
