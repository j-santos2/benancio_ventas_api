from . import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

class VendedorModelo(Base):
    __tablename__ = "vendedores"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable = False)
    apellido = Column(String, nullable = False)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable = False)
    sucursal = relationship("SucursalModelo", backref = "vendedor")
    