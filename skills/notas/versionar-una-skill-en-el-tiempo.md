# Cómo versionar una Skill en el tiempo sin romper lo que ya funcionaba

## La analogía general

Una skill suelta es como una receta escrita a mano y pegada en la puerta de la heladera. Si alguien tacha una línea y escribe algo nuevo encima, todos los que cocinen después usan la versión tachada, inmediatamente, sin ningún aviso de "esta es la versión 2" y sin ninguna forma sencilla de volver a la anterior si la nueva resulta peor. No existe una carpeta de "recetas viejas" archivadas — a menos que alguien, por su cuenta, decida guardarlas.

---

## 1. El hallazgo central: no hay versionado integrado para una skill suelta

Verificado contra la especificación oficial del estándar abierto Agent Skills: **no existe un campo `version` de primer nivel** en el `SKILL.md` de una skill suelta. Si hiciera falta un valor de versión, la recomendación del propio estándar es meterlo dentro del campo `metadata` — un mapa libre de datos propios que Claude Code no interpreta ni hace cumplir, solo lo deja pasar.

La conclusión textual de esa documentación es directa: no hay actualmente un sistema de versionado integrado para skills — si se actualiza el comportamiento de una skill, todas las aplicaciones que la usan empiezan a usar la versión nueva **inmediatamente**. No hay staging, no hay rollback automático, no hay forma de "quedarse en la versión anterior" mientras se prueba la nueva.

> **Analogía:** es la diferencia entre publicar un libro con ediciones numeradas, cada una archivada en una biblioteca, y corregir a mano el único ejemplar que existe — la corrección entra en vigor apenas se hace, y el ejemplar anterior deja de existir salvo que alguien haya fotocopiado la página antes de tacharla.

---

## 2. Contraste con lo que sí tiene versión real: un plugin

Este repositorio ya documentó, en [Skills sueltas vs Skills empaquetadas en un plugin](./skills-como-plugin.md) y en [Cómo distribuir un marketplace entre computadoras distintas](./distribuir-marketplace-entre-pcs.md), que un **plugin** sí tiene un campo `version` real en su `plugin.json`, con una jerarquía de resolución documentada (versión en `plugin.json` > versión en la entrada del marketplace > commit SHA de git > hash sha256 para archivos zip). Los plugins, además, cuentan con un mecanismo de `renames` en el `marketplace.json` que migra automáticamente a quienes ya tenían instalada una versión anterior cuando un plugin se renombra o se elimina, sin que se les rompa nada.

Una skill suelta no tiene ninguna de las dos cosas: ni versión real, ni compatibilidad automática al renombrarla. Esto es, de hecho, un argumento técnico concreto — no solo estético — para graduar una skill suelta a plugin en el momento en que de verdad empieza a importar no romper lo que ya funcionaba para otras personas que dependen de ella.

> **Analogía:** un plugin versionado es como un software con historial de lanzamientos, cada uno con su número y sus notas de cambios. Una skill suelta es más parecida a un documento compartido que cualquiera puede editar directamente — funciona perfecto mientras es responsabilidad de una sola persona, y se vuelve frágil apenas depende gente que no participó en el cambio.

---

## 3. Un riesgo poco obvio: dos versiones conviviendo en la misma sesión

Cuando se invoca una skill, su contenido queda pegado en la conversación para el resto de la sesión — Claude Code no vuelve a leer el archivo en turnos posteriores de esa misma invocación ya cargada. Pero la detección de cambios en caliente sí permite que una **invocación nueva**, más adelante en la misma sesión, lea el archivo ya editado.

Esto genera una situación particular: si alguien edita el `SKILL.md` a mitad de una sesión larga y después vuelve a invocar esa misma skill, Claude Code **no reemplaza** la copia vieja que ya estaba en el contexto — agrega la copia nueva al lado de la anterior. Dentro de una misma sesión pueden terminar conviviendo dos versiones de instrucciones distintas, y potencialmente contradictorias, para la misma skill, sin que nadie lo haya pedido así.

> **Analogía:** es como corregir una receta a mitad de estar cocinando, sin arrancar la hoja vieja — quien está en la cocina ahora tiene, pegadas una al lado de la otra, dos versiones de instrucciones distintas para el mismo plato, y tiene que decidir por su cuenta cuál seguir.

---

## 4. Lo más cercano a un control de versiones que sí existe

La nota [Cómo evaluar rigurosamente si una Skill funciona bien](./evaluar-una-skill-rigurosamente.md) ya describió la metodología de `skill-creator`. Ahí aparece la práctica más parecida a un control de versiones real disponible hoy para skills sueltas: cuando `skill-creator` mejora una skill existente, guarda un `skill-snapshot/` de la versión anterior **antes** de tocar nada — específicamente para poder comparar la versión nueva contra la vieja, y volver atrás si la "mejora" en realidad empeoró las cosas.

Esto no es un campo del frontmatter ni un mecanismo de Claude Code en sí — es una práctica de flujo de trabajo de una skill puntual. Pero es la pieza más cercana a "guardar una versión anterior por si hay que volver" que existe hoy, fuera de manejarlo enteramente por cuenta propia.

---

## 5. Prácticas reales que sí sirven, porque Claude Code no da nada de esto gratis

- **Usar git como mecanismo de versionado real** — exactamente lo que ya hace este mismo repositorio: cada commit es, de hecho, una versión de cada nota y cada skill. La única razón por la que acá se puede decir "así se veía esta skill hace tres commits" es git, no ninguna funcionalidad propia de Claude Code.
- **Antes de cambiar el `description` de una skill ya en uso**, volver a correr el trigger-rate testing descrito en la nota de evaluación rigurosa, comparando la versión vieja contra la nueva — tratar esa evaluación como el test de regresión que una skill no tiene por defecto.
- **Si hace falta renombrar una skill suelta**, no hay compatibilidad automática como la de un plugin. La única forma casera de no romper el hábito de quien ya escribía `/nombre-viejo` es dejar, a mano, una skill placeholder en el nombre viejo cuyo único contenido sea avisar que se movió al nombre nuevo.
- **Guardar una noción de versión propia**, si hace falta coordinarse con otras personas — a mano, en `metadata`, o con una convención de carpetas como sugiere la documentación del estándar (por ejemplo `.claude/skills/v1/`, `.claude/skills/v2/`) — sabiendo de antemano que Claude Code no la interpreta ni la hace cumplir: es pura documentación para humanos, no una regla que el sistema respete.

---

## Tabla resumen

| | Skill suelta | Plugin |
|---|---|---|
| Campo de versión real | No existe (solo `metadata` libre, sin efecto) | Sí, en `plugin.json` / entrada del marketplace |
| Mecanismo de renombrado con compatibilidad | No — se rompe en silencio | Sí, vía `renames` en `marketplace.json` |
| Quién resuelve versionado y migraciones | El propio autor, a mano (típicamente con git) | Claude Code, con reglas documentadas |

---

## Por qué esto importa

Con esta nota se cierra el último ítem pendiente real del roadmap original de este repositorio — solo queda pausado el tema de Skills en claude.ai/Cowork. Y deja planteado algo que este mismo repositorio venía haciendo desde el principio sin decirlo explícitamente: hacer `git commit` y `git push` después de cada nota o taller no fue solo una costumbre de organización — fue, sin que se llamara así hasta ahora, la única estrategia de versionado real que las skills y notas de este repositorio tuvieron desde el primer día.
