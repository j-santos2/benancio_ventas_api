from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable = False)
    precio = Column(Integer, nullable = False)
    
class Sucursal(Base):
    __tablename__ = "sucursales"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable = False)

class Vendedor(Base):
    __tablename__ = "vendedores"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable = False)
    apellido = Column(String, nullable = False)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"))
    sucursal = relationship("Sucursal", backref = "vendedor")

class Venta(Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True)
    vendedor_id = Column(Integer, ForeignKey("vendedores.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    vendedor = relationship("Vendedor", backref = "venta")
    producto = relationship("Producto", backref = "venta")
