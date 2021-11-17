import os
os.environ["DATABASE_ENV"] = "sqlite:////tmp/benancio_ventas_api.db"

from src.modelos import Base
from conexion import conexion

Base.metadata.create_all(conexion.engine)