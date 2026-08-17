# Seguridad y confianza al instalar Skills de terceros

## La analogía general

Instalar un plugin o una skill de alguien desconocido es como darle a un electricista las llaves de la casa entera para que arregle un enchufe puntual. Una vez adentro, con esas llaves puede abrir cualquier puerta de la casa — no solo la del cuarto donde está el enchufe. No hay ninguna jaula automática que lo limite a la tarea que dijo que iba a hacer. Confiar en que solo toque el enchufe depende enteramente de que esa persona sea, de hecho, confiable — no de ningún mecanismo que lo obligue.

---

## 1. El punto central: no hay sandboxing por defecto

La documentación oficial de Claude Code es explícita en esto: los plugins y los marketplaces son componentes altamente confiables, capaces de ejecutar código arbitrario en la máquina de quien los instala, con los mismos privilegios de esa persona. No existe una caja de arena que aísle lo que un plugin puede hacer — corre con el mismo nivel de acceso que tendría cualquier otro programa que se ejecute en esa cuenta de usuario. La recomendación oficial, sin matices, es instalar plugins y agregar marketplaces solo de fuentes en las que ya se confía de antemano.

> **Analogía:** esto es la diferencia entre contratar un electricista con antecedentes verificados por una empresa seria, y dejar entrar a alguien que tocó la puerta y dijo que era electricista. La "empresa seria" en este caso no existe por defecto — cada quien decide a quién le abre la puerta.

---

## 2. Los tres niveles reales de confianza — y por qué no son intercambiables

No todos los marketplaces tienen el mismo respaldo, aunque a simple vista parezcan igual de "oficiales":

- **Marketplace oficial de Anthropic** (`claude-plugins-official`): curado directamente por Anthropic, a su propio criterio. Es el nivel de mayor confianza disponible.
- **Marketplace de comunidad** (`claude-plugins-community`): plugins de terceros que pasaron una validación y un screening de seguridad **automáticos** de Anthropic — no una revisión humana caso por caso — y quedan fijados a un commit SHA específico dentro del catálogo, para que no puedan cambiar en silencio después de haber sido aprobados.
- **Cualquier otro marketplace** (un repositorio de GitHub cualquiera, uno local, uno que comparte un amigo): sin ninguna revisión de Anthropic. La confianza depende enteramente de quién lo publicó.

El propio [`taller-marketplace/`](../ejercicios/01-skill-como-plugin/taller-marketplace/) construido en este repositorio cae directamente en esta tercera categoría, si alguien más lo instalara: no tiene ningún screening detrás, más allá de que quien lo escribió lo haya revisado a mano.

> **Analogía:** es la diferencia entre un electricista certificado por un colegio profesional, uno que pasó un chequeo de antecedentes automático pero nunca conoció a un inspector en persona, y uno que simplemente golpeó la puerta. Los tres pueden llamarse "electricista" — el nivel de garantía detrás de esa palabra es completamente distinto.

---

## 3. Lo que sí se puede inspeccionar antes de instalar — con una limitación importante

Antes de confirmar una instalación, el panel interactivo `/plugin` muestra una vista de detalle con el costo de contexto estimado, la fecha de última actualización, y una sección **"Will install"** que lista exactamente qué comandos, skills, agentes, hooks y servidores MCP o LSP va a agregar el plugin. Es una inspección real, no solo una promesa de buena fe.

La limitación: esto depende de que el marketplace provea esos metadatos. En un marketplace local o personalizado — como el que se construyó en el [taller 01](../ejercicios/01-skill-como-plugin/GUIA.md) de este mismo repositorio — esa vista puede mostrar directamente **"Components will be discovered at installation"** en vez de la lista real. Es decir: justamente el tipo de marketplace que se armó acá para aprender tiene **menos** visibilidad previa que uno bien documentado y publicado con cuidado.

> **Analogía:** es como pedirle al electricista una lista escrita de qué herramientas va a usar antes de dejarlo entrar — funciona perfecto si la lista existe. Si llega sin ella, la alternativa es "confiar y ver qué hace", que es exactamente la situación menos segura de las dos.

---

## 4. La acción concreta que la documentación recomienda: revisar `allowed-tools` a mano

