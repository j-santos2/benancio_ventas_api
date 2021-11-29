from random import choices, randint
import string
import unittest

from conexion import conexion
from src.modelos import SucursalModelo, VendedorModelo
from src.servicios import sucursal
from src.servicios.exceptions import ErrorDeIntegridad, ObjetoNoEncontrado


class Test_SucursalServicio(unittest.TestCase):

    def setUp(self):
        conexion.sesion.add(SucursalModelo(nombre="1ª sucursal"))
        conexion.sesion.add(SucursalModelo(nombre="2ª sucursal"))
        conexion.sesion.add(SucursalModelo(nombre="3ª sucursal"))
        conexion.sesion.add(SucursalModelo(nombre="4ª sucursal"))
        conexion.sesion.add(SucursalModelo(nombre="5ª sucursal"))

    def tearDown(self):
        conexion.sesion.query(VendedorModelo).delete()
        conexion.sesion.query(SucursalModelo).delete()

    def test_sucursal_obtener_todos_retorna_lista_con_objetos_con_id_nombre(self):
        resultado = sucursal.obtener_todos()
        self.assertTrue(isinstance(resultado[0].id, int))
        self.assertTrue(isinstance(resultado[0].nombre, str))

    def test_sucursal_obtener_uno_retorna_objeto_con_id_nombre(self):
        resultado = sucursal.obtener_uno(1)
        self.assertTrue(isinstance(resultado.id, int))
        self.assertTrue(isinstance(resultado.nombre, str))

    def test_sucursal_obtener_uno_con_id_inexistente_levanta_error(self):
        
        with self.assertRaises(ObjetoNoEncontrado) as cm:
            sucursal.obtener_uno(-1)

        self.assertEqual("Entidad con id -1 no existe", str(cm.exception))

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
        sucursal_nueva = SucursalModelo(nombre="Este nombre pasaaaa")
        conexion.sesion.add(sucursal_nueva)

        conexion.sesion.commit()

        _id = sucursal_nueva.id
        sucursal.eliminar(_id)
        resultado = conexion.sesion.get(SucursalModelo, _id)        
        self.assertEqual(None, resultado)        

    def test_eliminar_sucursal_id_no_existente_menos1_raise_exception(self):
        with self.assertRaises(Exception) as cm:
            sucursal.eliminar(-1)

        self.assertEqual("Entidad con id -1 no existe", str(cm.exception))

    def test_eliminar_sucursal_con_vendedores_atrapa_excepcion_y_rollback(self):
        sucursal_dot = SucursalModelo(nombre="Dot")
        conexion.sesion.add(sucursal_dot)
        conexion.sesion.commit()
        conexion.sesion.add(VendedorModelo(nombre="Aquiles", apellido="Bailo", sucursal_id=sucursal_dot.id))
        conexion.sesion.commit()
        with self.assertRaises(ErrorDeIntegridad) as cm:
            sucursal.eliminar(sucursal_dot.id)
            
        self.assertEqual("Acción no permitida sobre el recurso.", str(cm.exception))
        