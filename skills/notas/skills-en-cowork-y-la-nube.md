# Cómo funcionan las Skills en Cowork y sesiones en la nube

## La analogía general

Trabajar en la propia oficina, con el escritorio y el archivero al lado, es una cosa: todo lo que se necesita está a mano, en el mismo edificio. Trabajar desde una sucursal remota de la misma empresa es otra muy distinta — esa sucursal no tiene acceso físico al archivero de la oficina de origen. Necesita que alguien mande copias de los documentos relevantes por correo interno antes de empezar el día, y si un documento nunca se mandó, simplemente no está ahí, por más que exista, perfectamente guardado, en el archivero original. Cowork y las sesiones en la nube son esa sucursal remota.

---

## 1. El punto central: Cowork y la nube no leen el disco local

La nota [Dónde colocar una Skill para que Claude Code la detecte](./donde-colocar-una-skill.md) documentó, y verificó en la práctica, cómo una sesión local de Claude Code lee `.claude/skills/` del proyecto o `~/.claude/skills/` del usuario. Ese modelo asume todo el tiempo una sesión corriendo en la propia máquina, con acceso directo al disco.

Las sesiones de Cowork y las sesiones en la nube — incluidas las *routines* programadas — rompen esa suposición: **no leen `~/.claude/skills/` de la máquina del usuario**. En su lugar, cargan las skills habilitadas para la **cuenta** de claude.ai del usuario, sincronizadas al iniciar la sesión. Es un modelo de distribución distinto, no una simple variante del mismo mecanismo.

> **Analogía:** es la diferencia entre que un empleado lleve sus propias herramientas al trabajo todos los días, y que la empresa le entregue, en la sucursal remota, solo las herramientas que quedaron registradas a su nombre en el sistema central — no las que tiene guardadas en su propio galpón en casa.

---

## 2. Cómo se habilita una skill para que Cowork o la nube la vean

A diferencia de una sesión local — donde alcanza con colocar una carpeta en el lugar correcto del disco — habilitar una skill para Cowork o la nube se administra desde **"Customize"** en la barra lateral de la app de escritorio, o desde la configuración de skills en claude.ai. No es un archivo que se edita; es una configuración de cuenta.

---

## 3. Un canal adicional exclusivo de las sesiones en la nube

Las sesiones en la nube tienen algo que Cowork puro no tiene: además de las skills sincronizadas de la cuenta, también cargan las **project skills comiteadas** en `.claude/skills/` del repositorio clonado. Es decir, para una sesión en la nube, comitear una skill al repositorio la hace disponible ahí, aunque nunca se haya habilitado para la cuenta — un segundo camino de acceso que Cowork, por sí solo, no ofrece.

> **Analogía:** es como si la sucursal remota, además de recibir las herramientas registradas a nombre del empleado, también tuviera acceso al depósito compartido del proyecto en el que está trabajando — dos fuentes distintas, no una sola.

---

## 4. El error real: "skill not found" en una routine

Si una skill existe solo en `~/.claude/skills/` de la máquina local, y nunca se habilitó para la cuenta ni se comiteó a ningún repositorio, una *routine* (tarea programada en la nube) la reporta como **no encontrada** al intentar invocarla. La razón: cada corrida de una routine arranca como una sesión remota completamente nueva, sin ningún acceso al disco de la máquina de origen — el documento nunca salió del archivero original.

Existen tres formas reales de evitarlo:

- Habilitar la skill para la cuenta de claude.ai — sirve tanto para Cowork como para sesiones en la nube.
- Comitear la skill al `.claude/skills/` del repositorio — sirve solo para sesiones en la nube.
- Empaquetarla en un plugin **declarado en el `.claude/settings.json`** del repositorio — los plugins declarados a nivel de repositorio se instalan al iniciar la sesión en la nube, pero uno habilitado solo en la configuración personal del usuario no se transfiere.

> **Analogía:** es como programar una entrega automática a una sucursal que nunca recibió la dirección de destino — el paquete simplemente no llega, no porque se haya perdido, sino porque nunca se le dijo al sistema que debía viajar hasta ahí.

---

## 5. Lo que sí sigue siendo local: las tareas programadas de escritorio

