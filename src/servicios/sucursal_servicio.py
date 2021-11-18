from .recurso_servicio import RecursoServicio
from .decorators_servicios import commit_after
from ..modelos import Sucursal

class SucursalServicio(RecursoServicio):
    def obtener_todos(self):
        return self._sesion.query(Sucursal).all()

    def obtener_uno (self, _id):
        return self._sesion.query(Sucursal).filter(Sucursal.id == _id).first()

    @commit_after
    def insertar(self, nombre):
        self._sesion.add(Sucursal(nombre = nombre))

    @commit_after
    def actualizar(self, id, nombre):
        self._sesion.query(Sucursal).filter(Sucursal.id == id).update({"nombre" : nombre})
    
    @commit_after
    def eliminar(self, id):
        elemento = self._sesion.get(Sucursal, id)
        if elemento == None:
            raise Exception("Registro no encontrado")
        self._sesion.delete(elemento)

sucursal = SucursalServicio()