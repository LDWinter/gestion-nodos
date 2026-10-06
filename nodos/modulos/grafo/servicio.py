"""Lógica del módulo grafo."""


def grafo(conn):
    """Todos los lotes (nodos) y relaciones (aristas), listo para dibujar."""
    nodos = [{"id": f["id"], "titulo": f["titulo"], "tipo": f["tipo"]} for f in conn.execute(
        """SELECT l.id, l.titulo, t.nombre AS tipo FROM lotes l
           JOIN tipos_lote t ON t.id = l.tipo_id WHERE l.borrado = 0 ORDER BY l.id""")]
    aristas = [{"id": f["id"], "origen": f["origen_id"], "destino": f["destino_id"], "tipo": f["tipo"]}
               for f in conn.execute("SELECT * FROM relaciones ORDER BY id")]
    return {"nodos": nodos, "aristas": aristas}
