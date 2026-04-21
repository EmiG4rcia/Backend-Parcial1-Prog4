# ============================================================
# PRODUCTO_INGREDIENTE SERVICE
# ============================================================
# Lógica de negocio para la relación N:N
# entre Producto e Ingrediente.
# ============================================================

from sqlmodel import Session
from typing import List, Optional
from app.producto_ingrediente.schema import ProductoIngredienteCreate
from app.producto_ingrediente.model import ProductoIngrediente
from app.producto_ingrediente.uow import ProductoIngredienteUoW


def obtener_por_producto(session: Session, producto_id: int) -> List[ProductoIngrediente]:
    """Retorna todos los ingredientes de un producto."""
    with ProductoIngredienteUoW(session) as uow:
        return uow.repository.get_by_producto(producto_id)


def crear(session: Session, data: ProductoIngredienteCreate) -> ProductoIngrediente:
    """
    Vincula un ingrediente a un producto.
    Si ya existe el vínculo lo retorna sin duplicar.
    """
    with ProductoIngredienteUoW(session) as uow:
        existente = uow.repository.get_by_ids(data.producto_id, data.ingrediente_id)
        if existente:
            return existente
        vinculo = uow.repository.create(data)
        uow.commit()
        uow.refresh(vinculo)
        return vinculo


def eliminar(session: Session, producto_id: int, ingrediente_id: int) -> bool:
    """Elimina el vínculo entre un producto y un ingrediente."""
    with ProductoIngredienteUoW(session) as uow:
        vinculo = uow.repository.get_by_ids(producto_id, ingrediente_id)
        if not vinculo:
            return False
        uow.repository.delete(vinculo)
        uow.commit()
        return True