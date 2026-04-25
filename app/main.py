# ============================================================
# MAIN.PY - Punto de entrada de la aplicación
# ============================================================
# Crea la instancia de FastAPI, configura CORS y registra
# todos los routers de cada módulo.
# El evento "startup" crea las tablas en PostgreSQL
# si no existen al iniciar la aplicación.
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_db_and_tables
from app.categoria.router import router as categoria_router
from app.ingrediente.router import router as ingrediente_router
from app.producto.router import router as producto_router
from app.producto_categoria.router import router as producto_categoria_router
from app.producto_ingrediente.router import router as producto_ingrediente_router


app = FastAPI(
    title="API Parcial 1 - Catálogo de Productos",
    description="API REST con FastAPI + SQLModel + PostgreSQL. Gestión de Categorías, Productos e Ingredientes con relaciones N:N.",
    version="1.0.0"
)

# ============================================================
# CORS - Cross Origin Resource Sharing
# Permite que el frontend en localhost:5173 (Vite)
# pueda hacer requests al backend en localhost:8000
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """
    es ejecutado automáticamente al iniciar el servidor y se crean todas lss tablas en PostgreSQL si no existen
    """
    create_db_and_tables()


# ============================================================
# REGISTRO DE ROUTERS
# Cada módulo tiene su propio router con su prefijo y tag
# ============================================================
app.include_router(categoria_router)
app.include_router(ingrediente_router)
app.include_router(producto_router)
app.include_router(producto_categoria_router)
app.include_router(producto_ingrediente_router)