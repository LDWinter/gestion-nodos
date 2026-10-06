"""Lógica del módulo lotes."""
import json

from nodos.nucleo import eventos
from nodos.nucleo.registro import registrar
from nodos.nucleo.validacion import validar_contenido
from nodos.modulos.tipos import campos_del_tipo


def _validar(conn, tipo_id, contenido):
    errores = validar_contenido(campos_del_tipo(conn, tipo_id), contenido)
    if errores:
        raise ValueError("; ".join(errores))


def _foto(lote):
    """Lo que se guarda en el registro como 'antes' o 'después' de un lote."""
    return {"titulo": lote["titulo"], "contenido": lote["contenido"]}


def crear_lote(conn, tipo_id, titulo, contenido, usuario):
    """Valida el contenido contra su tipo y crea el lote. Devuelve el id nuevo."""
    _validar(conn, tipo_id, contenido)
    cur = conn.execute("INSERT INTO lotes (tipo_id, titulo, contenido) VALUES (?, ?, ?)",
                       (tipo_id, titulo, json.dumps(contenido, ensure_ascii=False)))
    registrar(conn, usuario, "crear_lote", cur.lastrowid,
              {"despues": {"titulo": titulo, "contenido": contenido}})
    conn.commit()
    return cur.lastrowid


def obtener_lote(conn, lote_id):
    """Devuelve un lote como diccionario (incluye el nombre de su tipo), o None si no existe."""
    f = conn.execute(
        """SELECT l.*, t.nombre AS tipo FROM lotes l
           JOIN tipos_lote t ON t.id = l.tipo_id WHERE l.id = ?""", (lote_id,)).fetchone()
    if f is None:
        return None
    return {"id": f["id"], "tipo_id": f["tipo_id"], "tipo": f["tipo"], "titulo": f["titulo"],
            "contenido": json.loads(f["contenido"]), "version": f["version"],
            "borrado": bool(f["borrado"]), "creado_en": f["creado_en"],
            "actualizado_en": f["actualizado_en"]}


def lote_vivo(conn, lote_id):
    """Devuelve el lote si existe y no está borrado; si no, lanza ValueError.
    Otros módulos (por ejemplo relaciones) la usan para verificar lotes."""
    lote = obtener_lote(conn, lote_id)
    if lote is None or lote["borrado"]:
        raise ValueError(f"el lote {lote_id} no existe")
    return lote


def listar_lotes(conn, tipo_id=None):
    """Lista los lotes no borrados (opcionalmente de un solo tipo), ordenados por id."""
    sql = "SELECT id FROM lotes WHERE borrado = 0"
    params = ()
    if tipo_id is not None:
        sql += " AND tipo_id = ?"
        params = (tipo_id,)
    return [obtener_lote(conn, f["id"]) for f in conn.execute(sql + " ORDER BY id", params)]


def editar_lote(conn, lote_id, usuario, titulo=None, contenido=None):
    """Cambia el título y/o el contenido, sube la versión y registra antes/después.
    Devuelve el número de versión nuevo."""
    lote = lote_vivo(conn, lote_id)
    nuevo_titulo = lote["titulo"] if titulo is None else titulo
    nuevo_contenido = lote["contenido"] if contenido is None else contenido
    _validar(conn, lote["tipo_id"], nuevo_contenido)
    nueva_version = lote["version"] + 1
    conn.execute(
        """UPDATE lotes SET titulo = ?, contenido = ?, version = ?, actualizado_en = CURRENT_TIMESTAMP
           WHERE id = ?""",
        (nuevo_titulo, json.dumps(nuevo_contenido, ensure_ascii=False), nueva_version, lote_id))
    registrar(conn, usuario, "editar_lote", lote_id,
              {"antes": _foto(lote), "despues": {"titulo": nuevo_titulo, "contenido": nuevo_contenido}})
    conn.commit()
    return nueva_version


def borrar_lote(conn, lote_id, usuario):
    """Borrado lógico: marca el lote como borrado. Emite el evento "lote_borrado" para que otros
    módulos limpien lo suyo (por ejemplo, relaciones quita las flechas del lote)."""
    lote = lote_vivo(conn, lote_id)
    eventos.emitir("lote_borrado", conn, lote_id=lote_id)
    conn.execute("UPDATE lotes SET borrado = 1, actualizado_en = CURRENT_TIMESTAMP WHERE id = ?", (lote_id,))
    registrar(conn, usuario, "borrar_lote", lote_id, {"antes": _foto(lote)})
    conn.commit()
