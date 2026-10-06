"""Lógica del módulo historial."""
import json


def historial(conn, lote_id=None):
    """El registro de acciones, del más nuevo al más viejo (opcionalmente solo de un lote)."""
    sql = "SELECT * FROM registro"
    params = ()
    if lote_id is not None:
        sql += " WHERE lote_id = ?"
        params = (lote_id,)
    return [{"id": f["id"], "fecha": f["fecha"], "usuario": f["usuario"], "accion": f["accion"],
             "lote_id": f["lote_id"], "detalle": json.loads(f["detalle"])}
            for f in conn.execute(sql + " ORDER BY id DESC", params)]
