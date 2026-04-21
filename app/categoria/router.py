# ============================================================
# CATEGORIA ROUTER
# ============================================================
# Define los endpoints HTTP para Categoria.
# Usa Annotated + Query para paginación y filtros.
# Usa Depends(get_session) para inyección de sesión DB.
# Maneja excepciones con HTTPException y códigos de estado.
# ============================================================

from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from sqlmodel import Session
from typing import List, Annotated
from app.core.database import get_session
from app.categoria.schema import CategoriaCreate, CategoriaUpdate, CategoriaRead
from app.categoria import service

router = APIRouter(prefix="/categorias", tags=["Categorías"])

# Anotación reutilizable para la sesión de DB
SessionDep = Annotated[Session, Depends(get_session)]


@router.get(
    "/",
    response_model=List[CategoriaRead],
    status_code=status.HTTP_200_OK,
    summary="Listar categorías"
)
def listar_categorias(
    session: SessionDep,
    # Annotated + Query con validaciones para paginación
    skip: Annotated[int, Query(ge=0, description="Registros a saltar")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Máximo de registros")] = 10,
):
    """
    Retorna todas las categorías activas (no eliminadas) con paginación.
    - skip: cantidad de registros a saltar (para paginación)
    - limit: cantidad máxima de registros a retornar
    """
    return service.obtener_todas(session, skip, limit)


@router.get(
    "/{id}",
    response_model=CategoriaRead,
    status_code=status.HTTP_200_OK,
    summary="Obtener categoría por ID"
)
def obtener_categoria(
    session: SessionDep,
    id: Annotated[int, Path(gt=0, description="ID de la categoría")]
):
    """
    Retorna una categoría específica por su ID.
    Lanza 404 si no existe o fue eliminada.
    """
    categoria = service.obtener_por_id(session, id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con id {id} no encontrada"
        )
    return categoria


@router.post(
    "/",
    response_model=CategoriaRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear categoría"
)
def crear_categoria(session: SessionDep, data: CategoriaCreate):
    """
    Crea una nueva categoría.
    Si parent_id es null, es una categoría raíz.
    """
    return service.crear(session, data)


@router.patch(
    "/{id}",
    response_model=CategoriaRead,
    status_code=status.HTTP_200_OK,
    summary="Actualizar categoría"
)
def actualizar_categoria(
    session: SessionDep,
    data: CategoriaUpdate,
    id: Annotated[int, Path(gt=0, description="ID de la categoría")]
):
    """
    Actualización parcial de una categoría.
    Solo modifica los campos enviados en el request.
    """
    categoria = service.actualizar(session, id, data)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con id {id} no encontrada"
        )
    return categoria


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar categoría (soft delete)"
)
def eliminar_categoria(
    session: SessionDep,
    id: Annotated[int, Path(gt=0, description="ID de la categoría")]
):
    """
    Soft delete: marca la categoría como eliminada sin borrarla físicamente.
    Retorna 204 No Content si fue exitoso.
    """
    eliminada = service.eliminar(session, id)
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con id {id} no encontrada"
        )