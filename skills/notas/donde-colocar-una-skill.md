# Dónde colocar una Skill para que Claude Code la detecte

> Esta nota es específica de **Claude Code** — la ubicación y el mecanismo de detección son distintos en claude.ai o Claude Cowork. Información verificada de forma práctica, no solo teórica.

## La analogía general

Ya vimos que una Skill es como el manual de procedimientos de un oficio. Pero un manual guardado en el cajón equivocado no le sirve a nadie — tiene que estar **en el lugar exacto donde el empleado nuevo sabe que debe buscarlo el primer día**. Claude Code solo revisa dos "cajones" específicos al llegar a trabajar: uno para el proyecto en el que estás, y otro para ti como persona, sin importar en qué proyecto estés.

---

## 1. Las dos ubicaciones posibles

| Alcance | Ruta | Cuándo usarla |
|---|---|---|
| **Solo este proyecto** | `.claude/skills/<nombre-skill>/SKILL.md` | Cuando la Skill solo tiene sentido para este repositorio específico (convenciones propias del proyecto, stack particular) |
| **Todos tus proyectos** | `~/.claude/skills/<nombre-skill>/SKILL.md` | Cuando la Skill es genérica y quieres usarla sin importar en qué carpeta/proyecto estés trabajando |

> **Analogía:** la carpeta del proyecto (`.claude/skills/`) es como el manual pegado en la pared **de esa sucursal específica** — solo aplica ahí. La carpeta personal (`~/.claude/skills/`) es como el manual que llevas **en tu propia mochila** a donde quiera que vayas a trabajar, sin importar en qué sucursal estés ese día.

La ruta del proyecto además se busca hacia arriba: Claude Code revisa la carpeta actual y **sube por los directorios padre hasta la raíz**, buscando un `.claude/skills/` en el camino — no hace falta que sea literalmente la carpeta donde escribes el comando, mientras esté en algún punto de esa cadena hacia arriba.

---

## 2. El error más común: anidar un nivel de más

```
# ❌ Incorrecto — un nivel extra de carpeta antes del SKILL.md
.claude/skills/mi-skill/documentacion/SKILL.md

# ✅ Correcto — el SKILL.md va directo dentro de la carpeta de la skill
.claude/skills/mi-skill/SKILL.md
```

> **Analogía:** es como archivar un documento importante **dentro de una carpeta extra sin etiquetar**, adentro del archivero correcto — técnicamente está "en algún lugar del archivero", pero nadie que solo revise la primera capa lo va a encontrar. Claude Code espera el `SKILL.md` exactamente un nivel adentro de la carpeta con el nombre de la skill, ni más profundo ni más superficial.

Los recursos opcionales (`scripts/`, `references/`, `assets/`) sí van anidados **dentro de esa misma carpeta**, junto al `SKILL.md`:

```
.claude/skills/mi-skill/
├── SKILL.md              ← obligatorio, directo aquí
├── scripts/               ← opcional
├── references/            ← opcional
└── assets/                ← opcional
```

---

## 3. Cómo y cuándo se cargan (el "costo idle")

- **Al iniciar una sesión**, Claude Code escanea el frontmatter (`name` + `description`) de **todas** las Skills disponibles en ambas ubicaciones — esto tiene un costo aproximado de ~100 tokens por Skill, sin importar si se va a usar o no en esa sesión.
- El **cuerpo completo del `SKILL.md`** (y sus recursos empaquetados) solo se carga cuando la tarea del usuario coincide con la descripción — la misma carga progresiva que ya se explicó en la nota de "¿Qué son las Skills?".

> **Analogía:** es como pasar lista de todos los manuales disponibles en el estante al abrir la oficina por la mañana (leer solo el lomo de cada uno) — no se lee cada manual completo de principio a fin todos los días, solo se confirma que están ahí y de qué tratan a grandes rasgos.

---

## 4. Detección de cambios en caliente (con una excepción)

Claude Code **vigila** las carpetas de Skills durante la sesión, y detecta cambios sin necesidad de reiniciar — con una excepción importante:

| Situación | ¿Necesita reiniciar? |
|---|---|
| Editar el contenido de una Skill ya existente | No |
| Agregar una Skill nueva dentro de una carpeta `skills/` que ya existía | No |
| Crear la carpeta `skills/` de nivel superior **por primera vez** | **Sí** |

> **Analogía:** es como si el empleado revisara el estante de manuales cada cierto rato durante el día para ver si hay ediciones nuevas en manuales que ya conocía — pero si **el estante en sí nunca había existido** en esa oficina, hace falta que alguien le avise explícitamente "acabamos de instalar un estante nuevo, revísalo" (el reinicio de sesión) para que empiece a mirarlo por primera vez.

---

## 5. Tabla resumen

| Concepto | Detalle confirmado |
|---|---|
| Ruta de proyecto | `.claude/skills/<nombre-skill>/SKILL.md` (busca hacia arriba hasta la raíz) |
| Ruta personal/global | `~/.claude/skills/<nombre-skill>/SKILL.md` |
| Único archivo obligatorio | `SKILL.md`, directo dentro de la carpeta de la skill (sin nivel extra) |
| Carpetas opcionales | `scripts/`, `references/`, `assets/` — anidadas junto al `SKILL.md` |
| Costo idle | ~100 tokens por skill (solo el frontmatter), en cada inicio de sesión |
| Detección en caliente | Sí, salvo la primera vez que se crea la carpeta `skills/` de nivel superior |

---

## 6. Cómo probar que quedó bien colocada

1. Colocar la carpeta de la Skill en la ruta correcta (proyecto o personal).
2. Si es la primera Skill de ese proyecto (primera vez que existe `.claude/skills/`), reiniciar la sesión de Claude Code.
3. Pedir algo que debería activar esa Skill según su `description`.
4. Si el resultado sigue el formato/instrucciones definidas en el `SKILL.md`, la Skill se detectó y se usó correctamente.

### ✅ Verificado en la práctica

Con la skill `nota-tecnica-con-analogias` colocada en `.claude/skills/nota-tecnica-con-analogias/SKILL.md`, el prompt:

> *"Escríbeme una nota sobre los flujos que se realizaron hoy!"*

Disparó automáticamente:

```
Skill(nota-tecnica-con-analogias)
  └ Successfully loaded skill
```

Sin mencionar la palabra "skill" ni el nombre exacto de la skill — exactamente el comportamiento esperado de un `description` bien escrito ("insistente", cubriendo variaciones de cómo alguien lo pediría). Esto confirma de punta a punta: la ubicación (`.claude/skills/`), la estructura (un solo nivel, `SKILL.md` directo adentro), y el mecanismo de activación por `description`, todos funcionando juntos en un caso real.

---

## Por qué esto importa antes de construir más Skills propias

Con la ubicación exacta confirmada, cualquier Skill nueva que se construya (siguiendo el proceso de la nota anterior) puede probarse de inmediato en la práctica, sin quedar atascada en la duda de "¿la escribí bien pero la puse en el lugar equivocado?".
