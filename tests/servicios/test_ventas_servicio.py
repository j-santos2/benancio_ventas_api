import unittest

from conexion import conexion
from src.modelos import Venta, ProductoModelo, VendedorModelo, SucursalModelo
from src.servicios import venta

class Test_VentasServicio(unittest.TestCase):
    def setUp(self):
        primera_sucursal = SucursalModelo(nombre = "Primera sucursal")
        segunda_sucursal = SucursalModelo(nombre = "Segunda sucursal")
        conexion.sesion.add(primera_sucursal)
        conexion.sesion.add(segunda_sucursal)
        conexion.sesion.commit()
        
        primer_vendedor = VendedorModelo(nombre="1º", apellido="vendedor", sucursal_id=primera_sucursal.id)
        segundo_vendedor = VendedorModelo(nombre="5º", apellido="vendedor", sucursal_id=segunda_sucursal.id)
        conexion.sesion.add(primer_vendedor)
        conexion.sesion.add(segundo_vendedor)

        primer_producto = ProductoModelo(nombre="1º producto", precio=10000)
        segundo_producto = ProductoModelo(nombre="2º producto", precio=20000)
        conexion.sesion.add(primer_producto)
        conexion.sesion.add(segundo_producto)
        
        conexion.sesion.commit()

        conexion.sesion.add(Venta(producto_id=primer_producto.id, vendedor_id=primer_vendedor.id))
        conexion.sesion.add(Venta(producto_id=segundo_producto.id, vendedor_id=segundo_vendedor.id))
        conexion.sesion.add(Venta(producto_id=segundo_producto.id, vendedor_id=primer_vendedor.id))
        conexion.sesion.add(Venta(producto_id=primer_producto.id, vendedor_id=segundo_vendedor.id))

    def tearDown(self):
        conexion.sesion.query(VendedorModelo).delete()
        conexion.sesion.query(SucursalModelo).delete()
        conexion.sesion.query(ProductoModelo).delete()
        conexion.sesion.query(Venta).delete()

    def test_venta_obtener_todos_retorna_lista_con_objetos_con_id_productoid_vendedorid(self):
        resultado = venta.obtener_todos()
        self.assertTrue(isinstance(resultado[0].id, int))
        self.assertTrue(isinstance(resultado[0].producto_id, int))
        self.assertTrue(isinstance(resultado[0].vendedor_id, int))

    def test_venta_obtener_uno_retorna_objeto_con_id_nombre(self):
        resultado = venta.obtener_uno(1)
        self.assertTrue(isinstance(resultado.id, int))
        self.assertTrue(isinstance(resultado.producto_id, int))
        self.assertTrue(isinstance(resultado.vendedor_id, int))

    def test_insertar_venta_ultima_venta_tiene_los_valores_de_la_venta_insertada(self):
        venta.insertar(1, 1)

        ventas = venta.obtener_todos()

        self.assertEqual(1, ventas[-1].producto_id)
        self.assertEqual(1, ventas[-1].vendedor_id)