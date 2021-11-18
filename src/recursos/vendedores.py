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

class Vendedor(Resource):
    @api.marshal_with(vendedor_model)
    def get(self, id):
        return vendedor.obtener_uno(id)
