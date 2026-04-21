# ============================================================
# DATABASE.PY - Configuración de la conexión a PostgreSQL
# ============================================================
# Usa URL.create de SQLAlchemy para evitar problemas de
# codificación con caracteres especiales en la ruta del proyecto.
# ============================================================

from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from sqlalchemy import URL
import os
from dotenv import load_dotenv

load_dotenv()

# URL.create evita el error UnicodeDecodeError causado por
# caracteres especiales (acentos) en la ruta del proyecto
connection_string = URL.create(
    drivername="postgresql",
    username=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "prog4_parcial1")
)

engine = create_engine(connection_string, echo=True)


def create_db_and_tables():
    """
    Crea todas las tablas definidas con SQLModel en la base de datos.
    """
    from app.categoria.model import Categoria
    from app.producto.model import Producto
    from app.ingrediente.model import Ingrediente
    from app.producto_categoria.model import ProductoCategoria
    from app.producto_ingrediente.model import ProductoIngrediente

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Generador que provee una sesión de base de datos por request.
    """
    with Session(engine) as session:
        yield session