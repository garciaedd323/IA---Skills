# ¿Qué son las Skills de una IA? (usando Claude como ejemplo)

## La analogía general

Imagina que contratas a un asistente brillante y con mucho conocimiento general — sabe de casi todo, pero **nunca ha trabajado en tu empresa específica**. El primer día, es capaz pero genérico: si le pides "hazme un documento de Word profesional", probablemente lo haga razonablemente bien, pero sin conocer los trucos específicos que tu empresa ya aprendió a las malas (qué formato evitar, qué plantilla usar, qué errores son comunes en ese tipo de documento).

Una **Skill** es como entregarle a ese asistente **el manual de procedimientos de un oficio específico**, antes de que empiece la tarea — no se le enseña "todo de cero", se le da el atajo de la experiencia ya acumulada por otros, para que no tenga que reinventar el enfoque cada vez.

---

## 1. Qué es una Skill, técnicamente

Una Skill es una **carpeta** con, como mínimo, un archivo llamado `SKILL.md`, que contiene:

```
mi-skill/
├── SKILL.md (obligatorio)
│   ├── Frontmatter YAML (description — recomendado; name — opcional, si falta se usa el nombre de la carpeta)
│   └── Instrucciones en Markdown
└── Recursos empaquetados (opcionales)
    ├── scripts/     — código ejecutable para tareas repetitivas/deterministas
    ├── references/  — documentación que se carga solo cuando se necesita
    └── assets/      — archivos usados en el resultado final (plantillas, íconos, fuentes)
```

> **Analogía:** el `SKILL.md` es el manual de procedimientos en sí — la portada (`name` + `description`) es como el título y el resumen en el lomo del manual, que dice de qué trata sin tener que abrirlo. El cuerpo del documento son las instrucciones detalladas. Y las carpetas opcionales (`scripts/`, `references/`, `assets/`) son como los anexos del manual: herramientas específicas, documentos de consulta, y plantillas que solo se sacan cuando realmente se necesitan, no se cargan todas de entrada.

---

## 2. El `description` es la parte más importante (y la más subestimada)

```yaml
---
name: generador-reportes-ventas
description: Genera reportes de ventas mensuales con gráficos y tablas comparativas. Usar esta skill cuando el usuario mencione reportes de ventas, análisis mensual, comparativos de ingresos, o pida visualizar datos comerciales, incluso si no dice la palabra "reporte" explícitamente.
---
```

El `description` no es solo una etiqueta decorativa — es **el mecanismo principal por el cual la IA decide cuándo usar esa Skill**. Si el `description` es vago o muy corto, la Skill puede existir perfectamente bien pero **nunca activarse** cuando debería.

> **Analogía:** es como el índice de materias de una biblioteca enorme. Si el manual de "cómo arreglar una fuga de agua" está catalogado solo como "Documento #4521", nadie lo va a encontrar cuando tenga una fuga real, aunque el contenido adentro sea perfecto. El `description` es la ficha del catálogo — tiene que decir explícitamente "usar esto cuando pase X, Y o Z", no solo "documento sobre plomería".

---

## 3. Carga progresiva — por qué esto es más inteligente de lo que parece

Las Skills no se cargan "todas de una" en la memoria de la IA. Funcionan en **tres niveles**:

| Nivel | Qué se carga | Cuándo |
|---|---|---|
| 1. Metadata (`name` + `description`) | ~100 palabras | Siempre, para todas las Skills disponibles |
| 2. Cuerpo del `SKILL.md` | Hasta ~500 líneas | Solo cuando esa Skill específica se activa |
| 3. Recursos empaquetados (`scripts/`, `references/`, `assets/`) | Sin límite | Solo si el cuerpo del SKILL.md indica que hacen falta |

> **Analogía:** es como un archivo de oficina bien organizado. En el escritorio (nivel 1) solo están los **títulos** de todas las carpetas disponibles — no hace falta leer cada carpeta completa para saber que existe. Cuando una tarea específica lo requiere, **se abre esa carpeta puntual** (nivel 2) y se lee su contenido principal. Y si esa carpeta menciona "revisa el anexo B para el detalle técnico", **recién ahí** se va por el anexo (nivel 3) — no antes, porque cargar todos los anexos de todas las carpetas desde el principio sería un desorden innecesario.

Esto es clave para que una IA pueda tener **cientos de Skills disponibles** sin que eso sature su contexto — solo "paga el costo" de leer completa la Skill que realmente necesita en ese momento.

---

## 4. Ejemplo real de funcionamiento (para que no sea abstracto)

Un caso concreto: cuando una IA como Claude genera un documento de Word, PowerPoint o PDF, existe una Skill específica para cada formato — antes de escribir una sola línea de código, se revisa el `SKILL.md` correspondiente, que indica cosas como "usa esta librería específica", "evita este error común de formato", "esta es la estructura recomendada". Sin esa Skill, el modelo tendría que adivinar basándose solo en lo que aprendió de forma general durante el entrenamiento — que puede estar incompleto, o desactualizado frente a la mejor práctica actual.

---

## 5. El "Principio de no sorpresa"

Una Skill nunca debería hacer algo distinto a lo que su descripción promete — no puede contener instrucciones maliciosas, ni comportamientos ocultos que sorprendan a quien la usa. Si una Skill dice "genera reportes de ventas", no debería aprovechar esa confianza para hacer algo no relacionado ni dañino por debajo.

> **Analogía:** es como la caja de un electrodoméstico — si dice "licuadora" en la caja, no debería sorprender que también sea una aspiradora escondida. La descripción y el comportamiento real deben coincidir siempre.

---

## 6. Tabla resumen

| Concepto | Una frase para recordarlo |
|---|---|
| `SKILL.md` | El manual de procedimientos de un oficio específico |
| `description` | El índice de catálogo — decide cuándo se activa la Skill |
| Carga progresiva | Solo se lee completo lo que realmente se necesita, cuando se necesita |
| `scripts/` | Herramientas ejecutables para tareas repetitivas |
| `references/` | Documentación de consulta, cargada solo si hace falta |
| `assets/` | Plantillas/archivos usados en el resultado final |
| Principio de no sorpresa | La Skill hace exactamente lo que su descripción promete, nada más |

---

## 7. Por qué esto importa antes de crear una Skill propia

Entender estas piezas (el `description` como mecanismo de activación, la carga progresiva, y qué va en cada carpeta opcional) es la base para el siguiente paso natural: construir una Skill propia desde cero, con una intención clara de qué debe hacer y cuándo debe activarse.

---

> **Corrección (verificada contra la documentación oficial):** esta nota decía originalmente que `name` y `description` eran ambos obligatorios en el frontmatter. En realidad, solo `description` es recomendado (ni siquiera obligatorio en sentido estricto), y `name` es opcional — si falta, se usa el nombre de la carpeta de la skill. El frontmatter, además, admite muchos más campos además de estos dos (por ejemplo `allowed-tools`, `disable-model-invocation`, `argument-hint`, `context: fork`), vistos en la práctica en el taller [Una Skill que incluye un script](../ejercicios/02-skill-con-script/GUIA.md).
