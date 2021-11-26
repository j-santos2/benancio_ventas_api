from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from ..servicios import producto
from src import api


producto_model = api.model('Producto', {
    'id': fields.Integer(readonly=True, description='El identificador único del producto'),
    'nombre': fields.String,
    'precio': fields.Integer,
    'uri': fields.Url('producto_ep', readonly=True)
})

class Productos(Resource):
    @api.marshal_with(producto_model)
    def get(self):
        return producto.obtener_todos()

    @api.expect(producto_model)
    @api.marshal_with(producto_model, code=201)
    def post(self):
        respuesta = producto.insertar(api.payload['nombre'], api.payload['precio'])
        return respuesta, 201

class Producto(Resource):
    @api.marshal_with(producto_model)
    def get(self, id):
        return producto.obtener_uno(id)

    @api.expect(producto_model)
    @api.marshal_with(producto_model, code=200)
    def put(self, id):
        respuesta = producto.actualizar(id, api.payload['nombre'], api.payload['precio'])
        return respuesta, 200

    @jwt_required()
    def delete(self, id):
        producto.eliminar(id)
        return "", 204