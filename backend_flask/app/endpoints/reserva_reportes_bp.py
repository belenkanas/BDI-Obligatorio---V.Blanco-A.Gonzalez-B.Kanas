from flask import Blueprint, jsonify
from app.services.reserva_reportes_service import (
    salas_mas_reservadas,
    turnos_mas_demandados,
    promedio_participantes_por_sala,
    reservas_por_carrera,
    ocupacion_por_edificio,
    actividad_participantes,
    cantidad_sanciones
)

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
