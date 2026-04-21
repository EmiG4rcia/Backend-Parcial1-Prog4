# ============================================================
# INGREDIENTE ROUTER
# ============================================================
# Endpoints HTTP para Ingrediente.
# CRUD completo con paginación y filtro por es_alergeno.
# ============================================================

from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from sqlmodel import Session
from typing import List, Annotated
from app.core.database import get_session
from app.ingrediente.schema import IngredienteCreate, IngredienteUpdate, IngredienteRead
from app.ingrediente import service

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.get(
    "/",
    response_model=List[IngredienteRead],
    status_code=status.HTTP_200_OK,
    summary="Listar ingredientes"
)
def listar_ingredientes(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    """
    Retorna todos los ingredientes con paginación.
    """
    return service.obtener_todos(session, skip, limit)


@router.get(
    "/{id}",
    response_model=IngredienteRead,
    status_code=status.HTTP_200_OK,
    summary="Obtener ingrediente por ID"
)
def obtener_ingrediente(
    session: SessionDep,
    id: Annotated[int, Path(gt=0)]
):
    ingrediente = service.obtener_por_id(session, id)
    if not ingrediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingrediente con id {id} no encontrado"
        )
    return ingrediente


@router.post(
    "/",
    response_model=IngredienteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear ingrediente"
)
def crear_ingrediente(session: SessionDep, data: IngredienteCreate):
    """
    Crea un nuevo ingrediente global.
    """
    return service.crear(session, data)


@router.patch(
    "/{id}",
    response_model=IngredienteRead,
    status_code=status.HTTP_200_OK,
    summary="Actualizar ingrediente"
)
def actualizar_ingrediente(
    session: SessionDep,
    data: IngredienteUpdate,
    id: Annotated[int, Path(gt=0)]
):
    ingrediente = service.actualizar(session, id, data)
    if not ingrediente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingrediente con id {id} no encontrado"
        )
    return ingrediente


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar ingrediente"
)
def eliminar_ingrediente(
    session: SessionDep,
    id: Annotated[int, Path(gt=0)]
):
    eliminado = service.eliminar(session, id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingrediente con id {id} no encontrado"
        )