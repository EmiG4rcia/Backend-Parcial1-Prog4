# ============================================================
# INGREDIENTE SCHEMAS
# ============================================================
# CategoriaCreate: datos de entrada para crear un ingrediente
# IngredienteUpdate: actualización parcial
# IngredienteRead: respuesta de la API
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class IngredienteCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, example="Mozzarella")
    descripcion: Optional[str] = Field(None, example="Queso mozzarella fresco")
    es_alergeno: bool = Field(default=False, example=False)


class IngredienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = None
    es_alergeno: Optional[bool] = None


class IngredienteRead(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    es_alergeno: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True