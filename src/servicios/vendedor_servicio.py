from .recurso_servicio import RecursoServicio
from .decorators_servicios import commit_after
from ..modelos import VendedorModelo


class VendedorServicio(RecursoServicio):
    def obtener_todos(self):
        return self._sesion.query(VendedorModelo).all()

    def obtener_uno (self, _id):
        return self._get_or_fail(VendedorModelo, _id)

    def obtener_vendedores_por_sucursal(self,_id):
        return self._sesion.query(VendedorModelo).filter(VendedorModelo.sucursal_id == _id).all()
    
    @commit_after
    def insertar(self, nombre, apellido, sucursal_id):
        vendedor_nuevo = VendedorModelo(nombre = nombre,apellido = apellido, sucursal_id = sucursal_id)
        self._sesion.add(vendedor_nuevo)

        return vendedor_nuevo

    @commit_after
    def actualizar(self, _id, nombre, apellido, sucursal_id):
        vendedor_a_actualizar = self.obtener_uno(_id)

        vendedor_a_actualizar.nombre = nombre
        vendedor_a_actualizar.apellido = apellido
        vendedor_a_actualizar.sucursal_id = sucursal_id

        return vendedor_a_actualizar
    
    @commit_after
    def eliminar(self, _id):
        elemento = self.obtener_uno(_id)
        self._sesion.delete(elemento)

vendedor = VendedorServicio()
