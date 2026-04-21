# ============================================================
# INGREDIENTE SERVICE
# ============================================================
# Lógica de negocio para Ingrediente.
# Usa IngredienteUoW para coordinar repositorio y sesión.
# ============================================================

from sqlmodel import Session
from typing import List, Optional
from app.ingrediente.schema import IngredienteCreate, IngredienteUpdate
from app.ingrediente.model import Ingrediente
from app.ingrediente.uow import IngredienteUoW


def obtener_todos(session: Session, skip: int = 0, limit: int = 10) -> List[Ingrediente]:
    """Retorna todos los ingredientes con paginación."""
    with IngredienteUoW(session) as uow:
        return uow.repository.get_all(skip, limit)


def obtener_por_id(session: Session, id: int) -> Optional[Ingrediente]:
    """Retorna un ingrediente por ID."""
    with IngredienteUoW(session) as uow:
        return uow.repository.get_by_id(id)


def crear(session: Session, data: IngredienteCreate) -> Ingrediente:
    """Crea un nuevo ingrediente."""
    with IngredienteUoW(session) as uow:
        ingrediente = uow.repository.create(data)
        uow.commit()
        uow.refresh(ingrediente)
        return ingrediente


def actualizar(session: Session, id: int, data: IngredienteUpdate) -> Optional[Ingrediente]:
    """Actualización parcial de un ingrediente."""
    with IngredienteUoW(session) as uow:
        ingrediente = uow.repository.get_by_id(id)
        if not ingrediente:
            return None
        ingrediente = uow.repository.update(ingrediente, data)
        uow.commit()
        uow.refresh(ingrediente)
        return ingrediente


def eliminar(session: Session, id: int) -> bool:
    """Eliminación física del ingrediente."""
    with IngredienteUoW(session) as uow:
        ingrediente = uow.repository.get_by_id(id)
        if not ingrediente:
            return False
        uow.repository.delete(ingrediente)
        uow.commit()
        return True