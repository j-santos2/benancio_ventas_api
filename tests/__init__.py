import os
os.environ['JWT_SECRET_KEY'] = "Clave secreta"
os.environ["DATABASE_ENV"] = "sqlite:////tmp/benancio_ventas_api.db"
if os.path.exists("/tmp/benancio_ventas_api.db"):
    os.remove("/tmp/benancio_ventas_api.db")

from src.modelos import Base
from conexion import conexion

Base.metadata.create_all(conexion.engine)