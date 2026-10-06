# Punto de guardado — Gestión de Nodos (se actualiza al avanzar)

**Para retomar:** abrir Claude Code en `~/Proyectos/gestion-nodos` y decir "continuá desde PUNTO-DE-GUARDADO.md".

## Contexto
- Base de datos empresarial basada en nodos (Python + SQL/PostgreSQL). Cada nodo es un **lote** de
  información precisa y separada en campos; los lotes se unen entre sí. Diseño completo en `DISENO.md`.
- Base: `./db.sh arrancar` (Docker `gestion-nodos-db`, puerto 5433). Bases `nodos` y `nodos_test`.
- Tests: `.venv/bin/pytest -q`.

## Hecho
- 2026-10-06: proyecto creado, DISENO.md, db.sh, venv (psycopg 3, pytest), contenedor Postgres, tests fase 1.

## Siguiente paso
- Fase 1: `sql/schema.sql`, `nodos/db.py`, `nodos/lotes.py` hasta que pasen `tests/test_lotes.py` y `tests/test_esquema.py`
  (delegado a ia-local programador).

## Pendiente para el usuario
- Definir la lógica de "dosificar" información por rol, lista final de roles e interfaz final (CLI/API/web).
