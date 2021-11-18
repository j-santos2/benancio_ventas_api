from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app, version='1.0', title='Benancio Ventas API', description='La API Rest de Benancio Ventas')
