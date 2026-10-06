from flask import Blueprint, jsonify
from nodos import web
from . import servicio
import sys

bp = Blueprint('lotes', __name__)

@bp.route('/lotes', methods=['POST'])
def crear_lote():
    conn = web.conn()
    usuario = web.usuario()
    d = web.datos()
    id = servicio.crear_lote(conn, d.get('tipo_id'), d.get('titulo', ''), d.get('contenido', {}), usuario)
    return jsonify({'id': id}), 201

@bp.route('/lotes', methods=['GET'])
def listar_lotes():
    conn = web.conn()
    return jsonify(servicio.listar_lotes(conn))

@bp.route('/lotes/<int:lote_id>', methods=['GET'])
def obtener_lote(lote_id):
    conn = web.conn()
    lote = servicio.obtener_lote(conn, lote_id)
    if lote is None or lote.get('borrado'):
        return jsonify({'error': 'no existe'}), 404

    vecinos = []
    historial = []

    m_rel = sys.modules.get('nodos.modulos.relaciones')
    if m_rel:
        vecinos = m_rel.vecinos(conn, lote_id)

    m_his = sys.modules.get('nodos.modulos.historial')
    if m_his:
        historial = m_his.historial(conn, lote_id)

    return jsonify({'lote': lote, 'vecinos': vecinos, 'historial': historial})

@bp.route('/lotes/<int:lote_id>', methods=['PUT'])
def editar_lote(lote_id):
    conn = web.conn()
    usuario = web.usuario()
    d = web.datos()
    v = servicio.editar_lote(conn, lote_id, usuario, titulo=d.get('titulo'), contenido=d.get('contenido'))
    return jsonify({'version': v})

@bp.route('/lotes/<int:lote_id>', methods=['DELETE'])
def borrar_lote(lote_id):
    conn = web.conn()
    usuario = web.usuario()
    servicio.borrar_lote(conn, lote_id, usuario)
    return jsonify({'ok': True})
