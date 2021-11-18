from flask_restx import Resource, fields
from ..servicios import sucursal
from src import api


sucursal_model = api.model('Sucursal', {
    'id': fields.Integer,
    'nombre': fields.String,
    'uri': fields.Url('sucursal_ep')
})

class Sucursales(Resource):
    @api.marshal_with(sucursal_model)
    def get(self):
        return sucursal.obtener_todos()

class Sucursal(Resource):
    @api.marshal_with(sucursal_model)
    def get(self, id):
        return sucursal.obtener_uno(id)
