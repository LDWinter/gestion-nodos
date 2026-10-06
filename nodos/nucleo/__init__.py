"""Núcleo: lo que el sistema necesita SIEMPRE, sin importar qué módulos estén activos.

- db.py          → abrir la base y crear las tablas (las del núcleo + las de cada módulo activo)
- registro.py    → anotar acciones en la bitácora
- validacion.py  → validar el contenido de un lote contra los campos de su tipo
- eventos.py     → avisos entre módulos sin que dependan entre sí
- modulos.py     → cargar los módulos de la lista de config.py y revisar sus dependencias
"""
