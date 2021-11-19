from .recurso_servicio import RecursoServicio
from .decorators_servicios import commit_after
from ..modelos import ProductoModelo
from dataclasses import dataclass 

@dataclass
class ProductoServicio(RecursoServicio):
    id: int = None
    nombre: str = None
    precio: int = None
    
    def obtener_todos(self):
        return self._sesion.query(ProductoModelo).all()

    def obtener_uno (self, _id):
        return self._sesion.query(ProductoModelo).filter(ProductoModelo.id == _id).first()

    @commit_after
    def insertar(self, nombre, precio):
        producto_nuevo = ProductoModelo(nombre = nombre,precio = precio)
        self._sesion.add(producto_nuevo)
        
        return producto_nuevo 

    @commit_after
    def actualizar(self, id, nombre, precio):
        self._sesion.query(ProductoModelo).filter(ProductoModelo.id == id).update({"nombre" : nombre, "precio" : precio})
    
    @commit_after
    def eliminar(self, id):
        elemento = self._sesion.get(ProductoModelo, id)
        if elemento == None:
            raise Exception("Registro no encontrado")
        self._sesion.delete(elemento)

producto = ProductoServicio()
