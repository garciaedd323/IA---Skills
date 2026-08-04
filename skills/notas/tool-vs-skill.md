# Tool vs Skill: dos formas distintas de darle capacidades a una IA

## La analogía general

Imagina que quieres que un asistente pueda hacer dos cosas: **consultar el clima exacto de hoy** y **redactar un contrato de arrendamiento bien hecho**. Para lo primero, le das acceso a un **teléfono con un número específico** que marca y obtiene un dato exacto, estructurado, sin ambigüedad. Para lo segundo, le entregas **el manual de un abogado experimentado**, con ejemplos de cláusulas, errores comunes a evitar, y el razonamiento detrás de cada decisión — algo que él lee y aplica con criterio, no un botón que aprieta para obtener un resultado fijo.

Eso es, en esencia, la diferencia entre una **Tool** (el teléfono con el número específico) y una **Skill** (el manual del abogado).

---

## 1. Qué es cada una, técnicamente

| | Tool (función) | Skill |
|---|---|---|
| **Qué es** | Código invocable, con un esquema de entrada/salida fijo | Un documento con instrucciones, más recursos opcionales |
| **Cómo se ejecuta** | El modelo *llama* la función y recibe un resultado estructurado | El modelo *lee* el contenido y lo incorpora a su razonamiento |
| **Flexibilidad** | Rígida — inputs y outputs ya definidos de antemano | Flexible — texto libre, ejemplos, manejo de casos borde |
| **Analogía** | Como llamar a una API | Como leer el manual de un compañero experto antes de trabajar |

> **El punto que más fácil se malinterpreta:** una Skill **no es código que "se ejecuta"** por sí sola. Es texto que el modelo lee y sigue como instrucción — si esa Skill trae consigo scripts (en su carpeta `scripts/`), esos scripts sí se ejecutan, pero mediante una Tool de ejecución de código, no porque la Skill "corra" directamente.

---

## 2. El flujo real de cómo trabajan juntas

1. **Registro** — el sistema mantiene un catálogo de Tools y de Skills disponibles. Las Skills solo muestran su nombre + descripción corta (barato en contexto); las Tools declaran su esquema completo de entrada/salida.
2. **Disparo (triggering)** — cuando llega una tarea, el modelo compara lo que se le pide contra las descripciones disponibles y decide qué Tools llamar y qué Skills activar.
3. **Carga** — si una Skill parece relevante, el modelo usa una herramienta de lectura de archivos para cargar el `SKILL.md` completo a su contexto. Aquí es donde una **Tool de lectura de archivos** (`read_file`, `view`, etc.) hace posible que la Skill "entre en juego".
4. **Aplicación** — el modelo sigue las instrucciones de la Skill al hacer la tarea, y si esa Skill trae scripts auxiliares, los ejecuta a través de una **Tool de ejecución de código** (`bash`, `run_code`, etc.).
5. **Combinación** — es común que varias Skills se apliquen a la vez sobre la misma tarea (por ejemplo, una Skill de "generar reportes" junto con una Skill de "formato de documentos Word").

> **Analogía:** el catálogo es como el directorio de la oficina — algunos números de teléfono directos (Tools) y algunos manuales disponibles en el estante (Skills), todos listados por su nombre. Cuando llega una tarea, el empleado revisa ese directorio, decide si necesita marcar un número específico o ir a leer un manual — y para poder ir a "leer el manual", primero necesita saber usar el clasificador de la biblioteca (la Tool de lectura de archivos). Las Skills, entonces, **dependen de que existan Tools básicas** (leer archivos, y a veces ejecutar código) para poder funcionar — no son completamente independientes.

---

## 3. Por qué esta distinción importa en la práctica

- **Una Tool es predecible y estructurada** — ideal quan el resultado necesita encajar en un formato exacto (una consulta a una base de datos, una operación matemática, una llamada a una API externa).
- **Una Skill es flexible y contextual** — ideal cuando la tarea requiere criterio, ejemplos, manejo de casos particulares, o "la forma correcta de hacer algo" que es difícil de reducir a un esquema fijo de inputs/outputs.

> **Analogía:** no le pides al manual del abogado que "calcule automáticamente" un número exacto — para eso usas la calculadora (Tool). Y no le pides al teléfono con el número específico que "use su criterio" para redactar una cláusula matizada — para eso existe el manual (Skill). Cada una resuelve un tipo de problema distinto, y muchas veces se necesitan **las dos combinadas** para completar una tarea real.

---

## 4. Cómo se ve esto si armaras tu propio sistema (fuera de Claude Code)

Si estuvieras construyendo tu propio agente con la API directamente (no usando Claude Code, que ya trae esto resuelto), el patrón general sería:

1. Guardar las Skills en una carpeta del proyecto (`skills/mi-skill/SKILL.md`).
2. Incluir en el prompt del sistema **solo el nombre + descripción corta** de cada Skill disponible — nunca el `SKILL.md` completo de entrada, para no gastar contexto de más.
3. Darle al modelo una **Tool de lectura de archivos**, para que pueda cargar el `SKILL.md` completo cuando la tarea coincida con la descripción.
4. Si alguna Skill trae scripts, darle también una **Tool de ejecución de código**.
5. Dejar que el ciclo normal de uso de herramientas ("tool use loop") haga el resto: el modelo pide leer el archivo, se le entrega el contenido, y sigue las instrucciones — repitiendo hasta terminar la tarea.

> Si en cambio se trabaja directamente sobre **Claude Code o el Agent SDK**, este mecanismo ya viene incorporado — no hace falta reimplementar el "loop" de lectura de Skills manualmente, solo colocar la Skill en la ruta esperada (ver la nota de [dónde colocar una Skill](./donde-colocar-una-skill.md)).

---

## 5. Tabla resumen

| Concepto | Una frase para recordarlo |
|---|---|
| Tool | Función invocable con esquema fijo — como marcar un número de teléfono específico |
| Skill | Documento con instrucciones y criterio — como leer el manual de un compañero experto |
| Una Skill no "se ejecuta" | Se **lee**; si trae scripts, esos sí se ejecutan, mediante una Tool aparte |
| Dependencia | Las Skills necesitan Tools básicas (leer archivos, a veces ejecutar código) para poder funcionar |
| Cuándo usar cada una | Tool = resultado estructurado y predecible · Skill = criterio, contexto, casos particulares |

---

## Por qué esto importa antes de seguir construyendo Skills propias

Entender que una Skill depende de Tools básicas (lectura de archivos, ejecución de código) para funcionar explica por qué, en Claude Code, todo esto "ya viene incorporado" sin que el usuario tenga que configurar nada — el propio Claude Code ya trae esas Tools fundamentales integradas. Si en algún momento se quisiera construir un agente propio desde la API pura (fuera de Claude Code), esta es la pieza de infraestructura que habría que armar primero, antes de que cualquier Skill propia pudiera funcionar.
