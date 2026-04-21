# ============================================================
# INGREDIENTE REPOSITORY
# ============================================================
# Responsable únicamente de las operaciones de DB
# para el módulo Ingrediente.
# ============================================================

from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from app.ingrediente.model import Ingrediente
from app.ingrediente.schema import IngredienteCreate, IngredienteUpdate


class IngredienteRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 10) -> List[Ingrediente]:
        """Retorna todos los ingredientes con paginación."""
        statement = select(Ingrediente).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_by_id(self, id: int) -> Optional[Ingrediente]:
        """Retorna un ingrediente por ID."""
        return self.session.get(Ingrediente, id)

    def create(self, data: IngredienteCreate) -> Ingrediente:
        """Crea un nuevo ingrediente y lo agrega a la sesión."""
        ingrediente = Ingrediente(
            nombre=data.nombre,
            descripcion=data.descripcion,
            es_alergeno=data.es_alergeno,
        )
        self.session.add(ingrediente)
        return ingrediente

    def update(self, ingrediente: Ingrediente, data: IngredienteUpdate) -> Ingrediente:
        """Actualiza los campos modificados de un ingrediente."""
        if data.nombre is not None:
            ingrediente.nombre = data.nombre
        if data.descripcion is not None:
            ingrediente.descripcion = data.descripcion
        if data.es_alergeno is not None:
            ingrediente.es_alergeno = data.es_alergeno
        ingrediente.updated_at = datetime.utcnow()
        self.session.add(ingrediente)
        return ingrediente

    def delete(self, ingrediente: Ingrediente) -> None:
        """Eliminación física del ingrediente."""
        self.session.delete(ingrediente)