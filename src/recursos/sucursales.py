from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import Resource, fields
from ..servicios import sucursal
from src import api


sucursal_model = api.model('Stores', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(attribute='nombre'),
    'uri': fields.Url('sucursal_ep', readonly=True)
})

class Sucursales(Resource):
    @api.marshal_with(sucursal_model)
    def get(self):
        return sucursal.obtener_todos()

    @api.expect(sucursal_model)
    @api.marshal_with(sucursal_model, code=201)
    @jwt_required()
    def post(self):
        respuesta = sucursal.insertar(api.payload['name'])
        return respuesta, 201

class Sucursal(Resource):
    @api.marshal_with(sucursal_model)
    def get(self, id):
        return sucursal.obtener_uno(id)
    
    @api.expect(sucursal_model)
    @api.marshal_with(sucursal_model, code=200)
    @jwt_required()
    def put(self, id):
        respuesta = sucursal.actualizar(id, api.payload['name'])
        return respuesta, 200

    @jwt_required()
    def delete(self, id):
        sucursal.eliminar(id)
        return "", 204
    
