from flask import Flask
from flask_restx import Api, Resource, fields

from src.servicios import producto, vendedor, sucursal, venta

app = Flask(__name__)
api = Api(app, version='1.0', title='Benancio Ventas API', description='La API Rest de Benancio Ventas')

producto_model = api.model('Producto', {
    'id': fields.Integer(readonly=True, description='El identificador único del producto'),
    'nombre': fields.String,
    'precio': fields.Integer,
    'uri': fields.Url('producto_ep', readonly=True)
})
vendedor_model = api.model('Vendedor', {
    'id': fields.Integer,
    'nombre': fields.String,
    'apellido': fields.String,
    'sucursal_id': fields.Integer,
    'uri': fields.Url('vendedor_ep')
})
sucursal_model = api.model('Sucursal', {
    'id': fields.Integer,
    'nombre': fields.String,
    'uri': fields.Url('sucursal_ep')
})
venta_model = api.model('Venta', {
    'id': fields.Integer,
    'producto_id': fields.Integer,
    'vendedor_id': fields.Integer,
    'uri': fields.Url('venta_ep')
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

class Vendedores(Resource):
    @api.marshal_with(vendedor_model)
    def get(self):
        return vendedor.obtener_todos()

class Vendedor(Resource):
    @api.marshal_with(vendedor_model)
    def get(self, id):
        return vendedor.obtener_uno(id)

class Sucursales(Resource):
    @api.marshal_with(sucursal_model)
    def get(self):
        return sucursal.obtener_todos()

class Sucursal(Resource):
    @api.marshal_with(sucursal_model)
    def get(self, id):
        return sucursal.obtener_uno(id)

class Ventas(Resource):
    @api.marshal_with(venta_model)
    def get(self):
        return venta.obtener_todos()

class Venta(Resource):
    @api.marshal_with(venta_model)
    def get(self, id):
        return venta.obtener_uno(id)

api.add_resource(Productos, '/productos', endpoint = 'productos_ep')
api.add_resource(Producto, '/productos/<int:id>', endpoint = 'producto_ep')

api.add_resource(Vendedores, '/vendedores/', endpoint = 'vendedores_ep')
api.add_resource(Vendedor, '/vendedores/<int:id>', endpoint = 'vendedor_ep')

api.add_resource(Sucursales, '/sucursales', endpoint = 'sucursales_ep')
api.add_resource(Sucursal, '/sucursales/<int:id>', endpoint = 'sucursal_ep')

api.add_resource(Ventas, '/ventas', endpoint = 'ventas_ep')
api.add_resource(Venta, '/ventas/<int:id>', endpoint = 'venta_ep')