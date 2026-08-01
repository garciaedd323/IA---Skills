---
name: nota-tecnica-con-analogias
description: Escribe notas técnicas educativas en Markdown, en español, con analogías cotidianas para explicar conceptos técnicos de programación, testing, automatización o IA. Usar esta skill siempre que el usuario pida crear, escribir o redactar una nota, documentación, explicación, o artículo técnico para uno de sus repositorios de aprendizaje personal — incluso si no menciona la palabra "skill", "analogía" o "nota" explícitamente, por ejemplo si dice "explícame X y hazme un archivo .md" o "documenta esto para mi repo".
---

# Nota técnica con analogías

Esta skill genera notas técnicas educativas siguiendo un estilo específico ya validado: explicaciones que combinan precisión técnica con analogías cotidianas, pensadas para que alguien sin experiencia previa entienda el concepto real, no solo memorice sintaxis.

## Por qué este estilo funciona

Explicar un concepto técnico solo con definiciones formales asume que el lector ya tiene el marco mental necesario para entenderlas. Una analogía cotidiana bien elegida le da al lector ese marco mental **antes** de la definición técnica, así que cuando llega el detalle preciso, ya tiene dónde "colgarlo" mentalmente.

## Estructura obligatoria de la nota

1. **Título** (`# Título del tema`)
2. **`## La analogía general`** — un párrafo que presenta el concepto completo a través de UNA analogía central de la vida cotidiana, antes de cualquier detalle técnico. Esta analogía general se puede retomar en secciones posteriores.
3. **Secciones numeradas** (`## 1.`, `## 2.`, etc.) — cada una cubre un aspecto específico del tema. Dentro de cada sección:
   - Explicación técnica precisa (con código de ejemplo si aplica).
   - Un bloque `> **Analogía:** ...` que traduce esa pieza técnica específica a la vida cotidiana. No repetir la misma analogía general palabra por palabra — extenderla o variarla según el sub-tema.
4. **Al menos una tabla resumen** en algún punto de la nota — comparando conceptos, opciones, o resumiendo términos clave.
5. **Si existe una herramienta o concepto "hermano" ya cubierto antes** (por ejemplo, si ya se escribió una nota de Selenium y esta nueva es de Cypress), incluir comparaciones explícitas con lo ya conocido, no explicar desde cero como si fuera aislado.
6. **Cierre con "Por qué esto importa"** — una sección final corta que conecta el tema con lo que viene después, dando sentido a por qué se aprendió en este momento y no en otro.

## Tono y estilo de redacción

- Español neutro, evitando dirigirse al lector como "tú" cuando sea posible (preferir formas impersonales: "se hace", "conviene", en vez de "tú haces", "te conviene") — esto es una preferencia de estilo específica del usuario, mantenerla consistente.
- Evitar sonar como un anuncio publicitario de la herramienta — se puede señalar limitaciones y contras reales, no solo ventajas.
- Usar tablas Markdown para comparaciones, no párrafos largos enumerando diferencias.
- Los bloques de código deben ser reales y correctos para el lenguaje/herramienta en cuestión — no pseudocódigo vago.

## Ejemplo de una sección completa (referencia de formato)

```markdown
## 3. Auto-waiting — por qué no hace falta un `WebDriverWait`

Playwright verifica automáticamente que un elemento esté listo antes de actuar sobre él.

\`\`\`typescript
await page.getByRole('button', { name: 'Guardar' }).click();
\`\`\`

> **Analogía:** es como un protocolo de seguridad de un elevador antes de cerrar las puertas — revisa que no haya nada atascado antes de proceder, sin que nadie tenga que pedírselo.
```

## Cuándo generar el archivo vs. responder en el chat

- Si el usuario pide explícitamente "créame un archivo .md" o "quiero un archivo aparte" → generar el archivo con `create_file` y compartirlo.
- Si solo pide "explícame X" sin mencionar archivo → responder primero en el chat con este mismo formato, y ofrecer crear el archivo después si lo confirma.

## Checklist final antes de entregar la nota

- [ ] ¿Tiene la sección `## La analogía general` al principio?
- [ ] ¿Cada sección técnica tiene su bloque `> **Analogía:**` correspondiente?
- [ ] ¿Hay al menos una tabla resumen?
- [ ] ¿Se compara con herramientas/conceptos ya cubiertos antes, si aplica?
- [ ] ¿Cierra con una sección de "por qué esto importa" hacia el siguiente tema?
