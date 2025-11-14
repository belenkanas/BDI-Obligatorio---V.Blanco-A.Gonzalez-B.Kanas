from flask import Blueprint, request, jsonify
<<<<<<< HEAD:backend_flask/src/endpoints/reserva_participante_bp.py
from services.reserva_participante_service import (
=======
from app.services.reserva_participante_service import (
>>>>>>> 0f41fcacfd9edfbb6bb53766061c2c1037d5f104:backend_flask/app/endpoints/reserva_participante_bp.py
    listar_reservas_participantes,
    obtener_participantes_por_reserva,
    crear_reserva_participante,
    actualizar_asistencia,
    eliminar_reserva_participante
)

reserva_participante_bp = Blueprint('reserva_participante', __name__)

@reserva_participante_bp.route('/reservas-participantes', methods=['GET'])
def listar_todos():
    registros = listar_reservas_participantes()
    return jsonify(registros), 200


@reserva_participante_bp.route('/reservas/<int:id_reserva>/participantes', methods=['GET'])
def obtener_por_reserva(id_reserva):
    participantes = obtener_participantes_por_reserva(id_reserva)
    return jsonify(participantes), 200


@reserva_participante_bp.route('/reservas/<int:id_reserva>/participantes', methods=['POST'])
def crear(id_reserva):
    data = request.get_json()
    ci_participante = data.get('ci_participante')
    asistencia = data.get('asistencia', None)

    registro, mensaje = crear_reserva_participante(ci_participante, id_reserva, asistencia)
    if registro:
        return jsonify({"mensaje": mensaje, "registro": registro}), 201
    return jsonify({"mensaje": mensaje}), 400


@reserva_participante_bp.route('/reservas/<int:id_reserva>/participantes/<string:ci_participante>/asistencia', methods=['PUT'])
def actualizar_asistencia_participante(id_reserva, ci_participante):
    data = request.get_json()
    asistencia = data.get('asistencia')

    resultado, mensaje = actualizar_asistencia(ci_participante, id_reserva, asistencia)
    if resultado:
        return jsonify({"mensaje": mensaje, "registro": resultado}), 200
    return jsonify({"mensaje": mensaje}), 404


@reserva_participante_bp.route('/reservas/<int:id_reserva>/participantes/<string:ci_participante>', methods=['DELETE'])
def eliminar(id_reserva, ci_participante):
    exito = eliminar_reserva_participante(ci_participante, id_reserva)
    if exito:
        return jsonify({"mensaje": "Participante eliminado de la reserva"}), 200
    return jsonify({"mensaje": "No se encontró el vínculo"}), 404
