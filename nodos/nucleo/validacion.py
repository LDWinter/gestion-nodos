from datetime import date
from typing import List, Any

def validar_contenido(campos: List[dict], contenido: Any) -> List[str]:
    if not isinstance(contenido, dict):
        return ["el contenido debe ser un objeto JSON"]

    errores = []
    campos_declarados = {c['nombre']: c for c in campos}

    for campo in campos:
        nombre = campo['nombre']
        tipo_esperado = campo['tipo']
        obligatorio = campo.get('obligatorio', False)

        if nombre not in contenido:
            if obligatorio:
                errores.append(f"{nombre} es obligatorio")
            continue

        valor = contenido[nombre]

        valido_tipo = True
        if tipo_esperado == "texto":
            if not isinstance(valor, str):
                valido_tipo = False
        elif tipo_esperado == "numero":
            if not isinstance(valor, (int, float)) or isinstance(valor, bool):
                valido_tipo = False
        elif tipo_esperado == "fecha":
            if not isinstance(valor, str):
                valido_tipo = False
            else:
                try:
                    date.fromisoformat(valor)
                except ValueError:
                    valido_tipo = False
        elif tipo_esperado == "booleano":
            if not isinstance(valor, bool):
                valido_tipo = False
        elif tipo_esperado == "lista":
            if not isinstance(valor, list):
                valido_tipo = False

        if not valido_tipo:
            errores.append(f"El campo '{nombre}' tiene un tipo incorrecto (esperado {tipo_esperado})")

    for clave in contenido:
        if clave not in campos_declarados:
            errores.append(f"La clave '{clave}' no está en campos")

    return errores
