from werkzeug.security import generate_password_hash
from .recurso_servicio import RecursoServicio
from .decorators_servicios import commit_after
from ..modelos import UsuarioModelo


class UsuarioServicio(RecursoServicio):

    @commit_after
    def insertar(self, nombre, clave):
        pass_hasheado = generate_password_hash(clave)
        usuario_nuevo = UsuarioModelo(nombre = nombre, clave = pass_hasheado)
        self._sesion.add(usuario_nuevo)

        return usuario_nuevo

usuario = UsuarioServicio()