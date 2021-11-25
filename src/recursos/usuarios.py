from flask_jwt_extended import create_access_token
from flask_restx import Resource, fields
from ..servicios import usuario
from src import api

usuario_model = api.model('Usuario', {
    'id': fields.Integer,
    'nombre': fields.String
})

class Usuarios(Resource):
    @api.marshal_with(usuario_model, code = 201)
    def post(self):
        respuesta = usuario.insertar(api.payload["nombre"], api.payload["clave"])
        
        return respuesta, 201

class UsuarioLogin(Resource):
    def post(self):
        access_token = create_access_token(identity = api.payload["nombre"])

        return {"token":access_token}, 201