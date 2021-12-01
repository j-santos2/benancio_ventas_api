import os
import tempfile
path_database = f"{tempfile.gettempdir()}/benancio_ventas_api.db"
os.environ['JWT_SECRET_KEY'] = "Clave secreta"
os.environ["DATABASE_ENV"] = f"sqlite:///{path_database}"
if os.path.exists(path_database):
    os.remove(path_database)

from src.modelos import Base
from conexion import conexion

Base.metadata.create_all(conexion.engine)