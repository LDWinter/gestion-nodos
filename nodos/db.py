import sqlite3
import pathlib

def conectar(ruta=':memory:'):
    conn = sqlite3.connect(ruta)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def crear_esquema(conn):
    schema_path = pathlib.Path(__file__).parent / 'esquema.sql'
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
