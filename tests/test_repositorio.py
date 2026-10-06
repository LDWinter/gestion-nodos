import pytest
from nodos import repositorio as repo
from nodos.nucleo import db


def test_esquema_idempotente(conn):
    db.crear_esquema(conn)


def test_crear_y_obtener_lote(conn, datos):
    lote = repo.obtener_lote(conn, datos["a"])
    assert lote["titulo"] == "A" and lote["tipo"] == "cliente"
    assert lote["contenido"] == {"razon_social": "Acme"}
    assert lote["version"] == 1 and lote["borrado"] is False


def test_obtener_inexistente(conn):
    assert repo.obtener_lote(conn, 999) is None


def test_tipo_duplicado(conn, datos):
    with pytest.raises(ValueError):
        repo.crear_tipo(conn, "cliente", [], "ana")


def test_listar_tipos(conn, datos):
    tipos = repo.listar_tipos(conn)
    assert tipos[0]["nombre"] == "cliente" and tipos[0]["campos"][0]["nombre"] == "razon_social"


def test_lote_invalido(conn, datos):
    with pytest.raises(ValueError):
        repo.crear_lote(conn, datos["tipo"], "X", {"empleados": 2}, "ana")
    with pytest.raises(ValueError):
        repo.crear_lote(conn, 999, "X", {"razon_social": "x"}, "ana")


def test_editar_lote(conn, datos):
    v = repo.editar_lote(conn, datos["a"], "beto", contenido={"razon_social": "Acme SA"})
    assert v == 2
    lote = repo.obtener_lote(conn, datos["a"])
    assert lote["contenido"]["razon_social"] == "Acme SA" and lote["titulo"] == "A"
    h = repo.historial(conn, datos["a"])[0]
    assert h["accion"] == "editar_lote" and h["usuario"] == "beto"
    assert h["detalle"]["antes"]["contenido"] == {"razon_social": "Acme"}
    assert h["detalle"]["despues"]["contenido"] == {"razon_social": "Acme SA"}


def test_editar_invalido_no_cambia(conn, datos):
    with pytest.raises(ValueError):
        repo.editar_lote(conn, datos["a"], "beto", contenido={"color": "rojo"})
    assert repo.obtener_lote(conn, datos["a"])["version"] == 1


def test_listar_lotes(conn, datos):
    assert [l["titulo"] for l in repo.listar_lotes(conn)] == ["A", "B"]
    assert repo.listar_lotes(conn, tipo_id=999) == []


def test_relacionar_y_vecinos(conn, datos):
    r = repo.relacionar(conn, datos["a"], datos["b"], "referencia", "ana")
    va = repo.vecinos(conn, datos["a"])
    assert va == [{"relacion_id": r, "tipo": "referencia", "direccion": "sale", "lote": {"id": datos["b"], "titulo": "B"}}]
    assert repo.vecinos(conn, datos["b"])[0]["direccion"] == "entra"


@pytest.mark.parametrize("caso", ["mismo", "duplicada", "inexistente"])
def test_relaciones_invalidas(conn, datos, caso):
    a, b = datos["a"], datos["b"]
    repo.relacionar(conn, a, b, "referencia", "ana")
    args = {"mismo": (a, a), "duplicada": (a, b), "inexistente": (a, 999)}[caso]
    with pytest.raises(ValueError):
        repo.relacionar(conn, *args, "referencia", "ana")


def test_quitar_relacion(conn, datos):
    r = repo.relacionar(conn, datos["a"], datos["b"], "referencia", "ana")
    repo.quitar_relacion(conn, r, "ana")
    assert repo.vecinos(conn, datos["a"]) == []
    with pytest.raises(ValueError):
        repo.quitar_relacion(conn, r, "ana")


def test_borrar_lote(conn, datos):
    repo.relacionar(conn, datos["a"], datos["b"], "referencia", "ana")
    repo.borrar_lote(conn, datos["a"], "ana")
    assert repo.obtener_lote(conn, datos["a"])["borrado"] is True
    assert [l["titulo"] for l in repo.listar_lotes(conn)] == ["B"]
    assert repo.vecinos(conn, datos["b"]) == []
    with pytest.raises(ValueError):
        repo.editar_lote(conn, datos["a"], "ana", titulo="Z")
    with pytest.raises(ValueError):
        repo.relacionar(conn, datos["b"], datos["a"], "referencia", "ana")


def test_grafo(conn, datos):
    r = repo.relacionar(conn, datos["a"], datos["b"], "parte_de", "ana")
    g = repo.grafo(conn)
    assert {n["titulo"] for n in g["nodos"]} == {"A", "B"} and g["nodos"][0]["tipo"] == "cliente"
    assert g["aristas"] == [{"id": r, "origen": datos["a"], "destino": datos["b"], "tipo": "parte_de"}]


def test_registro_de_todo(conn, datos):
    r = repo.relacionar(conn, datos["a"], datos["b"], "referencia", "ana")
    repo.quitar_relacion(conn, r, "ana")
    repo.borrar_lote(conn, datos["b"], "ana")
    acciones = [h["accion"] for h in repo.historial(conn)]
    assert acciones == ["borrar_lote", "quitar_relacion", "relacionar", "crear_lote", "crear_lote", "crear_tipo"]
    alta = repo.historial(conn, datos["a"])[-1]
    assert alta["accion"] == "crear_lote" and alta["detalle"]["despues"]["contenido"] == {"razon_social": "Acme"}
