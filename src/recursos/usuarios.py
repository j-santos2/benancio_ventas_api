from flask_restx import Resource, fields
#from ..servicios import usuario
from src import api

usuario_model = api.model('Usuario', {
    'id': fields.Integer,
    'nombre': fields.String
})

class Usuarios(Resource):
    @api.marshal_with(usuario_model, code = 201)
    def post(self):
        #respuesta = usuario.insertar(api.payload["nombre"], api.payload["clave"])
        respuesta = {"id": 1 , "nombre":api.payload["nombre"]}
        return respuesta, 201