# ============================================================
# PRODUCTO_INGREDIENTE MODEL
# ============================================================
# Tabla de unión N:N entre Producto e Ingrediente.
# Características clave:
# - Clave primaria compuesta (producto_id + ingrediente_id)
# - es_removible: indica si el cliente puede pedir que lo quiten
# - Relationships hacia ambos lados
# ============================================================

from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.producto.model import Producto
    from app.ingrediente.model import Ingrediente


class ProductoIngrediente(SQLModel, table=True):
    __tablename__ = "producto_ingrediente"

    # Clave primaria compuesta
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    ingrediente_id: int = Field(foreign_key="ingrediente.id", primary_key=True)

    # Flag que indica si el cliente puede solicitar que se quite
    es_removible: bool = Field(default=False, nullable=False)

    # Navegación bidireccional
    producto: Optional["Producto"] = Relationship(back_populates="ingredientes")
    ingrediente: Optional["Ingrediente"] = Relationship(back_populates="productos")