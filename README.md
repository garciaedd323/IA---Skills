# IA-skills

> Bitácora de aprendizaje personal sobre inteligencia artificial — empezando por las Skills de Claude/Anthropic, y creciendo hacia donde el aprendizaje lo lleve. Este repo documenta mi propio proceso de entender cómo funciona esto por dentro, con la intención de que en algún momento le sirva a alguien más que esté empezando lo mismo.

---

## 📌 ¿Qué es esto?

Este repositorio recopila notas, ejemplos y ejercicios sobre inteligencia artificial aplicada — no es documentación oficial de Anthropic, es mi propio camino de aprendizaje, escrito a medida que voy entendiendo cada pieza y **verificando en la práctica** lo que voy documentando. Empieza con las **Skills** (cómo se construyen, dónde se colocan, cómo se activan), y se irá ampliando según hacia dónde vaya profundizando.

> 📌 Este repo se construye de forma incremental — no está "terminado" ni pretende serlo. Si algo está incompleto o marcado como pendiente, es porque genuinamente todavía no llegué ahí en mi propio aprendizaje.

---

## 🗂 Estructura del repositorio

```
IA-skills/
├── README.md
├── skills/
│   ├── notas/          ← conceptos, cómo funcionan, dónde se colocan
│   ├── ejemplos/        ← Skills reales de ejemplo, listas para copiar
│   └── ejercicios/      ← retos prácticos para crear Skills propias
└── docs/                ← para cuando el repo crezca más allá de Skills
```

---

## 📖 Contenido disponible

### `skills/notas/`

- [¿Qué son las Skills de una IA?](./skills/notas/que-son-las-skills.md) — qué es un `SKILL.md`, por qué el `description` es la parte más importante (es el mecanismo de activación), el sistema de carga progresiva en 3 niveles, qué va en `scripts/`/`references/`/`assets/`, y el "principio de no sorpresa". Incluye analogías cotidianas (manual de procedimientos de un oficio, índice de biblioteca) y ejemplo real de funcionamiento.

- [Cómo crear una Skill propia, paso a paso](./skills/notas/como-crear-una-skill.md) — proceso completo en 6 pasos: confirmar que hace falta una Skill, capturar la intención, investigar casos límite, escribir el `SKILL.md` (con la clave de un `description` "insistente"), decidir recursos empaquetados, probar con prompts reales, e iterar. Incluye tabla de errores comunes.

- [Dónde colocar una Skill para que Claude Code la detecte](./skills/notas/donde-colocar-una-skill.md) — 🟢 **Verificado en la práctica.** Las dos rutas posibles (`.claude/skills/` por proyecto vs `~/.claude/skills/` global), el error más común (anidar un nivel de más), el "costo idle" de ~100 tokens por skill al iniciar sesión, detección de cambios en caliente (con la excepción del primer `skills/`), y la confirmación real de una Skill cargando correctamente en Claude Code.

- [Tool vs Skill: dos formas distintas de darle capacidades a una IA](./skills/notas/tool-vs-skill.md) — la diferencia entre una función invocable con esquema fijo (Tool) y conocimiento procedimental que el modelo lee y aplica con criterio (Skill), el flujo real de cómo trabajan juntas (registro → disparo → carga → aplicación → combinación), por qué una Skill depende de Tools básicas para funcionar (lectura de archivos, ejecución de código), y cómo se vería armar este mecanismo desde cero fuera de Claude Code. Incluye analogías cotidianas (teléfono con número específico vs manual de un abogado experto).

- [Skills vs MCP vs Subagentes vs Slash Commands](./skills/notas/skills-vs-mcp-vs-subagentes.md) — los cuatro mecanismos que le dan capacidades a Claude, comparados directamente: MCP (acceso a sistemas externos), Skill (criterio/conocimiento aplicado automáticamente), Subagente (tarea grande resuelta en contexto aislado), y Slash command (atajo disparado manualmente). Incluye un árbol de decisión simple para elegir cuál usar, y la conexión explícita con un repo de investigación de MCP.

- [Cómo escribir buenas instrucciones dentro de una Skill: grados de libertad](./skills/notas/grados-de-libertad.md) — cuánta rigidez darle al modelo según qué tan determinista es la tarea (baja libertad con instrucciones exactas o scripts, alta libertad con principios y ejemplos), por qué el exceso de SIEMPRE/NUNCA en mayúsculas es una señal de alerta, cuándo algo debería ser un script en vez de texto, y cómo cambia el criterio de evaluación entre tareas objetivas y subjetivas. Incluye el ejemplo aplicado a la propia Skill `nota-tecnica-con-analogias` ya construida.

