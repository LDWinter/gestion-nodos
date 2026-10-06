"""Aplicación web (Flask). Junta las rutas de todos los módulos activos.

Levantar:  .venv/bin/python -m nodos.app   →  http://127.0.0.1:5000
"""
from flask import Flask, jsonify, render_template

from nodos import config
from nodos.nucleo import db
from nodos.nucleo.modulos import cargar


def crear_app(ruta_base=None, modulos=None):
    """Crea la aplicación. `ruta_base` = archivo de la base (":memory:" en los tests).
    `modulos` = lista de módulos activos (por defecto, config.MODULOS)."""
    app = Flask(__name__)
    conn = db.conectar(ruta_base or config.RUTA_BASE)
    db.crear_esquema(conn, modulos)
    app.config["CONN"] = conn

    activos = cargar(modulos)
    for modulo in activos:
        # Si el módulo tiene rutas web (rutas.py con un Blueprint `bp`), se registran.
        try:
            rutas = __import__(f"{modulo.__name__}.rutas", fromlist=["bp"])
        except ModuleNotFoundError:
            continue
        app.register_blueprint(rutas.bp, url_prefix="/api")

    @app.get("/")
    def inicio():
        nombres = [m.__name__.rsplit(".", 1)[-1] for m in activos]
        return render_template("index.html", modulos=nombres)

    # Errores de uso (ValueError) → respuesta 400 con el mensaje, para todos los módulos.
    @app.errorhandler(ValueError)
    def error_de_uso(e):
        return jsonify({"error": str(e)}), 400

    return app


if __name__ == "__main__":
    crear_app().run(debug=True)
