# ============================================================
# INGREDIENTE MODEL
# ============================================================
# Define la tabla 'ingrediente' en PostgreSQL.
# Características clave:
# - nombre único (no se duplican ingredientes)
# - es_alergeno: flag para marcar alérgenos
# - Relación N:N con Producto a través de ProductoIngrediente
# ============================================================

from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.producto_ingrediente.model import ProductoIngrediente


class Ingrediente(SQLModel, table=True):
    __tablename__ = "ingrediente"

    # Clave primaria autoincremental
    id: Optional[int] = Field(default=None, primary_key=True)

    # Nombre único — no se duplican ingredientes globalmente
    nombre: str = Field(max_length=100, unique=True, nullable=False)
    descripcion: Optional[str] = Field(default=None)

    # Flag para identificar alérgenos — importante para UI
    es_alergeno: bool = Field(default=False, nullable=False)

    # Timestamps de auditoría
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relación N:N con Producto a través de ProductoIngrediente
    productos: List["ProductoIngrediente"] = Relationship(back_populates="ingrediente")