El punto más accionable de toda esta nota: revisar manualmente el campo `allowed-tools` de cada `SKILL.md` de un plugin antes de instalarlo o confiar en él. Una skill puede otorgarse a sí misma acceso amplio a herramientas — sin pedir ningún permiso adicional durante el turno en que se invoca. La documentación oficial lo dice sin rodeos: conviene revisar el `allowed-tools` de las skills de un repositorio ajeno antes de correr Claude Code sobre él.

Esto es distinto, y más delicado, que un script guardado en `scripts/` (como el del [taller 02](../ejercicios/02-skill-con-script/GUIA.md)): un script ahí es algo que Claude decide ejecutar, y esa decisión queda a la vista en el momento. `allowed-tools`, en cambio, es una **pre-aprobación silenciosa** — el permiso ya está dado de antemano, sin que nadie tenga que aprobarlo en el momento en que realmente se usa.

> **Analogía:** un script en `scripts/` es como ver al electricista sacar una herramienta de su caja frente a uno — se nota. `allowed-tools` es como haberle entregado, antes de que llegue, una copia de la llave de un cajón puntual: cuando la usa, nadie lo ve pedir permiso, porque ya se lo dieron por adelantado.

---

## 5. Un vector menos obvio: la inyección de contexto dinámico

Un `SKILL.md` puede incluir comandos con la sintaxis `` !`comando` ``, que se ejecutan automáticamente apenas se invoca la skill — **antes** de que Claude muestre nada del contenido. Si ya existe una regla de permiso amplia que cubre ese comando (por ejemplo, un allow rule que ya se aprobó antes en la sesión), corre en silencio, sin pedir una aprobación nueva. Si ningún permiso lo cubre, no hay un punto intermedio de "preguntar": la invocación completa se aborta.

Esto significa que, a diferencia de un script explícito que Claude decide correr, un comando de este tipo se dispara automáticamente por el solo hecho de invocar la skill — la única defensa real es que las reglas de permiso no lo cubran de antemano.

> **Analogía:** es como si el electricista, apenas cruzar la puerta, ya tuviera una llave que abre un cajón puntual sin necesidad de pedir permiso — no porque sea un mal electricista, sino porque esa llave ya se le había entregado de antes, sin que nadie recordara para qué era exactamente.

---

## 6. A nivel organización, esto ya se toma en serio

Los equipos pueden restringir qué marketplaces está permitido agregar, mediante una configuración administrativa (`strictKnownMarketplaces`) que bloquea cualquier fuente no explícitamente aprobada. Esto no aplica a alguien aprendiendo por su cuenta, pero confirma que el riesgo no es una preocupación menor o teórica — es lo bastante real como para que existan controles formales pensados específicamente para él.

---

## Tabla resumen

| Nivel | Quién lo revisa | Qué tan protegido queda quien instala |
|---|---|---|
| Marketplace oficial (`claude-plugins-official`) | Anthropic, directamente y a su criterio | Alto — es el nivel de mayor confianza disponible |
| Marketplace de comunidad (`claude-plugins-community`) | Screening automático de Anthropic + fijado a un commit SHA | Medio — sin revisión humana caso por caso, pero no puede cambiar en silencio después de aprobado |
| Cualquier otro marketplace (incluido uno propio o de un amigo) | Nadie, salvo quien lo publicó | Bajo — la confianza depende enteramente de la fuente |

---

## Por qué esto importa

La nota [¿Qué son las Skills de una IA?](./que-son-las-skills.md) ya había planteado el "principio de no sorpresa": una skill no debería hacer nada distinto de lo que su descripción promete. Esta nota completa esa idea con su contraparte técnica: qué mecanismos reales existen — o no existen — para verificar que ese principio se cumple antes de instalar algo. La respuesta corta es que la verificación automática es parcial (y a veces ni siquiera está disponible, como en un marketplace local), así que la revisión manual del `allowed-tools` de cada `SKILL.md` sigue siendo, hoy, el paso más concreto que queda en manos de quien instala. Esto incluye a los propios plugins construidos en este repositorio: la familiaridad con el código propio no reemplaza la misma revisión técnica que se le pediría a un plugin de un desconocido.
