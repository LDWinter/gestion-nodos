from datetime import datetime
from typing import List, Any

def validar_contenido(campos: List[dict], contenido: Any) -> List[str]:
    errores = []

    if not isinstance(contenido, dict):
        return ["El contenido debe ser un objeto JSON (diccionario)"]

    # Campos declarados en el tipo de lote
    campos_declarados = {c['nombre']: c for c in campos}

    # Verificar campos obligatorios y tipos
    for campo in campos:
        nombre = campo['nombre']
        tipo_esperado = campo['tipo']
        obligatorio = campo.get('obligatorio', False)

        if nombre not in contenido:
            if obligatorio:
                errores.append(f"Falta el campo obligatorio: {nombre}")
            continue

        valor = contenido[nombre]

        # Validar tipo
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
                    datetime.date.fromisoformat(valor)
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

    # Verificar campos no declarados
    for nombre_contenido in contenido:
        if nombre_contenido not in campos_declarados:
            errores.append(f"El campo '{nombre_contenido}' no está declarado en el tipo de lote")

    return errores
