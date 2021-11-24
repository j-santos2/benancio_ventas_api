from sqlalchemy.sql.expression import null
from . import Base
from sqlalchemy import Column, Integer, String

class UsuarioModelo(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable = False, unique=True)
    clave = Column(String(255), nullable=False)