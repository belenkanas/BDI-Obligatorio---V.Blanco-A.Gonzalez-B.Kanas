from flask import Flask
from database.obligatorio import conexion
from endpoints.login_bp import login_bp

def create_app():
     app = Flask(__name__)
     conexion.init_app(app)

     app.register_blueprint(login_bp)

     return app
