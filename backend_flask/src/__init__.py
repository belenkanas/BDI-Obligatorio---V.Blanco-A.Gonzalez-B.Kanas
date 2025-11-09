from flask import Flask, jsonify
from flask_cors import CORS
import logging
from database import conexion
from endpoints import (
    login_bp,
    participante_bp,
    programa_academico_bp,
    participante_programa_academico_bp,
    reserva_bp,
    reserva_participante_bp,
    sanciones_bp,
)

def create_app():
    app = Flask(__name__)
    
    app.config["JSON_AS_ASCII"] = False  # Permite caracteres con tilde/ñ
    app.config["JSON_SORT_KEYS"] = False  # No ordena las claves del JSON automáticamente

    # Permite acceso al backend desde cualquier origen
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Registrar Blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(participante_bp)
    app.register_blueprint(programa_academico_bp)
    app.register_blueprint(participante_programa_academico_bp)
    app.register_blueprint(reserva_bp)
    app.register_blueprint(reserva_participante_bp)
    app.register_blueprint(sanciones_bp)

    # Manejo de errores
    @app.errorhandler(404)
    def recurso_no_encontrado(e):
        return jsonify({"error": "Ruta no encontrada", "detalle": str(e)}), 404

    @app.errorhandler(500)
    def error_interno(e):
        app.logger.error(f"Error interno del servidor: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

    # logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    app.logger.info("Aplicación Flask inicializada correctamente")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)