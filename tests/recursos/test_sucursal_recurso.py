import json
import unittest
from app import app
from src.modelos import SucursalModelo, VendedorModelo
from conexion import conexion

class Test_RecursoSucursales(unittest.TestCase):
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
            
    def tearDown(self):
        conexion.sesion.query(SucursalModelo).delete()
        conexion.sesion.query(VendedorModelo).delete()


    def test_endpoint_sucursales_retorna_json_con_sucursales(self):
        response = self.app.get("/sucursales")

        response_json = json.loads(response.data.decode("utf-8"))
        primera_sucursal = response_json[0]

        self.assertTrue("id" in primera_sucursal)
        self.assertTrue("nombre" in primera_sucursal)
        self.assertTrue("uri" in primera_sucursal)
        self.assertEqual(200, response.status_code)

    def test_endpoint_sucursales_get_con_id_retorna_json_de_la_sucursal_con_sus_campos(self):
        nueva_sucursal = SucursalModelo(nombre="Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)        
        conexion.sesion.commit()

        uri_nueva_sucursal = f"/sucursales/{nueva_sucursal.id}"
        response = self.app.get(uri_nueva_sucursal)
        
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(nueva_sucursal.id, response_json["id"])
        self.assertEqual(nueva_sucursal.nombre, response_json["nombre"])
        self.assertEqual(uri_nueva_sucursal, response_json["uri"])        
        self.assertEqual(200, response.status_code)

    def test_endpoint_sucursales_get_con_id_menos_1_retorna_error(self):
        response = self.app.get("/sucursales/9999")
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual({"msg": "Entidad con id 9999 no existe"}, response_json)
        self.assertEqual(400, response.status_code)

    def test_endpoint_sucursales_post_sucursales_con_nombre_retorna_json_con_sucursal(self):
        nueva_sucursal = dict(
            nombre='Pacífico'
        )
        response = self.app.post('/sucursales', json=nueva_sucursal)
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertIsNotNone(response_json["id"])
        self.assertEqual(nueva_sucursal["nombre"], response_json["nombre"])
        self.assertEqual(201, response.status_code)

    def test_endpoint_sucursales_put_a_sucursal_con_id_retorna_sucursal_actualizada(self):
        nueva_sucursal = SucursalModelo(nombre="Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)        
        conexion.sesion.commit()
        
        sucursal_actualizada = dict(
            nombre='Abasto Shopping'
        )

        response = self.app.put(f'/sucursales/{nueva_sucursal.id}', json=sucursal_actualizada)
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(sucursal_actualizada["nombre"], response_json["nombre"])
        self.assertEqual(200, response.status_code)


    def test_endpoint_sucursales_delete_id_retorna_status_code_204(self):
        nueva_sucursal = SucursalModelo(nombre="Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)        
        conexion.sesion.commit()
        
        response = self.app.delete(f'/sucursales/{nueva_sucursal.id}')

        self.assertEqual(204, response.status_code)

    def test_endpoint_sucursales_delete_id_9000_retorna_mensaje_sucursal_id_9000_no_existe(self):
        response = self.app.delete('/sucursales/9000')

        respuesta = json.loads(response.data.decode("utf-8"))

        self.assertEqual({"msg":"Entidad con id 9000 no existe"}, respuesta)
        self.assertEqual(400, response.status_code)

    def test_endpoint_sucursales_con_vendedores_retorna_vendedores_de_cada_sucursal(self):
        nueva_sucursal = SucursalModelo(nombre="Nueva sucursal")
        conexion.sesion.add(nueva_sucursal)        
        conexion.sesion.commit()

        conexion.sesion.add(VendedorModelo(nombre="1º", apellido="vendedor", sucursal_id=nueva_sucursal.id))
        conexion.sesion.add(VendedorModelo(nombre="2º", apellido="vendedor", sucursal_id=nueva_sucursal.id))
        conexion.sesion.add(VendedorModelo(nombre="3º", apellido="vendedor", sucursal_id=nueva_sucursal.id))
        conexion.sesion.commit()
        
        response = self.app.get(f"/sucursales/{nueva_sucursal.id}/vendedores")
        
        response_json = json.loads(response.data.decode("utf-8"))

        for vendedor in response_json:
            self.assertEqual(nueva_sucursal.id, vendedor["sucursal_id"])
        
        self.assertEqual(200, response.status_code)
