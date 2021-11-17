from . import Base
from sqlalchemy import Column, Integer, String

    
class Sucursal(Base):
    __tablename__ = "sucursales"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable = False)
