# ============================================================
# CATEGORIA SERVICE
# ============================================================
# El service contiene la lógica de negocio.
# Usa el UoW para acceder al repositorio y gestionar
# la transacción. El service decide cuándo hacer commit.
# El router llama al service pasando la sesión de DB.
# ============================================================

from sqlmodel import Session
from typing import List, Optional
from app.categoria.schema import CategoriaCreate, CategoriaUpdate
from app.categoria.model import Categoria
from app.categoria.uow import CategoriaUoW


def obtener_todas(session: Session, skip: int = 0, limit: int = 10) -> List[Categoria]:
    """Retorna todas las categorías activas con paginación."""
    with CategoriaUoW(session) as uow:
        return uow.repository.get_all(skip, limit)


def obtener_por_id(session: Session, id: int) -> Optional[Categoria]:
    """Retorna una categoría por ID."""
    with CategoriaUoW(session) as uow:
        return uow.repository.get_by_id(id)


def crear(session: Session, data: CategoriaCreate) -> Categoria:
    """
    Crea una nueva categoría.
    El UoW garantiza que el commit solo ocurre si todo va bien.
    """
    with CategoriaUoW(session) as uow:
        categoria = uow.repository.create(data)
        uow.commit()
        uow.refresh(categoria)
        return categoria


def actualizar(session: Session, id: int, data: CategoriaUpdate) -> Optional[Categoria]:
    """Actualización parcial de una categoría."""
    with CategoriaUoW(session) as uow:
        categoria = uow.repository.get_by_id(id)
        if not categoria:
            return None
        categoria = uow.repository.update(categoria, data)
        uow.commit()
        uow.refresh(categoria)
        return categoria


def eliminar(session: Session, id: int) -> bool:
    """Soft delete de una categoría."""
    with CategoriaUoW(session) as uow:
        categoria = uow.repository.get_by_id(id)
        if not categoria:
            return False
        uow.repository.soft_delete(categoria)
        uow.commit()
        return True