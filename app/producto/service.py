# ============================================================
# PRODUCTO SERVICE
# ============================================================
# Lógica de negocio para Producto.
# Usa ProductoUoW para coordinar repositorio y sesión.
# ============================================================

from sqlmodel import Session
from typing import List, Optional
from app.producto.schema import ProductoCreate, ProductoUpdate
from app.producto.model import Producto
from app.producto.uow import ProductoUoW


def obtener_todos(session: Session, skip: int = 0, limit: int = 10) -> List[Producto]:
    """Retorna todos los productos activos con paginación."""
    with ProductoUoW(session) as uow:
        return uow.repository.get_all(skip, limit)


def obtener_por_id(session: Session, id: int) -> Optional[Producto]:
    """Retorna un producto por ID."""
    with ProductoUoW(session) as uow:
        return uow.repository.get_by_id(id)


def crear(session: Session, data: ProductoCreate) -> Producto:
    """Crea un nuevo producto."""
    with ProductoUoW(session) as uow:
        producto = uow.repository.create(data)
        uow.commit()
        uow.refresh(producto)
        return producto


def actualizar(session: Session, id: int, data: ProductoUpdate) -> Optional[Producto]:
    """Actualización parcial de un producto."""
    with ProductoUoW(session) as uow:
        producto = uow.repository.get_by_id(id)
        if not producto:
            return None
        producto = uow.repository.update(producto, data)
        uow.commit()
        uow.refresh(producto)
        return producto


def eliminar(session: Session, id: int) -> bool:
    """Soft delete del producto."""
    with ProductoUoW(session) as uow:
        producto = uow.repository.get_by_id(id)
        if not producto:
            return False
        uow.repository.soft_delete(producto)
        uow.commit()
        return True