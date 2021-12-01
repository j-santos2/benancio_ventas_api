from . import conexion
from abc import ABC
from .exceptions import ObjetoNoEncontrado

class RecursoServicio(ABC):
    _sesion = conexion.sesion

    def _get_or_fail(self, modelo, _id):
        entidad = self._sesion.get(modelo, _id)
        if entidad == None:
            raise ObjetoNoEncontrado(f"Entity with id {_id} not found") 
        return entidad
