class ObjetoNoEncontrado(Exception):
    pass

class ErrorDeIntegridad(Exception):
    def __str__(self):
        return "Acción no permitida sobre el recurso."