from flask import Blueprint, request, jsonify
from app.services.sala_service import (
    listar_salas, obtener_sala, agregar_sala, eliminar_sala
)

sala_bp = Blueprint('sala', __name__)

@sala_bp.route('/salas', methods=['GET'])
def obtener_todas_salas():
    salas = listar_salas()
    return jsonify(salas), 200


@sala_bp.route('/salas/<nombre_sala>', methods=['GET'])
def obtener_una_sala(nombre_sala):
    sala = obtener_sala(nombre_sala)
    if sala:
        return jsonify(sala), 200
    return jsonify({"mensaje": "Sala no encontrada"}), 404


@sala_bp.route('/salas', methods=['POST'])
def crear_sala():
    data = request.get_json()

    nombre_sala = data.get('nombre_sala')
    edificio = data.get('edificio')
    capacidad = data.get('capacidad')
    tipo_sala = data.get('tipo_sala')

    sala, mensaje = agregar_sala(nombre_sala, edificio, capacidad, tipo_sala)

    if sala:
        return jsonify({"mensaje": mensaje, "sala": sala}), 201
    return jsonify({"mensaje": mensaje}), 400


@sala_bp.route('/salas/<nombre_sala>', methods=['DELETE'])
def eliminar_sala_endpoint(nombre_sala):
    if eliminar_sala(nombre_sala):
        return jsonify({"mensaje": "Sala eliminada exitosamente"}), 200
    return jsonify({"mensaje": "Sala no encontrada"}), 404
