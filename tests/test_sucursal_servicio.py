import unittest
from querys import sucursal
from random import choices
import string

class Test_SucursalServicio(unittest.TestCase):
    def test_sucursal_obtener_todos_retorna_lista_con_objetos_con_id_nombre(self):
        resultado = sucursal.obtener_todos()
        self.assertTrue(isinstance(resultado[0].id, int))
        self.assertTrue(isinstance(resultado[0].nombre, str))

    def test_sucursal_obtener_uno_retorna_objeto_con_id_nombre(self):
        resultado = sucursal.obtener_uno(1)
        self.assertTrue(isinstance(resultado.id, int))
        self.assertTrue(isinstance(resultado.nombre, str))

    def test_sucursal_insertar_nombre_ultima_sucursal_tiene_este_valor(self):
        nombre_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        
        sucursal.insertar(nombre_rnd)
        sucursals = sucursal.obtener_todos()

        self.assertEqual(nombre_rnd, sucursals[-1].nombre)

    def test_sucursal_actualizar_ultimo_id_nombre_ultima_sucursal_tiene_valor_nuevos(self):
        nombre_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        
        _id = sucursal.obtener_todos()[-1].id

        sucursal.actualizar(_id, nombre_rnd)
        
        resultado = sucursal.obtener_uno(_id)

        self.assertEqual(nombre_rnd, resultado.nombre)

    def test_eliminar_sucursal_nueva_obtener_uno_devuelve_none(self):
        nombre_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        sucursal.insertar(nombre_rnd)

        _id = sucursal.obtener_todos()[-1].id
        sucursal.eliminar(_id)
        resultado = sucursal.obtener_uno(_id)
        self.assertEqual(None, resultado)

    def test_eliminar_sucursal_id_no_existente_menos1_raise_exception(self):
        with self.assertRaises(Exception) as cm:
            sucursal.eliminar(-1)

        self.assertEqual("Registro no encontrado", str(cm.exception))