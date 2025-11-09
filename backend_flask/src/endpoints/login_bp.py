from flask import Blueprint, request, jsonify
from backend_flask.src.services.login_service import login, register_user

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def iniciar_sesion():
    data = request.get_json()
    correo = data.get('correo')
    password = data.get('password')

    usuario = login(correo, password)
    if usuario:
        return jsonify({"mensaje": "Inicio de sesión exitoso", "usuario": usuario}), 200
    return jsonify({"mensaje": "Credenciales inválidas"}), 401


@login_bp.route('/register', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    correo = data.get('correo')
    password = data.get('password')

    usuario, mensaje = register_user(correo, password)
    if usuario:
        return jsonify({"mensaje": mensaje, "usuario": usuario}), 201
    return jsonify({"mensaje": mensaje}), 400
