# Qué pasa cuando dos Skills se superponen en su `description`

## La analogía general

Dos empleados nuevos entran a trabajar el mismo día en la misma oficina. Cada uno tiene su propia tarjeta de presentación, con un nombre distinto, pero las dos tarjetas describen un tipo de trabajo casi idéntico, con palabras distintas. Cuando llega un pedido ambiguo a recepción, cualquiera de los dos podría atenderlo perfectamente bien — y no hay ningún protocolo escrito en la oficina que diga a cuál de los dos hay que mandarlo. La decisión queda en manos de quien recibe el pedido ese día en particular, y esa persona podría decidir distinto un martes que un jueves, sin que nadie haya cambiado nada.

---

## 1. El contraste central: colisión de nombre vs colisión de significado

Este repositorio ya documentó, en [Skills sueltas vs Skills empaquetadas en un plugin](./skills-como-plugin.md), que la colisión de **nombre** entre skills tiene reglas deterministas y documentadas: entre niveles, enterprise pisa a personal, personal pisa a proyecto; y el namespacing `plugin:skill` evita directamente que dos plugins distintos choquen por tener una skill con el mismo nombre corto.

La colisión **semántica** es un problema distinto: dos skills con nombres completamente diferentes, cuyo `description` dice, en esencia, lo mismo con otras palabras. La documentación oficial de Claude Code define reglas de resolución **solo** para el caso de nombre igual — nunca para el caso de significado parecido con nombre distinto. Eso no es un vacío accidental de esta nota: es un vacío real en el mecanismo mismo.

> **Analogía:** la colisión de nombre es como que dos empleados tengan la misma credencial de acceso — un problema que el sistema de seguridad del edificio detecta y resuelve solo, con una regla fija. La colisión semántica es que dos empleados con credenciales distintas puedan, cada uno por su cuenta, resolver el mismo pedido igual de bien — ahí no hay ningún sistema automático que decida, porque el problema no es de identificación, es de criterio.

---

## 2. Un ejemplo real, no hipotético, usando piezas que ya existen

La skill `generador-mensaje-commit`, construida en el [taller 01](../ejercicios/01-skill-como-plugin/GUIA.md) de este mismo repositorio, tiene un `description` centrado en ayudar a escribir el mensaje de un commit de git. El marketplace oficial de Anthropic (`claude-plugins-official`) incluye un plugin real llamado `commit-commands`, que ofrece flujos de trabajo de commits de git — incluyendo, también, generar el mensaje.

Si alguien tuviera instalados los dos al mismo tiempo — el propio de este repositorio y el oficial de Anthropic — y pidiera *"ayudame con el mensaje de commit"*, ambas skills tienen un `description` que plausiblemente aplica. Esto no es un escenario inventado para ilustrar el punto: es una colisión real, con dos piezas que ya existen hoy en este mismo ecosistema.

> **Analogía:** es como si el electricista del ejemplo de seguridad de otra nota de este repo y un segundo electricista, contratado por separado, aparecieran el mismo día para el mismo trabajo — ninguno de los dos hizo nada mal, el problema es que nadie coordinó de antemano cuál de los dos debía tocar ese cable puntual.

---

## 3. Por qué esto es más difícil de detectar que la colisión de nombre

La colisión de nombre se detecta con solo mirar si dos carpetas se llaman igual — es una comparación de texto, mecánica, verificable antes de que nadie use nada. La colisión semántica exige leer el **significado** de dos descriptions y juzgar si se superponen — no hay ningún chequeo automático que lo señale de antemano.

Peor todavía: el propio comportamiento del modelo eligiendo entre dos skills en conflicto puede variar de una sesión a otra frente al mismo pedido exacto. Esto conecta directo con lo que ya explicó [Cómo evaluar rigurosamente si una Skill funciona bien](./evaluar-una-skill-rigurosamente.md): correr la misma consulta varias veces y medir la tasa de activación no es solo una buena práctica general — es, de hecho, la única forma real de **medir** si existe una colisión semántica entre dos skills concretas, en lugar de suponerlo por intuición.

