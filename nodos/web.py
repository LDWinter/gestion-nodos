"""Herramientas comunes para las rutas web de los módulos (rutas.py)."""
from flask import current_app, request


def conn():
    """La conexión a la base de datos de la aplicación."""
    return current_app.config["CONN"]


def usuario():
    """Quién hace el pedido: viene en el encabezado HTTP X-Usuario (en la v1 no hay login)."""
    return request.headers.get("X-Usuario", "anonimo")


def datos():
    """El cuerpo JSON del pedido como diccionario (vacío si no vino nada)."""
    return request.get_json(silent=True) or {}
