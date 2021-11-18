from .recurso_servicio import RecursoServicio
from .decorators_servicios import commit_after
from ..modelos import Venta


class VentaServicio(RecursoServicio):
    def obtener_todos(self):
        return self._sesion.query(Venta).all()

    def obtener_uno (self, _id):
        return self._sesion.query(Venta).filter(Venta.id == _id).first()

    @commit_after
    def insertar(self, producto_id, vendedor_id):
        self._sesion.add(Venta(producto_id = producto_id,vendedor_id = vendedor_id))

venta = VentaServicio()