> **Analogía:** revisar si dos carpetas tienen el mismo nombre es como comparar dos números de documento — o coinciden, o no. Juzgar si dos descripciones de trabajo se superponen es como preguntarle a distintas personas si dos anuncios de empleo son "el mismo puesto" — pueden no ponerse de acuerdo, y la misma persona podría responder distinto en dos momentos diferentes.

---

## 4. Mitigaciones reales — todas preventivas, ninguna en tiempo real

Existen mecanismos concretos para reducir el riesgo, no solo el consejo general de "escribir mejor el `description`":

- **Líneas explícitas de desambiguación** dentro del propio `description`, del estilo "usar esto para X, no para Y". Es una práctica de escritura, no un mecanismo técnico, pero es la primera línea de defensa y la más barata de aplicar.
- **`disable-model-invocation: true`** en el frontmatter de una de las dos skills en conflicto: la saca por completo de la competencia automática del modelo, dejándola invocable solo a mano con `/nombre`. Elimina la ambigüedad de raíz para esa skill puntual, al costo de que deja de activarse sola.
- **El campo `paths`** (patrones de archivo) en el frontmatter: en vez de competir solo por el texto del pedido, cada skill puede quedar acotada a activarse automáticamente solo cuando se está trabajando sobre archivos que coincidan con un patrón — particionando la activación por **contexto**, no por semántica pura del pedido.
- **El trigger-rate testing con near-misses**, ya descrito en la nota anterior, aplicado de forma específica: usar las queries "verdaderas" de una skill como near-misses de la otra, y viceversa. Es la manera concreta de confirmar si la colisión existe en la práctica, en lugar de asumirlo.

> **Analogía:** todo esto es como coordinar de antemano quién atiende qué tipo de pedido antes de que llegue el cliente — un cartel más claro en cada escritorio, asignarle a un empleado solo los pedidos que llegan por un canal específico, o simplemente decirle a uno de los dos "vos no atendés a nadie que no te llame por tu nombre directamente".

---

## 5. La verdad incómoda: no hay resolución determinista en tiempo real

A diferencia de la colisión de nombre, **no existe ningún mecanismo determinista de resolución en el momento** en que dos skills ya instaladas compiten por el mismo pedido ambiguo. Todas las mitigaciones de la sección anterior son preventivas — se aplican al diseñar o escribir la skill, de antemano. Ninguna resuelve el conflicto en el instante exacto en que ocurre. Esa decisión queda, sin más, a criterio del modelo en ese momento específico — lo cual significa que puede no dar el mismo resultado dos veces frente al mismo pedido.

---

## Tabla resumen

| | Colisión de nombre | Colisión semántica de `description` |
|---|---|---|
| Cómo se detecta | Comparación de texto — mecánica y verificable de antemano | Requiere leer el significado y juzgar si se superpone |
| ¿Hay regla determinista de resolución? | Sí (jerarquía enterprise/personal/proyecto, namespacing `plugin:skill`) | No — ninguna documentada |
| Dónde se soluciona | En el sistema, automáticamente | En el diseño de cada skill, antes de que ocurra la competencia |
| Ejemplo | Dos plugins con una skill llamada igual | `generador-mensaje-commit` (este repo) vs `commit-commands` (marketplace oficial) |

---

## Por qué esto importa

Con esta nota, el repositorio deja resuelto — o al menos entendido a fondo — prácticamente todo lo que quedaba pendiente en el roadmap original, salvo cómo versionar una skill en el tiempo y el tema, todavía pausado, de Skills en claude.ai/Cowork. Junto con [Seguridad y confianza al instalar Skills de terceros](./seguridad-instalar-skills-de-terceros.md) y [Cómo evaluar rigurosamente si una Skill funciona bien](./evaluar-una-skill-rigurosamente.md), estas tres notas forman en conjunto una visión bastante completa de los riesgos y límites reales de trabajar con Skills — más allá de solo saber construirlas.
