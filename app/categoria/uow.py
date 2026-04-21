# ============================================================
# CATEGORIA UNIT OF WORK
# ============================================================
# El Unit of Work (UoW) coordina la sesión de base de datos
# y el repositorio. Garantiza que todas las operaciones de
# una transacción se confirmen (commit) o se reviertan
# (rollback) juntas.
# Se usa como context manager: with CategoriaUoW(session) as uow
# ============================================================

from sqlmodel import Session
from app.categoria.repository import CategoriaRepository


class CategoriaUoW:
    def __init__(self, session: Session):
        # Recibe la sesión de FastAPI (Depends)
        self.session = session
        # Instancia el repositorio con la misma sesión
        self.repository = CategoriaRepository(session)

    def __enter__(self):
        """Inicia el contexto del UoW."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Si ocurre una excepción hace rollback.
        Si todo va bien, el commit lo hace el service explícitamente.
        """
        if exc_type:
            self.session.rollback()

    def commit(self):
        """Confirma todos los cambios pendientes en la sesión."""
        self.session.commit()

    def refresh(self, instance):
        """Recarga el objeto desde la DB después del commit."""
        self.session.refresh(instance)