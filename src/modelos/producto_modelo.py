from . import Base
from sqlalchemy import Column, Integer, String

class ProductoModelo(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable = False)
    precio = Column(Integer, nullable = False)

