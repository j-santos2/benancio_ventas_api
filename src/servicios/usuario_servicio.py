from werkzeug.security import generate_password_hash, check_password_hash
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

    def login(self, nombre, clave):

        usuario = self._sesion.query(UsuarioModelo).filter(UsuarioModelo.nombre == nombre).first()

        if usuario == None:
            return False
        
        return check_password_hash(usuario.clave, clave)

usuario = UsuarioServicio()