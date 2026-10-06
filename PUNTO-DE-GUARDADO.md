# Punto de guardado — Gestión de Nodos (se actualiza al avanzar)

**Para retomar:** abrir Claude Code en `~/Proyectos/gestion-nodos` y decir "continuá desde PUNTO-DE-GUARDADO.md".

## Contexto
- Materia **Metodología y Testing** (3er semestre). Base de datos empresarial basada en nodos estilo Obsidian;
  cada nodo es un **lote** de información separada en campos; los lotes se unen; todo queda registrado.
- Referencia: NodoERP (https://script.google.com/macros/s/AKfycbwVYcfXANa_ct3bVOYjWj2rxGWucPKsDelXxomqCIfCX5eTlib94QUQuitRV0IOkHcy-Q/exec),
  análisis en `futuro/referencia-nodoerp.md`.
- Plan: `HOJA-DE-RUTA.md`. Diseño v1 (SQLite + Flask, simple de estudiantes): `DISENO.md`. Tests: `.venv/bin/pytest -q`.
- PostgreSQL quedó para v4 (`futuro/`, contenedor `gestion-nodos-db` detenido, `./db.sh`).
- Docs se suben a Drive: FACULTAD/tercer semestre/METODOLOGIA Y TESTING (id 1wGGI-ouOYJS461DSCUQd8R6MzpVT9pYk).
- Repo GitHub privado (ver Hecho).

## Hecho
- 2026-10-06: proyecto creado; primero diseño con PostgreSQL (archivado en futuro/), luego v1 simplificada a SQLite.
  HOJA-DE-RUTA.md, DISENO.md v1, tests de especificación (test_lotes, test_repositorio).

## Siguiente paso
- v1 paso A: `nodos/esquema.sql`, `db.py`, `lotes.py` (ia-local programador).
- v1 paso B: `repositorio.py` hasta pasar tests/test_repositorio.py.
- v1 paso C: `app.py` + `templates/index.html` (grafo vis-network + panel) + tests API + `semilla.py`.

## Pendiente para el usuario
- Definir la lógica de "dosificar" información por rol, lista final de roles e interfaz final (CLI/API/web).
- Drive: carpeta 'Gestión de Nodos' (id 1XT1T3RxsYgV_XsTuWNnayJuH7E_LR021) con 'Hoja de ruta' (1qKiyoiTcjXNwMQZ4dPGD9-bPVFsO-Y7ie3dgYx7dXVQ) y 'Diseño v1' (1eRUdGnRcMOtyR7IMTorI8IsnSqOD87waSY_HOuNbesY). GitHub privado: LDWinter/gestion-nodos.
