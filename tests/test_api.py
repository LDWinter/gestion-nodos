import pytest
from nodos.app import crear_app

CAMPOS = [{"nombre": "razon_social", "tipo": "texto", "obligatorio": True}]


@pytest.fixture
def cliente():
    app = crear_app(":memory:")
    app.config["TESTING"] = True
    return app.test_client()


def _alta(cliente):
    t = cliente.post("/api/tipos", json={"nombre": "cliente", "campos": CAMPOS}).get_json()["id"]
    a = cliente.post("/api/lotes", json={"tipo_id": t, "titulo": "A", "contenido": {"razon_social": "Acme"}},
                     headers={"X-Usuario": "ana"}).get_json()["id"]
    b = cliente.post("/api/lotes", json={"tipo_id": t, "titulo": "B", "contenido": {"razon_social": "Beta"}}).get_json()["id"]
    return t, a, b


def test_pagina(cliente):
    r = cliente.get("/")
    assert r.status_code == 200 and b"vis-network" in r.data


def test_alta_y_detalle(cliente):
    t, a, b = _alta(cliente)
    r = cliente.post("/api/relaciones", json={"origen_id": a, "destino_id": b, "tipo": "referencia"})
    assert r.status_code == 201
    d = cliente.get(f"/api/lotes/{a}").get_json()
    assert d["lote"]["titulo"] == "A"
    assert d["vecinos"][0]["lote"]["titulo"] == "B"
    assert d["historial"][-1]["usuario"] == "ana"


def test_grafo_y_tipos(cliente):
    _alta(cliente)
    g = cliente.get("/api/grafo").get_json()
    assert len(g["nodos"]) == 2 and g["aristas"] == []
    assert cliente.get("/api/tipos").get_json()[0]["nombre"] == "cliente"


def test_errores(cliente):
    t, a, _ = _alta(cliente)
    r = cliente.post("/api/lotes", json={"tipo_id": t, "titulo": "X", "contenido": {}})
    assert r.status_code == 400 and "error" in r.get_json()
    assert cliente.post("/api/relaciones", json={"origen_id": a, "destino_id": a, "tipo": "x"}).status_code == 400
    assert cliente.get("/api/lotes/999").status_code == 404


def test_editar_borrar_e_historial(cliente):
    t, a, b = _alta(cliente)
    r = cliente.put(f"/api/lotes/{a}", json={"titulo": "A2"}, headers={"X-Usuario": "beto"})
    assert r.status_code == 200 and r.get_json()["version"] == 2
    rel = cliente.post("/api/relaciones", json={"origen_id": a, "destino_id": b, "tipo": "ref"}).get_json()["id"]
    assert cliente.delete(f"/api/relaciones/{rel}").status_code == 200
    assert cliente.delete(f"/api/lotes/{b}").status_code == 200
    acciones = [h["accion"] for h in cliente.get("/api/historial").get_json()]
    assert acciones[:4] == ["borrar_lote", "quitar_relacion", "relacionar", "editar_lote"]
