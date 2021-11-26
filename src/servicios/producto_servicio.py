from src.servicios.exceptions import ObjetoNoEncontrado
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
        producto_obtenido = self._sesion.query(ProductoModelo).filter(ProductoModelo.id == _id).first()
        if producto_obtenido == None:
            raise ObjetoNoEncontrado(f"Producto con id {_id} no existe")
        return producto_obtenido

    @commit_after
    def insertar(self, nombre, precio):
        producto_nuevo = ProductoModelo(nombre = nombre,precio = precio)
        self._sesion.add(producto_nuevo)
        
        return producto_nuevo 

    @commit_after
    def actualizar(self, _id, nombre, precio):
        producto_a_actualizar = self._sesion.query(ProductoModelo).filter(ProductoModelo.id == _id).first()
        if producto_a_actualizar == None:
            raise ObjetoNoEncontrado(f"Producto con id {_id} no existe")
        producto_a_actualizar.nombre = nombre
        producto_a_actualizar.precio = precio

        return producto_a_actualizar

    @commit_after
    def eliminar(self, _id):
        elemento = self._sesion.get(ProductoModelo, _id)
        if elemento == None:
            raise ObjetoNoEncontrado(f"Producto con id {_id} no existe")
        self._sesion.delete(elemento)

producto = ProductoServicio()
