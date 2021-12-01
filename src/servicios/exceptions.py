class ObjetoNoEncontrado(Exception):
    pass

class ErrorDeIntegridad(Exception):
    def __str__(self):
        return "Action not allowed on this entity."