from flask_restx import Resource, fields
from ..servicios import venta
from src import api


venta_model = api.model('Venta', {
    'id': fields.Integer,
    'producto_id': fields.Integer,
    'vendedor_id': fields.Integer,
    'uri': fields.Url('venta_ep')
})
class Ventas(Resource):
    @api.marshal_with(venta_model)
    def get(self):
        return venta.obtener_todos()

    @api.expect(venta_model)
    @api.marshal_with(venta_model, code=201)
    def post(self):
        respuesta = venta.insertar(api.payload['producto_id'], api.payload['vendedor_id'])
        return respuesta, 201

class Venta(Resource):
    @api.marshal_with(venta_model)
    def get(self, id):
        return venta.obtener_uno(id)