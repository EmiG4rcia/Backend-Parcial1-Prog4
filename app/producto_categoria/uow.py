# ============================================================
# PRODUCTO_CATEGORIA UNIT OF WORK
# ============================================================

from sqlmodel import Session
from app.producto_categoria.repository import ProductoCategoriaRepository


class ProductoCategoriaUoW:
    def __init__(self, session: Session):
        self.session = session
        self.repository = ProductoCategoriaRepository(session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()

    def commit(self):
        self.session.commit()

    def refresh(self, instance):
        self.session.refresh(instance)