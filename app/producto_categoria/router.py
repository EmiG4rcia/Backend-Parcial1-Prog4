# ============================================================
# PRODUCTO_CATEGORIA ROUTER
# ============================================================
# Endpoints para gestionar la relación N:N
# entre Producto y Categoria.
# ============================================================

from fastapi import APIRouter, HTTPException, Depends, Path, status
from sqlmodel import Session
from typing import List, Annotated
from app.core.database import get_session
from app.producto_categoria.schema import ProductoCategoriaCreate, ProductoCategoriaRead
from app.producto_categoria import service

router = APIRouter(prefix="/producto-categorias", tags=["Producto-Categoría"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.get(
    "/producto/{producto_id}",
    response_model=List[ProductoCategoriaRead],
    status_code=status.HTTP_200_OK,
    summary="Categorías de un producto"
)
def categorias_de_producto(
    session: SessionDep,
    producto_id: Annotated[int, Path(gt=0)]
):
    """
    Retorna todas las categorías asociadas a un producto.
    """
    return service.obtener_por_producto(session, producto_id)


@router.get(
    "/categoria/{categoria_id}",
    response_model=List[ProductoCategoriaRead],
    status_code=status.HTTP_200_OK,
    summary="Productos de una categoría"
)
def productos_de_categoria(
    session: SessionDep,
    categoria_id: Annotated[int, Path(gt=0)]
):
    """
    Retorna todos los vínculos de productos para una categoría.
    """
    return service.obtener_por_categoria(session, categoria_id)


@router.post(
    "/",
    response_model=ProductoCategoriaRead,
    status_code=status.HTTP_201_CREATED,
    summary="Vincular producto con categoría"
)
def vincular(session: SessionDep, data: ProductoCategoriaCreate):
    """
    Crea el vínculo entre un producto y una categoría.
    Si ya existe, retorna el existente sin duplicar.
    """
    return service.crear(session, data)


@router.delete(
    "/{producto_id}/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desvincular producto de categoría"
)
def desvincular(
    session: SessionDep,
    producto_id: Annotated[int, Path(gt=0)],
    categoria_id: Annotated[int, Path(gt=0)]
):
    eliminado = service.eliminar(session, producto_id, categoria_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vínculo no encontrado"
        )