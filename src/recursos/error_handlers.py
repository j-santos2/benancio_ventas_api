from src import api
from src.servicios.exceptions import ObjetoNoEncontrado, ErrorDeIntegridad

@api.errorhandler(ObjetoNoEncontrado)
def handle_objeto_no_encontrado(e):
    return {"msg":str(e)}, 400

@api.errorhandler(ErrorDeIntegridad)
def handle_error_de_integridad(e):
    return {"msg":str(e)}, 400
