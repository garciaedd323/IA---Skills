# Skills vs MCP vs Subagentes vs Slash Commands

## La analogía general

Imagina que se dirige una empresa y hay cuatro formas distintas de resolver que se haga un trabajo:

- **Se contrata a un proveedor externo especializado** con su propio equipo y sistemas (MCP) — se le pide algo, él usa sus propias herramientas, y devuelve un resultado.
- **Se le da a un empleado el manual de procedimientos de un oficio** (Skill) — conocimiento que él mismo lee y aplica con su propio criterio.
- **Se delega una tarea completa a un empleado dedicado, en su propia oficina, que solo reporta el resultado final** (Subagente) — no se ve todo lo que hizo en el camino, solo el resumen.
- **Se tiene un botón de acceso rápido para una instrucción que se repite seguido** (Slash command) — un atajo que ya se sabe exactamente qué hace, sin tener que explicarlo cada vez.

Los cuatro le dan capacidades a Claude, pero **resuelven problemas distintos** — y mezclarlos sin entender la diferencia es la fuente más común de confusión.

> ⚠️ Los detalles exactos de Subagentes y Slash commands (sintaxis, ubicación de archivos) pueden variar entre versiones de Claude Code — lo que sigue es el concepto general; conviene verificar el detalle específico vigente en `docs.claude.com` antes de darlo por definitivo, igual que se hizo con la ubicación de las Skills.

---

## 1. Comparación directa

| | MCP | Skill | Subagente | Slash command |
|---|---|---|---|---|
| **Qué es** | Un servidor externo que expone herramientas/datos | Un documento con instrucciones que el modelo lee | Una instancia separada de Claude, con su propio contexto | Un atajo de texto reutilizable |
| **Cómo se activa** | El modelo llama una herramienta que el servidor expone | El modelo detecta que la tarea coincide con el `description` | Se invoca explícitamente para una tarea acotada | El usuario escribe `/nombre-comando` |
| **Dónde vive el "conocimiento"** | En el código del servidor MCP (fuera de Claude) | En el `SKILL.md` (texto, leído por el modelo) | En las instrucciones de configuración del subagente | En el texto del comando guardado |
| **Contexto** | Comparte el contexto de la conversación principal | Comparte el contexto de la conversación principal | Tiene su **propio contexto aislado**, separado del principal | Se inyecta en la conversación principal |
| **Analogía** | Proveedor externo con su propio equipo | Manual de procedimientos que se lee y aplica | Empleado dedicado en su propia oficina | Botón de acceso rápido |

---

## 2. MCP — capacidades que vienen de afuera

Un servidor MCP (`filesystem`, `playwright`, `appium`) le da a Claude acceso a **sistemas externos reales** — un navegador, el sistema de archivos, un dispositivo móvil. El servidor MCP expone "herramientas" con un esquema definido, y Claude las llama cuando las necesita.

> **Analogía:** es literalmente el proveedor externo — tiene su propia infraestructura (el navegador real, el filesystem real), y solo se le pide "haz esto", sin necesitar saber cómo lo hace por dentro.

---

## 3. Skill — conocimiento que Claude lee y aplica

Un `SKILL.md` con instrucciones que el modelo **lee** (no ejecuta como código) y sigue con su propio criterio. No necesita ningún servidor externo — vive como texto dentro del propio proyecto o en la carpeta personal.

> **Diferencia clave con MCP:** MCP da **acceso a algo que no existía antes** (un navegador, un filesystem remoto). Una Skill no da acceso a nada nuevo — da **mejor criterio sobre cómo hacer algo que Claude ya podía intentar hacer de todas formas**, solo que ahora con la experiencia ya documentada de antemano.

---

## 4. Subagente — un empleado dedicado en su propia oficina

Un subagente es una instancia de Claude que se invoca para resolver una tarea acotada, **con su propio contexto separado** del hilo principal de la conversación. Solo devuelve al hilo principal un resumen o resultado final, no todo el proceso interno.

> **Analogía:** es como mandar a un empleado a investigar algo complicado en otra ciudad — no manda un reporte de cada paso que dio en el camino (eso saturaría el propio escritorio de información), solo entrega el informe final ya resuelto. Esto es valioso cuando una tarea requiere mucha exploración "de bajo valor" (leer muchos archivos, probar varias cosas) que no vale la pena que ocupe espacio en la conversación principal.

**Cuándo usar un subagente en vez de una Skill:** cuando la tarea es lo bastante grande o exploratoria como para que valga la pena aislarla en su propio contexto, en vez de solo aplicar un criterio ya conocido (que es lo que resuelve una Skill).

---

## 5. Slash command — el atajo de texto

Un slash command es un fragmento de texto guardado (típicamente un prompt o instrucción reutilizable) que se dispara escribiendo `/nombre-del-comando`, en vez de escribir la instrucción completa cada vez.

> **Analogía:** es el botón de marcado rápido del teléfono — en vez de escribir el número completo cada vez, se aprieta un solo botón que ya tiene todo configurado.

**Diferencia clave con una Skill:** un slash command lo **dispara explícitamente el usuario** (nunca "se activa solo"). Una Skill, en cambio, se activa **automáticamente** cuando el modelo detecta que la tarea coincide con su `description`, sin que el usuario tenga que invocarla por nombre.

---

## 6. Cómo decidir cuál usar (árbol de decisión simple)

```
¿Se necesita acceso a algo externo que Claude no puede tocar por sí solo
(un navegador real, un filesystem, una app)?
    → MCP

¿Es una tarea grande/exploratoria que conviene resolver aparte,
sin llenar la conversación principal de pasos intermedios?
    → Subagente

¿Es conocimiento de "cómo se hace bien algo", que se quiere que se
aplique automáticamente cuando corresponda, sin tener que pedirlo?
    → Skill

¿Es una instrucción específica que el usuario quiere disparar manualmente,
cuando decida, con un atajo corto?
    → Slash command
```

---

## 7. Por qué esto conecta con un repo de MCP

Un repo de investigación de MCP documenta el primer mecanismo (acceso a sistemas externos). Un repo de Skills documenta el segundo (criterio/conocimiento aplicado). **No compiten entre sí** — de hecho, en un caso de estudio real de automatización con MCP, una Skill bien escrita podría capturar la metodología incremental descubierta a las malas, para que la próxima vez no haya que re-descubrirla desde cero.

---

## Tabla resumen final

| Mecanismo | Resuelve... |
|---|---|
| MCP | "Se necesita que Claude pueda tocar algo externo real" |
| Skill | "Se quiere que Claude sepa hacer bien X, automáticamente, cuando corresponda" |
| Subagente | "Esta tarea es grande, se quiere que se resuelva aparte sin ensuciar la conversación" |
| Slash command | "Se quiere un atajo para algo que se dispara seguido" |
