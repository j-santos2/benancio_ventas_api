from src import app, api
import src.recursos.error_handlers
from src.recursos import Productos, Producto, Vendedores, Vendedor, VendedorConVentas, Sucursales, Sucursal, SucursalConVendedores, Ventas, Venta, Usuarios, UsuarioLogin


api.add_resource(Productos, '/products', endpoint = 'productos_ep')
api.add_resource(Producto, '/products/<int:id>', endpoint = 'producto_ep')

api.add_resource(Vendedores, '/salesperson', endpoint = 'vendedores_ep')
api.add_resource(Vendedor, '/salesperson/<int:id>', endpoint = 'vendedor_ep')
api.add_resource(VendedorConVentas, '/salesperson/<int:id>/sales', endpoint = 'vendedor_ventas_ep')

api.add_resource(Sucursales, '/sucursales', endpoint = 'sucursales_ep')
api.add_resource(Sucursal, '/sucursales/<int:id>', endpoint = 'sucursal_ep')
api.add_resource(SucursalConVendedores, '/sucursales/<int:id>/vendedores', endpoint = 'sucursal_vendedores_ep')

api.add_resource(Ventas, '/ventas', endpoint = 'ventas_ep')
api.add_resource(Venta, '/ventas/<int:id>', endpoint = 'venta_ep')

api.add_resource(Usuarios,'/usuarios', endpoint = 'usuarios_ep')
api.add_resource(UsuarioLogin, '/usuarios/login', endpoint = 'usuario_login_ep')