# ============================================================
# CATEGORIA SCHEMAS
# ============================================================
# Los schemas de Pydantic controlan:
# - CategoriaCreate: datos que el cliente envía para crear
# - CategoriaUpdate: datos opcionales para actualizar
# - CategoriaRead: datos que la API devuelve (response_model)
# Separar estos schemas evita exponer datos internos
# y permite validaciones específicas por operación.
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoriaCreate(BaseModel):
    # Annotated + Field para validaciones explícitas
    nombre: str = Field(..., min_length=2, max_length=100, example="Pizzas")
    descripcion: Optional[str] = Field(None, example="Pizzas artesanales")
    imagen_url: Optional[str] = Field(None, example="https://example.com/img.jpg")
    parent_id: Optional[int] = Field(None, example=None, description="ID de la categoría padre, null si es raíz")


class CategoriaUpdate(BaseModel):
    # Todos opcionales — permite actualización parcial
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    parent_id: Optional[int] = None


class CategoriaRead(BaseModel):
    # Solo exponemos los campos que el cliente necesita ver
    id: int
    nombre: str
    descripcion: Optional[str]
    imagen_url: Optional[str]
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True