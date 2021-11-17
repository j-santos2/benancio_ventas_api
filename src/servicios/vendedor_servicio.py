from . import RecursoServicio, commit_after
from ..modelos import Vendedor


class VendedorServicio(RecursoServicio):
    def obtener_todos(self):
        return self._sesion.query(Vendedor).all()

    def obtener_uno (self, _id):
        return self._sesion.query(Vendedor).filter(Vendedor.id == _id).first()

    @commit_after
    def insertar(self, nombre, apellido, sucursal_id):
        self._sesion.add(Vendedor(nombre = nombre,apellido = apellido, sucursal_id = sucursal_id))

    @commit_after
    def actualizar(self, id, nombre, apellido, sucursal_id):
        self._sesion.query(Vendedor).filter(Vendedor.id == id).update({"nombre" : nombre, "apellido" : apellido, "sucursal_id" : sucursal_id})
    
    @commit_after
    def eliminar(self, id):
        elemento = self._sesion.get(Vendedor, id)
        if elemento == None:
            raise Exception("Registro no encontrado")
        self._sesion.delete(elemento)
vendedor = VendedorServicio()
