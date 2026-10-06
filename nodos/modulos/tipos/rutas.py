from flask import Blueprint, jsonify
from nodos import web
from . import servicio

bp = Blueprint('tipos', __name__)

@bp.route('/tipos', methods=['GET'])
def listar_tipos():
    conn = web.conn()
    return jsonify(servicio.listar_tipos(conn))

@bp.route('/tipos', methods=['POST'])
def crear_tipo():
    conn = web.conn()
    usuario = web.usuario()
    d = web.datos()
    id = servicio.crear_tipo(conn, d.get('nombre'), d.get('campos', []), usuario)
    return jsonify({'id': id}), 201
