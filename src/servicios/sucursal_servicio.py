from .recurso_servicio import RecursoServicio
from .decorators_servicios import commit_after
from ..modelos import SucursalModelo
from .exceptions import ObjetoNoEncontrado

class SucursalServicio(RecursoServicio):
    def obtener_todos(self):
        return self._sesion.query(SucursalModelo).all()

    def obtener_uno (self, _id):
        return self._get_or_fail(SucursalModelo, _id)

    @commit_after
    def insertar(self, nombre):
        sucursal_nueva = SucursalModelo(nombre = nombre)
        self._sesion.add(sucursal_nueva)

        return sucursal_nueva
    
    @commit_after
    def actualizar(self, _id, nombre):
        sucursal_a_actualizar = self.obtener_uno(_id)
        sucursal_a_actualizar.nombre = nombre

        return sucursal_a_actualizar
    
    @commit_after
    def eliminar(self, _id):
        sucursal_a_eliminar = self.obtener_uno(_id)
        self._sesion.delete(sucursal_a_eliminar)

sucursal = SucursalServicio()