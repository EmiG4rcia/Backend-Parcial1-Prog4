# ============================================================
# PRODUCTO ROUTER
# ============================================================
# Endpoints HTTP para Producto.
# CRUD completo con paginación y soft delete.
# ============================================================

from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from sqlmodel import Session
from typing import List, Annotated
from app.core.database import get_session
from app.producto.schema import ProductoCreate, ProductoUpdate, ProductoRead
from app.producto import service

router = APIRouter(prefix="/productos", tags=["Productos"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.get(
    "/",
    response_model=List[ProductoRead],
    status_code=status.HTTP_200_OK,
    summary="Listar productos"
)
def listar_productos(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    """
    Retorna todos los productos activos con paginación.
    """
    return service.obtener_todos(session, skip, limit)


@router.get(
    "/{id}",
    response_model=ProductoRead,
    status_code=status.HTTP_200_OK,
    summary="Obtener producto por ID"
)
def obtener_producto(
    session: SessionDep,
    id: Annotated[int, Path(gt=0)]
):
    producto = service.obtener_por_id(session, id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con id {id} no encontrado"
        )
    return producto


@router.post(
    "/",
    response_model=ProductoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear producto"
)
def crear_producto(session: SessionDep, data: ProductoCreate):
    """
    Crea un nuevo producto.
    imagenes_url se serializa internamente como JSON string.
    """
    return service.crear(session, data)


@router.patch(
    "/{id}",
    response_model=ProductoRead,
    status_code=status.HTTP_200_OK,
    summary="Actualizar producto"
)
def actualizar_producto(
    session: SessionDep,
    data: ProductoUpdate,
    id: Annotated[int, Path(gt=0)]
):
    producto = service.actualizar(session, id, data)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con id {id} no encontrado"
        )
    return producto


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar producto (soft delete)"
)
def eliminar_producto(
    session: SessionDep,
    id: Annotated[int, Path(gt=0)]
):
    eliminado = service.eliminar(session, id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con id {id} no encontrado"
        )