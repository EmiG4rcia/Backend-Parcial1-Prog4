# ============================================================
# PRODUCTO_INGREDIENTE REPOSITORY
# ============================================================
# Responsable de las operaciones de DB para la tabla
# de unión N:N entre Producto e Ingrediente.
# ============================================================

from sqlmodel import Session, select
from typing import List, Optional
from app.producto_ingrediente.model import ProductoIngrediente
from app.producto_ingrediente.schema import ProductoIngredienteCreate


class ProductoIngredienteRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_producto(self, producto_id: int) -> List[ProductoIngrediente]:
        """Retorna todos los ingredientes asociados a un producto."""
        statement = select(ProductoIngrediente).where(
            ProductoIngrediente.producto_id == producto_id
        )
        return self.session.exec(statement).all()

    def get_by_ids(self, producto_id: int, ingrediente_id: int) -> Optional[ProductoIngrediente]:
        """Retorna un vínculo específico por sus dos IDs."""
        return self.session.get(ProductoIngrediente, (producto_id, ingrediente_id))

    def create(self, data: ProductoIngredienteCreate) -> ProductoIngrediente:
        """Crea el vínculo entre producto e ingrediente."""
        vinculo = ProductoIngrediente(
            producto_id=data.producto_id,
            ingrediente_id=data.ingrediente_id,
            es_removible=data.es_removible,
        )
        self.session.add(vinculo)
        return vinculo

    def delete(self, vinculo: ProductoIngrediente) -> None:
        """Elimina el vínculo entre producto e ingrediente."""
        self.session.delete(vinculo)