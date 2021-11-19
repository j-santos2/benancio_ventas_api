from .recurso_servicio import RecursoServicio
from .decorators_servicios import commit_after
from ..modelos import VendedorModelo


class VendedorServicio(RecursoServicio):
    def obtener_todos(self):
        return self._sesion.query(VendedorModelo).all()

    def obtener_uno (self, _id):
        return self._sesion.query(VendedorModelo).filter(VendedorModelo.id == _id).first()

    @commit_after
    def insertar(self, nombre, apellido, sucursal_id):
        self._sesion.add(VendedorModelo(nombre = nombre,apellido = apellido, sucursal_id = sucursal_id))

    @commit_after
    def actualizar(self, id, nombre, apellido, sucursal_id):
        self._sesion.query(VendedorModelo).filter(VendedorModelo.id == id).update({"nombre" : nombre, "apellido" : apellido, "sucursal_id" : sucursal_id})
    
    @commit_after
    def eliminar(self, id):
        elemento = self._sesion.get(VendedorModelo, id)
        if elemento == None:
            raise Exception("Registro no encontrado")
        self._sesion.delete(elemento)
vendedor = VendedorServicio()
