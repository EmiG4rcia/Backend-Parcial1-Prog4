# ============================================================
# PRODUCTO_INGREDIENTE SCHEMAS
# ============================================================
# Schema para gestionar la relación N:N entre Producto e Ingrediente.
# ProductoIngredienteCreate: vincula un producto con un ingrediente
# ProductoIngredienteRead: respuesta con datos del vínculo
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional


class ProductoIngredienteCreate(BaseModel):
    producto_id: int = Field(..., example=1)
    ingrediente_id: int = Field(..., example=1)
    # es_removible indica si el cliente puede pedir que se quite
    es_removible: bool = Field(default=False, example=False)


class ProductoIngredienteRead(BaseModel):
    producto_id: int
    ingrediente_id: int
    es_removible: bool

    class Config:
        from_attributes = True