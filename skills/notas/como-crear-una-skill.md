# Cómo crear una Skill propia, paso a paso

## La analogía general

Crear una Skill es parecido a escribir el manual de entrenamiento para un nuevo empleado que va a hacer una tarea específica una y otra vez. No se le escribe un libro completo de "todo lo que existe" — se le escribe **justo lo que necesita saber para esa tarea puntual**, de forma clara, con ejemplos, y anticipando las preguntas que probablemente tenga.

---

## Paso 0: ¿De verdad hace falta una Skill?

Antes de crear una, conviene preguntarse:

- **¿Es una tarea que se va a repetir muchas veces**, no solo una vez? Si es algo que se hace una sola vez, probablemente baste con explicarlo directamente en la conversación.
- **¿El resultado se puede verificar objetivamente** (un archivo con cierto formato, un cálculo correcto), o es algo muy subjetivo (estilo de escritura, arte)? Ambos casos pueden ser Skills, pero cambia cómo se prueban después.

> Si la respuesta es "esto se va a necesitar una y otra vez, y se quiere que se haga siempre de la misma forma correcta", ahí es donde una Skill empieza a tener sentido.

---

## Paso 1: Capturar la intención (antes de escribir una sola línea)

Responder estas 4 preguntas primero:

1. **¿Qué debe permitir hacer esta Skill?** (la tarea concreta)
2. **¿Cuándo debe activarse?** (qué frases o contextos del usuario deberían dispararla)
3. **¿Cuál es el formato de salida esperado?**
4. **¿Se necesitan casos de prueba** para verificar que funciona, o el resultado es más subjetivo?

> **Analogía:** es como definir el puesto de trabajo antes de contratar a alguien — si no está claro "qué hace este puesto" y "cuándo se le llama", se termina con un empleado confundido que no sabe cuándo debe intervenir.

---

## Paso 2: Investigar antes de escribir (la parte que casi todos se saltan)

Antes de redactar el `SKILL.md`, conviene pensar activamente en:
- **Casos límite** — ¿qué pasa si la entrada viene rara o incompleta?
- **Ejemplos de entrada/salida reales** — no genéricos, sino ejemplos concretos de lo que se esperaría ver.
- **Criterios de éxito** — ¿cómo se sabría que la Skill hizo bien su trabajo?
- **Dependencias** — ¿necesita alguna herramienta o librería específica para funcionar?

> **Analogía:** es la diferencia entre escribir un manual de capacitación **después de haber visto a alguien hacer mal la tarea varias veces** (rico en detalles reales) versus escribir uno **de forma completamente teórica antes de haber visto el trabajo real** (genérico y con huecos).

---

## Paso 3: Escribir el `SKILL.md`

### 3.1 — El `name`
Un identificador simple, corto, que describa la Skill.

### 3.2 — El `description` — la parte más importante, y hay que hacerla "un poco insistente"

Este es un consejo directo y muy concreto: las IAs tienden a **no activar una Skill cuando deberían** ("subactivación"). Para contrarrestar esto, el `description` debe ser explícito y algo "empujón", no tímido.

```yaml
# ❌ Descripción tímida — es más probable que nunca se active
description: Cómo construir un dashboard simple para mostrar datos internos.

# ✅ Descripción "pushy" — cubre variaciones de cómo alguien lo pediría
description: Cómo construir un dashboard rápido para mostrar datos internos. Usar esta skill siempre que el usuario mencione dashboards, visualización de datos, métricas internas, o quiera mostrar cualquier tipo de dato de la empresa, incluso si no pide explícitamente un "dashboard".
```

> **Analogía:** es la diferencia entre un letrero tímido que dice solo "Farmacia" versus uno que dice "Farmacia — medicamentos, vitaminas, primeros auxilios, también atendemos sin cita". El segundo letrero **captura más situaciones reales** en las que alguien debería entrar, en vez de esperar que adivinen que ahí también venden vitaminas.

### 3.3 — El cuerpo del documento

Aquí van las instrucciones reales. Algunas pautas importantes:

