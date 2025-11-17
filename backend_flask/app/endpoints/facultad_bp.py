from flask import Blueprint, request, jsonify
from app.services.facultad_service import (
    listar_facultades, obtener_facultad, agregar_facultad, eliminar_facultad
)

facultad_bp = Blueprint('facultad', __name__)

@facultad_bp.route('/facultades', methods=['GET'])
def obtener_todas_facultades():
    facultades = listar_facultades()
    return jsonify(facultades), 200


@facultad_bp.route('/facultades/<id_facultad>', methods=['GET'])
def obtener_una_facultad(id_facultad):
    facultad = obtener_facultad(id_facultad)
    if facultad:
        return jsonify(facultad), 200
    return jsonify({"mensaje": "Facultad no encontrada"}), 404


@facultad_bp.route('/facultades', methods=['POST'])
def crear_facultad():
    data = request.get_json()
    nombre = data.get('nombre')

    facultad, mensaje = agregar_facultad(nombre)

    if facultad:
        return jsonify({"mensaje": mensaje, "facultad": facultad}), 201
    return jsonify({"mensaje": mensaje}), 400


@facultad_bp.route('/facultades/<id_facultad>', methods=['DELETE'])
def eliminar_facultad_endpoint(id_facultad):
    if eliminar_facultad(id_facultad):
        return jsonify({"mensaje": "Facultad eliminada exitosamente"}), 200
    return jsonify({"mensaje": "Facultad no encontrada"}), 404
