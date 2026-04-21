# ============================================================
# PRODUCTO MODEL
# ============================================================
# Define la tabla 'producto' en PostgreSQL.
# Características clave:
# - precio_base con CHECK >= 0
# - stock_cantidad con CHECK >= 0
# - disponible: flag independiente del stock
# - imagenes_url: texto libre (se guarda como JSON string)
# - Soft delete con deleted_at
# - Relaciones N:N con Categoria e Ingrediente
# ============================================================

from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal

if TYPE_CHECKING:
    from app.producto_categoria.model import ProductoCategoria
    from app.producto_ingrediente.model import ProductoIngrediente


class Producto(SQLModel, table=True):
    __tablename__ = "producto"

    # Clave primaria autoincremental
    id: Optional[int] = Field(default=None, primary_key=True)

    nombre: str = Field(max_length=150, nullable=False)
    descripcion: Optional[str] = Field(default=None)

    # precio_base >= 0 validado a nivel de schema Pydantic
    precio_base: float = Field(nullable=False, ge=0)

    # imagenes_url se guarda como string JSON "[]"
    imagenes_url: Optional[str] = Field(default=None)

    # stock_cantidad >= 0, default 0
    stock_cantidad: int = Field(default=0, nullable=False, ge=0)

    # disponible es independiente del stock
    # stock=0 + disponible=true → badge "Sin stock" en UI
    disponible: bool = Field(default=True, nullable=False)

    # Timestamps de auditoría
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Soft delete
    deleted_at: Optional[datetime] = Field(default=None)

    # Relación N:N con Categoria a través de ProductoCategoria
    categorias: List["ProductoCategoria"] = Relationship(back_populates="producto")

    # Relación N:N con Ingrediente a través de ProductoIngrediente
    ingredientes: List["ProductoIngrediente"] = Relationship(back_populates="producto")