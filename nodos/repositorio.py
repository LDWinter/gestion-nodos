"""Fachada: junta en un solo lugar las funciones de todos los módulos.

Sirve para usar el sistema sin saber en qué módulo está cada cosa:
    from nodos import repositorio as repo
    repo.crear_lote(...)
Si un módulo no está instalado, sus funciones simplemente no aparecen acá.
"""
from nodos.nucleo.modulos import cargar

for _modulo in cargar():
    for _nombre in dir(_modulo):
        if not _nombre.startswith("_") and callable(getattr(_modulo, _nombre)):
            globals()[_nombre] = getattr(_modulo, _nombre)
