-- Tabla del módulo 'lotes'. Se crea solo si el módulo está activo (ver nodos/config.py).
CREATE TABLE IF NOT EXISTS lotes (
    id INTEGER PRIMARY KEY,
    tipo_id INTEGER NOT NULL REFERENCES tipos_lote(id),
    titulo TEXT NOT NULL,
    contenido TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    borrado INTEGER NOT NULL DEFAULT 0,
    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
