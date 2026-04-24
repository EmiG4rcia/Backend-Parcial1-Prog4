
# CategoriaCreate: datos de entrada para crear una categoría
# CategoriaUpdate: actualización parcial
# CategoriaRead: respuesta estándar de la API
# CategoriaWithLevel: incluye nivel de profundidad y ruta completa
#   usado para el dropdown indentado en el frontend
# =====================================

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CategoriaCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, example="Pizzas")
    descripcion: Optional[str] = Field(None, example="Pizzas artesanales")
    imagen_url: Optional[str] = Field(None, example="https://example.com/img.jpg")
    parent_id: Optional[int] = Field(None, description="ID de la categoría padre, null si es raíz")


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    parent_id: Optional[int] = None


class CategoriaRead(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    imagen_url: Optional[str]
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoriaWithLevel(BaseModel):
    """
    Schema extendido para el dropdown indentado del frontend.
    level: profundidad en el árbol (0 = raíz, 1 = hijo, 2 = nieto...)
    path: ruta completa desde la raíz hasta esta categoría
        ejemplo: "Hamburguesas > De carne > Con Carne Sin Verdura"
    """
    id: int
    nombre: str
    descripcion: Optional[str]
    imagen_url: Optional[str]
    parent_id: Optional[int]
    level: int
    path: str

    class Config:
        from_attributes = True


class CategoriaRuta(BaseModel):
    """
    Representa la ruta completa de una categoría desde la raíz.
    categorias: lista ordenada desde la raíz hasta la categoría actual
    path: string formateado "Raíz > Hijo > Nieto"
    """
    categorias: List[CategoriaRead]
    path: str