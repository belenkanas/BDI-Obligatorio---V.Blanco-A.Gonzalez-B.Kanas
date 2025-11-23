from flask import Blueprint, jsonify
from app.services.reserva_reportes_service import *

reserva_reportes_bp = Blueprint('reserva_reportes', __name__)

@reserva_reportes_bp.route('/reservas/reportes/salas-mas-reservadas', methods=['GET'])
def endpoint_salas_mas_reservadas():
    return jsonify(salas_mas_reservadas()), 200

@reserva_reportes_bp.route('/reservas/reportes/turnos-mas-demandados', methods=['GET'])
def endpoint_turnos_mas_demandados():
    return jsonify(turnos_mas_demandados()), 200

@reserva_reportes_bp.route('/reservas/reportes/promedio-participantes-sala', methods=['GET'])
def endpoint_promedio_participantes():
    return jsonify(promedio_participantes_por_sala()), 200

@reserva_reportes_bp.route('/reservas/reportes/reservas-por-carrera', methods=['GET'])
def endpoint_reservas_por_carrera():
    return jsonify(reservas_por_carrera()), 200

@reserva_reportes_bp.route('/reservas/reportes/ocupacion-edificio', methods=['GET'])
def endpoint_ocupacion_por_edificio():
    return jsonify(ocupacion_por_edificio()), 200

@reserva_reportes_bp.route('/reservas/reportes/actividad-personas', methods=['GET'])
def endpoint_actividad_personas():
    return jsonify(actividad_participantes()), 200

@reserva_reportes_bp.route('/reservas/reportes/sanciones', methods=['GET'])
def endpoint_sanciones():
    return jsonify(cantidad_sanciones()), 200

#Participantes que más cancelan
@reserva_reportes_bp.route('/reservas/reportes/participantes-canceladores', methods=['GET'])
def obtener_participantes_que_mas_cancelan():
    resultados = participantes_que_mas_cancelan()
    return jsonify(resultados), 200

#Salas sin reservas
@reserva_reportes_bp.route('/reservas/reportes/salas-sin-reservas', methods=['GET'])
def endpoint_salas_sin_reservas():
    return jsonify(salas_sin_reservas()), 200

#Programas que mas usan los edificios
@reserva_reportes_bp.route('/reservas/reportes/programas-edificios', methods=['GET'])
def endpoint_programas_edificios():
    return jsonify(programas_que_mas_usan_los_edificios()), 200

#Porcentajes por tipo de reservas (canceladas, activas, finalizadas)
@reserva_reportes_bp.route('/reservas/reportes/porcentaje-reservas', methods=['GET'])
def endpoint_porcentajes_reservas():
    return jsonify(porcentajes_tipos_reservas()), 200

