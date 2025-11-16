from flask import Flask, jsonify
from flask_cors import CORS
from app.database.conexion_db import conexion
from app.endpoints import (
    login_bp,
    participante_bp,
    programa_academico_bp,
    participante_programa_academico_bp,
    reserva_bp,
    reserva_participante_bp,
    sanciones_bp,
)
import logging

def create_app():
    app = Flask(__name__)

    app.config["JSON_AS_ASCII"] = False
    app.config["JSON_SORT_KEYS"] = False

    CORS(app, resources={r"/*": {"origins": "*"}})

    # Registrar blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(participante_bp)
    app.register_blueprint(programa_academico_bp)
    app.register_blueprint(participante_programa_academico_bp)
    app.register_blueprint(reserva_bp)
    app.register_blueprint(reserva_participante_bp)
    app.register_blueprint(sanciones_bp)

    #Ruta raiz
    @app.route("/")
    def home():
        return {
            "mensaje": "API del obligatorio funcionando 🎉",
            "estado": "ok"
        }
    
    #Manejo de errores
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Ruta no encontrada"}), 404

    logging.basicConfig(level=logging.INFO)
    app.logger.info("Flask inicializado correctamente")

    return app

