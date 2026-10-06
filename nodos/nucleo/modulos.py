"""Carga de módulos. Cada módulo es una carpeta dentro de nodos/modulos/ con:

    __init__.py   → DEPENDE_DE = [...] y las funciones públicas del módulo
    servicio.py   → la lógica (funciones que usan la base de datos)
    rutas.py      → (opcional) las rutas web del módulo: un Blueprint de Flask llamado `bp`
    esquema.sql   → (opcional) las tablas que el módulo necesita

Para AGREGAR un módulo: crear su carpeta y sumarlo a MODULOS en nodos/config.py.
Para QUITAR un módulo: sacarlo de MODULOS (los que dependan de él avisan con un error claro).
"""
import importlib

from nodos import config


def cargar(nombres=None):
    """Importa los módulos indicados (por defecto, los de config.MODULOS) y revisa sus dependencias.
    Devuelve la lista de módulos ya importados, en el mismo orden."""
    nombres = list(config.MODULOS if nombres is None else nombres)
    modulos = []
    for nombre in nombres:
        modulo = importlib.import_module(f"nodos.modulos.{nombre}")
        for dependencia in getattr(modulo, "DEPENDE_DE", []):
            if dependencia not in nombres[: nombres.index(nombre)]:
                raise RuntimeError(
                    f"el módulo '{nombre}' necesita '{dependencia}' activo y cargado antes en config.MODULOS")
        modulos.append(modulo)
    return modulos
