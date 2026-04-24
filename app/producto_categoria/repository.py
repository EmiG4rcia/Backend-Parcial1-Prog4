# ============================================================
# PRODUCTO_CATEGORIA REPOSITORY
# ============================================================
# Responsable de las operaciones de DB para la tabla
# de unión N:N entre Producto y Categoria.
# ============================================================

from sqlmodel import Session, select
from typing import List, Optional
from app.producto_categoria.model import ProductoCategoria
from app.producto_categoria.schema import ProductoCategoriaCreate


class ProductoCategoriaRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_producto(self, producto_id: int) -> List[ProductoCategoria]:
        """Retorna todas las categorías asociadas a un producto."""
        statement = select(ProductoCategoria).where(
            ProductoCategoria.producto_id == producto_id
        )
        return self.session.exec(statement).all()

    def get_by_categoria(self, categoria_id: int) -> List[ProductoCategoria]:
        """Retorna todos los vínculos de una categoría."""
        statement = select(ProductoCategoria).where(
            ProductoCategoria.categoria_id == categoria_id
        )
        return self.session.exec(statement).all()

    def get_by_ids(self, producto_id: int, categoria_id: int) -> Optional[ProductoCategoria]:
        """Retorna un vínculo específico por sus dos IDs."""
        return self.session.get(ProductoCategoria, (producto_id, categoria_id))

    def get_principal_by_categoria(self, categoria_id: int) -> Optional[ProductoCategoria]:
        """
        Verifica si esta categoría es es_principal para algún producto.
        Se usa antes de eliminar una categoría para bloquear
        la eliminación si está siendo usada como principal.
        """
        statement = select(ProductoCategoria).where(
            ProductoCategoria.categoria_id == categoria_id,
            ProductoCategoria.es_principal == True
        )
        return self.session.exec(statement).first()

    def create(self, data: ProductoCategoriaCreate) -> ProductoCategoria:
        """Crea el vínculo entre producto y categoría."""
        vinculo = ProductoCategoria(
            producto_id=data.producto_id,
            categoria_id=data.categoria_id,
            es_principal=data.es_principal,
        )
        self.session.add(vinculo)
        return vinculo

    def delete(self, vinculo: ProductoCategoria) -> None:
        """Elimina el vínculo entre producto y categoría."""
        self.session.delete(vinculo)