# Cómo evaluar rigurosamente si una Skill funciona bien

## La analogía general

Pisar el freno del auto una vez en el estacionamiento y sentir que frena "se siente bien" da una sensación de tranquilidad. Una prueba de choque estandarizada — con velocidades fijas, repeticiones, sensores, y escenarios diseñados a propósito para encontrar el punto donde algo falla — da una respuesta distinta: no una sensación, sino un número confiable. Probar una skill con 2 o 3 pedidos escritos a mano es el equivalente de la prueba de estacionamiento: genera confianza, pero no dice nada sobre los casos que no se probaron.

---

## 1. Dos preguntas distintas, no una sola

Evaluar una skill no es una sola pregunta ("¿respondió bien?"), son dos, y se responden con métodos diferentes:

- **¿El `description` activa la skill en los momentos correctos, y no se activa cuando no debería?** — esto es la tasa de activación (*trigger rate*).
- **¿El contenido de la skill, una vez activada, mejora realmente el resultado?** — esto es la calidad del output.

Es perfectamente posible que una skill tenga instrucciones excelentes pero un `description` tan vago que casi nunca se active — o al revés, un `description` tan agresivo que se dispare en pedidos que no le corresponden. Confundir estas dos preguntas es la razón más común por la que "probé 2-3 prompts" da una falsa sensación de seguridad: normalmente solo se está probando una de las dos.

> **Analogía:** es la diferencia entre preguntar "¿el bombero llega rápido cuando hay un incendio real?" y preguntar "¿el bombero apaga bien el fuego una vez que llegó?". Un cuerpo de bomberos puede ser excelente apagando incendios y, aun así, fallar si la alarma nunca los llama a tiempo — o los llama por error a una casa sin fuego.

---

## 2. Probar la activación con un conjunto real de 20 casos

La metodología que usa `skill-creator` — la skill oficial de Anthropic para crear y mejorar skills — arma un conjunto de **20 queries de prueba**, divididas en dos grupos deliberadamente desiguales en dificultad:

- **8 a 10 que deberían activar la skill**: distintas formas de pedir lo mismo, casos donde la persona no menciona la skill explícitamente, pedidos informales, formales, con errores de tipeo, y usos poco comunes.
- **8 a 10 que NO deberían activarla**: sobre todo **near-misses** — pedidos con palabras clave parecidas pero que en realidad necesitan una herramienta distinta, dominios vecinos, y casos ambiguos donde una coincidencia ingenua de palabras activaría la skill sin que correspondiera.

La calidad de estas queries importa tanto como su cantidad. Una query de prueba como *"Format this data"* es demasiado prolija — nadie escribe así en la vida real. Una query realista se parece más a esto:

> "ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"

> **Analogía:** los near-misses son como simular un incendio de cocina para ver si el sistema de alarma de una casa no reacciona con la misma urgencia que ante un incendio real de verdad — no alcanza con probar que la alarma suena ante fuego, también hay que probar que NO suena ante vapor de una olla.

---

## 3. Separar entrenamiento de prueba, y repetir cada corrida

El conjunto de 20 queries no se usa entero para ajustar el `description`. Se divide **60% para entrenar** (ajustar la redacción según lo que falla) y **40% se guarda aparte**, sin tocar, como conjunto de prueba real.

Además, cada query se corre **3 veces**, no una sola — porque la activación de una skill no es 100% determinística: la misma pregunta, hecha en tres sesiones idénticas, puede activar la skill dos de tres veces. Correrla una sola vez no distingue "funciona siempre" de "funcionó esta vez por casualidad".

El proceso itera hasta 5 veces, proponiendo mejoras al `description` según lo que falló, y **elige la versión final por su puntaje en el conjunto de prueba, no en el de entrenamiento** — justamente para evitar la trampa de ajustar la redacción hasta que le vaya perfecto solo a los ejemplos que ya se vieron. Es el mismo problema de sobreajuste (*overfitting*) que existe en cualquier modelo entrenado con datos: optimizar contra los ejemplos conocidos no garantiza que funcione con ejemplos nuevos.

> **Analogía:** es como estudiar para un examen usando solo la mitad de los ejercicios del libro, y reservar la otra mitad, nunca vista, para el examen real — si solo se estudiara con todos los ejercicios y después se repitieran esos mismos en el examen, "aprobar" no diría nada sobre si el tema realmente se entendió.

---

## 4. Comparar con la skill y sin la skill

Un control que suele faltar en una evaluación casera: correr el **mismo pedido dos veces** — una con la skill cargada, otra sin ella — para ver si la skill realmente mejora el resultado, o si Claude ya lo hacía igual de bien sin necesitar nada extra.

