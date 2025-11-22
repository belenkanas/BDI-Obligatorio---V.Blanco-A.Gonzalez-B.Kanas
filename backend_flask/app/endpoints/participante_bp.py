from flask import Blueprint, request, jsonify
from app.services.participante_service import (listar_participantes, obtener_participante, agregar_participante, eliminar_participante, obtener_participantes_permitidos)

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


from flask import Blueprint, request, jsonify
from app.services.participante_service import eliminar_participante

participante_bp = Blueprint("participante", __name__)

@participante_bp.route("/participantes/<ci>", methods=["DELETE"])
def eliminar_participante_endpoint(ci):

    # Leer parámetro force del query string (?force=true)
    force_param = request.args.get("force", "false").lower()
    force = force_param == "true"

    eliminado, requiere_force, mensaje = eliminar_participante(ci, force)

    # Caso: debe forzar pero no se pasó force=true
    if requiere_force and not force:
        return jsonify({
            "eliminado": False,
            "requiere_force": True,
            "mensaje": "El participante tiene reservas activas. Confirma si deseas borrar forzadamente."
        }), 409  # 409 Conflict

    # Caso: error interno u otra condición
    if not eliminado:
        return jsonify({
            "eliminado": False,
            "requiere_force": False,
            "mensaje": mensaje or "Error eliminando participante."
        }), 400

    # Caso: eliminado con éxito
    return jsonify({
        "eliminado": True,
        "mensaje": "Participante eliminado correctamente."
    }), 200


@participante_bp.route('/participantes-permitidos', methods=['GET'])
def participantes_permitidos():
    id_sala = int(request.args.get('id_sala'))
    participantes = obtener_participantes_permitidos(id_sala)
    return jsonify(participantes), 200