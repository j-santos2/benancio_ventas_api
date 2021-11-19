from flask_restx import Resource, fields
from ..servicios import vendedor
from src import api


vendedor_model = api.model('Vendedor', {
    'id': fields.Integer,
    'nombre': fields.String,
    'apellido': fields.String,
    'sucursal_id': fields.Integer,
    'uri': fields.Url('vendedor_ep')
})

class Vendedores(Resource):
    @api.marshal_with(vendedor_model)
    def get(self):
        return vendedor.obtener_todos()

    @api.expect(vendedor_model)
    @api.marshal_with(vendedor_model, code=201)
    def post(self):
        respuesta = vendedor.insertar(api.payload['nombre'], api.payload['apellido'], api.payload['sucursal_id'])
        return respuesta, 201

class Vendedor(Resource):
    @api.marshal_with(vendedor_model)
    def get(self, id):
        return vendedor.obtener_uno(id)
