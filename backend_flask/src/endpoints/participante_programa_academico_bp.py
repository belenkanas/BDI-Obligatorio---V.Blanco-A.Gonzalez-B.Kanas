from flask import Blueprint, request, jsonify
from services.participante_programa_academico_service import (listar_registros, obtener_registro, crear_registro, eliminar_registro)

participante_programa_academico_bp = Blueprint('participante_programa_academico', __name__)

@participante_programa_academico_bp.route('/participantes_programa_academico', methods=['GET'])
def obtener_todos():
    registros = listar_registros()
    return jsonify(registros), 200


@participante_programa_academico_bp.route('/participantes_programa_academico/<int:id_alumno_programa>', methods=['GET'])
def obtener_uno(id_alumno_programa):
    registro = obtener_registro(id_alumno_programa)
    if registro:
        return jsonify(registro), 200
    return jsonify({"mensaje": "Registro no encontrado"}), 404


@participante_programa_academico_bp.route('/participantes_programa_academico', methods=['POST'])
def crear():
    data = request.get_json()
    ci_participante = data.get('ci_participante')
    id_programa = data.get('id_programa')
    rol = data.get('rol')

    registro, mensaje = crear_registro(ci_participante, id_programa, rol)
    return jsonify({"mensaje": mensaje, "registro": registro}), 201


@participante_programa_academico_bp.route('/participantes_programa_academico/<int:id_alumno_programa>', methods=['DELETE'])
def eliminar(id_alumno_programa):
    if eliminar_registro(id_alumno_programa):
        return jsonify({"mensaje": "Registro eliminado exitosamente"}), 200
    return jsonify({"mensaje": "Registro no encontrado"}), 404