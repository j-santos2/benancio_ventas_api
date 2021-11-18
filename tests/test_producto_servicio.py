from random import choices, randint
import string
import unittest

from conexion import conexion
from src.modelos import Producto
from src.servicios import producto


class Test_ProductoServicio(unittest.TestCase):

    def setUp(self):
        conexion.sesion.add(Producto(nombre="1º producto", precio=10000))
        conexion.sesion.add(Producto(nombre="2º producto", precio=20000))
        conexion.sesion.add(Producto(nombre="3º producto", precio=30000))
        conexion.sesion.add(Producto(nombre="4º producto", precio=40000))
        conexion.sesion.add(Producto(nombre="5º producto", precio=50000))

    def tearDown(self):
        conexion.sesion.query(Producto).delete()

    def test_producto_obtener_todos_retorna_lista_con_objetos_con_id_nombre_precio(self):
        resultado = producto.obtener_todos()
        self.assertTrue(isinstance(resultado[0].id, int))
        self.assertTrue(isinstance(resultado[0].nombre, str))
        self.assertTrue(isinstance(resultado[0].precio, int))

    def test_producto_obtener_uno_retorna_objeto_con_id_nombre_precio(self):
        resultado = producto.obtener_uno(1)
        self.assertTrue(isinstance(resultado.id, int))
        self.assertTrue(isinstance(resultado.nombre, str))
        self.assertTrue(isinstance(resultado.precio, int))

    def test_producto_insertar_nombre_precio_ultimo_producto_tiene_estos_valores(self):
        nombre_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        precio_rnd = randint(100,300)
        
        producto.insertar(nombre_rnd, precio_rnd)
        productos = producto.obtener_todos()

        self.assertEqual(nombre_rnd, productos[-1].nombre)
        self.assertEqual(precio_rnd, productos[-1].precio)

    def test_producto_insertado_tiene_id_distinto_de_none(self):        
        producto_nuevo = producto.insertar('Producto con ID', 1000)

        self.assertIsNotNone(producto_nuevo.id)

    def test_producto_actualizar_ultimo_id_nombre_precio_ultimo_producto_tiene_valores_nuevos(self):
        nombre_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        precio_rnd = randint(100,300)
        
        _id = producto.obtener_todos()[-1].id

        producto.actualizar(_id, nombre_rnd, precio_rnd)
        
        resultado = producto.obtener_uno(_id)

        self.assertEqual(nombre_rnd, resultado.nombre)
        self.assertEqual(precio_rnd, resultado.precio)

    def test_eliminar_producto_nuevo_obtener_uno_devuelve_none(self):
        nombre_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        precio_rnd = randint(100,300)
        producto.insertar(nombre_rnd, precio_rnd)

        _id = producto.obtener_todos()[-1].id
        producto.eliminar(_id)
        resultado = producto.obtener_uno(_id)
        self.assertEqual(None, resultado)

    def test_eliminar_producto_id_no_existente_menos1_raise_exception(self):
        with self.assertRaises(Exception) as cm:
            producto.eliminar(-1)

        self.assertEqual("Registro no encontrado", str(cm.exception))