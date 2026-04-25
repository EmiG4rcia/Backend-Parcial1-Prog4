
# Lógica de negocio para Categoria.
# Reglas de negocio clave:
# - Nombres únicos en todo el árbol (409 Conflict)
# - Soft delete recursivo de hijos al eliminar un padre
# - BLOQUEO de eliminación si la categoría (o cualquiera
#   de sus hijos) es es_principal para algún producto.
#   El usuario debe reasignar el producto antes de eliminar.


# ==========

from sqlmodel import Session
from typing import List, Optional
from fastapi import HTTPException, status
from app.categoria.schema import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaWithLevel,
    CategoriaRuta,
)
from app.categoria.model import Categoria
from app.categoria.uow import CategoriaUoW
from app.producto_categoria.repository import ProductoCategoriaRepository


def obtener_todas(session: Session, skip: int = 0, limit: int = 100) -> List[Categoria]:
    """Retorna todas las categorías activas con paginación."""
    with CategoriaUoW(session) as uow:
        return uow.repository.get_all(skip, limit)


def obtener_por_id(session: Session, id: int) -> Optional[Categoria]:
    """Retorna una categoría por ID."""
    with CategoriaUoW(session) as uow:
        return uow.repository.get_by_id(id)


def obtener_raices(session: Session) -> List[Categoria]:
    """Retorna todas las categorías raíz."""
    with CategoriaUoW(session) as uow:
        return uow.repository.get_roots()


def obtener_hijos(session: Session, parent_id: int) -> List[Categoria]:
    """Retorna los hijos directos de una categoría."""
    with CategoriaUoW(session) as uow:
        return uow.repository.get_children(parent_id)


def obtener_ruta(session: Session, id: int) -> CategoriaRuta:
    """Construye la ruta completa desde la raíz hasta la categoría."""
    with CategoriaUoW(session) as uow:
        categorias = uow.repository.get_tree_path(id)
        path = " > ".join([c.nombre for c in categorias])
        return CategoriaRuta(categorias=categorias, path=path)


def obtener_plano_con_nivel(session: Session) -> List[CategoriaWithLevel]:
    """Retorna todas las categorías con nivel de profundidad y ruta."""
    with CategoriaUoW(session) as uow:
        flat = uow.repository.get_all_flat_with_level()
        return [CategoriaWithLevel(**item) for item in flat]


def crear(session: Session, data: CategoriaCreate) -> Categoria:
    """
    Crea una nueva categoría.
    Valida unicidad del nombre en todo el árbol.
    """
    with CategoriaUoW(session) as uow:
        existente = uow.repository.get_by_nombre(data.nombre)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una categoría con el nombre '{data.nombre}'"
            )
        categoria = uow.repository.create(data)
        uow.commit()
        uow.refresh(categoria)
        return categoria


def actualizar(session: Session, id: int, data: CategoriaUpdate) -> Optional[Categoria]:
    """
    Actualización parcial de una categoría.
    Valida unicidad del nombre si se está cambiando.
    """
    with CategoriaUoW(session) as uow:
        categoria = uow.repository.get_by_id(id)
        if not categoria:
            return None
        if data.nombre is not None and data.nombre != categoria.nombre:
            existente = uow.repository.get_by_nombre(data.nombre)
            if existente:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe una categoría con el nombre '{data.nombre}'"
                )
        categoria = uow.repository.update(categoria, data)
        uow.commit()
        uow.refresh(categoria)
        return categoria


def _verificar_es_principal_recursivo(
    session: Session,
    categoria_id: int,
    pc_repo: ProductoCategoriaRepository,
    cat_repo
) -> Optional[str]:
    """
    Verifica recursivamente si esta categoría o alguno de sus hijos
    es es_principal para algún producto.
    Retorna el nombre de la categoría bloqueante si existe, None si no.
    Esta función es privada — solo la usa el service de eliminar.
    """
    # Verificar la categoría actual
    vinculo_principal = pc_repo.get_principal_by_categoria(categoria_id)
    if vinculo_principal:
        cat = cat_repo.get_by_id(categoria_id)
        return cat.nombre if cat else f"ID {categoria_id}"

    # Verificar recursivamente los hijos
    children = cat_repo.get_children(categoria_id)
    for child in children:
        resultado = _verificar_es_principal_recursivo(
            session, child.id, pc_repo, cat_repo
        )
        if resultado:
            return resultado

    return None


def eliminar(session: Session, id: int) -> bool:
    """
    Soft delete de una categoría y todos sus hijos recursivamente.
    BLOQUEA la eliminación si la categoría o cualquiera de sus hijos
    es es_principal para algún producto.
    El usuario debe reasignar el producto antes de eliminar.
    """
    with CategoriaUoW(session) as uow:
        categoria = uow.repository.get_by_id(id)
        if not categoria:
            return False

        # Verificar si esta categoría o sus hijos son es_principal
        pc_repo = ProductoCategoriaRepository(session)
        bloqueante = _verificar_es_principal_recursivo(
            session, id, pc_repo, uow.repository
        )

        if bloqueante:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"No se puede eliminar esta categoría porque "
                    f"'{bloqueante}' es la categoría principal de uno o más productos. "
                    f"Reasigná la categoría principal de esos productos antes de eliminar."
                )
            )

        # Soft delete recursivo de todos los hijos
        uow.repository.soft_delete_children(id)
        # Soft delete del padre
        uow.repository.soft_delete(categoria)
        uow.commit()
        return True