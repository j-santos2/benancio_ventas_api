from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

from .producto_modelo import ProductoModelo
from .vendedor_modelo import VendedorModelo
from .sucursales_modelo import SucursalModelo
from .ventas_modelo import VentaModelo
from .usuario_modelo import UsuarioModelo