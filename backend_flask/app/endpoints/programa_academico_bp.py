from flask import Blueprint, request, jsonify
from app.services.programa_academico_service import (listar_programas, obtener_programa, crear_programa, eliminar_programa)

programa_academico_bp = Blueprint('programa_academico', __name__)

@programa_academico_bp.route('/programas', methods=['GET'])
def obtener_todos():
    programas = listar_programas()
    return jsonify(programas), 200


@programa_academico_bp.route('/programas/<int:id_programa>', methods=['GET'])
def obtener_uno(id_programa):
    programa = obtener_programa(id_programa)

    if programa:
        return jsonify(programa), 200
    return jsonify({"mensaje": "Programa no encontrado"}), 404


@programa_academico_bp.route('/programas', methods=['POST'])
def crear():
    data = request.get_json()
    nombre = data.get('nombre_programa')
    id_facultad = data.get('id_facultad')
    tipo = data.get('tipo')

    programa, mensaje = crear_programa(nombre, id_facultad, tipo)
    
    if programa:
        return jsonify({"mensaje": mensaje, "programa": programa}), 201
    return jsonify({"mensaje": mensaje}), 400


@programa_academico_bp.route('/programas/<int:id_programa>', methods=['DELETE'])
def eliminar(id_programa):
    if eliminar_programa(id_programa):
        return jsonify({"mensaje": "Programa eliminado exitosamente"}), 200
    return jsonify({"mensaje": "Programa no encontrado"}), 404