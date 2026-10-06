"""Tests de la arquitectura modular: se pueden quitar módulos y las dependencias se revisan."""
import pytest
from nodos.nucleo import db
from nodos.nucleo.modulos import cargar


def _tablas(conn):
    return {f[0] for f in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}


def test_solo_modulos_elegidos_crean_tablas():
    conn = db.conectar()
    db.crear_esquema(conn, ["tipos", "lotes"])
    assert _tablas(conn) == {"registro", "tipos_lote", "lotes"}   # sin 'relaciones'


def test_todos_los_modulos():
    conn = db.conectar()
    db.crear_esquema(conn)
    assert _tablas(conn) == {"registro", "tipos_lote", "lotes", "relaciones"}


def test_dependencia_faltante_avisa():
    with pytest.raises(RuntimeError, match="tipos"):
        cargar(["lotes"])          # lotes necesita tipos


def test_dependencia_en_orden_incorrecto_avisa():
    with pytest.raises(RuntimeError):
        cargar(["lotes", "tipos"])  # tipos tiene que ir antes


def test_app_sin_modulo_historial():
    from nodos.app import crear_app
    cliente = crear_app(":memory:", ["tipos", "lotes", "relaciones", "grafo"]).test_client()
    assert cliente.get("/api/historial").status_code == 404   # la ruta no existe si el módulo no está
    assert cliente.get("/api/grafo").status_code == 200
