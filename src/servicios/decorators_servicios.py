import functools
from conexion import conexion

def commit_after(data_function):
    @functools.wraps(data_function)
    def wrapper(*args):
        objeto_nuevo = data_function(*args)
        conexion.sesion.commit()
        return objeto_nuevo
    return wrapper