Sin esta comparación, es fácil confundir "la skill funcionó" con "Claude es capaz en general" — atribuirle a la skill un mérito que en realidad no le corresponde.

> **Analogía:** es como probar si un suplemento vitamínico realmente ayuda: hay que comparar contra alguien que no lo tomó, no solo confirmar que la persona que lo tomó se sintió bien.

---

## 5. Assertions objetivas vs juicio humano subjetivo

Cómo se califica un resultado depende del tipo de skill:

- **Skills objetivas** (transformar archivos, extraer datos, generar código, pasos de flujo fijo): se pueden usar *assertions* verificables — por ejemplo, "el CSV tiene una columna llamada `profit_margin`", "el JSON es válido". Cada assertion se registra con qué se revisó, si pasó o no, y la evidencia concreta encontrada.
- **Skills subjetivas** (estilo de escritura, calidad de diseño): la recomendación explícita de Anthropic es **no forzar assertions rígidas** sobre algo que necesita juicio humano — en su lugar, una persona revisa el resultado y da retroalimentación en texto libre.

Esto se conecta directo con la propia [`nota-tecnica-con-analogias`](../ejemplos/nota-tecnica-con-analogias/) de este repositorio: es una skill fundamentalmente **subjetiva** — su éxito depende de si la analogía elegida realmente ayuda a entender, no de una regla verificable a simple vista. Evaluarla con una lista de assertions binarias sería aplicar la herramienta equivocada; le corresponde revisión cualitativa, no un checklist de sí/no.

> **Analogía:** revisar que un JSON sea válido es como revisar que una puerta cierre — o cierra, o no cierra, no hay término medio. Revisar si una analogía es clara es como revisar si un chiste es gracioso: dos personas honestas pueden evaluarlo distinto, y forzar una regla fija para "medirlo" no captura lo que realmente importa.

---

## 6. Análisis de varianza, no solo un promedio

Al juntar los resultados de todas las corridas, se calculan métricas con **media y desviación estándar** — tasa de aciertos, tiempo de ejecución, tokens usados — comparando siempre la versión "con skill" contra su versión base correspondiente. Un promedio simple puede esconder que una corrida salió excelente y otra salió mal; la desviación estándar es lo que permite distinguir una mejora real y consistente de una casualidad de una sola corrida con suerte.

---

## Tabla resumen: evaluación casera vs evaluación rigurosa

| | Evaluación casera ("probé 2-3 prompts") | Evaluación rigurosa (metodología de `skill-creator`) |
|---|---|---|
| Cantidad de casos de prueba | 2-3, elegidos a mano | 20, con near-misses incluidos a propósito |
| Mide activación incorrecta (falsos positivos) | Casi nunca | Sí, explícitamente (8-10 casos que NO deberían activarla) |
| Compara con la skill vs sin ella | Casi nunca | Sí, siempre |
| Repite cada corrida | Una sola vez | 3 veces, para medir variabilidad |
| Separa entrenamiento de prueba | No | Sí (60% / 40%), para evitar sobreajuste |
| Tipo de calificación | Impresión general | Assertions objetivas o juicio humano cualitativo, según el tipo de skill |

---

## Un cierre honesto: esto ya existe, no hace falta reconstruirlo

Toda esta metodología — el testeo de activación con near-misses, la separación entrenamiento/prueba, la comparación con y sin skill, el sistema de assertions, el análisis de varianza, e incluso un visor interactivo para revisar los resultados — ya está implementada de verdad en `skill-creator`, la skill oficial de Anthropic para crear y mejorar skills, disponible como skill invocable en este mismo entorno de Claude Code. No hace falta reconstruir este aparato a mano desde cero: el siguiente paso natural, si se quiere ir más allá de la teoría de esta nota, es invocar esa skill directamente sobre una skill real de este repositorio — por ejemplo, `nota-tecnica-con-analogias` — y correr una evaluación de verdad.

---

## Por qué esto importa

Esto conecta directo con un punto que sigue abierto en el roadmap de este repositorio: qué pasa cuando dos Skills se superponen en su `description`. El testeo de activación con near-misses es exactamente la herramienta que permitiría **detectar esa colisión de forma medible** — probando a propósito los casos ambiguos entre dos skills parecidas — en vez de descubrirla por casualidad cuando ya está pasando en producción. Y vale decirlo con la misma honestidad que el resto de este repositorio: la propia `nota-tecnica-con-analogias` nunca fue evaluada con este rigor — solo "probada en producción" de forma informal, como ya lo dice el README. Queda como una aplicación real pendiente, no solo una idea teórica.
