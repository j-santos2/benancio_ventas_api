import json
import unittest

from flask_jwt_extended import decode_token
from app import app
from src.modelos import UsuarioModelo
from conexion import conexion
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

class Test_UsuarioRecurso(unittest.TestCase):

    def setUp(self):
        self.__app = app.test_client()

    def tearDown(self):
        conexion.sesion.query(UsuarioModelo).delete()

    def test_endpoint_usuarios_post_crea_usuario_y_devuelve_usuario_y_status_201(self):
        response = self.__app.post("/usuarios",json = {"nombre": "Pepito", "clave":"dificil123"})
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual("Pepito", response_json["nombre"])
        self.assertEqual(201, response.status_code)

    def test_endpoint_usuarios_login_retorna_token_de_acceso_y_201(self):
        pass_hasheado = generate_password_hash("dificil123")
        nuevo_usuario = UsuarioModelo(nombre="Pepito", clave=pass_hasheado)
        conexion.sesion.add(nuevo_usuario)
        conexion.sesion.commit()

        response = self.__app.post("/usuarios/login",json = {"nombre": "Pepito", "clave":"dificil123"})
        response_json = json.loads(response.data.decode("utf-8"))

        with self.__app.application.app_context():
            access_token = decode_token(response_json['token'])
        
        self.assertEqual(nuevo_usuario.nombre, access_token['sub'])
        self.assertEqual(201, response.status_code)

    def test_endpoint_usuarios_login_usuario_no_valido_retorna_mensaje_de_error_y_401(self):
        response = self.__app.post("/usuarios/login",json = {"nombre": "Pepito", "clave":"dificil123"})
        response_json = json.loads(response.data.decode("utf-8"))
        
        self.assertEqual({"Mensaje":"Nombre de usuario y/o clave incorrecta"}, response_json)
        self.assertEqual(401, response.status_code)