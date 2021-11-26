from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from .servicios.exceptions import ObjetoNoEncontrado

app = Flask(__name__)
api = Api(app, version='1.0', title='Benancio Ventas API', description='La API Rest de Benancio Ventas')
app.config['JWT_SECRET_KEY'] = 'Esta es mi clabe secreta'
app.config["ERROR_INCLUDE_MESSAGE"] = False
jwt = JWTManager(app)

@api.errorhandler(ObjetoNoEncontrado)
def handle_exception(e):
    '''Return a custom message and 400 status code'''
    return {"msg":str(e)}, 400