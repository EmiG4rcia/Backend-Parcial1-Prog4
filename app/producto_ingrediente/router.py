# ============================================================
# PRODUCTO_INGREDIENTE ROUTER
# ============================================================
# Endpoints para gestionar la relación N:N
# entre Producto e Ingrediente.
# ============================================================

from fastapi import APIRouter, HTTPException, Depends, Path, status
from sqlmodel import Session
from typing import List, Annotated
from app.core.database import get_session
from app.producto_ingrediente.schema import ProductoIngredienteCreate, ProductoIngredienteRead
from app.producto_ingrediente import service

router = APIRouter(prefix="/producto-ingredientes", tags=["Producto-Ingrediente"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.get(
    "/producto/{producto_id}",
    response_model=List[ProductoIngredienteRead],
    status_code=status.HTTP_200_OK,
    summary="Ingredientes de un producto"
)
def ingredientes_de_producto(
    session: SessionDep,
    producto_id: Annotated[int, Path(gt=0)]
):
    """
    Retorna todos los ingredientes asociados a un producto.
    """
    return service.obtener_por_producto(session, producto_id)


@router.post(
    "/",
    response_model=ProductoIngredienteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Vincular ingrediente a producto"
)
def vincular(session: SessionDep, data: ProductoIngredienteCreate):
    """
    Crea el vínculo entre un producto y un ingrediente.
    """
    return service.crear(session, data)


@router.delete(
    "/{producto_id}/{ingrediente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desvincular ingrediente de producto"
)
def desvincular(
    session: SessionDep,
    producto_id: Annotated[int, Path(gt=0)],
    ingrediente_id: Annotated[int, Path(gt=0)]
):
    eliminado = service.eliminar(session, producto_id, ingrediente_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vínculo no encontrado"
        )