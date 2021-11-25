import json
import unittest
from app import app
from src.modelos import UsuarioModelo
from conexion import conexion

class Test_UsuarioRecurso(unittest.TestCase):

    def setUp(self):
        self.__app = app.test_client()

    def test_endpoint_usuarios_post_crea_usuario_y_devuelve_usuario_y_status_201(self):
        response = self.__app.post("/usuarios",json = {"nombre": "Pepito", "clave":"dificil123"})
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual("Pepito", response_json["nombre"])
        self.assertEqual(201, response.status_code)
