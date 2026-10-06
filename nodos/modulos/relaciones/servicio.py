"""Lógica del módulo relaciones."""
import sqlite3

from nodos.nucleo.registro import registrar
from nodos.modulos.lotes import lote_vivo


def relacionar(conn, origen_id, destino_id, tipo, usuario):
    """Une dos lotes con una flecha origen → destino. Devuelve el id de la relación."""
    if origen_id == destino_id:
        raise ValueError("un lote no se puede relacionar consigo mismo")
    lote_vivo(conn, origen_id)
    lote_vivo(conn, destino_id)
    try:
        cur = conn.execute("INSERT INTO relaciones (origen_id, destino_id, tipo) VALUES (?, ?, ?)",
                           (origen_id, destino_id, tipo))
    except sqlite3.IntegrityError:  # UNIQUE(origen, destino, tipo)
        raise ValueError("esa relación ya existe")
    registrar(conn, usuario, "relacionar", origen_id,
              {"relacion_id": cur.lastrowid, "origen_id": origen_id, "destino_id": destino_id, "tipo": tipo})
    conn.commit()
    return cur.lastrowid


def quitar_relacion(conn, relacion_id, usuario):
    """Quita una relación por su id."""
    f = conn.execute("SELECT * FROM relaciones WHERE id = ?", (relacion_id,)).fetchone()
    if f is None:
        raise ValueError(f"la relación {relacion_id} no existe")
    conn.execute("DELETE FROM relaciones WHERE id = ?", (relacion_id,))
    registrar(conn, usuario, "quitar_relacion", f["origen_id"],
              {"relacion_id": relacion_id, "origen_id": f["origen_id"],
               "destino_id": f["destino_id"], "tipo": f["tipo"]})
    conn.commit()


def vecinos(conn, lote_id):
    """Con qué lotes está unido este lote. 'sale' = la flecha parte de este lote; 'entra' = llega a él."""
    filas = conn.execute(
        """SELECT r.id AS relacion_id, r.tipo, 'sale' AS direccion, l.id, l.titulo
             FROM relaciones r JOIN lotes l ON l.id = r.destino_id WHERE r.origen_id = ?
           UNION ALL
           SELECT r.id, r.tipo, 'entra', l.id, l.titulo
             FROM relaciones r JOIN lotes l ON l.id = r.origen_id WHERE r.destino_id = ?
           ORDER BY relacion_id""", (lote_id, lote_id))
    return [{"relacion_id": f["relacion_id"], "tipo": f["tipo"], "direccion": f["direccion"],
             "lote": {"id": f["id"], "titulo": f["titulo"]}} for f in filas]


def al_borrar_lote(conn, lote_id):
    """Reacción al evento "lote_borrado": quita todas las flechas que entran o salen del lote."""
    conn.execute("DELETE FROM relaciones WHERE origen_id = ? OR destino_id = ?", (lote_id, lote_id))
