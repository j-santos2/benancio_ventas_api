from flask_jwt_extended import create_access_token
from flask_restx import Resource, fields
from ..servicios import usuario
from src import api

usuario_model = api.model('Users', {
    'id': fields.Integer,
    'name': fields.String(attribute='nombre')
})

class Usuarios(Resource):
    @api.marshal_with(usuario_model, code = 201)
    def post(self):
        respuesta = usuario.insertar(api.payload["name"], api.payload["password"])
        
        return respuesta, 201

class UsuarioLogin(Resource):
    def post(self):
        if usuario.login(api.payload["name"], api.payload["password"]):
            access_token = create_access_token(identity = api.payload["name"])
            return {"token":access_token}, 201
        else:
            return {"msg":"Username and/or password is incorrect"}, 401