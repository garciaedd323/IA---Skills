---
description: Genera un mensaje de commit en espanol, en minuscula y en modo imperativo, a partir de los cambios que el usuario describe. Usar esta skill cuando el usuario pida ayuda para escribir el mensaje de un commit de git, o pregunte como resumir sus cambios para un commit.
---

# Generador de mensaje de commit

Cuando el usuario describa los cambios que acaba de hacer y pida ayuda con el mensaje del commit:

1. Resumir el cambio en una sola linea, en espanol, en minuscula, en modo imperativo (por ejemplo "agregar", "corregir", "actualizar", "eliminar"), sin punto final.
2. Si el cambio tiene mas de un aspecto relevante, agregar un cuerpo de una o dos lineas debajo del titulo, separado por una linea en blanco.
3. No inventar detalles que el usuario no haya mencionado explicitamente.
