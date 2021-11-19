from . import Base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

class VentaModelo(Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True)
    vendedor_id = Column(Integer, ForeignKey("vendedores.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    vendedor = relationship("VendedorModelo", backref = "venta")
    producto = relationship("ProductoModelo", backref = "venta")