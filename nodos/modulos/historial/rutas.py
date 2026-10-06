from flask import Blueprint, jsonify
from nodos import web
from . import servicio

bp = Blueprint('historial', __name__)

@bp.route('/historial', methods=['GET'])
def listar_historial():
    conn = web.conn()
    return jsonify(servicio.historial(conn))
