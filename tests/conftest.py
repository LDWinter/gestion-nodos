import os
import pytest
from nodos import db

DSN_TEST = os.environ.get("NODOS_DSN_TEST", "postgresql://nodos:nodos@127.0.0.1:5433/nodos_test")


@pytest.fixture
def conn():
    c = db.conectar(DSN_TEST)
    with c.cursor() as cur:
        cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
    c.commit()
    db.crear_esquema(c)
    yield c
    c.rollback()
    c.close()
