"""Carga datos de ejemplo en nodos.db (si ya existe, la borra y la vuelve a crear).

Uso:  .venv/bin/python semilla.py
"""
import pathlib

from nodos import config, repositorio as repo
from nodos.nucleo import db

ruta = pathlib.Path(config.RUTA_BASE)
if ruta.exists():
    ruta.unlink()          # arrancamos de cero para que los datos de ejemplo queden prolijos
conn = db.conectar(str(ruta))
db.crear_esquema(conn)
U = "semilla"

# ---- tipos de lote (moldes)
cliente = repo.crear_tipo(conn, "cliente", [
    {"nombre": "razon_social", "tipo": "texto", "obligatorio": True},
    {"nombre": "cuit", "tipo": "texto", "obligatorio": True},
    {"nombre": "empleados", "tipo": "numero", "obligatorio": False},
    {"nombre": "activo", "tipo": "booleano", "obligatorio": False},
], U)
proyecto = repo.crear_tipo(conn, "proyecto", [
    {"nombre": "nombre", "tipo": "texto", "obligatorio": True},
    {"nombre": "inicio", "tipo": "fecha", "obligatorio": True},
    {"nombre": "presupuesto", "tipo": "numero", "obligatorio": False},
    {"nombre": "etiquetas", "tipo": "lista", "obligatorio": False},
], U)
factura = repo.crear_tipo(conn, "factura", [
    {"nombre": "numero", "tipo": "texto", "obligatorio": True},
    {"nombre": "fecha", "tipo": "fecha", "obligatorio": True},
    {"nombre": "monto", "tipo": "numero", "obligatorio": True},
    {"nombre": "pagada", "tipo": "booleano", "obligatorio": False},
], U)
empleado = repo.crear_tipo(conn, "empleado", [
    {"nombre": "nombre", "tipo": "texto", "obligatorio": True},
    {"nombre": "area", "tipo": "texto", "obligatorio": True},
], U)
documento = repo.crear_tipo(conn, "documento", [
    {"nombre": "titulo", "tipo": "texto", "obligatorio": True},
    {"nombre": "resumen", "tipo": "texto", "obligatorio": False},
], U)

# ---- lotes (fichas)
acme = repo.crear_lote(conn, cliente, "Acme Corp", {"razon_social": "Acme Corp SA", "cuit": "30-71234567-8", "empleados": 120, "activo": True}, U)
beta = repo.crear_lote(conn, cliente, "Beta SRL", {"razon_social": "Beta SRL", "cuit": "30-70000001-2", "empleados": 15}, U)
erp = repo.crear_lote(conn, proyecto, "Migración ERP", {"nombre": "Migración ERP", "inicio": "2026-08-01", "presupuesto": 50000, "etiquetas": ["sistemas", "prioridad alta"]}, U)
web = repo.crear_lote(conn, proyecto, "Portal web", {"nombre": "Portal web", "inicio": "2026-09-15", "etiquetas": ["marketing"]}, U)
f1 = repo.crear_lote(conn, factura, "Factura A-0001", {"numero": "A-0001", "fecha": "2026-09-01", "monto": 12500.5, "pagada": True}, U)
f2 = repo.crear_lote(conn, factura, "Factura A-0002", {"numero": "A-0002", "fecha": "2026-10-01", "monto": 8300, "pagada": False}, U)
ana = repo.crear_lote(conn, empleado, "Ana López", {"nombre": "Ana López", "area": "Sistemas"}, U)
luis = repo.crear_lote(conn, empleado, "Luis Pérez", {"nombre": "Luis Pérez", "area": "Ventas"}, U)
contrato = repo.crear_lote(conn, documento, "Contrato Acme", {"titulo": "Contrato de servicios Acme", "resumen": "Alcance y plazos de la migración"}, U)

# ---- relaciones (flechas)
for origen, destino, tipo in [
    (acme, erp, "contrata"), (beta, web, "contrata"),
    (f1, acme, "facturada_a"), (f2, beta, "facturada_a"),
    (f1, erp, "corresponde_a"), (f2, web, "corresponde_a"),
    (ana, erp, "trabaja_en"), (luis, web, "trabaja_en"), (luis, acme, "gestiona"),
    (contrato, acme, "firmado_por"), (contrato, erp, "documenta"),
]:
    repo.relacionar(conn, origen, destino, tipo, U)

# ---- un cambio de ejemplo para que el historial muestre "antes / después"
repo.editar_lote(conn, f2, "ana", contenido={"numero": "A-0002", "fecha": "2026-10-01", "monto": 8300, "pagada": True})

g = repo.grafo(conn)
print(f"Listo: {len(g['nodos'])} lotes, {len(g['aristas'])} relaciones en {ruta}")