Las tareas programadas de escritorio (*Desktop scheduled tasks*) son distintas de las routines en la nube, aunque suenen parecidas: corren **localmente** en la máquina del usuario, y cargan skills exactamente de las mismas ubicaciones que cualquier otra sesión local. No tienen el problema del punto anterior — porque nunca dejan de estar en la oficina original.

---

## 6. Llevar skills sincronizadas a una sesión local normal

Es posible, aunque no ocurre por defecto, hacer que una sesión local normal cargue las skills habilitadas para la cuenta de claude.ai:

1. Habilitar cada skill deseada para la cuenta (mismo lugar de la sección 2).
2. Correr Claude Code en modo no interactivo con la sincronización activada:

   ```bash
   CLAUDE_CODE_SYNC_SKILLS=1 claude -p "List the skills you have available"
   ```

   Esto descarga las skills habilitadas hacia una carpeta especial, `~/.claude/skills/synced/`, en el disco local.
3. Confirmar que cargaron corriendo `/skills` en una sesión interactiva normal (sin la variable de entorno) — deberían listarse bajo la etiqueta **"claude.ai sync"**.

Un dato curioso que se desprende de esto: el nombre de carpeta `synced` queda **reservado** dentro de las ubicaciones de skills (enterprise, personal, proyecto). Si alguien intentara crear una skill propia llamada literalmente `synced`, Claude Code la ignoraría a favor de esta carpeta especial.

---

## 7. Un matiz de seguridad que ya viene incorporado

La nota [Seguridad y confianza al instalar Skills de terceros](./seguridad-instalar-skills-de-terceros.md) describió, como riesgo genérico, que un comando de inyección de contexto dinámico (`` !comando ``) dentro de un `SKILL.md` se ejecuta automáticamente al invocar la skill. Para las skills sincronizadas desde la cuenta, Anthropic ya neutralizó parte de ese riesgo de antemano, con dos protecciones concretas:

- Claude Code **sanea el texto de exhibición** de una skill sincronizada — como su `description` — removiendo caracteres de control y escapando los signos `<` y `>`, para que el texto no pueda imitar el formato interno de Claude Code.
- En una sesión de Cowork en el escritorio, y en cualquier sesión local que haya cargado skills sincronizadas manualmente (sección 6), Claude Code **no ejecuta** los comandos `` !comando `` que sí correrían en una skill local común — los reemplaza por un aviso, o los deja como texto literal, según el tipo de sesión.

En una sesión en la **nube**, en cambio, el cuerpo de una skill sincronizada se comporta igual que el de una skill local común — porque esa sesión ya corre dentro de un contenedor aislado, y el riesgo del comando automático queda contenido por el aislamiento del entorno en sí, no por una regla especial sobre el contenido de la skill.

> **Analogía:** es como si el correo interno que trae los documentos a la sucursal remota, además, viniera con un sello que impide que cualquier instrucción escondida adentro del documento se haga pasar por una orden oficial de la empresa — una capa de revisión que no existe cuando el documento se usa en el archivero original de siempre.

---

## Tabla resumen

| | Sesión local normal | Cowork | Sesión en la nube (routine) | Desktop scheduled task |
|---|---|---|---|---|
| ¿Lee `~/.claude/skills/` del disco? | Sí | No | No | Sí |
| ¿Carga skills sincronizadas de la cuenta? | Solo si se activó manualmente | Sí, automático | Sí, automático | No |
| ¿Carga project skills del repo clonado? | N/A (ya está en el repo) | No | Sí | N/A |
| ¿Ejecuta `` !comando `` de una skill sincronizada? | No aplica (no sincroniza por defecto) | No | Sí (igual que una skill local) | No aplica |

---

## Por qué esto importa

Con esta nota se destraba el último ítem que quedaba pendiente en el roadmap original de este repositorio — pausado hasta ahora por falta de información concreta. El repositorio queda con un mapa bastante completo del tema con el que arrancó: qué es una skill, dónde se coloca localmente, cómo se empaqueta en un plugin, cómo se distribuye entre computadoras distintas, cómo se evalúa con rigor, qué riesgos de seguridad implica instalar una de terceros, qué pasa cuando dos colisionan por significado, cómo se versiona en el tiempo, y ahora también cómo cambia todo esto en Cowork y en la nube.
