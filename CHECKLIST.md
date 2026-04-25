# Checklist — Backend (FastAPI + SQLModel)

## Entorno
- Entorno virtual .venv creado y activado
- requirements.txt con todas las dependencias
- FastAPI corriendo en modo dev

## Modelado
- Tabla Categoría con auto-referencia (parent_id) y soft delete
- Tabla Producto con soft delete e imagenes_url
- Tabla Ingrediente con flag es_alergeno
- Tabla ProductoCategoria — relación N:N con es_principal
- Tabla ProductoIngrediente — relación N:N con es_removible
- Relaciones Relationship con back_populates en todos los modelos

## Validación
- Uso de Annotated para tipado explícito de dependencias
- Uso de Query con ge, le para paginación (skip, limit)
- Uso de Path con gt=0 para validación de IDs
- Schemas separados: Create, Update, Read por módulo

## CRUD Persistente

- Endpoints funcionales para Crear, Leer, Actualizar y Borrar (de forma lógica) en PostgreSQL

## Seguridad de Datos
- response_model en todos los endpoints
- Schemas de lectura separados de los de escritura
- deleted_at no expuesto en respuestas

## Estructura
- Código organizado por módulos
- Cada módulo tiene: router, schema, service, model, repository, uow
- database.py centraliza la conexión a PostgreSQL
- .env para variables de entorno sensibles


