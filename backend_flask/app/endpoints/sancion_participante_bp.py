from flask import Blueprint, jsonify, request
from app.services.sancion_participante_service import *

sanciones_bp = Blueprint('sanciones', __name__)

#Obtener TODAS las sanciones 
@sanciones_bp.route('/sanciones', methods=['GET'])
def obtener_todas_sanciones():
    sanciones = listar_sanciones()
    return jsonify(sanciones), 200

#Obtener solo las sanciones ACITVAS
@sanciones_bp.route('/sanciones/activas', methods=['GET'])
def obtener_sanciones_activas():
    sanciones = listar_sanciones_activas()
    return jsonify(sanciones), 200

#Sanciones de un participante
@sanciones_bp.route('/sanciones/<ci_participante>', methods=['GET'])
def obtener_sanciones_de_participante(ci_participante):
    sanciones = obtener_sanciones_participante(ci_participante)
    if sanciones:
        return jsonify(sanciones), 200
    return jsonify({"mensaje": f"No se encontraron sanciones para el participante {ci_participante}"}), 404

@sanciones_bp.route('/sanciones/por-rol-tipo', methods=['GET'])
def obtener_sanciones_por_rol_y_tipo():
    resultados = sanciones_por_rol_y_tipo()
    return jsonify(resultados), 200

#Participantes que más cancelan
@sanciones_bp.route('/sanciones/participantes-canceladores', methods=['GET'])
def obtener_participantes_que_mas_cancelan():
    resultados = participantes_que_mas_cancelan()
    return jsonify(resultados), 200

#Crear sanción manualmente
@sanciones_bp.route('/sanciones', methods=['POST'])
def crear_nueva_sancion():
    data = request.get_json()
    ci_participante = data.get('ci_participante')
    fecha_inicio = data.get('fecha_inicio')
    meses = data.get('meses', 2)

    if not ci_participante:
        return jsonify({"mensaje": "El campo 'ci_participante' es obligatorio"}), 400

    sancion, mensaje = crear_sancion(ci_participante, fecha_inicio, meses)
    if sancion:
        return jsonify({"mensaje": mensaje, "sancion": sancion}), 201
    return jsonify({"mensaje": mensaje}), 400


#Creación de sancion automática
@sanciones_bp.route('/sanciones/automatica/<int:id_reserva>', methods=['POST'])
def sancionar_reserva_sin_asistencia(id_reserva):
    resultado, mensaje = sancionar_participantes_sin_asistencia(id_reserva)
    if resultado:
        return jsonify({"mensaje": mensaje, "participantes_sancionados": resultado}), 201
    return jsonify({"mensaje": mensaje}), 400