import unittest
from werkzeug.security import generate_password_hash, check_password_hash
from conexion import conexion
from src.modelos import UsuarioModelo
from src.servicios import usuario
from src.servicios.usuario_servicio import UsuarioServicio


class Test_UsuarioServicio(unittest.TestCase):

    def tearDown(self):
        conexion.sesion.query(UsuarioModelo).delete()

    def test_insertar_usuario_retorna_usuario_creado(self):
        respuesta = usuario.insertar("Juancito", "qwerty12345")

        self.assertEqual("Juancito", respuesta.nombre)
        self.assertIsInstance(respuesta.id, int)

    def test_clave_de_usuario_insertado_esta_hasheada_en_la_base(self):
        respuesta = usuario.insertar("Juancito", "qwerty12345")

        self.assertTrue(check_password_hash(respuesta.clave, "qwerty12345"))

        

    
