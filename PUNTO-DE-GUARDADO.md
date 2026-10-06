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
- v1 FUNCIONANDO (2026-10-06): módulos núcleo + tipos/lotes/relaciones/grafo/historial, rutas (ia-local),
  página con grafo vis-network, semilla.py. 33 tests en verde. Prototipo: `.venv/bin/python semilla.py` +
  `.venv/bin/python -m nodos.app` → http://127.0.0.1:5000
- Falta para cerrar v1: que el usuario pruebe la web y dé su opinión; tag v1.0; reporte de pruebas para la materia.
- Luego v2 (usuarios y roles) según HOJA-DE-RUTA.md.

## Pendiente para el usuario
- Definir la lógica de "dosificar" información por rol, lista final de roles e interfaz final (CLI/API/web).
- Drive: carpeta 'Gestión de Nodos' (id 1XT1T3RxsYgV_XsTuWNnayJuH7E_LR021) con 'Hoja de ruta' (1qKiyoiTcjXNwMQZ4dPGD9-bPVFsO-Y7ie3dgYx7dXVQ) y 'Diseño v1' (1eRUdGnRcMOtyR7IMTorI8IsnSqOD87waSY_HOuNbesY). GitHub privado: LDWinter/gestion-nodos.
- 2026-10-06: guía para principiantes completa (manual de la web, práctica de módulos, estado). Docs sincronizados
  a Drive con rclone (`marcamaldita:` + `--drive-root-folder-id 1XT1T3RxsYgV_XsTuWNnayJuH7E_LR021 --drive-import-formats md`).
- 2026-10-06: CAMBIO DE ENFOQUE (pedido del usuario): la carpeta de Drive "Gestión de Nodos" se movió a la RAÍZ del Drive.
  Este proyecto queda como SOLUCIÓN DE REFERENCIA. El usuario aprende a hacer la BD desde cero en ~/Proyectos/bd-desde-cero
  (PLAN.md; Drive: METODOLOGIA Y TESTING/Base de datos desde cero, id 1UOvqMpUjifbOxgqPm_IbEcJN6Puh83NY).
