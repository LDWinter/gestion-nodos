from flask import Blueprint, jsonify
from nodos import web
from . import servicio

bp = Blueprint('relaciones', __name__)

@bp.route('/relaciones', methods=['POST'])
def relacionar():
    conn = web.conn()
    usuario = web.usuario()
    d = web.datos()
    id = servicio.relacionar(conn, d.get('origen_id'), d.get('destino_id'), d.get('tipo', 'referencia'), usuario)
    return jsonify({'id': id}), 201

@bp.route('/relaciones/<int:relacion_id>', methods=['DELETE'])
def quitar_relacion(relacion_id):
    conn = web.conn()
    usuario = web.usuario()
    servicio.quitar_relacion(conn, relacion_id, usuario)
    return jsonify({'ok': True})
