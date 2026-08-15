# Skills sueltas vs Skills empaquetadas en un plugin

## La analogía general

Una Skill suelta es como una receta escrita en una hoja que queda en la cocina de una casa (`.claude/skills/`, específica de ese proyecto) o en el recetario personal de quien cocina (`~/.claude/skills/`, disponible en cualquier cocina donde esa persona trabaje). Un **plugin** es, en cambio, un **libro de cocina completo y publicado**: trae varias recetas (Skills), pero también utensilios especializados (subagentes), atajos de menú (slash commands), automatizaciones de cocina (hooks) y hasta contactos con proveedores externos (servidores MCP) — todo empaquetado como una sola unidad que otra persona puede instalar de una vez, en lugar de copiar hoja por hoja.

---

## 1. Qué es técnicamente un plugin

Un plugin de Claude Code es una carpeta con un manifiesto obligatorio, `.claude-plugin/plugin.json` (nombre, versión, descripción, autor), y cualquier combinación de subcarpetas opcionales:

```
mi-plugin/
├── .claude-plugin/
│   └── plugin.json          ← manifiesto obligatorio
├── skills/
│   └── mi-skill/SKILL.md    ← mismo formato que una skill suelta
├── agents/                  ← subagentes
├── commands/                ← slash commands
├── hooks/
│   └── hooks.json           ← automatizaciones
└── .mcp.json                ← servidores MCP
```

La Skill que vive *adentro* de un plugin es exactamente el mismo `SKILL.md` ya conocido — mismo frontmatter, misma lógica de activación por `description`, mismas carpetas opcionales `scripts/`/`references/`/`assets/`. Nada de eso cambia. Lo único que cambia es el **contenedor** que la transporta.

> **Analogía:** una receta dentro de un libro de cocina publicado sigue teniendo los mismos ingredientes y pasos que si estuviera suelta en una hoja — lo que cambia es que ahora viene encuadernada junto con otras recetas, bajo una portada y un índice común.

---

## 2. Cómo se distribuye: el "marketplace"

Una Skill suelta se instala copiando una carpeta a mano, o haciendo `git pull` de un repositorio como este. Un plugin, en cambio, se instala desde un **marketplace**: un repositorio o registro que lista varios plugins disponibles mediante un archivo `marketplace.json`. El flujo típico es agregar ese marketplace como fuente y luego instalar el plugin específico desde ahí.

> **Analogía:** es la diferencia entre imprimir una receta suelta desde un blog de cocina y comprar un libro de una editorial que además avisa cuando sale una edición corregida. El marketplace es la librería; el plugin es el libro con ficha de catálogo propia.

---

## 3. Namespacing por plugin — resuelve una duda pendiente del roadmap

Este mismo repositorio dejó anotada una pregunta sin resolver: qué pasa cuando dos Skills se superponen en su `description`. Los plugins responden, en parte, a una versión de ese problema: cada Skill que llega empaquetada en un plugin queda identificada como `nombre-del-plugin:nombre-de-la-skill`, no solo por su nombre corto.

Evidencia observada en la práctica, dentro de una sesión real de Claude: entre las Skills disponibles aparecían `anthropic-skills:docx`, `anthropic-skills:pdf` y `cowork-plugin-management:create-cowork-plugin`. Dos plugins distintos podrían tener, cada uno, una Skill llamada `docx` sin que colisionen entre sí, porque el identificador completo incluye siempre el plugin de origen.

Importante no confundir esto con una solución completa: el namespacing resuelve la colisión de **nombre**. No resuelve que dos `description` distintos, de dos plugins distintos, describan una intención tan parecida que ambos compitan por activarse ante el mismo pedido del usuario. Esa ambigüedad semántica sigue siendo un problema abierto.

> **Analogía:** es como dos autores distintos que titulan un capítulo "Introducción" en sus propios libros — no hay colisión real porque cada capítulo se referencia como "Introducción, del libro de Fulano" o "Introducción, del libro de Mengano". Pero si un lector busca ayuda y ambas introducciones prometen resolver lo mismo, el nombre distinto no evita la confusión de cuál abrir primero.

---

## 4. Ciclo de vida: unidad atómica vs archivo suelto

| | Skill suelta | Skill de plugin |
|---|---|---|
| Instalación | Copiar la carpeta a mano | Instalar el plugin completo desde un marketplace |
| Actualización | Editar el `SKILL.md` directamente, o `git pull` | Actualizar el plugin entero (no solo esa Skill) |
| Desinstalación | Borrar la carpeta | Desinstalar el plugin completo |
| Qué se lleva consigo | Solo esa Skill | Esa Skill + todo lo demás que traiga el plugin (agents, commands, hooks, MCP) |
| Versionado | Manual, sin mecanismo formal | Versión declarada en `plugin.json` |

