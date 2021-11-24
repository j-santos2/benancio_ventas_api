from flask_restx import Resource, fields
from ..servicios import venta
from src import api

venta_con_datos_model = api.model('Venta', {
    'id': fields.Integer,
    'producto': fields.String(attribute='producto.nombre'),
    'precio': fields.Integer(attribute='producto.precio'),
    'vendedor_id': fields.Integer,
    'uri': fields.Url('venta_ep')
})

class VendedorConVentas(Resource):
    @api.marshal_with(venta_con_datos_model)
    def get(self, id):
        return venta.obtener_ventas_por_vendedor(id)
