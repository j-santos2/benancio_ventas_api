from random import choices, randint
import string
import unittest

from conexion import conexion
from src.modelos import ProductoModelo
from src.servicios import producto


class TestProductoServicio(unittest.TestCase):

    def setUp(self):
        conexion.sesion.add(ProductoModelo(nombre="1º producto", precio=10000))
        conexion.sesion.add(ProductoModelo(nombre="2º producto", precio=20000))
        conexion.sesion.add(ProductoModelo(nombre="3º producto", precio=30000))
        conexion.sesion.add(ProductoModelo(nombre="4º producto", precio=40000))
        conexion.sesion.add(ProductoModelo(nombre="5º producto", precio=50000))

    def tearDown(self):
        conexion.sesion.query(ProductoModelo).delete()

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
        producto_nuevo = producto.insertar('ProductoModelo con ID', 1000)

        self.assertIsNotNone(producto_nuevo.id)

    def test_producto_actualizar_ultimo_id_nombre_precio_ultimo_producto_tiene_valores_nuevos(self):
        nombre_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        precio_rnd = randint(100,300)
        
        _id = producto.obtener_todos()[-1].id

        producto.actualizar(_id, nombre_rnd, precio_rnd)
        
        resultado = producto.obtener_uno(_id)

        self.assertEqual(nombre_rnd, resultado.nombre)
        self.assertEqual(precio_rnd, resultado.precio)

    def test_eliminar_producto_nuevo_obtener_uno_levanta_(self):
        producto_nuevo = ProductoModelo(nombre="1º producto", precio=10000)
        conexion.sesion.add(producto_nuevo)
        conexion.sesion.commit()
        
        id_producto_a_eliminar = producto_nuevo.id
        producto.eliminar(id_producto_a_eliminar)
        
        
        respuesta = conexion.sesion.query(ProductoModelo).filter(ProductoModelo.id == id_producto_a_eliminar).first()

        self.assertEqual(None, respuesta)

    def test_eliminar_producto_id_no_existente_menos1_raise_exception(self):
        with self.assertRaises(Exception) as cm:
            producto.eliminar(-1)

        self.assertEqual("Entity with id -1 not found", str(cm.exception))

    def test_obtener_todos_paginado_retorna_los_primeros_2_registros(self):
        respuesta = producto.obtener_todos_paginado(2)

        self.assertEqual(2, len(respuesta))
        self.assertEqual("1º producto", respuesta[0].nombre)
        self.assertEqual(10000, respuesta[0].precio)
        self.assertEqual("2º producto", respuesta[1].nombre)
        self.assertEqual(20000, respuesta[1].precio)

    def test_obtener_todos_paginado_con_inicio_2_limite_2_retorna_registros_correctos(self):
        respuesta = producto.obtener_todos_paginado(2, 2)

        self.assertEqual(2, len(respuesta))
        self.assertEqual("3º producto", respuesta[0].nombre)
        self.assertEqual(30000, respuesta[0].precio)
        self.assertEqual("4º producto", respuesta[1].nombre)
        self.assertEqual(40000, respuesta[1].precio)
        