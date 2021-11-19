from .recurso_servicio import RecursoServicio
from .decorators_servicios import commit_after
from ..modelos import VentaModelo


class VentaServicio(RecursoServicio):
    def obtener_todos(self):
        return self._sesion.query(VentaModelo).all()

    def obtener_uno (self, _id):
        return self._sesion.query(VentaModelo).filter(VentaModelo.id == _id).first()

    @commit_after
    def insertar(self, producto_id, vendedor_id):
        self._sesion.add(VentaModelo(producto_id = producto_id,vendedor_id = vendedor_id))

venta = VentaServicio()
