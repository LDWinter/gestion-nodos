-- Tabla del módulo 'tipos'. Se crea solo si el módulo está activo (ver nodos/config.py).
CREATE TABLE IF NOT EXISTS tipos_lote (
    id INTEGER PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    campos TEXT NOT NULL
);