- [Skills sueltas vs Skills empaquetadas en un plugin](./skills/notas/skills-como-plugin.md) — qué es técnicamente un plugin de Claude Code (`.claude-plugin/plugin.json` + `skills/`/`agents/`/`commands/`/`hooks/`/`.mcp.json`), cómo se distribuye vía marketplace, el namespacing `plugin:skill` que resuelve la colisión de nombre (no la semántica) entre Skills, la diferencia de ciclo de vida frente a una Skill suelta, y el prefijo "primo" por carpeta de proyecto que no hay que confundir con este. Incluye nota explícita de qué queda pendiente de verificar en la práctica.

- [Cómo distribuir un marketplace de plugins entre computadoras distintas](./skills/notas/distribuir-marketplace-entre-pcs.md) — por qué una ruta local al marketplace solo sirve dentro de la misma máquina, el flujo real con dos personas separadas (crear el repo de git, publicarlo en GitHub, y del otro lado `/plugin marketplace add` + `/plugin install`), el requisito de que `marketplace.json` viva en la raíz del repositorio publicado (y por qué eso vuelve al taller `taller-marketplace/` de este repo no instalable tal cual desde otra computadora), la variante con repositorio privado, y la alternativa sin git vía `.zip` + `--plugin-dir`.

- [Seguridad y confianza al instalar Skills de terceros](./skills/notas/seguridad-instalar-skills-de-terceros.md) — por qué no hay sandboxing por defecto (los plugins corren con los mismos privilegios del usuario), los tres niveles reales de confianza (oficial, comunidad con screening automático, y cualquier otro sin revisión alguna), qué se puede inspeccionar antes de instalar vía el panel `/plugin` y su limitación en marketplaces locales, la revisión manual de `allowed-tools` como acción concreta recomendada, y el vector menos obvio de la inyección de contexto dinámico (`!comando`). Cierra explicando que ni los propios talleres de este repo quedan exentos de esta misma revisión.

- [Cómo evaluar rigurosamente si una Skill funciona bien](./skills/notas/evaluar-una-skill-rigurosamente.md) — la metodología real que usa `skill-creator`, la skill oficial de Anthropic: las dos preguntas separadas (tasa de activación vs calidad del output), el conjunto de 20 queries con near-misses diseñados a propósito, el split entrenamiento/prueba 60/40 para evitar sobreajuste, la comparación con-skill-vs-sin-skill, la diferencia entre assertions objetivas y juicio humano cualitativo (conectada con `nota-tecnica-con-analogias` como caso subjetivo real), y el análisis de varianza con media y desviación estándar. Cierra reconociendo que esta skill de ejemplo del repo nunca fue evaluada con este rigor todavía.

- [Qué pasa cuando dos Skills se superponen en su `description`](./skills/notas/colision-semantica-de-description.md) — el contraste entre colisión de nombre (con reglas deterministas documentadas) y colisión semántica (sin ninguna regla de resolución en tiempo real), con un ejemplo real de este mismo ecosistema (`generador-mensaje-commit` de este repo vs `commit-commands` del marketplace oficial de Anthropic), las mitigaciones preventivas que sí existen (`disable-model-invocation`, `paths`, líneas de desambiguación, trigger-rate testing entre las dos skills), y la verdad incómoda de que ninguna resuelve el conflicto en el momento en que realmente ocurre.

- [Cómo versionar una Skill en el tiempo sin romper lo que ya funcionaba](./skills/notas/versionar-una-skill-en-el-tiempo.md) — el hallazgo central, verificado contra el estándar oficial Agent Skills: no existe versionado integrado para una skill suelta (los cambios aplican de inmediato, sin staging ni rollback), en contraste con el `version` real y el mecanismo de `renames` que sí tienen los plugins. Cubre el riesgo poco obvio de que dos versiones de una misma skill convivan en la misma sesión tras editarla en caliente, la práctica de `skill-snapshot/` de `skill-creator`, y por qué git — el propio hábito de este repositorio — termina siendo la única estrategia de versionado real disponible.

### `skills/ejemplos/`

