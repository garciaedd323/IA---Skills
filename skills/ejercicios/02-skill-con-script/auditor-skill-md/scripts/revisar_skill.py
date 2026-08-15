#!/usr/bin/env python3
"""Audita un archivo SKILL.md: frontmatter valido, description presente, y longitud."""

import sys
from pathlib import Path

LIMITE_LINEAS = 500


def leer_frontmatter(lineas):
    """Separa el bloque de frontmatter (entre '---' y '---') del resto del archivo."""
    if not lineas or lineas[0].strip() != "---":
        return None, lineas

    fin = None
    for i in range(1, len(lineas)):
        if lineas[i].strip() == "---":
            fin = i
            break

    if fin is None:
        return None, lineas

    return lineas[1:fin], lineas[fin + 1:]


def buscar_campo(frontmatter, nombre):
    """Busca un campo simple tipo 'nombre: valor' dentro del frontmatter."""
    for linea in frontmatter:
        if linea.strip().startswith(f"{nombre}:"):
            return linea.split(":", 1)[1].strip()
    return None


def main():
    if len(sys.argv) != 2:
        print("Uso: python revisar_skill.py <ruta-al-SKILL.md>")
        sys.exit(1)

    ruta = Path(sys.argv[1])
    if not ruta.is_file():
        print(f"No se encontro el archivo: {ruta}")
        sys.exit(1)

    lineas = ruta.read_text(encoding="utf-8").splitlines()
    frontmatter, _cuerpo = leer_frontmatter(lineas)

    problemas = []
    avisos = []

    if frontmatter is None:
        problemas.append("No se encontro un bloque de frontmatter valido (debe empezar y terminar con '---').")
    else:
        description = buscar_campo(frontmatter, "description")
        if not description:
            problemas.append("Falta el campo 'description' (o esta vacio) - sin el, Claude no sabe cuando usar esta skill.")
        elif len(description) < 20:
            avisos.append(f"El 'description' es muy corto ({len(description)} caracteres) - puede no alcanzar para que Claude decida activarla.")

    if len(lineas) > LIMITE_LINEAS:
        avisos.append(f"El archivo tiene {len(lineas)} lineas, por encima de las {LIMITE_LINEAS} recomendadas. Conviene mover detalle a archivos de referencia aparte.")

    print(f"Revisando: {ruta}")
    print(f"Lineas totales: {len(lineas)}")
    print()

    if not problemas and not avisos:
        print("No se encontraron problemas.")
    else:
        if problemas:
            print("Problemas:")
            for p in problemas:
                print(f"  - {p}")
        if avisos:
            print("Avisos:")
            for a in avisos:
                print(f"  - {a}")

    sys.exit(1 if problemas else 0)


if __name__ == "__main__":
    main()
