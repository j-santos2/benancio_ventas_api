from abc import ABC
from modelos import Producto, Sucursal, Venta, Vendedor 
from conexion import conexion
import functools
from dataclasses import dataclass 

def commit_after(data_function):
    @functools.wraps(data_function)
    def wrapper(*args):
        data_function(*args)
        conexion.sesion.commit()
    return wrapper

class RecursoServicio(ABC):
    _sesion = conexion.sesion

@dataclass
class ProductoServicio(RecursoServicio):
    id: int = None
    nombre: str = None
    precio: int = None
    
    def obtener_todos(self):
        return self._sesion.query(Producto).all()

    def obtener_uno (self, _id):
        return self._sesion.query(Producto).filter(Producto.id == _id).first()

    @commit_after
    def insertar(self, nombre, precio):
        self._sesion.add(Producto(nombre = nombre,precio = precio))

    @commit_after
    def actualizar(self, id, nombre, precio):
        self._sesion.query(Producto).filter(Producto.id == id).update({"nombre" : nombre, "precio" : precio})
    
    @commit_after
    def eliminar(self, id):
        elemento = self._sesion.get(Producto, id)
        if elemento == None:
            raise Exception("Registro no encontrado")
        self._sesion.delete(elemento)

class SucursalServicio(RecursoServicio):
    def obtener_todos(self):
        return self._sesion.query(Sucursal).all()

    def obtener_uno (self, _id):
        return self._sesion.query(Sucursal).filter(Sucursal.id == _id).first()

    @commit_after
    def insertar(self, nombre):
        self._sesion.add(Sucursal(nombre = nombre))

    @commit_after
    def actualizar(self, id, nombre):
        self._sesion.query(Sucursal).filter(Sucursal.id == id).update({"nombre" : nombre})
    
    @commit_after
    def eliminar(self, id):
        elemento = self._sesion.get(Sucursal, id)
        if elemento == None:
            raise Exception("Registro no encontrado")
        self._sesion.delete(elemento)

class VendedorServicio(RecursoServicio):
    def obtener_todos(self):
        return self._sesion.query(Vendedor).all()

    def obtener_uno (self, _id):
        return self._sesion.query(Vendedor).filter(Vendedor.id == _id).first()

    @commit_after
    def insertar(self, nombre, apellido, sucursal_id):
        self._sesion.add(Vendedor(nombre = nombre,apellido = apellido, sucursal_id = sucursal_id))

    @commit_after
    def actualizar(self, id, nombre, apellido, sucursal_id):
        self._sesion.query(Vendedor).filter(Vendedor.id == id).update({"nombre" : nombre, "apellido" : apellido, "sucursal_id" : sucursal_id})
    
    @commit_after
    def eliminar(self, id):
        elemento = self._sesion.get(Vendedor, id)
        if elemento == None:
            raise Exception("Registro no encontrado")
        self._sesion.delete(elemento)

class VentaServicio(RecursoServicio):
    def obtener_todos(self):
        return self._sesion.query(Venta).all()

    def obtener_uno (self, _id):
        return self._sesion.query(Venta).filter(Venta.id == _id).first()

    @commit_after
    def insertar(self, producto_id, vendedor_id):
        self._sesion.add(Venta(producto_id = producto_id,vendedor_id = vendedor_id))

producto = ProductoServicio()
vendedor = VendedorServicio()
sucursal = SucursalServicio()
venta = VentaServicio()

if __name__ == "__main__":
    objeto = ProductoServicio(None,None,None)
    rta = objeto.obtener_uno(1)
    print(rta)
