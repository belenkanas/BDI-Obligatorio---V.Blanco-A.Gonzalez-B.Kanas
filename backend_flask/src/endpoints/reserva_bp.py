from flask import Blueprint, request, jsonify
from services.reserva_service import (
    listar_reservas,
    obtener_reserva,
    crear_reserva,
    actualizar_estado_reserva,
    cancelar_reserva
)

reserva_bp = Blueprint('reserva', __name__)

# Listar todas las reservas
@reserva_bp.route('/reservas', methods=['GET'])
def listar_todas():
    reservas = listar_reservas()
    return jsonify(reservas), 200


# Obtener una reserva específica
@reserva_bp.route('/reservas/<int:id_reserva>', methods=['GET'])
def obtener(id_reserva):
    reserva = obtener_reserva(id_reserva)
    if reserva:
        return jsonify(reserva), 200
    return jsonify({"mensaje": "Reserva no encontrada"}), 404


# Crear nueva reserva
@reserva_bp.route('/reservas', methods=['POST'])
def crear():
    data = request.get_json()
    id_sala = data.get('id_sala')
    fecha = data.get('fecha')  # formato "YYYY-MM-DD"
    id_turno = data.get('id_turno')
    estado = data.get('estado', 'activa')
    participantes = data.get('participantes', [])  # lista de CIs

    reserva, mensaje = crear_reserva(id_sala, fecha, id_turno, estado, participantes)
    if reserva:
        return jsonify({"mensaje": mensaje, "reserva": reserva}), 201
    return jsonify({"mensaje": mensaje}), 400

# Actualizar estado
@reserva_bp.route('/reservas/<int:id_reserva>/estado', methods=['PUT'])
def actualizar_estado(id_reserva):
    data = request.get_json()
    nuevo_estado = data.get('estado')

    if nuevo_estado not in ['activa', 'cancelada', 'sin asistencia', 'finalizada']:
        return jsonify({"mensaje": "Estado inválido"}), 400

    resultado, mensaje = actualizar_estado_reserva(id_reserva, nuevo_estado)
    if resultado:
        return jsonify({"mensaje": mensaje, "reserva": resultado}), 200
    return jsonify({"mensaje": mensaje}), 404


#  Cancelar reserva
@reserva_bp.route('/reservas/<int:id_reserva>/cancelar', methods=['PUT'])
def cancelar(id_reserva):
    resultado, mensaje = cancelar_reserva(id_reserva)
    if resultado:
        return jsonify({"mensaje": mensaje, "reserva": resultado}), 200
    return jsonify({"mensaje": mensaje}), 404
