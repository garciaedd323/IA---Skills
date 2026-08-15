# Cómo distribuir un marketplace de plugins entre computadoras distintas

## La analogía general

Dos personas, cada una en su propia casa. Una de ellas tiene, en la cocina de su propia casa, una carpeta con varias recetas ya armadas y probadas (los plugins). La otra persona quiere esas recetas en su propia cocina. Decirle "están en el cajón de la izquierda de mi cocina" no le sirve de nada — ese cajón solo existe en esa casa. Para que la receta llegue a la otra cocina, hace falta algo que ambas casas puedan alcanzar: un correo, una plataforma compartida, algo publicado. Una ruta local a un plugin funciona exactamente igual — solo tiene sentido dentro de la misma casa (la misma computadora).

---

## 1. El punto central: una ruta local no cruza de una computadora a otra

Todo lo que se armó en [Skills sueltas vs Skills empaquetadas en un plugin](./skills-como-plugin.md) usaba una ruta local para el marketplace (`./mi-marketplace`, `./taller-marketplace`). Eso funciona perfecto mientras quien crea el marketplace y quien lo instala están, literalmente, sentados frente a la misma máquina, con acceso al mismo disco.

En el momento en que se trata de dos computadoras distintas, esa ruta deja de significar nada para la segunda persona — no hay ningún disco compartido entre ambas. Para que el marketplace sea instalable desde otra máquina, tiene que estar publicado en algo alcanzable por red: típicamente, un repositorio de git hosteado (GitHub, GitLab, un servidor propio).

> **Analogía:** una ruta local es como decir "andá al tercer cajón de mi cocina" — una instrucción perfectamente válida, pero solo para quien ya está parado en esa cocina. No importa cuán clara sea la instrucción si la otra persona vive en otra ciudad.

---

## 2. El flujo real, con dos personas separadas

### Persona A (quien crea y publica los plugins)

Convierte la carpeta del marketplace en un repositorio de git:

```bash
cd mis-plugins
git init
git add .
git commit -m "coleccion inicial de plugins"
```

La sube a GitHub:

```bash
gh repo create mis-plugins --public --source=. --push
```

(o, sin la herramienta `gh`: crear el repositorio vacío desde github.com, y después `git remote add origin https://github.com/mi-usuario/mis-plugins.git` seguido de `git push -u origin main`)

Y le pasa a la Persona B solo un dato: el identificador `mi-usuario/mis-plugins`. Nada más — no hace falta enviar archivos, ni carpetas, ni explicar rutas.

### Persona B (quien instala)

Abre Claude Code:

```bash
claude
```

Agrega el marketplace usando ese identificador:

```
/plugin marketplace add mi-usuario/mis-plugins
```

Instala el plugin específico que le interesa (no hace falta instalar todos los que el catálogo ofrezca):

```
/plugin install commit-helper@mis-plugins
```

Si el resumen de instalación indica `Run /reload-plugins to activate.`, corre ese comando. Confirma que cargó revisando `/help` → pestaña **Custom commands**, donde debería aparecer `commit-helper:generador-mensaje-commit`. Y lo prueba con un pedido real.

> **Analogía:** esto es el equivalente de subir la receta a un sitio de recetas público y mandarle a la otra persona solo el link — no el archivo, no una foto de la hoja, solo la dirección donde encontrarla. La otra persona la busca, la abre y la cocina en su propia casa, sin haber tenido nunca acceso físico a la cocina original.

---

## 3. Un dato técnico importante: dónde tiene que vivir el `marketplace.json`

El archivo `marketplace.json` tiene que estar en la **raíz** del repositorio de git que se publica — dentro de `.claude-plugin/marketplace.json`, justo en esa raíz. No enterrado varios niveles adentro de un repositorio más grande que contiene otras cosas además del marketplace.

