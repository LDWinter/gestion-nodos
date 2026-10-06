"""Configuración del sistema.

MODULOS: los módulos activos, EN ORDEN (un módulo va después de los que necesita).
Para quitar uno, borralo de la lista; para agregar uno nuevo, creá su carpeta en nodos/modulos/ y sumalo acá.
"""
MODULOS = ["tipos", "lotes", "relaciones", "grafo", "historial"]

# Archivo de la base de datos que usa la aplicación (los tests usan una base en memoria).
RUTA_BASE = "nodos.db"