> **Analogía:** no se puede arrancar una sola receta de un libro encuadernado sin afectar el resto del libro — se actualiza o se retira la edición completa. Con una hoja suelta, en cambio, se cambia solo esa hoja sin tocar nada más.

---

## 5. Lo que no cambia

El costo idle de aproximadamente 100 tokens por Skill al iniciar sesión, ya documentado en [Dónde colocar una Skill](./donde-colocar-una-skill.md), aplica exactamente igual para una Skill empaquetada en un plugin. Venir empaquetada dentro de un libro no la vuelve gratis de tener en el estante. Tampoco cambia la carga progresiva en 3 niveles: metadata siempre visible, cuerpo del `SKILL.md` solo al activarse, recursos empaquetados solo si el cuerpo los pide.

> **Analogía:** que una receta venga dentro de un libro publicado no significa que ocupe menos espacio en la cocina que la misma receta en una hoja suelta — el espacio que ocupa el título en el índice es el mismo, esté donde esté.

---

## 6. Un mecanismo primo, pero distinto — para no confundirlo

Existe otro tipo de prefijo, que se ve parecido pero resuelve un problema distinto: cuando una Skill con el mismo nombre corto existe tanto a nivel de proyecto como a nivel global, se referencia con el prefijo de su carpeta (por ejemplo, `apps/web:deploy`). Ese prefijo namespacea por **origen físico** — de qué carpeta viene, proyecto o global — tal como ya se documentó en [Dónde colocar una Skill](./donde-colocar-una-skill.md). El prefijo `plugin:skill`, en cambio, namespacea por **plugin de origen** — de qué paquete distribuido viene. Son dos mecanismos de desambiguación separados que conviene no mezclar solo porque ambos usan la misma sintaxis con dos puntos.

> **Analogía:** es la diferencia entre identificar un documento por el cajón físico donde está guardado y identificarlo por la editorial que lo publicó. Ambos datos desambiguan, pero responden preguntas distintas.

---

## 7. Cuándo conviene cada modelo

- **Skill suelta:** mientras se está desarrollando o iterando en solitario, o cuando es específica de un solo repositorio — como el caso de `nota-tecnica-con-analogias` en este mismo repositorio, que tiene sentido mientras siga siendo una herramienta personal en construcción.
- **Plugin:** cuando se quiere distribuir la Skill junto con subagentes, comandos o conexiones MCP que la acompañan como un flujo coherente, o cuando se busca poder instalar y desinstalar todo ese conjunto como una sola pieza, con versión propia.

Esto conecta directo con la comparación ya hecha en [Skills vs MCP vs Subagentes vs Slash Commands](./skills-vs-mcp-vs-subagentes.md): un plugin no es un quinto mecanismo nuevo, es una forma de **empaquetar varios de esos cuatro mecanismos juntos** para distribuirlos como unidad.

---

## 8. Pendiente de verificar en la práctica

A diferencia de [Dónde colocar una Skill](./donde-colocar-una-skill.md), que está verificado en la práctica, este tema queda por ahora sin esa marca. No hay certeza total sobre el comando exacto ni la ubicación local del caché de plugins instalados en una instalación estándar de Claude Code CLI. Lo único comprobado hasta ahora es que, en un entorno particular revisado, no existía ninguna carpeta local de tipo `~/.claude/plugins` visible en el sistema de archivos — lo que sugiere que, al menos en ese entorno, las Skills de plugin se resuelven del lado de la plataforma, no desde una carpeta física local como sucede con las Skills sueltas. Falta instalar un plugin real desde un marketplace, en una instalación local de Claude Code, y observar dónde queda físicamente antes de marcar esto como verificado.

---

## Tabla resumen

| Concepto | Skill suelta | Skill de plugin |
|---|---|---|
| Contenedor | Carpeta individual | Plugin (paquete con manifiesto propio) |
| Distribución | Copiar carpeta / `git pull` | Marketplace + instalación con versión |
| Identificador | Nombre corto | `plugin:nombre-corto` |
| Actualización | Independiente, manual | Atada al plugin completo |
| Costo idle | ~100 tokens por Skill | Igual, sin descuento por venir empaquetada |
| Resuelve colisión de nombre | No | Sí, mediante el namespace del plugin |
| Resuelve colisión semántica de `description` | No | No (sigue abierto) |

---

## Por qué esto importa

Entender esta distinción evita dos errores simétricos: tratar un plugin como "una Skill más" cuando en realidad es una unidad que arrastra consigo agents, commands y hooks completos al actualizarse o desinstalarse; y, al revés, subestimar una Skill suelta pensando que necesita "convertirse en plugin" para ser tomada en serio, cuando muchas veces el formato suelto es exactamente el correcto mientras algo sigue en desarrollo personal. Esta distinción también deja más clara la pregunta pendiente sobre seguridad al instalar Skills de terceros: instalar un plugin de un marketplace desconocido no es solo confiar en una Skill, es confiar en todo lo que ese paquete trae consigo de una sola vez.
