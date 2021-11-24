from src.recursos import Productos, Producto, Vendedores, Vendedor, VendedorConVentas, Sucursales, Sucursal, SucursalConVendedores, Ventas, Venta

from src import app, api


api.add_resource(Productos, '/productos', endpoint = 'productos_ep')
api.add_resource(Producto, '/productos/<int:id>', endpoint = 'producto_ep')

api.add_resource(Vendedores, '/vendedores', endpoint = 'vendedores_ep')
api.add_resource(Vendedor, '/vendedores/<int:id>', endpoint = 'vendedor_ep')
api.add_resource(VendedorConVentas, '/vendedores/<int:id>/ventas', endpoint = 'vendedor_ventas_ep')

api.add_resource(Sucursales, '/sucursales', endpoint = 'sucursales_ep')
api.add_resource(Sucursal, '/sucursales/<int:id>', endpoint = 'sucursal_ep')
api.add_resource(SucursalConVendedores, '/sucursales/<int:id>/vendedores', endpoint = 'sucursal_vendedores_ep')

api.add_resource(Ventas, '/ventas', endpoint = 'ventas_ep')
api.add_resource(Venta, '/ventas/<int:id>', endpoint = 'venta_ep')