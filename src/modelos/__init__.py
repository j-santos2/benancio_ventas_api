from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

from .producto_modelo import ProductoModelo
from .vendedor_modelo import Vendedor
from .sucursales_modelo import Sucursal
from .ventas_modelo import Venta