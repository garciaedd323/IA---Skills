# Cómo escribir buenas instrucciones dentro de una Skill: grados de libertad

## La analogía general

Imagina que se dan instrucciones a dos empleados distintos: a uno se le dice **"llena este formulario tributario exactamente en este orden, campo por campo, sin desviarte"** — porque un error ahí tiene consecuencias legales. Al otro se le dice **"diseña una propuesta creativa para el cliente, usa tu criterio, aquí tienes ejemplos de propuestas que funcionaron antes"** — porque forzarlo a seguir un guion rígido produciría algo genérico y peor.

Escribir una Skill bien requiere la misma decisión: **¿cuánta libertad de criterio se le da al modelo, según qué tan determinista o creativa es la tarea?** Ese ajuste es lo que separa una Skill que funciona siempre igual de bien, de una que solo funcionó en el caso exacto que se probó.

---

## 1. El espectro: de instrucciones rígidas a criterio libre

| Tipo de tarea | Nivel de libertad recomendado | Ejemplo |
|---|---|---|
| Generar un formato exacto (XML, JSON con schema fijo, un cálculo matemático) | 🔴 Baja — instrucciones muy precisas, o directamente un script | "Genera el XML siguiendo exactamente esta plantilla, campo por campo" |
| Aplicar una convención con variaciones esperables | 🟡 Media — reglas claras, pero con espacio para adaptarse | "Nombra las Tasks en inglés con sufijo `Task`, adaptando el nombre al contexto de la acción real" |
| Tareas creativas o de criterio (redacción, diseño, análisis subjetivo) | 🟢 Alta — principios y ejemplos, no una receta paso a paso | "Explica el concepto con una analogía cotidiana que ayude a entenderlo, no una lista fija de analogías predefinidas" |

> **Analogía:** es como decidir cuánto detalle poner en una receta de cocina. Para hacer pan (donde las proporciones exactas de levadura importan mucho), la receta debe ser precisa a la gota. Para hacer una ensalada, una receta demasiado rígida ("exactamente 7 hojas de lechuga, ni una más") es absurda — ahí lo que se necesita es un principio ("usar vegetales frescos, balancear sabores"), no una medida exacta.

---

## 2. Por qué la rigidez excesiva falla en tareas de criterio

Un patrón real observado al escribir Skills: si el cuerpo del `SKILL.md` está lleno de **SIEMPRE** y **NUNCA** en mayúsculas, con estructuras muy rígidas, es una señal de alerta — no necesariamente de que esté mal, sino de que probablemente se puede lograr un mejor resultado **explicando el razonamiento** detrás de la regla, en vez de solo imponerla.

Los modelos de lenguaje actuales tienen buena capacidad de razonamiento — cuando entienden **por qué** algo importa, pueden generalizar ese principio a casos que la instrucción rígida nunca cubrió explícitamente. Cuando solo reciben una orden seca, se quedan sin capacidad de adaptarse si el caso real se desvía un poco de lo previsto.

> **Analogía:** es la diferencia entre un empleado que memorizó "nunca le digas que no al cliente" sin entender por qué, y uno que entiende "se prioriza la satisfacción del cliente porque la retención es más rentable que una venta puntual" — el segundo va a saber improvisar bien en una situación que la regla memorizada nunca contempló; el primero se queda paralizado o hace algo absurdo.

---

## 3. Cuándo SÍ conviene la rigidez total: usar un script, no solo instrucciones

Para tareas verdaderamente **deterministas y repetitivas** (generar un archivo con un formato exacto, hacer un cálculo específico), la mejor "instrucción rígida" ni siquiera es texto — es directamente un **script ejecutable** en la carpeta `scripts/` de la Skill.

> **Analogía:** para una tarea 100% mecánica y repetitiva, no se le da al empleado una hoja de instrucciones ultra-detallada para que la siga a mano cada vez — se le da una **máquina que hace exactamente eso**, sin margen de error humano. El script es la forma más alta de "rigidez" posible: ni siquiera depende de que el modelo interprete bien el texto.

**Señal práctica de que algo debería ser un script:** si al usar la Skill varias veces se nota que, cada vez, se termina escribiendo un código de apoyo muy similar (por ejemplo, siempre el mismo tipo de función para generar un gráfico), esa es la señal de que ese código debería empaquetarse una vez en `scripts/`, en vez de confiar en que el modelo lo "razone" bien cada vez desde cero.

---

## 4. Evaluación: distinto criterio según el tipo de tarea

Esto conecta directo con los grados de libertad: **cómo se prueba que una Skill funciona bien también depende de si la tarea es objetiva o subjetiva.**

- **Tareas objetivas** (baja libertad): se pueden verificar con afirmaciones concretas y comprobables — "¿el XML generado es válido según el schema?", "¿el cálculo dio el número correcto?". Idealmente, verificable con un script, no solo "a ojo".
- **Tareas subjetivas** (alta libertad): cosas como estilo de escritura o calidad de diseño se evalúan mejor con **juicio humano cualitativo** — forzar una lista de afirmaciones objetivas sobre algo inherentemente subjetivo produce una evaluación falsa de precisión.

> **Analogía:** no se puede poner una nota numérica exacta a "qué tan inspirador fue un discurso" de la misma forma que se califica un examen de matemáticas con respuesta única — cada tipo de tarea necesita su propia vara de medir.

---

## 5. Aplicando esto a un ejemplo real: la Skill de notas técnicas

Recordando la Skill `nota-tecnica-con-analogias` ya construida y verificada:

- **Baja libertad (estructura obligatoria):** la nota siempre debe tener `## La analogía general` al inicio, secciones numeradas, y al menos una tabla resumen — esto es una regla fija, porque es la estructura que define el estilo del repo.
- **Alta libertad (contenido de las analogías):** qué analogía específica usar para cada concepto técnico se deja completamente al criterio del modelo — forzar una lista fija de analogías predefinidas produciría notas forzadas y poco naturales para temas que esa lista nunca anticipó.

Esta mezcla — estructura rígida + contenido flexible — es exactamente el balance que hace que la Skill funcione bien en temas muy distintos entre sí, no solo en el ejemplo que se probó la primera vez.

---

## 6. Tabla resumen

| Concepto | Una frase para recordarlo |
|---|---|
| Grados de libertad | Cuánta rigidez darle al modelo, según qué tan determinista es la tarea |
| Baja libertad | Instrucciones exactas, o mejor aún, un script — para tareas con una única respuesta correcta |
| Alta libertad | Principios y ejemplos, no una receta paso a paso — para tareas de criterio/creatividad |
| Señal de alerta | Demasiados SIEMPRE/NUNCA en mayúsculas sin explicar el porqué |
| Trabajo repetido | Señal de que algo debería moverse de "instrucción en texto" a "script en `scripts/`" |
| Evaluación | Objetiva y verificable para tareas deterministas; cualitativa para tareas subjetivas |

---

## Por qué esto importa para cualquier Skill futura

Antes de escribir el cuerpo de una nueva Skill, vale la pena preguntarse explícitamente: **¿qué partes de esta tarea son deterministas y cuáles requieren criterio?** — y escribir cada parte con el nivel de libertad correspondiente, en vez de aplicar el mismo estilo de instrucción rígida (o el mismo estilo de instrucción vaga) a toda la Skill por igual.
