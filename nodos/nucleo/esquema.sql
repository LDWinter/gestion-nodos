-- Tabla del NÚCLEO: la bitácora. Existe siempre, la usan todos los módulos.
CREATE TABLE IF NOT EXISTS registro (
    id INTEGER PRIMARY KEY,
    fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario TEXT NOT NULL,
    accion TEXT NOT NULL,
    lote_id INTEGER NULL,
    detalle TEXT NOT NULL DEFAULT '{}'
);
