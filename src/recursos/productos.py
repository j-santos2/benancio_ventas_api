from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from ..servicios import producto
from src import api


producto_model = api.model('Product', {
    'id': fields.Integer(readonly=True, description='Product ID'),
    'name': fields.String(attribute='nombre'),
    'price': fields.Integer(attribute='precio'),
    'uri': fields.Url('producto_ep', readonly=True)
})

class Productos(Resource):
    @api.marshal_with(producto_model)
    def get(self):
        limit = request.args.get("limit", 100, type=int)
        offset = request.args.get("offset", 0, type=int)
        return producto.obtener_todos_paginado(limit, offset)

    @api.expect(producto_model)
    @api.marshal_with(producto_model, code=201)
    @jwt_required()
    def post(self):
        respuesta = producto.insertar(api.payload['name'], api.payload['price'])
        return respuesta, 201

class Producto(Resource):
    @api.marshal_with(producto_model)
    def get(self, id):
        return producto.obtener_uno(id)

    @api.expect(producto_model)
    @api.marshal_with(producto_model, code=200)
    @jwt_required()
    def put(self, id):
        respuesta = producto.actualizar(id, api.payload['name'], api.payload['price'])
        return respuesta, 200

    @jwt_required()
    def delete(self, id):
        producto.eliminar(id)
        return "", 204