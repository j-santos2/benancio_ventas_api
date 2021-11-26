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

    @api.expect(sucursal_model)
    @api.marshal_with(sucursal_model, code=201)
    def post(self):
        respuesta = sucursal.insertar(api.payload['nombre'])
        return respuesta, 201

class Sucursal(Resource):
    @api.marshal_with(sucursal_model)
    def get(self, id):
        return sucursal.obtener_uno(id)
    
    @api.expect(sucursal_model)
    @api.marshal_with(sucursal_model, code=200)
    def put(self, id):
        respuesta = sucursal.actualizar(id, api.payload['nombre'])
        return respuesta, 200

    def delete(self, id):
        sucursal.eliminar(id)
        return "", 204
    
