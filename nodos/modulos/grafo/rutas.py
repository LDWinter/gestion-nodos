from flask import Blueprint, jsonify
from nodos import web
from . import servicio

bp = Blueprint('grafo', __name__)

@bp.route('/grafo', methods=['GET'])
def listar_grafo():
    conn = web.conn()
    return jsonify(servicio.grafo(conn))
