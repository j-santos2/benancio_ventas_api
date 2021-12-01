from inspect import Attribute
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from ..servicios import vendedor
from src import api


vendedor_model = api.model('Salesperson', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(attribute='nombre'), 
    'lastname': fields.String(attribute='apellido'),
    'store_id': fields.Integer(attribute='sucursal_id'),
    'uri': fields.Url('vendedor_ep', readonly=True)
})

class Vendedores(Resource):
    @api.marshal_with(vendedor_model)
    def get(self):
        return vendedor.obtener_todos()

    @api.expect(vendedor_model)
    @api.marshal_with(vendedor_model, code=201)
    @jwt_required()
    def post(self):
        respuesta = vendedor.insertar(api.payload['name'], api.payload['lastname'], api.payload['store_id'])
        return respuesta, 201

class Vendedor(Resource):
    @api.marshal_with(vendedor_model)
    def get(self, id):
        return vendedor.obtener_uno(id)
