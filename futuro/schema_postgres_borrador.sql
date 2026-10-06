CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT true,
    creado_en TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS proyectos (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT,
    creado_por INTEGER REFERENCES usuarios(id),
    creado_en TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS miembros (
    proyecto_id INTEGER REFERENCES proyectos(id),
    usuario_id INTEGER REFERENCES usuarios(id),
    rol TEXT NOT NULL CHECK (rol IN ('lector','editor','aprobador','admin')),
    PRIMARY KEY (proyecto_id, usuario_id)
);

CREATE TABLE IF NOT EXISTS tipos_lote (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT,
    campos JSONB NOT NULL DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS nodos (
    id SERIAL PRIMARY KEY,
    proyecto_id INTEGER REFERENCES proyectos(id),
    tipo_lote_id INTEGER REFERENCES tipos_lote(id),
    titulo TEXT NOT NULL,
    contenido JSONB NOT NULL DEFAULT '{}',
    version INTEGER NOT NULL DEFAULT 1,
    borrado BOOLEAN NOT NULL DEFAULT false,
    creado_por INTEGER REFERENCES usuarios(id),
    creado_en TIMESTAMPTZ DEFAULT now(),
    actualizado_en TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS relaciones (
    id SERIAL PRIMARY KEY,
    origen_id INTEGER REFERENCES nodos(id),
    destino_id INTEGER REFERENCES nodos(id),
    tipo TEXT NOT NULL,
    creado_por INTEGER REFERENCES usuarios(id),
    creado_en TIMESTAMPTZ DEFAULT now(),
    UNIQUE (origen_id, destino_id, tipo),
    CHECK (origen_id <> destino_id)
);

CREATE TABLE IF NOT EXISTS commits (
    id SERIAL PRIMARY KEY,
    proyecto_id INTEGER REFERENCES proyectos(id),
    autor_id INTEGER REFERENCES usuarios(id),
    mensaje TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente','aprobado','rechazado')),
    revisado_por INTEGER REFERENCES usuarios(id),
    creado_en TIMESTAMPTZ DEFAULT now(),
    revisado_en TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS cambios (
    id SERIAL PRIMARY KEY,
    commit_id INTEGER REFERENCES commits(id),
    nodo_id INTEGER REFERENCES nodos(id),
    relacion_id INTEGER REFERENCES relaciones(id),
    operacion TEXT NOT NULL CHECK (operacion IN ('crear_nodo','editar_nodo','borrar_nodo','crear_relacion','borrar_relacion')),
    antes JSONB,
    despues JSONB
);
