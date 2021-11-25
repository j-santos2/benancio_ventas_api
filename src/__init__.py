from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app, version='1.0', title='Benancio Ventas API', description='La API Rest de Benancio Ventas')
app.config['JWT_SECRET_KEY'] = 'Esta es mi clabe secreta'
jwt = JWTManager(app)
