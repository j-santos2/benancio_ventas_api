import functools
from conexion import conexion
from sqlalchemy.exc import IntegrityError

def commit_after(data_function):
    @functools.wraps(data_function)
    def wrapper(*args):
        try:
            objeto_nuevo = data_function(*args)
            conexion.sesion.commit()
        except IntegrityError as e:
            conexion.sesion.rollback()
            return {"Mensaje:":"Rollback realizado"}
        else:
            return objeto_nuevo
    return wrapper