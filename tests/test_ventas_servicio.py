import unittest
from querys import venta

class Test_VentasServicio(unittest.TestCase):
    def test_venta_obtener_todos_retorna_lista_con_objetos_con_id_productoid_vendedorid(self):
        resultado = venta.obtener_todos()
        self.assertTrue(isinstance(resultado[0].id, int))
        self.assertTrue(isinstance(resultado[0].producto_id, int))
        self.assertTrue(isinstance(resultado[0].vendedor_id, int))

    def test_venta_obtener_uno_retorna_objeto_con_id_nombre(self):
        resultado = venta.obtener_uno(1)
        self.assertTrue(isinstance(resultado.id, int))
        self.assertTrue(isinstance(resultado.producto_id, int))
        self.assertTrue(isinstance(resultado.vendedor_id, int))

    def test_insertar_venta_ultima_venta_tiene_los_valores_de_la_venta_insertada(self):
        venta.insertar(1, 1)

        ventas = venta.obtener_todos()

        self.assertEqual(1, ventas[-1].producto_id)
        self.assertEqual(1, ventas[-1].vendedor_id)