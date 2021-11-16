import unittest
from querys import producto, sucursal, vendedor, venta
from random import choices, randint
import string

class Test_ProductoServicio(unittest.TestCase):
    def test_producto_obtener_todos_retorna_lista_con_objetos_con_id_nombre_precio(self):
        resultado = producto.obtener_todos()
        self.assertTrue(isinstance(resultado[0].id, int))
        self.assertTrue(isinstance(resultado[0].nombre, str))
        self.assertTrue(isinstance(resultado[0].precio, int))

    def test_producto_obtener_uno_retorna_objeto_con_id_nombre_precio(self):
        resultado = producto.obtener_uno(1)
        self.assertTrue(isinstance(resultado.id, int))
        self.assertTrue(isinstance(resultado.nombre, str))
        self.assertTrue(isinstance(resultado.precio, int))

    def test_producto_insertar_nombre_precio_ultimo_producto_tiene_estos_valores(self):
        nombre_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        precio_rnd = randint(100,300)
        
        producto.insertar(nombre_rnd, precio_rnd)
        productos = producto.obtener_todos()

        self.assertEqual(nombre_rnd, productos[-1].nombre)
        self.assertEqual(precio_rnd, productos[-1].precio)

    def test_producto_actualizar_ultimo_id_nombre_precio_ultimo_producto_tiene_valores_nuevos(self):
        nombre_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        precio_rnd = randint(100,300)
        
        _id = producto.obtener_todos()[-1].id

        producto.actualizar(_id, nombre_rnd, precio_rnd)
        
        resultado = producto.obtener_uno(_id)

        self.assertEqual(nombre_rnd, resultado.nombre)
        self.assertEqual(precio_rnd, resultado.precio)

    def test_eliminar_producto_nuevo_obtener_uno_devuelve_none(self):
        nombre_rnd = ''.join(choices(string.ascii_lowercase, k=5))
        precio_rnd = randint(100,300)
        producto.insertar(nombre_rnd, precio_rnd)

        _id = producto.obtener_todos()[-1].id
        producto.eliminar(_id)
        resultado = producto.obtener_uno(_id)
        self.assertEqual(None, resultado)

    def test_eliminar_producto_id_no_existente_menos1_raise_exception(self):
        with self.assertRaises(Exception) as cm:
            producto.eliminar(-1)

        self.assertEqual("Registro no encontrado", str(cm.exception))



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

class Test_VendedorServicio(unittest.TestCase):
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