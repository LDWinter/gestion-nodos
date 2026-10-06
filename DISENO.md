# Diseño v1 — Gestión de Nodos (modelo básico)

Diseño completo para versiones futuras: `futuro/DISENO-completo.md`.

## Tecnología
Python 3.12, `sqlite3` (biblioteca estándar), Flask, vis-network (CDN) y pytest. Entorno: `.venv/`.
- Correr tests: `.venv/bin/pytest -q`
- Cargar datos de ejemplo: `.venv/bin/python semilla.py`, que crea `nodos.db`.
- Levantar la web: `.venv/bin/python -m nodos.app` → http://127.0.0.1:5000

## Base de datos (`nodos/esquema.sql`)
```
tipos_lote(id INTEGER PK, nombre TEXT UNIQUE NOT NULL, campos TEXT NOT NULL)   -- campos = JSON
lotes(id INTEGER PK, tipo_id → tipos_lote NOT NULL, titulo TEXT NOT NULL, contenido TEXT NOT NULL,  -- JSON
      version INTEGER NOT NULL DEFAULT 1, borrado INTEGER NOT NULL DEFAULT 0,
      creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, actualizado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)
relaciones(id INTEGER PK, origen_id → lotes NOT NULL, destino_id → lotes NOT NULL, tipo TEXT NOT NULL,
           creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
           UNIQUE(origen_id, destino_id, tipo), CHECK(origen_id <> destino_id))
registro(id INTEGER PK, fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, usuario TEXT NOT NULL,
         accion TEXT NOT NULL, lote_id INTEGER NULL, detalle TEXT NOT NULL DEFAULT '{}')     -- detalle = JSON
```
Campos de un tipo: `[{"nombre": str, "tipo": "texto|numero|fecha|booleano|lista", "obligatorio": bool}]`.

## Arquitectura modular
Pedido explícito: **todo en módulos, para poder quitar y agregar sin problemas.**
- `nodos/nucleo/`: lo imprescindible. `db.py` (conectar, crear_esquema), `registro.py` (bitácora),
  `validacion.py` (validar_contenido), `eventos.py` (suscribir/emitir) y `modulos.py` (cargar + dependencias).
- `nodos/modulos/<nombre>/`: `__init__.py` (`DEPENDE_DE` + API pública), `servicio.py` (lógica),
  `rutas.py` (Blueprint `bp`, opcional) y `esquema.sql` (opcional).
- `nodos/config.py`: `MODULOS = ["tipos", "lotes", "relaciones", "grafo", "historial"]` (en orden de dependencias).
- `nodos/app.py`: `crear_app(ruta_base, modulos)` registra el Blueprint de cada módulo activo bajo `/api`.
  `ValueError` → 400.
- `nodos/repositorio.py`: una fachada que reexporta las funciones de los módulos activos.
- La página oculta los formularios de los módulos inactivos.
- Desacople con eventos: `lotes` emite `lote_borrado` y `relaciones` se suscribe para quitar las flechas.

| Módulo | Depende de | Tabla |
|---|---|---|
| tipos | — | tipos_lote |
| lotes | tipos | lotes |
| relaciones | lotes | relaciones |
| grafo | lotes, relaciones | — |
| historial | — | registro (del núcleo) |

## Repositorio: contrato
| Función | Devuelve | Registro (`accion`) |
|---|---|---|
| `crear_tipo(conn, nombre, campos, usuario)` | id | `crear_tipo` |
| `listar_tipos(conn)` | `[{id, nombre, campos}]` | — |
| `crear_lote(conn, tipo_id, titulo, contenido, usuario)` (valida) | id | `crear_lote`, detalle `{"despues": {...}}` |
| `obtener_lote(conn, id)` | `{id, tipo_id, tipo, titulo, contenido, version, borrado, creado_en, actualizado_en}` o `None` | — |
| `listar_lotes(conn, tipo_id=None)` | lista sin borrados, ordenada por id | — |
| `editar_lote(conn, id, usuario, titulo=None, contenido=None)` (valida, version+1) | nueva versión | `editar_lote`, detalle `{"antes", "despues"}` |
| `borrar_lote(conn, id, usuario)` (lógico, también quita sus relaciones) | None | `borrar_lote` |
| `relacionar(conn, origen_id, destino_id, tipo, usuario)` | id | `relacionar` |
| `quitar_relacion(conn, relacion_id, usuario)` | None | `quitar_relacion` |
| `vecinos(conn, lote_id)` | `[{relacion_id, tipo, direccion: "sale"/"entra", lote: {id, titulo}}]` | — |
| `grafo(conn)` | `{"nodos": [{id, titulo, tipo}], "aristas": [{id, origen, destino, tipo}]}` | — |
| `historial(conn, lote_id=None)` | `[{id, fecha, usuario, accion, lote_id, detalle}]`, del más nuevo al más viejo | — |

`ValueError` en estos casos: el tipo o el lote no existen o están borrados, el contenido no es válido, se intenta
relacionar un lote consigo mismo, la relación está duplicada o la relación no existe.

## API (`app.py`), siempre JSON
- `GET /` → la página. `GET /api/grafo`, `GET /api/tipos`, `GET /api/lotes/<id>` (lote, vecinos e historial).
- `POST /api/tipos`, `POST /api/lotes`, `PUT /api/lotes/<id>`, `DELETE /api/lotes/<id>`, `POST /api/relaciones`, `DELETE /api/relaciones/<id>`.
- `GET /api/historial`. El usuario sale del header `X-Usuario` (por defecto `"anonimo"`).
- Una creación responde 201 con `{"id": n}` y un `ValueError` responde 400 con `{"error": "..."}`. Lo que no existe responde 404.
