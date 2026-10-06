"""Lógica del módulo tipos."""
import json
import sqlite3

from nodos.nucleo.registro import registrar


def crear_tipo(conn, nombre, campos, usuario):
    """Crea un tipo de lote. `campos` = [{"nombre", "tipo", "obligatorio"}, ...]. Devuelve el id."""
    try:
        cur = conn.execute("INSERT INTO tipos_lote (nombre, campos) VALUES (?, ?)",
                           (nombre, json.dumps(campos, ensure_ascii=False)))
    except sqlite3.IntegrityError:  # UNIQUE(nombre): ya hay un tipo con ese nombre
        raise ValueError(f"ya existe el tipo '{nombre}'")
    registrar(conn, usuario, "crear_tipo", detalle={"nombre": nombre, "campos": campos})
    conn.commit()
    return cur.lastrowid


def listar_tipos(conn):
    """Lista todos los tipos de lote, con sus campos ya convertidos de JSON a lista."""
    filas = conn.execute("SELECT id, nombre, campos FROM tipos_lote ORDER BY id")
    return [{"id": f["id"], "nombre": f["nombre"], "campos": json.loads(f["campos"])} for f in filas]


def campos_del_tipo(conn, tipo_id):
    """Devuelve la lista de campos de un tipo, o lanza ValueError si el tipo no existe."""
    fila = conn.execute("SELECT campos FROM tipos_lote WHERE id = ?", (tipo_id,)).fetchone()
    if fila is None:
        raise ValueError(f"el tipo {tipo_id} no existe")
    return json.loads(fila["campos"])
