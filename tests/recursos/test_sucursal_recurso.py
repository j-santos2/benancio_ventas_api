import json
import unittest

from flask_jwt_extended import create_access_token

from app import app
from src.modelos import SucursalModelo, VendedorModelo
from conexion import conexion


class TestRecursoSucursales(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        cls.app = app.test_client()

    def setUp(self):
        conexion.sesion.add(SucursalModelo(nombre="1º sucursal"))
        conexion.sesion.add(SucursalModelo(nombre="2º sucursal"))
        conexion.sesion.add(SucursalModelo(nombre="3º sucursal"))
        conexion.sesion.add(SucursalModelo(nombre="4º sucursal"))
        conexion.sesion.add(SucursalModelo(nombre="5º sucursal"))

        with self.app.application.app_context():
            self.__access_token = create_access_token('testuser')

        self.__headers = {
            'Authorization': f'Bearer {self.__access_token}'
        }

    def tearDown(self):
        conexion.sesion.query(SucursalModelo).delete()
        conexion.sesion.query(VendedorModelo).delete()


    def test_endpoint_sucursales_retorna_json_con_sucursales(self):
        response = self.app.get("/stores")

        response_json = json.loads(response.data.decode("utf-8"))
        primera_sucursal = response_json[0]

        self.assertTrue("id" in primera_sucursal)
        self.assertTrue("name" in primera_sucursal)
        self.assertTrue("uri" in primera_sucursal)
        self.assertEqual(200, response.status_code)

    def test_endpoint_sucursales_get_con_id_retorna_json_de_la_sucursal_con_sus_campos(self):
        nueva_sucursal = SucursalModelo(nombre="Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)        
        conexion.sesion.commit()

        uri_nueva_sucursal = f"/stores/{nueva_sucursal.id}"
        response = self.app.get(uri_nueva_sucursal)
        
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(nueva_sucursal.id, response_json["id"])
        self.assertEqual(nueva_sucursal.nombre, response_json["name"])
        self.assertEqual(uri_nueva_sucursal, response_json["uri"])        
        self.assertEqual(200, response.status_code)

    def test_endpoint_sucursales_get_con_id_menos_1_retorna_error(self):
        response = self.app.get("/stores/9999")
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual({"msg": "Entity with id 9999 not found"}, response_json)
        self.assertEqual(400, response.status_code)

    def test_endpoint_sucursales_post_sucursales_con_nombre_retorna_json_con_sucursal(self):
        nueva_sucursal = dict(
            name='Pacífico'
        )
        response = self.app.post('/stores', json=nueva_sucursal, headers=self.__headers)
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertIsNotNone(response_json["id"])
        self.assertEqual(nueva_sucursal["name"], response_json["name"])
        self.assertEqual(201, response.status_code)

    def test_endpoint_sucursales_put_a_sucursal_con_id_retorna_sucursal_actualizada(self):
        nueva_sucursal = SucursalModelo(nombre="Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)        
        conexion.sesion.commit()
        
        sucursal_actualizada = dict(
            name='Abasto Shopping'
        )

        response = self.app.put(f'/stores/{nueva_sucursal.id}', json=sucursal_actualizada, headers=self.__headers)
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(sucursal_actualizada["name"], response_json["name"])
        self.assertEqual(200, response.status_code)


    def test_endpoint_sucursales_delete_id_retorna_status_code_204(self):
        nueva_sucursal = SucursalModelo(nombre="Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)        
        conexion.sesion.commit()
        
        response = self.app.delete(f'/stores/{nueva_sucursal.id}', headers=self.__headers)

        self.assertEqual(204, response.status_code)

    def test_endpoint_sucursales_delete_id_9000_retorna_mensaje_sucursal_id_9000_no_existe(self):
        response = self.app.delete('/stores/9000', headers=self.__headers)

        respuesta = json.loads(response.data.decode("utf-8"))

        self.assertEqual({"msg":"Entity with id 9000 not found"}, respuesta)
        self.assertEqual(400, response.status_code)

    def test_endpoint_sucursales_con_vendedores_retorna_vendedores_de_cada_sucursal(self):
        nueva_sucursal = SucursalModelo(nombre="Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)        
        conexion.sesion.commit()

        conexion.sesion.add(VendedorModelo(nombre="1º", apellido="vendedor", sucursal_id=nueva_sucursal.id))
        conexion.sesion.add(VendedorModelo(nombre="2º", apellido="vendedor", sucursal_id=nueva_sucursal.id))
        conexion.sesion.add(VendedorModelo(nombre="3º", apellido="vendedor", sucursal_id=nueva_sucursal.id))
        conexion.sesion.commit()
        
        response = self.app.get(f"/stores/{nueva_sucursal.id}/salesperson")
        
        response_json = json.loads(response.data.decode("utf-8"))

        for vendedor in response_json:
            self.assertEqual(nueva_sucursal.id, vendedor["store_id"])
        
        self.assertEqual(200, response.status_code)
