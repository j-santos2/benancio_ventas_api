from .recurso_servicio import RecursoServicio
from .decorators_servicios import commit_after
from ..modelos import SucursalModelo
from .exceptions import ObjetoNoEncontrado

class SucursalServicio(RecursoServicio):
    def obtener_todos(self):
        return self._sesion.query(SucursalModelo).all()

    def obtener_uno (self, _id):
        sucursal_a_obtener = self._sesion.query(SucursalModelo).filter(SucursalModelo.id == _id).first()
        if sucursal_a_obtener == None:
            raise ObjetoNoEncontrado(f"Sucursal con id {_id} no existe")
        return sucursal_a_obtener

    @commit_after
    def insertar(self, nombre):
        sucursal_nueva = SucursalModelo(nombre = nombre)
        self._sesion.add(sucursal_nueva)

        return sucursal_nueva
    
    @commit_after
    def actualizar(self, _id, nombre):
        sucursal_a_actualizar = self._sesion.query(SucursalModelo).filter(SucursalModelo.id == _id).first()
        if sucursal_a_actualizar == None:
            raise ObjetoNoEncontrado(f"Sucursal con id {_id} no existe")
        sucursal_a_actualizar.nombre = nombre

        return sucursal_a_actualizar
    
    @commit_after
    def eliminar(self, _id):
        elemento = self._sesion.get(SucursalModelo, _id)
        if elemento == None:
            raise ObjetoNoEncontrado(f"Sucursal con id {_id} no existe")
        self._sesion.delete(elemento)

sucursal = SucursalServicio()