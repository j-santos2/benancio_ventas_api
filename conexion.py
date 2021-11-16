from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

class Conexion:
    def __init__(self, connectionstr):
        Sesion = sessionmaker(bind = create_engine(connectionstr))
        self.__sesion = Sesion()
    @property
    def sesion(self):
        return self.__sesion

    def __del__(self):
        self.__sesion.close()
        
conexion = Conexion()
