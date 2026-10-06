import psycopg
import pytest
from psycopg.types.json import Jsonb

TABLAS = {"usuarios", "proyectos", "miembros", "tipos_lote", "nodos", "relaciones", "commits", "cambios"}


def _base(conn):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO usuarios (nombre, email) VALUES ('Ana', 'ana@x.com') RETURNING id")
        u = cur.fetchone()[0]
        cur.execute("INSERT INTO proyectos (nombre, creado_por) VALUES ('P1', %s) RETURNING id", (u,))
        p = cur.fetchone()[0]
        cur.execute("INSERT INTO tipos_lote (nombre, campos) VALUES ('cliente', %s) RETURNING id",
                    (Jsonb([{"nombre": "razon_social", "tipo": "texto", "obligatorio": True}]),))
        t = cur.fetchone()[0]
        ids = []
        for titulo in ("A", "B"):
            cur.execute("INSERT INTO nodos (proyecto_id, tipo_lote_id, titulo, contenido, creado_por) "
                        "VALUES (%s, %s, %s, %s, %s) RETURNING id", (p, t, titulo, Jsonb({"razon_social": titulo}), u))
            ids.append(cur.fetchone()[0])
    return u, p, t, ids


def test_tablas_existen(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        assert TABLAS <= {r[0] for r in cur.fetchall()}


def test_crear_esquema_es_idempotente(conn):
    from nodos import db
    db.crear_esquema(conn)


def test_defaults_nodo(conn):
    _, _, _, (a, _) = _base(conn)
    with conn.cursor() as cur:
        cur.execute("SELECT version, borrado, creado_en IS NOT NULL FROM nodos WHERE id=%s", (a,))
        assert cur.fetchone() == (1, False, True)


def test_relacion_unica_y_sin_lazo(conn):
    u, _, _, (a, b) = _base(conn)
    with conn.cursor() as cur:
        cur.execute("INSERT INTO relaciones (origen_id, destino_id, tipo, creado_por) VALUES (%s,%s,'referencia',%s)", (a, b, u))
        with pytest.raises(psycopg.errors.UniqueViolation):
            cur.execute("INSERT INTO relaciones (origen_id, destino_id, tipo, creado_por) VALUES (%s,%s,'referencia',%s)", (a, b, u))
    conn.rollback()
    u, _, _, (a, b) = _base(conn)
    with conn.cursor() as cur, pytest.raises(psycopg.errors.CheckViolation):
        cur.execute("INSERT INTO relaciones (origen_id, destino_id, tipo, creado_por) VALUES (%s,%s,'referencia',%s)", (a, a, u))


def test_rol_invalido(conn):
    u, p, _, _ = _base(conn)
    with conn.cursor() as cur, pytest.raises(psycopg.errors.CheckViolation):
        cur.execute("INSERT INTO miembros (proyecto_id, usuario_id, rol) VALUES (%s,%s,'jefe')", (p, u))


def test_commit_y_cambio(conn):
    u, p, _, (a, _) = _base(conn)
    with conn.cursor() as cur:
        cur.execute("INSERT INTO commits (proyecto_id, autor_id, mensaje) VALUES (%s,%s,'alta') RETURNING id, estado", (p, u))
        c, estado = cur.fetchone()
        assert estado == "pendiente"
        cur.execute("INSERT INTO cambios (commit_id, nodo_id, operacion, despues) VALUES (%s,%s,'crear_nodo',%s)",
                    (c, a, Jsonb({"razon_social": "A"})))
        with pytest.raises(psycopg.errors.CheckViolation):
            cur.execute("INSERT INTO cambios (commit_id, nodo_id, operacion) VALUES (%s,%s,'romper')", (c, a))
