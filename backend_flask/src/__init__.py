from flask import Flask
from database.obligatorio import conexion
from endpoints.login_bp import login_bp
from endpoints.participante_bp import participante_bp
from endpoints.programa_academico_bp import programa_academico_bp
from endpoints.participante_programa_academico_bp import participante_programa_academico_bp
from endpoints.reserva_bp import reserva_bp
from endpoints.reserva_participante_bp import reserva_participante_bp
from endpoints.sancion_participante_bp import sanciones_bp

def create_app():
     app = Flask(__name__)

     app.register_blueprint(login_bp)
     app.register_blueprint(participante_bp)
     app.register_blueprint(programa_academico_bp)
     app.register_blueprint(participante_programa_academico_bp)
     app.register_blueprint(reserva_bp)
     app.register_blueprint(reserva_participante_bp)
     app.register_blueprint(sanciones_bp)
     return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)