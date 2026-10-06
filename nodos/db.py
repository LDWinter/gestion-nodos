import psycopg
from pathlib import Path

def conectar(dsn: str) -> psycopg.Connection:
    return psycopg.connect(dsn)

def crear_esquema(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        # Ruta relativa a este archivo: ../sql/schema.sql
        schema_path = Path(__file__).parent.parent / 'sql' / 'schema.sql'
        with open(schema_path, 'r', encoding='utf-8') as f:
            cur.execute(f.read())
        conn.commit()
