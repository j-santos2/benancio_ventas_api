from .recurso_servicio import RecursoServicio
from .decorators_servicios import commit_after
from ..modelos import SucursalModelo

class SucursalServicio(RecursoServicio):
    def obtener_todos(self):
        return self._sesion.query(SucursalModelo).all()

    def obtener_uno (self, _id):
        return self._sesion.query(SucursalModelo).filter(SucursalModelo.id == _id).first()

    @commit_after
    def insertar(self, nombre):
        sucursal_nueva = SucursalModelo(nombre = nombre)
        self._sesion.add(sucursal_nueva)

        return sucursal_nueva
    
    @commit_after
    def actualizar(self, id, nombre):
        sucursal_a_actualizar = self._sesion.query(SucursalModelo).filter(SucursalModelo.id == id).first()
        sucursal_a_actualizar.nombre = nombre

        return sucursal_a_actualizar
    
    @commit_after
    def eliminar(self, id):
        elemento = self._sesion.get(SucursalModelo, id)
        if elemento == None:
            raise Exception("Registro no encontrado")
        self._sesion.delete(elemento)

sucursal = SucursalServicio()