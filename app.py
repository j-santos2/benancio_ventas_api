from src import app, api
import src.recursos.error_handlers
from src.recursos import Productos, Producto, Vendedores, Vendedor, VendedorConVentas, Sucursales, Sucursal, SucursalConVendedores, Ventas, Venta, Usuarios, UsuarioLogin


api.add_resource(Productos, '/products', endpoint = 'productos_ep')
api.add_resource(Producto, '/products/<int:id>', endpoint = 'producto_ep')

api.add_resource(Vendedores, '/salesperson', endpoint = 'vendedores_ep')
api.add_resource(Vendedor, '/salesperson/<int:id>', endpoint = 'vendedor_ep')
api.add_resource(VendedorConVentas, '/salesperson/<int:id>/sales', endpoint = 'vendedor_ventas_ep')

api.add_resource(Sucursales, '/stores', endpoint = 'sucursales_ep')
api.add_resource(Sucursal, '/stores/<int:id>', endpoint = 'sucursal_ep')
api.add_resource(SucursalConVendedores, '/stores/<int:id>/salesperson', endpoint = 'sucursal_vendedores_ep')

api.add_resource(Ventas, '/sales', endpoint = 'ventas_ep')
api.add_resource(Venta, '/sales/<int:id>', endpoint = 'venta_ep')

api.add_resource(Usuarios,'/users', endpoint = 'usuarios_ep')
api.add_resource(UsuarioLogin, '/users/login', endpoint = 'usuario_login_ep')