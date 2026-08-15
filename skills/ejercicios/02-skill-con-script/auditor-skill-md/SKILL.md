---
description: Audita un archivo SKILL.md y reporta si tiene frontmatter valido, si falta el campo description, o si supera las 500 lineas recomendadas. Usar esta skill cuando el usuario pida revisar, auditar o validar una skill propia.
argument-hint: [ruta-al-SKILL.md]
allowed-tools: Bash(python ${CLAUDE_SKILL_DIR}/scripts/revisar_skill.py *)
---

# Auditor de SKILL.md

Cuando el usuario pida auditar un archivo `SKILL.md`:

1. Correr `python ${CLAUDE_SKILL_DIR}/scripts/revisar_skill.py $ARGUMENTS`, donde `$ARGUMENTS` es la ruta al archivo que se quiere revisar.
2. Mostrar el resultado del script, explicando en una frase cada problema o aviso que haya encontrado.
3. Si el script no encuentra nada, confirmarlo brevemente sin agregar mas.
