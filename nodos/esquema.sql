CREATE TABLE IF NOT EXISTS tipos_lote (
    id INTEGER PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    campos TEXT NOT NULL
);

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

CREATE TABLE IF NOT EXISTS relaciones (
    id INTEGER PRIMARY KEY,
    origen_id INTEGER NOT NULL REFERENCES lotes(id),
    destino_id INTEGER NOT NULL REFERENCES lotes(id),
    tipo TEXT NOT NULL,
    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(origen_id, destino_id, tipo),
    CHECK(origen_id <> destino_id)
);

CREATE TABLE IF NOT EXISTS registro (
    id INTEGER PRIMARY KEY,
    fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario TEXT NOT NULL,
    accion TEXT NOT NULL,
    lote_id INTEGER NULL,
    detalle TEXT NOT NULL DEFAULT '{}'
);
