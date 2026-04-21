# ============================================================
# CATEGORIA MODEL
# ============================================================
# Define la tabla 'categoria' en PostgreSQL usando SQLModel.
# Características clave:
# - parent_id: auto-referencia (una categoría puede tener padre)
# - Relationship con back_populates para navegación bidireccional
# - Soft delete con deleted_at (no se borra físicamente)
# - Timestamps de auditoría (created_at, updated_at)
# ============================================================

from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# TYPE_CHECKING evita importaciones circulares en tiempo de ejecución
# Solo se usan para que el type checker (mypy/pyright) entienda las relaciones
if TYPE_CHECKING:
    from app.producto_categoria.model import ProductoCategoria


class Categoria(SQLModel, table=True):
    __tablename__ = "categoria"

    # Clave primaria autoincremental
    id: Optional[int] = Field(default=None, primary_key=True)

    # Auto-referencia: una categoría puede tener una categoría padre
    # NULL significa que es una categoría raíz
    parent_id: Optional[int] = Field(default=None, foreign_key="categoria.id")

    # nombre único y no nulo
    nombre: str = Field(max_length=100, unique=True, nullable=False)
    descripcion: Optional[str] = Field(default=None)
    imagen_url: Optional[str] = Field(default=None)

    # Timestamps de auditoría
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Soft delete: si tiene fecha, está eliminada lógicamente
    deleted_at: Optional[datetime] = Field(default=None)

    # Relación con ProductoCategoria (1:N)
    # back_populates conecta ambos lados de la relación
    productos: List["ProductoCategoria"] = Relationship(back_populates="categoria")

    # Auto-referencia para categorías hijas
    subcategorias: List["Categoria"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Categoria.id == Categoria.parent_id",
            "foreign_keys": "[Categoria.parent_id]",
            "lazy": "select"
        }
    )