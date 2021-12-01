from flask_jwt_extended import jwt_required

from flask_restx import Resource, fields
from ..servicios import venta
from src import api


venta_model = api.model('Sales', {
    'id': fields.Integer(readonly=True),
    'product_id': fields.Integer(attribute='producto_id'),
    'salesperson_id': fields.Integer(attribute='vendedor_id'),
    'uri': fields.Url('venta_ep', readonly=True)
})
class Ventas(Resource):
    @api.marshal_with(venta_model)
    def get(self):
        return venta.obtener_todos()

    @api.expect(venta_model)
    @api.marshal_with(venta_model, code=201)
    @jwt_required()
    def post(self):
        respuesta = venta.insertar(api.payload['product_id'], api.payload['salesperson_id'])
        return respuesta, 201

class Venta(Resource):
    @api.marshal_with(venta_model)
    def get(self, id):
        return venta.obtener_uno(id)