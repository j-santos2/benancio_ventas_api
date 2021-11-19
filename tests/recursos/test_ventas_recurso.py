import json
import unittest
from app import app
from src.modelos import VentaModelo, SucursalModelo, VendedorModelo, ProductoModelo
from conexion import conexion

class Test_RecursoVenta(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        cls.app = app.test_client()

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

        conexion.sesion.add(VentaModelo(producto_id=primer_producto.id, vendedor_id=primer_vendedor.id))
        conexion.sesion.add(VentaModelo(producto_id=segundo_producto.id, vendedor_id=segundo_vendedor.id))
        conexion.sesion.add(VentaModelo(producto_id=segundo_producto.id, vendedor_id=primer_vendedor.id))
        conexion.sesion.add(VentaModelo(producto_id=primer_producto.id, vendedor_id=segundo_vendedor.id))

    def tearDown(self):
        conexion.sesion.query(VendedorModelo).delete()
        conexion.sesion.query(SucursalModelo).delete()
        conexion.sesion.query(ProductoModelo).delete()
        conexion.sesion.query(VentaModelo).delete()

    def test_endpoint_ventas_retorna_json_con_ventas(self):
        response = self.app.get("/ventas")

        response_json = json.loads(response.data.decode("utf-8"))
        primera_venta = response_json[0]

        self.assertTrue("id" in primera_venta)
        self.assertTrue("producto_id" in primera_venta)
        self.assertTrue("vendedor_id" in primera_venta)
        self.assertTrue("uri" in primera_venta)
        self.assertEqual(200, response.status_code)

    def test_endpoint_ventas_get_con_id_retorna_json_de_venta_con_sus_campos(self):
        nueva_sucursal = SucursalModelo(nombre = "Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)
        conexion.sesion.commit()

        nuevo_vendedor = VendedorModelo(nombre="Nuevo vendedor", apellido='Crack', sucursal_id=nueva_sucursal.id)
        conexion.sesion.add(nuevo_vendedor)
        nuevo_producto = ProductoModelo(nombre="Nuevo producto", precio=15000)
        conexion.sesion.add(nuevo_producto)         
        conexion.sesion.commit()

        nueva_venta = VentaModelo(producto_id=nuevo_producto.id, vendedor_id=nuevo_vendedor.id)
        conexion.sesion.add(nueva_venta)
        conexion.sesion.commit()   

        uri_nueva_venta= f"/ventas/{nueva_venta.id}"
        response = self.app.get(uri_nueva_venta)
        
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(nueva_venta.id, response_json["id"])
        self.assertEqual(nueva_venta.producto_id, response_json["producto_id"])
        self.assertEqual(nueva_venta.vendedor_id, response_json["vendedor_id"])
        self.assertEqual(uri_nueva_venta, response_json["uri"])        
        self.assertEqual(200, response.status_code)

    def test_endpoint_venta_post_venta_retorna_json_con_nueva_venta(self):
        nueva_sucursal = SucursalModelo(nombre = "Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)
        conexion.sesion.commit()

        nuevo_vendedor = VendedorModelo(nombre="Nuevo vendedor", apellido='Crack', sucursal_id=nueva_sucursal.id)
        conexion.sesion.add(nuevo_vendedor)
        nuevo_producto = ProductoModelo(nombre="Nuevo producto", precio=15000)
        conexion.sesion.add(nuevo_producto)         
        conexion.sesion.commit()

        nueva_venta = dict(vendedor_id=nuevo_vendedor.id, producto_id=nuevo_producto.id)
        response = self.app.post('/ventas', json=nueva_venta)
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertIsNotNone(response_json["id"])
        self.assertEqual(nueva_venta["producto_id"], response_json["producto_id"])
        self.assertEqual(nueva_venta['vendedor_id'], response_json["vendedor_id"])
        self.assertEqual(201, response.status_code)