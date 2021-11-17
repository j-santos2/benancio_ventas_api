from . import conexion
from abc import ABC

class RecursoServicio(ABC):
    _sesion = conexion.sesion