-- Tabla del módulo 'relaciones'. Se crea solo si el módulo está activo (ver nodos/config.py).
CREATE TABLE IF NOT EXISTS relaciones (
    id INTEGER PRIMARY KEY,
    origen_id INTEGER NOT NULL REFERENCES lotes(id),
    destino_id INTEGER NOT NULL REFERENCES lotes(id),
    tipo TEXT NOT NULL,
    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(origen_id, destino_id, tipo),
    CHECK(origen_id <> destino_id)
);
