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
    try:
        id_sala = int(id_sala)
    except:
        return jsonify({
            "eliminado": False,
            "requiere_force": False,
            "mensaje": "El ID de la sala debe ser numérico."
        }), 400

    force = request.args.get("force", "false").lower() == "true"

    eliminado, requiere_force, mensaje = eliminar_sala(id_sala, force)

    # Caso: requiere confirmación (force=false y hay reservas)
    if requiere_force and not force:
        return jsonify({
            "eliminado": False,
            "requiere_force": True,
            "mensaje": mensaje or "La sala tiene reservas asociadas. Debes usar force=true."
        }), 409

    # Caso: hubo error interno u operación fallida
    if not eliminado:
        return jsonify({
            "eliminado": False,
            "requiere_force": False,
            "mensaje": mensaje or "Error al eliminar la sala."
        }), 400

    # Caso: eliminado con éxito
    return jsonify({
        "eliminado": True,
        "mensaje": "Sala eliminada correctamente."
    }), 200



@sala_bp.route('/salas-permitidas', methods=['GET'])
def salas_permitidas():
    ci = request.args.get("ci")
    id_edificio = request.args.get("id_edificio")

    from app.services.sala_service import obtener_salas_permitidas_para_usuario
    salas = obtener_salas_permitidas_para_usuario(ci, id_edificio)
    return jsonify(salas), 200