- **`nota-tecnica-con-analogias/`** — Skill completa y funcional (probada en producción), que genera notas técnicas siguiendo el mismo estilo usado en este repo (analogía general, secciones numeradas con analogías, tabla resumen, cierre de "por qué importa"). Incluye `SKILL.md` y una plantilla en blanco (`assets/plantilla-nota.md`) lista para copiar a cualquier proyecto en `.claude/skills/`.

### `skills/ejercicios/`

- **[`01-skill-como-plugin/`](./skills/ejercicios/01-skill-como-plugin/GUIA.md)** — Taller desde cero, archivo por archivo y línea por línea, con analogías: crea la carpeta del plugin, el manifiesto `plugin.json`, la skill `SKILL.md`, la prueba local con `--plugin-dir`, y (opcional) el `marketplace.json` para distribuirlo, explicando qué hace cada línea de cada archivo antes de escribirla. Incluye una carpeta `taller-marketplace/` ya resuelta como "solución" para comparar.

- **[`02-skill-con-script/`](./skills/ejercicios/02-skill-con-script/GUIA.md)** — Taller desde cero de una Skill que empaqueta un script real (`scripts/revisar_skill.py`, en Python) que Claude ejecuta en vez de solo leer, explicado función por función. Cubre el campo `allowed-tools` con `${CLAUDE_SKILL_DIR}` para aprobar ese comando de antemano, y `argument-hint` + `$ARGUMENTS` para pasarle una ruta al invocarla. La skill resultante (`auditor-skill-md/`) audita cualquier `SKILL.md` del repo por frontmatter válido, `description` presente, y límite de 500 líneas. Pendiente de correr en una máquina con Python instalado.

---

## 🗺 Roadmap

- [x] Primera nota: ¿qué son las Skills?
- [x] Cómo crear una Skill propia, paso a paso
- [x] Dónde colocar una Skill en Claude Code (verificado en la práctica)
- [x] Ejemplo real de una Skill sencilla, construida y probada de principio a fin
- [x] Aclarar Tool vs Skill como concepto propio (diferencia entre función invocable y conocimiento procedimental)
- [x] Skills vs MCP vs Subagentes vs Slash Commands
- [ ] Cómo implementar Skills en claude.ai / Claude Cowork (pendiente de confirmar, distinto a Claude Code — puesto en pausa deliberadamente por ahora)
- [x] Ejercicios propios para practicar la creación de Skills (primer taller: skill empaquetada como plugin — pendiente de correr en una instalación real de Claude Code CLI para confirmar en la práctica)
- [x] Cómo distribuir un marketplace de plugins entre computadoras distintas (ruta local vs repositorio de git, requisito de `marketplace.json` en la raíz, alternativa sin git vía `.zip`)
- [x] Qué más puede llevar una Skill además de instrucciones en texto (segundo taller: skill con un script real en `scripts/`, y el resto de campos del frontmatter más allá de `name`/`description` — pendiente de correr en una máquina con Python instalado)
- [x] Cómo escribir buenas instrucciones dentro de una Skill (grados de libertad: rigidez vs criterio según el tipo de tarea)
- [x] Skills sueltas vs Skills empaquetadas en un plugin (namespacing, marketplace, ciclo de vida) — resuelve parcialmente la colisión de nombre, la colisión semántica de `description` sigue abierta
- [x] Seguridad y confianza al instalar/publicar Skills de terceros (retomando el "principio de no sorpresa" — los tres niveles reales de confianza, `allowed-tools` como punto de revisión concreto, y el vector de la inyección de contexto dinámico)
- [x] Cómo evaluar rigurosamente que una Skill funciona bien (más allá de "probé 2-3 prompts" — metodología real de `skill-creator`: trigger rate con near-misses, split train/test, comparación con/sin skill, análisis de varianza)
- [x] Qué pasa cuando dos Skills se superponen en su `description` (colisión semántica sin regla determinista de resolución en tiempo real — nota propia con ejemplo real y mitigaciones preventivas)
- [x] Cómo versionar/mantener una Skill en el tiempo sin romper lo que ya funcionaba (no hay versionado integrado para skills sueltas — verificado contra el estándar oficial; contraste con `version`/`renames` de un plugin; git como estrategia real)
- [ ] _(el resto del repo se irá definiendo a medida que el aprendizaje avance)_

---

📌 *Repositorio en construcción — bitácora personal que se actualiza a medida que aprendo y verifico las cosas en la práctica.*
