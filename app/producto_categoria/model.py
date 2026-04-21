# ============================================================
# PRODUCTO_CATEGORIA MODEL
# ============================================================
# Tabla de unión N:N entre Producto y Categoria.
# Características clave:
# - Clave primaria compuesta (producto_id + categoria_id)
# - es_principal: indica si es la categoría principal del producto
# - Relationships hacia ambos lados para navegación bidireccional
# ============================================================

from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.producto.model import Producto
    from app.categoria.model import Categoria


class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"

    # Clave primaria compuesta
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categoria.id", primary_key=True)

    # Flag que indica si esta es la categoría principal del producto
    es_principal: bool = Field(default=False, nullable=False)

    # Timestamp de creación del vínculo
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Navegación bidireccional
    producto: Optional["Producto"] = Relationship(back_populates="categorias")
    categoria: Optional["Categoria"] = Relationship(back_populates="productos")