
# Endpoints HTTP para Categoria.
# Nuevos endpoints para navegación del árbol:
# - GET /categorias/raices — categorías de primer nivel
# - GET /categorias/con-nivel — árbol completo con niveles
# - GET /categorias/{id}/hijos — hijos directos
# - GET /categorias/{id}/ruta — ruta completa hasta la raíz
# IMPORTANTE: las rutas estáticas (/raices, /con-nivel)
# deben estar ANTES que las rutas dinámicas (/{id})
# para que FastAPI no las confunda con IDs.

from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from sqlmodel import Session
from typing import List, Annotated
from app.core.database import get_session
from app.categoria.schema import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaRead,
    CategoriaWithLevel,
    CategoriaRuta,
)
from app.categoria import service

router = APIRouter(prefix="/categorias", tags=["Categorías"])

SessionDep = Annotated[Session, Depends(get_session)]


#  Rutas estáticas PRIMERO ------------------------------------------
# Deben ir antes de /{id} para evitar conflictos de routing

@router.get(
    "/raices",
    response_model=List[CategoriaRead],
    status_code=status.HTTP_200_OK,
    summary="Obtener categorías raíz"
)
def obtener_raices(session: SessionDep):
    """
    Retorna todas las categorías de primer nivel (sin padre).
    Se usa para construir el árbol en el frontend.
    """
    return service.obtener_raices(session)


@router.get(
    "/con-nivel",
    response_model=List[CategoriaWithLevel],
    status_code=status.HTTP_200_OK,
    summary="Obtener categorías con nivel de profundidad"
)
def obtener_con_nivel(session: SessionDep):
    """
    Retorna todas las categorías con su nivel de profundidad
    y ruta completa para el dropdown indentado del frontend.
    Ejemplo de respuesta:
    - nivel 0: Hamburguesas (path: "Hamburguesas")
    - nivel 1: De carne (path: "Hamburguesas > De carne")
    - nivel 2: Con Carne Sin Verdura (path: "Hamburguesas > De carne > Con Carne Sin Verdura")
    """
    return service.obtener_plano_con_nivel(session)


#  Rutas con paginación----------------------------- 

@router.get(
    "/",
    response_model=List[CategoriaRead],
    status_code=status.HTTP_200_OK,
    summary="Listar categorías"
)
def listar_categorias(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0, description="Registros a saltar")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Máximo de registros")] = 100,
):
    """Retorna todas las categorías activas con paginación."""
    return service.obtener_todas(session, skip, limit)


#  Rutas dinámicas ---------------------------------
# Van DESPUÉS de las rutas estáticas

@router.get(
    "/{id}",
    response_model=CategoriaRead,
    status_code=status.HTTP_200_OK,
    summary="Obtener categoría por ID"
)
def obtener_categoria(
    session: SessionDep,
    id: Annotated[int, Path(gt=0)]
):
    """Retorna una categoría específica por su ID."""
    categoria = service.obtener_por_id(session, id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con id {id} no encontrada"
        )
    return categoria


@router.get(
    "/{id}/hijos",
    response_model=List[CategoriaRead],
    status_code=status.HTTP_200_OK,
    summary="Obtener hijos de una categoría"
)
def obtener_hijos(
    session: SessionDep,
    id: Annotated[int, Path(gt=0)]
):
    """
    Retorna los hijos directos de una categoría.
    Se usa para expandir nodos del árbol en el frontend.
    """
    return service.obtener_hijos(session, id)


@router.get(
    "/{id}/ruta",
    response_model=CategoriaRuta,
    status_code=status.HTTP_200_OK,
    summary="Obtener ruta completa de una categoría"
)
def obtener_ruta(
    session: SessionDep,
    id: Annotated[int, Path(gt=0)]
):
    """
    Retorna la ruta completa desde la raíz hasta la categoría.
    Ejemplo: "Hamburguesas > De carne > Con Carne Sin Verdura"
    """
    categoria = service.obtener_por_id(session, id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con id {id} no encontrada"
        )
    return service.obtener_ruta(session, id)


@router.post(
    "/",
    response_model=CategoriaRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear categoría"
)
def crear_categoria(session: SessionDep, data: CategoriaCreate):
    """
    Crea una nueva categoría.
    Retorna 409 si el nombre ya existe en cualquier nivel del árbol.
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
    id: Annotated[int, Path(gt=0)]
):
    """Actualización parcial de una categoría."""
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
    summary="Eliminar categoría y sus hijos (soft delete recursivo)"
)
def eliminar_categoria(
    session: SessionDep,
    id: Annotated[int, Path(gt=0)]
):
    """
    Soft delete recursivo: elimina la categoría y todos sus hijos.
    Los registros permanecen en la DB marcados con deleted_at.
    """
    eliminada = service.eliminar(session, id)
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con id {id} no encontrada"
        )