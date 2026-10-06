"""La bitácora: cada acción que modifica algo se anota acá (tabla `registro`)."""
import json


def registrar(conn, usuario, accion, lote_id=None, detalle=None):
    """Anota una acción. No hace commit: lo hace la función que llamó, junto con su propio cambio."""
    conn.execute(
        "INSERT INTO registro (usuario, accion, lote_id, detalle) VALUES (?, ?, ?, ?)",
        (usuario, accion, lote_id, json.dumps(detalle or {}, ensure_ascii=False)),
    )
