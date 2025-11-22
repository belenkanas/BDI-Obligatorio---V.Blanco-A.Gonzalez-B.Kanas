from flask import Blueprint, request, jsonify
from app.services.sala_service import (listar_salas, obtener_sala, agregar_sala, eliminar_sala, obtener_salas_permitidas_para_usuario)

sala_bp = Blueprint('sala', __name__)

@sala_bp.route('/salas', methods=['GET'])
def obtener_todas_salas():
    salas = listar_salas()
    return jsonify(salas), 200


@sala_bp.route('/salas/<id_sala>', methods=['GET'])
def obtener_una_sala(id_sala):
    sala = obtener_sala(id_sala)
    if sala:
        return jsonify(sala), 200
    return jsonify({"mensaje": "Sala no encontrada"}), 404


@sala_bp.route('/salas', methods=['POST'])
def crear_sala():
    data = request.get_json()

    nombre_sala = data.get('nombre_sala')
    id_edificio = data.get('id_edificio')
    capacidad = data.get('capacidad')
    tipo_sala = data.get('tipo_sala')

    sala, mensaje = agregar_sala(nombre_sala, id_edificio, capacidad, tipo_sala)

    if sala:
        return jsonify({"mensaje": mensaje, "sala": sala}), 201
    return jsonify({"mensaje": mensaje}), 400


@sala_bp.route('/salas/<id_sala>', methods=['DELETE'])
def eliminar_sala_endpoint(id_sala):
    ok, error = eliminar_sala(id_sala)

    if ok:
        return jsonify({"mensaje": "Sala eliminada con éxito"}), 200
    else:
        return jsonify({"error": error}), 400
    
    

@sala_bp.route('/salas-permitidas', methods=['GET'])
def salas_permitidas():
    ci = request.args.get("ci")
    id_edificio = request.args.get("id_edificio")

    from app.services.sala_service import obtener_salas_permitidas_para_usuario
    salas = obtener_salas_permitidas_para_usuario(ci, id_edificio)
    return jsonify(salas), 200
