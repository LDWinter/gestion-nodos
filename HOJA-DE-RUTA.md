# Hoja de ruta — Gestión de Nodos

**Materia:** Metodología y Testing (3.er semestre).
**Idea:** una base de datos empresarial basada en nodos, al estilo Obsidian. Cada nodo es un **lote** de
información precisa y separada en campos, y los lotes se unen entre sí. Todo cambio queda registrado.
**Referencia visual:** NodoERP (Apps Script), con un grafo interactivo y un panel lateral que muestra la
vista, el JSON y los datos del nodo seleccionado. Hay un análisis en `futuro/referencia-nodoerp.md`.

## v1 — Modelo básico y funcional (ahora)
Objetivo: algo simple, que ande y que se pueda probar.
- [ ] Base **SQLite** (un archivo, sin instalar nada) con 4 tablas: `tipos_lote`, `lotes`, `relaciones`, `registro`.
- [ ] Tipos de lote con campos definidos y validación del contenido (campos obligatorios, sin campos de más, tipos correctos).
- [ ] Altas, ediciones y bajas lógicas de lotes. Crear y quitar relaciones entre lotes.
- [ ] **Registro** automático de cada acción: quién, cuándo, qué, y el antes y el después.
- [ ] Web con **Flask**: un grafo con vis-network y un panel lateral con las pestañas Detalle, JSON e Historial,
      más formularios para crear lotes y relaciones.
- [ ] Datos de ejemplo (`semilla.py`).
- [ ] Tests con **pytest**: unitarios del validador, de integración del repositorio y de la API.

## v2 — Usuarios y roles
- Inicio de sesión simple y roles: lector, editor y admin.
- Permisos verificados en cada acción, con tests de cada permiso.

## v3 — Control de cambios tipo "commits"
- Agrupar cambios en commits con mensaje.
- Estados pendiente, aprobado y rechazado, con un rol aprobador.
- Ver un lote en una versión anterior y restaurarlo.

## v4 — Escala empresarial
- Migrar a **PostgreSQL** (borrador listo en `futuro/schema_postgres_borrador.sql`) usando JSONB y consultas recursivas.
- "Dosificar" la información, es decir, qué campos ve cada rol (a definir).
- Búsqueda de texto, filtros por tipo y documentación en Markdown por lote.

## v5 — Entrega
- Documentación final, manual de usuario, plan y reporte de pruebas (cobertura) y demo.

## Metodología
- Trabajo incremental por versiones, cada una con su rama y su tag en Git.
- Cada funcionalidad nace con su test, siguiendo TDD liviano: test → código → refactor.
- `PUNTO-DE-GUARDADO.md` registra el avance y la documentación se sincroniza con Drive.
