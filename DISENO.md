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

## Módulos (`nodos/`)
- `db.py`: `conectar(ruta=":memory:")` devuelve una `sqlite3.Connection` con `row_factory = sqlite3.Row`
  y `PRAGMA foreign_keys = ON`. `crear_esquema(conn)` ejecuta `esquema.sql` y es idempotente.
- `lotes.py`: `validar_contenido(campos, contenido)` → `list[str]` de errores.
- `repositorio.py`: todas las operaciones. Cada escritura agrega una fila a `registro` y hace `commit()`.
  Los errores de uso lanzan `ValueError`.
- `app.py`: Flask con una API JSON y `templates/index.html`.

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
