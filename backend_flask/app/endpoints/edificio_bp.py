from flask import Blueprint, request, jsonify
from app.services.edificio_service import (
    listar_edificios, obtener_edificio, agregar_edificio, eliminar_edificio
)

edificio_bp = Blueprint('edificio', __name__)

@edificio_bp.route('/edificios', methods=['GET'])
def obtener_todos_edificios():
    edificios = listar_edificios()
    return jsonify(edificios), 200


@edificio_bp.route('/edificios/<id_edificio>', methods=['GET'])
def obtener_un_edificio(id_edificio):
    edificio = obtener_edificio(id_edificio)
    if edificio:
        return jsonify(edificio), 200
    return jsonify({"mensaje": "Edificio no encontrado"}), 404


@edificio_bp.route('/edificios', methods=['POST'])
def crear_edificio():
    data = request.get_json()

    nombre_edificio = data.get('nombre_edificio')
    direccion = data.get('direccion')
    departamento = data.get('departamento')

    edificio, mensaje = agregar_edificio(nombre_edificio, direccion, departamento)

    if edificio:
        return jsonify({"mensaje": mensaje, "edificio": edificio}), 201
    return jsonify({"mensaje": mensaje}), 400


@edificio_bp.route('/edificios/<id_edificio>', methods=['DELETE'])
def eliminar_edificio_endpoint(id_edificio):
    if eliminar_edificio(id_edificio):
        return jsonify({"mensaje": "Edificio eliminado exitosamente"}), 200
    return jsonify({"mensaje": "Edificio no encontrado"}), 404