Esto tiene una implicancia concreta y real para este mismo repositorio: el taller construido en [`skills/ejercicios/01-skill-como-plugin/taller-marketplace/`](../ejercicios/01-skill-como-plugin/taller-marketplace/) **no funcionaría** si alguien intentara instalarlo de verdad con `/plugin marketplace add usuario/IA---Skills`, porque su `marketplace.json` queda anidado varios niveles adentro de este repositorio (`skills/ejercicios/01-skill-como-plugin/taller-marketplace/.claude-plugin/marketplace.json`), no en la raíz de `IA---Skills`. Para que ese taller fuera instalable de verdad por otra persona, la carpeta `taller-marketplace/` tendría que publicarse como su **propio repositorio separado**, con su propio `.claude-plugin/marketplace.json` en la raíz de ese repositorio nuevo — no como una subcarpeta de este.

Esto no invalida el taller como ejercicio de aprendizaje (sigue funcionando perfecto con `--plugin-dir` y con `/plugin marketplace add ./ruta/local`, ambos probados desde la misma máquina), pero es una limitación real que conviene tener presente antes de asumir que "ya está listo para compartir con cualquiera".

> **Analogía:** es la diferencia entre tener la receta en la primera página de un libro propio, dedicado solo a esa receta, versus tenerla escrita en el medio de un cuaderno enorme que mezcla recetas con anotaciones de otras cosas. Alguien que busca "el libro de recetas" en la estantería espera encontrar la portada ahí mismo, no tener que hojear un cuaderno ajeno para encontrarla en el medio.

---

## 4. Variante: sin hacerlo público

El mismo flujo funciona igual con un repositorio **privado** de GitHub. La única diferencia es que la Persona B necesita tener acceso a ese repositorio — como colaboradora, o perteneciendo a la misma organización — para que `git` pueda clonarlo usando sus propias credenciales.

> **Analogía:** es la diferencia entre publicar la receta en un sitio abierto a cualquiera, o compartirla en un grupo cerrado donde solo entran las personas que uno invitó expresamente.

---

## 5. Alternativa sin git, para algo rápido y descartable

Si no hace falta nada permanente ni instalable — por ejemplo, para probar algo una sola vez — alcanza con comprimir la carpeta del plugin puntual (no el marketplace completo) en un `.zip`, y enviarlo por cualquier medio: correo, un servicio de archivos, un USB. Quien lo recibe lo descomprime y corre:

```bash
claude --plugin-dir ./nombre-del-plugin
```

directamente, sin pasar por ningún marketplace.

La contra de este camino: no hay namespacing permanente ni una instalación real registrada en ningún lado. Cada vez que se quiera usar ese plugin, hay que volver a repetir el flag `--plugin-dir` apuntando a esa carpeta, y no existe ningún mecanismo de actualización automática — si la Persona A corrige algo, hay que volver a mandar el `.zip` entero.

> **Analogía:** es como fotocopiar una sola receta suelta y dársela a alguien en mano, en vez de indicarle dónde está publicado el libro completo — rápido y directo, pero esa persona no se entera si la receta se corrige después, y tiene que volver a pedir una fotocopia nueva cada vez.

---

## Tabla resumen

| Situación | Qué sirve | Qué se pierde |
|---|---|---|
| Misma computadora, mismo usuario | Ruta local (`./mis-plugins`) | Nada — es el caso más simple |
| Computadoras distintas, se quiere algo instalable y permanente | Repositorio de git (GitHub u otro host) + `/plugin marketplace add usuario/repo` | Nada, siempre que el `marketplace.json` esté en la raíz de ese repositorio |
| Computadoras distintas, algo rápido y descartable, sin cuenta de git | `.zip` del plugin + `--plugin-dir` | Namespacing permanente, instalación registrada, actualizaciones automáticas |

---

## Por qué esto importa

Con esta nota, el repositorio ya cubre las tres piezas necesarias para entender el ciclo completo: qué es una Skill ([¿Qué son las Skills de una IA?](./que-son-las-skills.md)), qué es un plugin y cómo se empaqueta una Skill adentro ([Skills sueltas vs Skills empaquetadas en un plugin](./skills-como-plugin.md)), y ahora cómo ese plugin llega de verdad de una persona a otra, en computadoras distintas. Queda abierta, sin embargo, la pregunta de seguridad que ya estaba pendiente en el roadmap: instalar el marketplace de otra persona significa confiar en **todo** lo que ese repositorio trae consigo — no solo en la Skill puntual que se quería instalar, sino en cualquier otro plugin, hook o servidor MCP que ese mismo catálogo también ofrezca.
