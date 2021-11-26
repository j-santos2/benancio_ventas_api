from src import api
from src.servicios.exceptions import ObjetoNoEncontrado

@api.errorhandler(ObjetoNoEncontrado)
def handle_objeto_no_encontrado(e):
    return {"msg":str(e)}, 400