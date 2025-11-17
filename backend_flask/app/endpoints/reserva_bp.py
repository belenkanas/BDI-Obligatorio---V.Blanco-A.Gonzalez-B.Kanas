from flask import Blueprint, request, jsonify
from app.services.reserva_service import (
    listar_reservas,
    obtener_reserva,
    crear_reserva,
    actualizar_estado_reserva,
    cancelar_reserva,
    registrar_asistencias
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
    asistencias = data.get('asistencias') 

    if nuevo_estado not in ['activa', 'cancelada', 'sin asistencia', 'finalizada']:
        return jsonify({"mensaje": "Estado inválido"}), 400

    resultado, mensaje = actualizar_estado_reserva(id_reserva, nuevo_estado, asistencias)
    if resultado:
        return jsonify({"mensaje": mensaje, "reserva": resultado}), 200
    return jsonify({"mensaje": mensaje}), 404

# Registrar asistencias de una reserva
@reserva_bp.route('/reservas/<int:id_reserva>/asistencias', methods=['PUT'])
def registrar_asistencias_reserva(id_reserva):
    data = request.get_json()
    asistencias = data.get("asistencias")

    if not asistencias or not isinstance(asistencias, dict):
        return jsonify({"mensaje": "Debes enviar un diccionario con las asistencias por CI"}), 400

    resultado, mensaje = registrar_asistencias(id_reserva, asistencias)
    if resultado:
        return jsonify({"mensaje": mensaje, "resultado": resultado}), 200
    return jsonify({"mensaje": mensaje}), 400

# Listar reservas detalladas con filtros opcionales
@reserva_bp.route('/reservas/detalladas', methods=['GET'])
def obtener_reservas_con_filtro():
    from app.services.reserva_service import listar_reservas_con_asistencias_filtro
    estado = request.args.get("estado")
    fecha_desde = request.args.get("fecha_desde")
    fecha_hasta = request.args.get("fecha_hasta")
    id_edificio = request.args.get("id_edificio")
    tipo_sala = request.args.get("tipo_sala")

    reservas = listar_reservas_con_asistencias_filtro(
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        id_edificio=id_edificio,
        tipo_sala=tipo_sala
    )
    return jsonify(reservas), 200

#  Cancelar reserva
@reserva_bp.route('/reservas/<int:id_reserva>/cancelar', methods=['PUT'])
def cancelar(id_reserva):
    resultado, mensaje = cancelar_reserva(id_reserva)
    if resultado:
        return jsonify({"mensaje": mensaje, "reserva": resultado}), 200
    return jsonify({"mensaje": mensaje}), 404
