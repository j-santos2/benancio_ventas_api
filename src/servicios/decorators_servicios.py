import functools
from conexion import conexion

def commit_after(data_function):
    @functools.wraps(data_function)
    def wrapper(*args):
        data_function(*args)
        conexion.sesion.commit()
    return wrapper