import unittest
from unittest import mock

from src.modelos import ProductoModelo
from src.servicios.recurso_servicio import RecursoServicio 
from src.servicios.exceptions import ObjetoNoEncontrado


class Servicio(RecursoServicio):
    pass

class Test_RecursoServicio(unittest.TestCase):
    def setUp(self):
        self.__servicio = Servicio()        

    def test_get_or_fail_id_inexistente_levanta_ObjetoNoEncontrado(self):
        with mock.patch.object(self.__servicio._sesion, "get", return_value = None):
            with self.assertRaises(ObjetoNoEncontrado) as cm:
                self.__servicio._get_or_fail(mock.Mock(), 9000)

        self.assertEqual("Entidad con id 9000 no existe",  str(cm.exception))

    def test_get_or_fail_devuelve_objeto_encontrado(self):
        with mock.patch.object(self.__servicio._sesion, "get", return_value = mock.Mock(sabor = "chocolate con dulce de leche")):
            resultado = self.__servicio._get_or_fail(mock.Mock(), 1)

        self.assertEqual("chocolate con dulce de leche", resultado.sabor)
            