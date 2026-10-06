"""Módulo LOTES: las fichas de información (crear, ver, editar, borrar)."""
DEPENDE_DE = ["tipos"]
from .servicio import (crear_lote, obtener_lote, listar_lotes, editar_lote,  # noqa: E402,F401
                       borrar_lote, lote_vivo)
