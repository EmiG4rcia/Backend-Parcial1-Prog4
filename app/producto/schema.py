# ============================================================
# PRODUCTO SCHEMAS
# ============================================================
# ProductoCreate: datos de entrada con validaciones estrictas
# ProductoUpdate: actualización parcial
# ProductoRead: respuesta completa de la API
# ProductoReadSimple: respuesta reducida para listados
# ============================================================
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
import json


class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150, example="Pizza Margherita")
    descripcion: Optional[str] = Field(None, example="Pizza con tomate y mozzarella")
    precio_base: float = Field(..., ge=0, example=10.50)
    imagenes_url: Optional[List[str]] = Field(default=[], example=["https://example.com/pizza.jpg"])
    stock_cantidad: int = Field(default=0, ge=0, example=20)
    disponible: bool = Field(default=True, example=True)


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=150)
    descripcion: Optional[str] = None
    precio_base: Optional[float] = Field(None, ge=0)
    imagenes_url: Optional[List[str]] = None
    stock_cantidad: Optional[int] = Field(None, ge=0)
    disponible: Optional[bool] = None


class ProductoRead(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    precio_base: float
    # El validador convierte el string JSON a lista al leer de la DB
    imagenes_url: Optional[List[str]]
    stock_cantidad: int
    disponible: bool
    created_at: datetime
    updated_at: datetime

    @field_validator("imagenes_url", mode="before")
    @classmethod
    def deserializar_imagenes(cls, v):
        """
        Convierte el string JSON guardado en DB a lista de Python.
        Si ya es una lista, lo retorna tal cual.
        """
        if isinstance(v, str):
            return json.loads(v)
        if v is None:
            return []
        return v

    class Config:
        from_attributes = True