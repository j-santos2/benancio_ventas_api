from random import choices, randint
import string
import unittest

from sqlalchemy import func

from conexion import conexion
from src.modelos import VendedorModelo, SucursalModelo
from src.servicios import vendedor

class Test_VendedorServicio(unittest.TestCase):
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
    
    def test_vendedor_obtener_todos_retorna_lista_con_objetos_con_id_nombre_apellido_sucursal_id(self):
        resultado = vendedor.obtener_todos()
        self.assertTrue(isinstance(resultado[0].id, int))
        self.assertTrue(isinstance(resultado[0].nombre, str))
        self.assertTrue(isinstance(resultado[0].apellido, str))
        self.assertTrue(isinstance(resultado[0].sucursal_id, int))

    def test_vendedor_obtener_uno_retorna_objeto_con_id_nombre(self):
        resultado = vendedor.obtener_uno(1)
        self.assertTrue(isinstance(resultado.id, int))
        self.assertTrue(isinstance(resultado.nombre, str))
        self.assertTrue(isinstance(resultado.apellido, str))
        self.assertTrue(isinstance(resultado.sucursal_id, int))

    def test_vendedor_insertar_nombre_apellido_sucursalid_ultima_vendedor_tiene_estos_valores(self):
        nombre_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        apellido_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        
        vendedor.insertar(nombre_rnd, apellido_rnd, 1)
        vendedors = vendedor.obtener_todos()

        self.assertEqual(nombre_rnd, vendedors[-1].nombre)
        self.assertEqual(apellido_rnd, vendedors[-1].apellido)
        self.assertEqual(1, vendedors[-1].sucursal_id)

    def test_vendedor_actualizar_ultimo_id_nombre_apellido_ultimo_vendedor_tiene_valor_nuevos(self):
        nombre_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        apellido_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        ultimo_vendedor = vendedor.obtener_todos()[-1]

        _id = ultimo_vendedor.id
        sucursal_id = ultimo_vendedor.sucursal_id

        vendedor.actualizar(_id, nombre_rnd, apellido_rnd, sucursal_id)
        
        resultado = vendedor.obtener_uno(_id)

        self.assertEqual(nombre_rnd, resultado.nombre)
        self.assertEqual(apellido_rnd, resultado.apellido)
        self.assertEqual(sucursal_id, resultado.sucursal_id)

    def test_eliminar_vendedor_nueva_obtener_uno_devuelve_none(self):
        nombre_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        apellido_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        vendedor.insertar(nombre_rnd, apellido_rnd, 1)

        _id = vendedor.obtener_todos()[-1].id
        vendedor.eliminar(_id)
        resultado = vendedor.obtener_uno(_id)
        self.assertEqual(None, resultado)

    def test_eliminar_vendedor_id_no_existente_menos1_raise_exception(self):
        with self.assertRaises(Exception) as cm:
            vendedor.eliminar(-1)

        self.assertEqual("Registro no encontrado", str(cm.exception))