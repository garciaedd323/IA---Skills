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

### `skills/ejemplos/`

- **`nota-tecnica-con-analogias/`** — Skill completa y funcional (probada en producción), que genera notas técnicas siguiendo el mismo estilo usado en este repo (analogía general, secciones numeradas con analogías, tabla resumen, cierre de "por qué importa"). Incluye `SKILL.md` y una plantilla en blanco (`assets/plantilla-nota.md`) lista para copiar a cualquier proyecto en `.claude/skills/`.

---

## 🗺 Roadmap

- [x] Primera nota: ¿qué son las Skills?
- [x] Cómo crear una Skill propia, paso a paso
- [x] Dónde colocar una Skill en Claude Code (verificado en la práctica)
- [x] Ejemplo real de una Skill sencilla, construida y probada de principio a fin
- [x] Aclarar Tool vs Skill como concepto propio (diferencia entre función invocable y conocimiento procedimental)
- [x] Skills vs MCP vs Subagentes vs Slash Commands
- [ ] Cómo implementar Skills en claude.ai / Claude Cowork (pendiente de confirmar, distinto a Claude Code — puesto en pausa deliberadamente por ahora)
- [ ] Ejercicios propios para practicar la creación de Skills
- [ ] Cómo escribir buenas instrucciones dentro de una Skill (grados de libertad: rigidez vs criterio según el tipo de tarea)
- [ ] Seguridad y confianza al instalar/publicar Skills de terceros (retomando el "principio de no sorpresa")
- [ ] Cómo evaluar rigurosamente que una Skill funciona bien (más allá de "probé 2-3 prompts")
- [ ] Qué pasa cuando dos Skills se superponen en su `description`
- [ ] Cómo versionar/mantener una Skill en el tiempo sin romper lo que ya funcionaba
- [ ] _(el resto del repo se irá definiendo a medida que el aprendizaje avance)_

---

📌 *Repositorio en construcción — bitácora personal que se actualiza a medida que aprendo y verifico las cosas en la práctica.*
