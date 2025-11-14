from flask import Blueprint, request, jsonify
from app.services.participante_service import (listar_participantes, obtener_participante, agregar_participante, eliminar_participante)

participante_bp = Blueprint('participante', __name__)

@participante_bp.route('/participantes', methods=['GET'])
def obtener_todos():
    participantes = listar_participantes()
    return jsonify(participantes), 200


@participante_bp.route('/participantes/<ci>', methods=['GET'])
def obtener_uno(ci):
    participante = obtener_participante(ci)

    if participante:
        return jsonify(participante), 200
    return jsonify({"mensaje": "Participante no encontrado"}), 404


@participante_bp.route('/participantes', methods=['POST'])
def crear():
    data = request.get_json()
    ci = data.get('ci')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')

    participante, mensaje = agregar_participante(ci, nombre, apellido, email)
    
    if participante:
        return jsonify({"mensaje": mensaje, "participante": participante}), 201
    return jsonify({"mensaje": mensaje}), 400


@participante_bp.route('/participantes/<ci>', methods=['DELETE'])
def eliminar(ci):
    if eliminar_participante(ci):
        return jsonify({"mensaje": "Participante eliminado exitosamente"}), 200
    return jsonify({"mensaje": "Participante no encontrado"}), 404