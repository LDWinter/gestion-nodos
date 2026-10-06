# Gestión de Nodos

Base de datos empresarial basada en nodos al estilo Obsidian. Cada nodo es un **lote** de información
organizada en campos, los lotes se relacionan entre sí y cada cambio queda registrado.
Proyecto de la materia Metodología y Testing (3.er semestre).

- Plan por versiones: [HOJA-DE-RUTA.md](HOJA-DE-RUTA.md)
- Diseño de la v1: [DISENO.md](DISENO.md)

```bash
python3 -m venv .venv && .venv/bin/pip install flask pytest
.venv/bin/pytest -q              # tests
.venv/bin/python semilla.py      # datos de ejemplo
.venv/bin/python -m nodos.app    # web en http://127.0.0.1:5000
```
