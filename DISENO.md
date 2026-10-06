# Gestión de Nodos — Diseño

Plataforma empresarial para organizar datos y proyectos como **nodos relacionados** (estilo Obsidian).
**Cada nodo es un "lote"**: un paquete de información precisa, clara y bien diferenciada, organizada en
campos separados (según su tipo de lote). El valor del sistema está en la **unión de lotes entre sí**.
Origen de la idea: doc de Drive "Idea de Proyecto - Gestión de Nodos" (2026-09-29).

## Principios (del doc original)
1. **Formato estándar JSON**: el contenido de cada nodo es un documento JSON (columna `JSONB`).
2. **Única fuente de verdad / punteros**: un nodo existe una sola vez. Proyectos, relaciones y usuarios
   lo referencian por `id` (claves foráneas). Nunca se copia un nodo para otro participante.
3. **Commits**: todo cambio (crear/editar/borrar nodo, crear/quitar relación) se registra dentro de un
   commit con autor, fecha, mensaje y el antes/después en JSON. Trazabilidad completa.
4. **Roles y permisos**: cada usuario tiene un rol por proyecto que limita lo que puede hacer.

## Tecnología
- Python 3.12 + PostgreSQL 16 (Docker, contenedor `gestion-nodos-db`, puerto local **5433**; `./db.sh arrancar|parar|estado|psql`).
- DSN: `postgresql://nodos:nodos@127.0.0.1:5433/nodos` (tests: `.../nodos_test`).
- Driver: `psycopg` 3 (SQL a mano, sin ORM, para que el SQL quede visible).
- Tests: `pytest` contra la base de Docker (base `nodos_test`, se recrea en cada corrida).
- Entorno: `.venv/` (ya creado; `.venv/bin/pytest`).

## Modelo de datos (`sql/schema.sql`)
| Tabla | Columnas clave |
|---|---|
| `usuarios` | id, nombre, email (único), activo, creado_en |
| `proyectos` | id, nombre (único), descripcion, creado_por → usuarios, creado_en |
| `miembros` | proyecto_id, usuario_id, rol (`lector`/`editor`/`aprobador`/`admin`); PK (proyecto, usuario) |
| `tipos_lote` | id, nombre (único, p. ej. `cliente`, `contrato`, `tarea`), descripcion, campos JSONB: lista de `{"nombre","tipo":"texto|numero|fecha|booleano|lista","obligatorio":bool}` |
| `nodos` (lotes) | id, proyecto_id, tipo_lote_id → tipos_lote, titulo, contenido JSONB (un valor por campo del tipo), version (int), borrado (bool), creado_por, creado_en, actualizado_en |
| `relaciones` | id, origen_id → nodos, destino_id → nodos, tipo (p. ej. `referencia`, `depende_de`, `parte_de`), creado_por, creado_en; UNIQUE(origen, destino, tipo); CHECK origen ≠ destino |
| `commits` | id, proyecto_id, autor_id, mensaje, estado (`pendiente`/`aprobado`/`rechazado`), revisado_por, creado_en, revisado_en |
| `cambios` | id, commit_id, nodo_id (nullable), relacion_id (nullable), operacion (`crear_nodo`/`editar_nodo`/`borrar_nodo`/`crear_relacion`/`borrar_relacion`), antes JSONB, despues JSONB |

**Validación de lotes** (`nodos/lotes.py`): el `contenido` debe tener todos los campos obligatorios del
tipo, ningún campo que el tipo no declare y cada valor del tipo correcto. Así cada lote queda separado y
sin datos mezclados.

Los nodos se borran de forma lógica (`borrado = true`) para no romper el historial.

## Permisos por rol
| Acción | lector | editor | aprobador | admin |
|---|:-:|:-:|:-:|:-:|
| leer nodos y relaciones | ✔ | ✔ | ✔ | ✔ |
| crear/editar/borrar nodos | | ✔ | ✔ | ✔ |
| crear/quitar relaciones | | ✔ | ✔ | ✔ |
| aprobar/rechazar commits | | | ✔ | ✔ |
| gestionar miembros | | | | ✔ |

## Capas de código (`nodos/`)
- `db.py` — conexión (`conectar(dsn)`), `crear_esquema(conn)` que ejecuta `sql/schema.sql`.
- `lotes.py` — `validar_contenido(campos, contenido)` → lista de errores (vacía = válido).
- `permisos.py` — tabla de permisos y `verificar(conn, usuario_id, proyecto_id, accion)` → lanza `PermisoDenegado`.
- `repositorio.py` — operaciones; cada escritura abre un commit y registra los cambios.
- `grafo.py` — consultas del grafo: vecinos, recorrido recursivo (`WITH RECURSIVE`), caminos.
- `cli.py` — interfaz de línea de comandos (fase posterior).

## Fases
1. Esquema SQL + `db.py` + `lotes.py` (validación) + tests.
2. `permisos.py` + `repositorio.py` (nodos, relaciones, commits) + tests.
3. `grafo.py` (recorridos recursivos) + tests.
4. Interfaz (CLI y luego API/web) + datos de ejemplo.

## Pendientes a definir con el usuario (del doc)
- Lógica exacta para **"dosificar"** información (¿qué ve cada rol de cada nodo?).
- Lista final de roles (por ahora los 4 de arriba).
- Interfaz final: CLI, API REST o web.
