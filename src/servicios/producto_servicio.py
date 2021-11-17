from . import RecursoServicio, commit_after
from ..modelos import Producto
from dataclasses import dataclass 

@dataclass
class ProductoServicio(RecursoServicio):
    id: int = None
    nombre: str = None
    precio: int = None
    
    def obtener_todos(self):
        return self._sesion.query(Producto).all()

    def obtener_uno (self, _id):
        return self._sesion.query(Producto).filter(Producto.id == _id).first()

    @commit_after
    def insertar(self, nombre, precio):
        self._sesion.add(Producto(nombre = nombre,precio = precio))

    @commit_after
    def actualizar(self, id, nombre, precio):
        self._sesion.query(Producto).filter(Producto.id == id).update({"nombre" : nombre, "precio" : precio})
    
    @commit_after
    def eliminar(self, id):
        elemento = self._sesion.get(Producto, id)
        if elemento == None:
            raise Exception("Registro no encontrado")
        self._sesion.delete(elemento)

producto = ProductoServicio()
