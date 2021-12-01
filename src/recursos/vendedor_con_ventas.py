from flask_restx import Resource, fields
from ..servicios import venta
from src import api

venta_con_datos_model = api.model('Venta', {
    'id': fields.Integer,
    'product': fields.String(attribute='producto.nombre'),
    'price': fields.Integer(attribute='producto.precio'),
    'salesperson_id': fields.Integer(attribute='vendedor_id'),
    'uri': fields.Url('venta_ep')
})

class VendedorConVentas(Resource):
    @api.marshal_with(venta_con_datos_model)
    def get(self, id):
        return venta.obtener_ventas_por_vendedor(id)
