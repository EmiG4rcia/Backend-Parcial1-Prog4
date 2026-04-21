# ============================================================
# PRODUCTO_CATEGORIA SCHEMAS
# ============================================================
# Schema para gestionar la relación N:N entre Producto y Categoria.
# ProductoCategoriaCreate: vincula un producto con una categoría
# ProductoCategoriaRead: respuesta con datos de ambos lados
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductoCategoriaCreate(BaseModel):
    producto_id: int = Field(..., example=1)
    categoria_id: int = Field(..., example=1)
    # es_principal indica si esta es la categoría principal del producto
    es_principal: bool = Field(default=False, example=False)


class ProductoCategoriaRead(BaseModel):
    producto_id: int
    categoria_id: int
    es_principal: bool
    created_at: datetime

    class Config:
        from_attributes = True