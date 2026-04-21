# ============================================================
# PRODUCTO_CATEGORIA SERVICE
# ============================================================
# Lógica de negocio para la relación N:N
# entre Producto y Categoria.
# Regla de negocio: solo puede haber un es_principal = true
# por producto. Al marcar una categoría como principal,
# las demás se desmarcan automáticamente.
# ============================================================

from sqlmodel import Session
from typing import List, Optional
from app.producto_categoria.schema import ProductoCategoriaCreate
from app.producto_categoria.model import ProductoCategoria
from app.producto_categoria.uow import ProductoCategoriaUoW


def obtener_por_producto(session: Session, producto_id: int) -> List[ProductoCategoria]:
    """Retorna todas las categorías de un producto."""
    with ProductoCategoriaUoW(session) as uow:
        return uow.repository.get_by_producto(producto_id)


def obtener_por_categoria(session: Session, categoria_id: int) -> List[ProductoCategoria]:
    """Retorna todos los vínculos de una categoría."""
    with ProductoCategoriaUoW(session) as uow:
        return uow.repository.get_by_categoria(categoria_id)


def crear(session: Session, data: ProductoCategoriaCreate) -> ProductoCategoria:
    """
    Vincula un producto con una categoría.
    Si ya existe el vínculo lo retorna sin duplicar.
    Regla de negocio: si es_principal es True, desactiva
    el es_principal de todas las otras categorías del producto.
    """
    with ProductoCategoriaUoW(session) as uow:
        # Verificar si ya existe el vínculo
        existente = uow.repository.get_by_ids(data.producto_id, data.categoria_id)
        if existente:
            return existente

        # Si la nueva categoría es principal,
        # desmarcar todas las otras categorías principales del producto
        if data.es_principal:
            vinculos = uow.repository.get_by_producto(data.producto_id)
            for vinculo in vinculos:
                if vinculo.es_principal:
                    vinculo.es_principal = False
                    session.add(vinculo)

        vinculo = uow.repository.create(data)
        uow.commit()
        uow.refresh(vinculo)
        return vinculo


def eliminar(session: Session, producto_id: int, categoria_id: int) -> bool:
    """Elimina el vínculo entre un producto y una categoría."""
    with ProductoCategoriaUoW(session) as uow:
        vinculo = uow.repository.get_by_ids(producto_id, categoria_id)
        if not vinculo:
            return False
        uow.repository.delete(vinculo)
        uow.commit()
        return True