- **Usar forma imperativa** ("Genera el archivo...", no "El asistente debería generar...").
- **Explicar el porqué**, no solo el qué. Un modelo de lenguaje puede razonar mejor y adaptarse a casos no previstos si entiende la razón detrás de una instrucción, no solo la regla seca.
- **Evitar el abuso de MAYÚSCULAS y "SIEMPRE"/"NUNCA"** como única herramienta — si se encuentra escribiendo así todo el tiempo, es una señal de que puede convenir explicar mejor el razonamiento en vez de solo imponer una regla rígida.
- **Definir formatos de salida con plantillas explícitas** cuando el resultado debe seguir una estructura fija.

---

## Paso 4: Decidir qué recursos empaquetados hacen falta (opcional)

No toda Skill necesita `scripts/`, `references/`, o `assets/` — solo agregarlos si de verdad hacen falta:

| Carpeta | Cuándo usarla |
|---|---|
| `scripts/` | Cuando hay una tarea repetitiva/mecánica que conviene resolver con código, en vez de que el modelo la "razone" cada vez desde cero |
| `references/` | Cuando hay documentación extensa que **no siempre** hace falta leer completa (por ejemplo, detalles específicos por variante/plataforma) |
| `assets/` | Cuando el resultado final necesita plantillas, íconos, o archivos que se insertan directamente en la salida |

> Si el `SKILL.md` empieza a acercarse a las 500 líneas, es buena señal de que parte de ese contenido debería moverse a `references/`, con un puntero claro desde el cuerpo principal de cuándo ir a leerlo.

---

## Paso 5: Probar con 2-3 prompts reales

No conviene inventar casos de prueba artificiales — hay que pensar en **la frase real que un usuario diría** para activar esta Skill, y probarla.

> **Analogía:** es como hacerle una prueba de manejo real a alguien que dice saber conducir, en vez de solo preguntarle en un examen teórico — se necesita ver el comportamiento real ante una situación real, no solo la promesa de que "sí sabe".

---

## Paso 6: Iterar basándose en lo que salió mal (no en lo que "podría" salir mal)

Cuando algo no funcione como se esperaba:

1. **Generalizar a partir del problema puntual** — no arreglar solo ese caso exacto con un parche rígido; preguntarse por qué pasó y si hay una explicación más general que prevenga casos similares.
2. **Mantener el `SKILL.md` liviano** — si algo no está aportando valor real, quitarlo.
3. **Buscar trabajo repetido** — si se nota que, sin la Skill, siempre se termina escribiendo el mismo tipo de código de apoyo a mano, esa es la señal de que ese código debería empaquetarse en `scripts/` de una vez.

---

## Errores comunes al crear la primera Skill

| Error | Por qué es un problema |
|---|---|
| `description` demasiado corto o genérico | La Skill existe, pero nunca se activa cuando debería |
| Meter toda la lógica "por si acaso" desde el día uno | Hace la Skill difícil de mantener; mejor empezar simple e iterar con casos reales |
| Solo reglas rígidas ("SIEMPRE haz X"), sin explicar el porqué | El modelo no puede adaptarse bien a variaciones no previstas |
| No probarla con una frase real de usuario antes de darla por terminada | Puede fallar en la práctica de formas que nunca se imaginaron en la teoría |
| Poner criterios de "cuándo usar" dentro del cuerpo en vez de en el `description` | El mecanismo de activación real es el `description` — información de activación que vive solo en el cuerpo puede llegar demasiado tarde |

---

## Tabla resumen del proceso completo

| Paso | Qué se hace |
|---|---|
| 0 | Confirmar que de verdad conviene una Skill (tarea repetitiva, no puntual) |
| 1 | Capturar la intención: qué, cuándo, formato de salida, si necesita pruebas |
| 2 | Investigar casos límite, ejemplos reales, criterios de éxito |
| 3 | Escribir `SKILL.md` (name + description "pushy" + cuerpo con el porqué) |
| 4 | Decidir si hacen falta `scripts/`, `references/`, `assets/` |
| 5 | Probar con 2-3 prompts reales, no inventados |
| 6 | Iterar generalizando desde los problemas reales encontrados |

---

## Por qué esto importa antes de construir un ejemplo real

Con este proceso claro, el siguiente paso natural — construir una Skill real desde cero, de principio a fin — ya no es una lista de pasos abstractos, sino la aplicación directa de cada uno de estos 6 pasos a un caso concreto.
