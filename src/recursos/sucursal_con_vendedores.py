from flask_restx import Resource
from ..servicios import vendedor
from src import api
from .vendedores import vendedor_model

class SucursalConVendedores(Resource):
    @api.marshal_with(vendedor_model)
    def get(self,id):
        return vendedor.obtener_vendedores_por_sucursal(id)