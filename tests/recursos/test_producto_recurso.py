import json
import unittest
from unittest import mock

from flask_jwt_extended import create_access_token

from app import app
from src.modelos import ProductoModelo
from conexion import conexion
from src.servicios.exceptions import ObjetoNoEncontrado

class Test_RecursoProducto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        cls.app = app.test_client()

    def setUp(self):
        conexion.sesion.add(ProductoModelo(nombre="1º producto", precio=10000))
        conexion.sesion.add(ProductoModelo(nombre="2º producto", precio=20000))
        conexion.sesion.add(ProductoModelo(nombre="3º producto", precio=30000))
        conexion.sesion.add(ProductoModelo(nombre="4º producto", precio=40000))
        conexion.sesion.add(ProductoModelo(nombre="5º producto", precio=50000))

        with self.app.application.app_context():
            self.__access_token = create_access_token('testuser')

        self.__headers = {
            'Authorization': f'Bearer {self.__access_token}'
        }
            
    def tearDown(self):
        conexion.sesion.query(ProductoModelo).delete()


    def test_endpoint_productos_retorna_json_con_productos(self):
        response = self.app.get("/productos")

        response_json = json.loads(response.data.decode("utf-8"))
        primer_producto = response_json[0]

        self.assertTrue("id" in primer_producto)
        self.assertTrue("nombre" in primer_producto)
        self.assertTrue("precio" in primer_producto)
        self.assertTrue("uri" in primer_producto)
        self.assertEqual(200, response.status_code)

    def test_endpoint_productos_get_con_id_retorna_json_del_producto_con_sus_campos(self):
        nuevo_producto = ProductoModelo(nombre="Nuevo producto", precio=23430)
        conexion.sesion.add(nuevo_producto)        
        conexion.sesion.commit()

        uri_nuevo_producto = f"/productos/{nuevo_producto.id}"
        response = self.app.get(uri_nuevo_producto)
        
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(nuevo_producto.id, response_json["id"])
        self.assertEqual(nuevo_producto.nombre, response_json["nombre"])
        self.assertEqual(nuevo_producto.precio, response_json["precio"])
        self.assertEqual(uri_nuevo_producto, response_json["uri"])        
        self.assertEqual(200, response.status_code)

    def test_endpoint_productos_post_productos_con_nombre_item_precio_100_retorna_json_con_producto(self):
        nuevo_producto = dict(
            nombre='item',
            precio=100
        )
        response = self.app.post('/productos', json=nuevo_producto)
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertIsNotNone(response_json["id"])
        self.assertEqual(nuevo_producto["nombre"], response_json["nombre"])
        self.assertEqual(nuevo_producto["precio"], response_json["precio"])
        self.assertEqual(201, response.status_code)

    def test_endpoint_productos_put_productos_id_con_nombre_itemcambiado_precio_120_retorna_json_con_producto(self):
        nuevo_producto = ProductoModelo(nombre="Nuevo producto", precio=23430)
        conexion.sesion.add(nuevo_producto)        
        conexion.sesion.commit()
        
        producto_datos_actualizados = dict(
            nombre='itemcambiado',
            precio=120
        )

        response = self.app.put(f'/productos/{nuevo_producto.id}', json=producto_datos_actualizados)
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(producto_datos_actualizados["nombre"], response_json["nombre"])
        self.assertEqual(producto_datos_actualizados["precio"], response_json["precio"])
        self.assertEqual(200, response.status_code)

    def test_endpoint_productos_put_productos_id_9000_retorna_mensaje_producto_no_existe(self):
        producto_datos_actualizados = dict(
            nombre='itemcambiado',
            precio=120
        )

        response = self.app.put('/productos/9000', json=producto_datos_actualizados)
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual("Producto con id 9000 no existe", response_json["msg"])

    def test_endpoint_productos_delete_id_retorna_mensaje_producto_id_2_eliminado_con_exito(self):
        nuevo_producto = ProductoModelo(nombre="Nuevo producto", precio=23430)
        conexion.sesion.add(nuevo_producto)        
        conexion.sesion.commit()
        
        response = self.app.delete(f'/productos/{nuevo_producto.id}', headers=self.__headers)

        self.assertEqual(204, response.status_code)

    @mock.patch("src.recursos.productos.producto.eliminar")
    def test_endpoint_productos_delete_id_9000_retorna_mensaje_producto_id_9000_no_existe(self, m_eliminar):
        m_eliminar.side_effect = ObjetoNoEncontrado("Producto con id 9000 no existe")

        response = self.app.delete('/productos/9000', headers=self.__headers)
        respuesta = json.loads(response.data.decode("utf-8"))

        self.assertEqual({"msg":"Producto con id 9000 no existe"}, respuesta)
        self.assertEqual(400, response.status_code)
        m_eliminar.assert_called_once_with(9000)

    def test_endpoint_productos_delete_sin_token_devuelve_missing_authorization_y_status_401(self):
        response = self.app.delete('/productos/9000')
        respuesta = json.loads(response.data.decode("utf-8"))

        self.assertEqual({"msg":"Missing Authorization Header"}, respuesta)
        self.assertEqual(401, response.status_code)