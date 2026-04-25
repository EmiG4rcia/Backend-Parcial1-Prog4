
# Responsable únicamente de las operaciones de DB
# para el módulo Producto.
# imagenes_url se serializa/deserializa como JSON string
# ya que PostgreSQL TEXT no soporta arrays nativamente
# sin extensiones adicionales.


from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import json
from app.producto.model import Producto
from app.producto.schema import ProductoCreate, ProductoUpdate


def _serializar_imagenes(imagenes: Optional[List[str]]) -> Optional[str]:
    """Convierte lista de URLs a string JSON para guardar en DB."""
    if imagenes is None:
        return None
    return json.dumps(imagenes)


class ProductoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 10) -> List[Producto]:
        """Retorna todos los productos no eliminados con paginación."""
        statement = (
            select(Producto)
            .where(Producto.deleted_at == None)
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def get_by_id(self, id: int) -> Optional[Producto]:
        """Retorna un producto por ID si no está eliminado."""
        statement = (
            select(Producto)
            .where(Producto.id == id)
            .where(Producto.deleted_at == None)
        )
        return self.session.exec(statement).first()

    def create(self, data: ProductoCreate) -> Producto:
        """Crea un nuevo producto y lo agrega a la sesión."""
        producto = Producto(
            nombre=data.nombre,
            descripcion=data.descripcion,
            precio_base=data.precio_base,
            imagenes_url=_serializar_imagenes(data.imagenes_url),
            stock_cantidad=data.stock_cantidad,
            disponible=data.disponible,
        )
        self.session.add(producto)
        return producto

    def update(self, producto: Producto, data: ProductoUpdate) -> Producto:
        """Actualiza los campos modificados de un producto."""
        if data.nombre is not None:
            producto.nombre = data.nombre
        if data.descripcion is not None:
            producto.descripcion = data.descripcion
        if data.precio_base is not None:
            producto.precio_base = data.precio_base
        if data.imagenes_url is not None:
            producto.imagenes_url = _serializar_imagenes(data.imagenes_url)
        if data.stock_cantidad is not None:
            producto.stock_cantidad = data.stock_cantidad
        if data.disponible is not None:
            producto.disponible = data.disponible
        producto.updated_at = datetime.utcnow()
        self.session.add(producto)
        return producto

    def soft_delete(self, producto: Producto) -> None:
        """Marca el producto como eliminado (soft delete)."""
        producto.deleted_at = datetime.utcnow()
        self.session.add(producto)