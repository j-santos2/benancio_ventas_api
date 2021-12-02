from .recurso_servicio import RecursoServicio
from .decorators_servicios import commit_after
from ..modelos import ProductoModelo


class ProductoServicio(RecursoServicio):
    
    def obtener_todos(self):
        return self._sesion.query(ProductoModelo).all()

    def obtener_todos_paginado(self, limite, inicio=0):
        return self._sesion.query(ProductoModelo).slice(inicio, inicio+limite).all()

    def obtener_uno (self, _id):
        return self._get_or_fail(ProductoModelo, _id)

    @commit_after
    def insertar(self, nombre, precio):
        producto_nuevo = ProductoModelo(nombre = nombre,precio = precio)
        self._sesion.add(producto_nuevo)
        
        return producto_nuevo 

    @commit_after
    def actualizar(self, _id, nombre, precio):
        producto_a_actualizar = self.obtener_uno(_id)
        
        producto_a_actualizar.nombre = nombre
        producto_a_actualizar.precio = precio

        return producto_a_actualizar


    @commit_after
    def eliminar(self, _id):
        producto_a_eliminar = self.obtener_uno(_id)
        self._sesion.delete(producto_a_eliminar)
        
producto = ProductoServicio()
