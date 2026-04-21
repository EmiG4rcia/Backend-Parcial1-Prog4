# ============================================================
# CATEGORIA REPOSITORY
# ============================================================
# El repositorio es responsable ÚNICAMENTE de las operaciones
# de base de datos. No contiene lógica de negocio.
# Recibe la sesión como dependencia y ejecuta las queries.
# El service llama al repository a través del UoW.
# ============================================================

from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from app.categoria.model import Categoria
from app.categoria.schema import CategoriaCreate, CategoriaUpdate


class CategoriaRepository:
    def __init__(self, session: Session):
        # La sesión es inyectada desde el UoW
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 10) -> List[Categoria]:
        """Retorna todas las categorías no eliminadas."""
        statement = (
            select(Categoria)
            .where(Categoria.deleted_at == None)
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def get_by_id(self, id: int) -> Optional[Categoria]:
        """Retorna una categoría por ID si no está eliminada."""
        statement = (
            select(Categoria)
            .where(Categoria.id == id)
            .where(Categoria.deleted_at == None)
        )
        return self.session.exec(statement).first()

    def create(self, data: CategoriaCreate) -> Categoria:
        """Crea una nueva categoría y la agrega a la sesión."""
        categoria = Categoria(
            nombre=data.nombre,
            descripcion=data.descripcion,
            imagen_url=data.imagen_url,
            parent_id=data.parent_id,
        )
        self.session.add(categoria)
        return categoria

    def update(self, categoria: Categoria, data: CategoriaUpdate) -> Categoria:
        """Actualiza los campos modificados de una categoría."""
        if data.nombre is not None:
            categoria.nombre = data.nombre
        if data.descripcion is not None:
            categoria.descripcion = data.descripcion
        if data.imagen_url is not None:
            categoria.imagen_url = data.imagen_url
        if data.parent_id is not None:
            categoria.parent_id = data.parent_id
        categoria.updated_at = datetime.utcnow()
        self.session.add(categoria)
        return categoria

    def soft_delete(self, categoria: Categoria) -> None:
        """Marca la categoría como eliminada (soft delete)."""
        categoria.deleted_at = datetime.utcnow()
        self.session.add(categoria)