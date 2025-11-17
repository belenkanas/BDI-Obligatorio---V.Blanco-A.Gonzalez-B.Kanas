from flask import Blueprint, request, jsonify
from app.services.turno_service import (
    listar_turnos, obtener_turno, agregar_turno, eliminar_turno
)

turno_bp = Blueprint('turno', __name__)

@turno_bp.route('/turnos', methods=['GET'])
def obtener_todos_turnos():
    turnos = listar_turnos()
    return jsonify(turnos), 200


@turno_bp.route('/turnos/<id_turno>', methods=['GET'])
def obtener_un_turno(id_turno):
    turno = obtener_turno(id_turno)
    if turno:
        return jsonify(turno), 200
    return jsonify({"mensaje": "Turno no encontrado"}), 404


@turno_bp.route('/turnos', methods=['POST'])
def crear_turno():
    data = request.get_json()

    hora_inicio = data.get('hora_inicio')
    hora_fin = data.get('hora_fin')

    turno, mensaje = agregar_turno(hora_inicio, hora_fin)

    if turno:
        return jsonify({"mensaje": mensaje, "turno": turno}), 201
    return jsonify({"mensaje": mensaje}), 400


@turno_bp.route('/turnos/<id_turno>', methods=['DELETE'])
def eliminar_turno_endpoint(id_turno):
    if eliminar_turno(id_turno):
        return jsonify({"mensaje": "Turno eliminado exitosamente"}), 200
    return jsonify({"mensaje": "Turno no encontrado"}), 404
