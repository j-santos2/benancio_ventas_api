import json
import unittest
from app import app
from src.recursos.productos import Productos, Producto

class Test_RecursoProducto(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_enpoint_productos_retorna_json_con_productos(self):
        response = self.app.get("/productos")

        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual('<h1>Game 1</h1>', response_json)
        self.assertEqual(200, response.status_code)

    def test_enpoint_productos_id_2_retorna_json_con_producto_de_id_2(self):
        response = self.app.get("/productos/2")
        
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(2, response_json["id"])
        self.assertEqual(200, response.status_code)

    def test_endpoint_productos_post_productos_con_nombre_item_precio_100_retorna_json_con_producto(self):
        nuevo_producto = dict(
            nombre='item',
            precio=100
        )
        response = self.app.post('/productos', data=nuevo_producto)
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertIsNotNone(response_json["id"])
        self.assertEqual(nuevo_producto["nombre"], response_json["nombre"])
        self.assertEqual(nuevo_producto["precio"], response_json["precio"])
        self.assertEqual(201, response.status_code)

    def test_endpoint_productos_put_productos_id_2_con_nombre_itemcambiado_precio_120_retorna_json_con_producto(self):
        producto_datos_actualizados = dict(
            nombre='itemcambiado',
            precio=120
        )
        response = self.app.put('/productos/2', data=producto_datos_actualizados)
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(2, response_json["id"])
        self.assertEqual(producto_datos_actualizados["nombre"], response_json["nombre"])
        self.assertEqual(producto_datos_actualizados["precio"], response_json["precio"])
        self.assertEqual(200, response.status_code)

    def test_endpoint_productos_put_productos_id_2_con_nombre_itemcambiado_precio_120_retorna_retorna_mensaje_producto_id_60_no_existe(self):
        producto_datos_actualizados = dict(
            nombre='itemcambiado',
            precio=120
        )

        response = self.app.put('/productos/2', data=producto_datos_actualizados)

        self.assertEqual("{\"Mensaje\":\"Producto con id 60 no existe\"}", response.data.decode("utf-8"))
        self.assertEqual(204, response.status_code)

    def test_endpoint_productos_delete_id_2_retorna_mensaje_producto_id_2_eliminado_con_exito(self):
        response = self.app.delete('/productos/2')

        self.assertEqual("{\"Mensaje\":\"Producto con id 2 eliminado con exito\"}", response.data.decode("utf-8"))
        self.assertEqual(200, response.status_code)

    def test_endpoint_productos_delete_id_60_retorna_mensaje_producto_id_60_no_existe(self):
        response = self.app.delete('/productos/2')

        self.assertEqual("{\"Mensaje\":\"Producto con id 60 no existe\"}", response.data.decode("utf-8"))
        self.assertEqual(204, response.status_code)