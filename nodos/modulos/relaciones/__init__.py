"""Módulo RELACIONES: las flechas que unen lotes."""
DEPENDE_DE = ["lotes"]
from nodos.nucleo import eventos  # noqa: E402
from .servicio import relacionar, quitar_relacion, vecinos, al_borrar_lote  # noqa: E402,F401

# Cuando el módulo lotes avise que borró un lote, quitamos sus flechas.
eventos.suscribir("lote_borrado", al_borrar_lote)
