from src.servicios.exceptions import ObjetoNoEncontrado
from .recurso_servicio import RecursoServicio
from .decorators_servicios import commit_after
from ..modelos import VentaModelo


class VentaServicio(RecursoServicio):
    def obtener_todos(self):
        return self._sesion.query(VentaModelo).all()

    def obtener_uno (self, _id):
        venta_obtenida = self._sesion.query(VentaModelo).filter(VentaModelo.id == _id).first()
        if venta_obtenida == None:
            raise ObjetoNoEncontrado(f"Venta con id {_id} no existe")
        return venta_obtenida

    def obtener_ventas_por_vendedor(self, id):
        return self._sesion.query(VentaModelo).filter(VentaModelo.vendedor_id == id).all()

    @commit_after
    def insertar(self, producto_id, vendedor_id):
        venta_a_insertar = VentaModelo(producto_id = producto_id,vendedor_id = vendedor_id)
        self._sesion.add(venta_a_insertar)
        return venta_a_insertar

venta = VentaServicio()
