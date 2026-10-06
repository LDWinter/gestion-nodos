"""Conexión a la base de datos SQLite y creación de tablas."""
import sqlite3
import pathlib


def conectar(ruta=":memory:"):
    """Abre la base. ":memory:" = base temporal en memoria (se usa en los tests)."""
    conn = sqlite3.connect(ruta, check_same_thread=False)
    conn.row_factory = sqlite3.Row             # permite leer cada fila por nombre de columna: fila["titulo"]
    conn.execute("PRAGMA foreign_keys = ON")   # SQLite trae las claves foráneas apagadas: las prendemos
    return conn


def crear_esquema(conn, modulos=None):
    """Crea las tablas del núcleo y las de cada módulo activo (si tiene esquema.sql).
    Se puede llamar varias veces: todas las tablas usan CREATE TABLE IF NOT EXISTS."""
    from nodos.nucleo.modulos import cargar
    archivos = [pathlib.Path(__file__).parent / "esquema.sql"]
    for modulo in cargar(modulos):
        esquema = pathlib.Path(modulo.__file__).parent / "esquema.sql"
        if esquema.exists():
            archivos.append(esquema)
    for archivo in archivos:
        conn.executescript(archivo.read_text(encoding="utf-8"))
    conn.commit()
