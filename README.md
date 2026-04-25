## Video de presentación

https://youtu.be/ZdeUw92ZCuE



# Parcial 1 — Backend (FastAPI + SQLModel)

Backend REST API desarrollado con FastAPI, SQLModel y PostgreSQL para el sistema de catálogo de productos.

## Tecnologías
- FastAPI + Uvicorn
- SQLModel + SQLAlchemy
- PostgreSQL + psycopg2
- Arquitectura modular: routers, schemas, services, models, repositories, Unit of Work

## Módulos
- **Categoría** — CRUD completo con soft delete y auto-referencia (parent_id)
- **Producto** — CRUD completo con soft delete, imágenes y stock
- **Ingrediente** — CRUD completo
- **ProductoCategoria** — Relación N:N con flag es_principal
- **ProductoIngrediente** — Relación N:N con flag es_removible

## Instalación
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuración
Crear archivo `.env` en la raíz:

## Ejecución
```bash
fastapi dev app/main.py
```

## Documentación
Una vez corriendo, acceder a:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

