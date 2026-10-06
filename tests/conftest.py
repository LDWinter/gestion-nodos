import pytest
from nodos import db, repositorio as repo

CAMPOS_CLIENTE = [
    {"nombre": "razon_social", "tipo": "texto", "obligatorio": True},
    {"nombre": "empleados", "tipo": "numero", "obligatorio": False},
]


@pytest.fixture
def conn():
    c = db.conectar(":memory:")
    db.crear_esquema(c)
    yield c
    c.close()


@pytest.fixture
def datos(conn):
    """Un tipo 'cliente' y dos lotes A y B."""
    t = repo.crear_tipo(conn, "cliente", CAMPOS_CLIENTE, "ana")
    a = repo.crear_lote(conn, t, "A", {"razon_social": "Acme"}, "ana")
    b = repo.crear_lote(conn, t, "B", {"razon_social": "Beta", "empleados": 3}, "ana")
    return {"tipo": t, "a": a, "b": b}
