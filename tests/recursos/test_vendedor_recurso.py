import json
import unittest
from app import app
from src.modelos import VendedorModelo, SucursalModelo, ProductoModelo, VentaModelo
from conexion import conexion

class Test_RecursoVendedor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        cls.app = app.test_client()

    def setUp(self):
        primera_sucursal = SucursalModelo(nombre = "Primera sucursal")
        conexion.sesion.add(primera_sucursal)

        segunda_sucursal = SucursalModelo(nombre = "Segunda sucursal")
        conexion.sesion.add(segunda_sucursal)

        conexion.sesion.commit()
        
        conexion.sesion.add(VendedorModelo(nombre="1º", apellido="vendedor", sucursal_id=primera_sucursal.id))
        conexion.sesion.add(VendedorModelo(nombre="2º", apellido="vendedor", sucursal_id=primera_sucursal.id))
        conexion.sesion.add(VendedorModelo(nombre="3º", apellido="vendedor", sucursal_id=primera_sucursal.id))
        conexion.sesion.add(VendedorModelo(nombre="4º", apellido="vendedor", sucursal_id=segunda_sucursal.id))
        conexion.sesion.add(VendedorModelo(nombre="5º", apellido="vendedor", sucursal_id=segunda_sucursal.id))

    def tearDown(self):
        conexion.sesion.query(VendedorModelo).delete()
        conexion.sesion.query(SucursalModelo).delete()


    def test_endpoint_vendedres_retorna_json_con_vendedores(self):
        response = self.app.get("/vendedores")

        response_json = json.loads(response.data.decode("utf-8"))
        primer_vendedor = response_json[0]

        self.assertTrue("id" in primer_vendedor)
        self.assertTrue("nombre" in primer_vendedor)
        self.assertTrue("apellido" in primer_vendedor)
        self.assertTrue("sucursal_id" in primer_vendedor)
        self.assertTrue("uri" in primer_vendedor)
        self.assertEqual(200, response.status_code)

    def test_endpoint_vendedores_get_con_id_retorna_json_del_vendedor_con_sus_campos(self):
        nueva_sucursal = SucursalModelo(nombre = "Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)

        conexion.sesion.commit()

        nuevo_vendedor = VendedorModelo(nombre="Nuevo vendedor", apellido='Crack', sucursal_id=nueva_sucursal.id)
        conexion.sesion.add(nuevo_vendedor)        
        conexion.sesion.commit()

        uri_nuevo_vendedor = f"/vendedores/{nuevo_vendedor.id}"
        response = self.app.get(uri_nuevo_vendedor)
        
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(nuevo_vendedor.id, response_json["id"])
        self.assertEqual(nuevo_vendedor.nombre, response_json["nombre"])
        self.assertEqual(nuevo_vendedor.apellido, response_json["apellido"])
        self.assertEqual(nuevo_vendedor.sucursal_id, response_json["sucursal_id"])
        self.assertEqual(uri_nuevo_vendedor, response_json["uri"])        
        self.assertEqual(200, response.status_code)

    def test_endpoint_vendedores_post_vendedores_con_nombre_retorna_json_con_vendedor(self):
        nueva_sucursal = SucursalModelo(nombre = "Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)

        conexion.sesion.commit()

        nuevo_vendedor = dict(nombre='Juan', apellido="Perez", sucursal_id=nueva_sucursal.id)

        response = self.app.post('/vendedores', json=nuevo_vendedor)
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertIsNotNone(response_json["id"])
        self.assertEqual(nuevo_vendedor["nombre"], response_json["nombre"])
        self.assertEqual(nuevo_vendedor['apellido'], response_json["apellido"])
        self.assertEqual(nuevo_vendedor['sucursal_id'], response_json["sucursal_id"])
        self.assertEqual(201, response.status_code)

    def test_endpoint_vendedores_con_ventas_retorna_lista_de_ventas(self):

        primera_sucursal = SucursalModelo(nombre = "Primera sucursal")
        conexion.sesion.add(primera_sucursal)
        conexion.sesion.commit()

        primer_vendedor = VendedorModelo(nombre="1º", apellido="vendedor", sucursal_id=primera_sucursal.id)
        conexion.sesion.add(primer_vendedor)

        primer_producto = ProductoModelo(nombre="1º producto", precio=10000)
        segundo_producto = ProductoModelo(nombre="2º producto", precio=20000)

        conexion.sesion.add(primer_producto)
        conexion.sesion.add(segundo_producto)
        conexion.sesion.commit()

        conexion.sesion.add(VentaModelo(producto_id=primer_producto.id, vendedor_id=primer_vendedor.id))
        conexion.sesion.add(VentaModelo(producto_id=segundo_producto.id, vendedor_id=primer_vendedor.id))
        conexion.sesion.add(VentaModelo(producto_id=segundo_producto.id, vendedor_id=primer_vendedor.id))

        response = self.app.get(f'vendedores/{primer_vendedor.id}/ventas')
        respuesta = json.loads(response.data.decode("utf-8"))

        for venta in respuesta:
            self.assertEqual(primer_vendedor.id, venta['vendedor_id'])

        self.assertEqual(primer_producto.nombre, respuesta[0]['producto'])
        self.assertEqual(primer_producto.precio, respuesta[0]['precio'])

        self.assertEqual(segundo_producto.nombre, respuesta[1]['producto'])
        self.assertEqual(segundo_producto.precio, respuesta[1]['precio'])

        self.assertEqual(segundo_producto.nombre, respuesta[2]['producto'])
        self.assertEqual(segundo_producto.precio, respuesta[2]['precio'])