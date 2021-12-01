import json
import unittest

from flask_jwt_extended import create_access_token

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

        with self.app.application.app_context():
            self.__access_token = create_access_token('testuser')

        self.__headers = {
            'Authorization': f'Bearer {self.__access_token}'
        }

    def tearDown(self):
        conexion.sesion.query(VendedorModelo).delete()
        conexion.sesion.query(SucursalModelo).delete()


    def test_endpoint_vendedres_retorna_json_con_vendedores(self):
        response = self.app.get("/salesperson")

        response_json = json.loads(response.data.decode("utf-8"))
        primer_vendedor = response_json[0]

        self.assertTrue("id" in primer_vendedor)
        self.assertTrue("name" in primer_vendedor)
        self.assertTrue("lastname" in primer_vendedor)
        self.assertTrue("store_id" in primer_vendedor)
        self.assertTrue("uri" in primer_vendedor)
        self.assertEqual(200, response.status_code)

    def test_endpoint_vendedores_get_con_id_retorna_json_del_vendedor_con_sus_campos(self):
        nueva_sucursal = SucursalModelo(nombre = "Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)

        conexion.sesion.commit()

        nuevo_vendedor = VendedorModelo(nombre="Nuevo vendedor", apellido='Crack', sucursal_id=nueva_sucursal.id)
        conexion.sesion.add(nuevo_vendedor)        
        conexion.sesion.commit()

        uri_nuevo_vendedor = f"/salesperson/{nuevo_vendedor.id}"
        response = self.app.get(uri_nuevo_vendedor)
        
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(nuevo_vendedor.id, response_json["id"])
        self.assertEqual(nuevo_vendedor.nombre, response_json["name"])
        self.assertEqual(nuevo_vendedor.apellido, response_json["lastname"])
        self.assertEqual(nuevo_vendedor.sucursal_id, response_json["store_id"])
        self.assertEqual(uri_nuevo_vendedor, response_json["uri"])        
        self.assertEqual(200, response.status_code)

    def test_endpoint_vendedores_post_vendedores_con_nombre_retorna_json_con_vendedor(self):
        nueva_sucursal = SucursalModelo(nombre = "Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)

        conexion.sesion.commit()

        nuevo_vendedor = dict(name='Juan', lastname="Perez", store_id=nueva_sucursal.id)

        response = self.app.post('/salesperson', json=nuevo_vendedor, headers=self.__headers)
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertIsNotNone(response_json["id"])
        self.assertEqual(nuevo_vendedor["name"], response_json["name"])
        self.assertEqual(nuevo_vendedor['lastname'], response_json["lastname"])
        self.assertEqual(nuevo_vendedor['store_id'], response_json["store_id"])
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

        response = self.app.get(f'salesperson/{primer_vendedor.id}/sales')
        respuesta = json.loads(response.data.decode("utf-8"))

        for venta in respuesta:
            self.assertEqual(primer_vendedor.id, venta['salesperson_id'])

        self.assertEqual(primer_producto.nombre, respuesta[0]['product'])
        self.assertEqual(primer_producto.precio, respuesta[0]['price'])

        self.assertEqual(segundo_producto.nombre, respuesta[1]['product'])
        self.assertEqual(segundo_producto.precio, respuesta[1]['price'])

        self.assertEqual(segundo_producto.nombre, respuesta[2]['product'])
        self.assertEqual(segundo_producto.precio, respuesta[2]['price'])