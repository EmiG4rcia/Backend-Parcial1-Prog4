# Checklist — Backend (FastAPI + SQLModel)

## Entorno
- [x] Entorno virtual .venv creado y activado
- [x] requirements.txt con todas las dependencias
- [x] FastAPI corriendo en modo dev

## Modelado
- [x] Tabla Categoría con auto-referencia (parent_id) y soft delete
- [x] Tabla Producto con soft delete e imagenes_url
- [x] Tabla Ingrediente con flag es_alergeno
- [x] Tabla ProductoCategoria — relación N:N con es_principal
- [x] Tabla ProductoIngrediente — relación N:N con es_removible
- [x] Relaciones Relationship con back_populates en todos los modelos

## Validación
- [x] Uso de Annotated para tipado explícito de dependencias
- [x] Uso de Query con ge, le para paginación (skip, limit)
- [x] Uso de Path con gt=0 para validación de IDs
- [x] Schemas separados: Create, Update, Read por módulo

## CRUD Persistente
- [x] Categorías: GET, POST, PATCH, DELETE (soft delete)
- [x] Productos: GET, POST, PATCH, DELETE (soft delete)
- [x] Ingredientes: GET, POST, PATCH, DELETE
- [x] ProductoCategoria: GET, POST, DELETE
- [x] ProductoIngrediente: GET, POST, DELETE

## Seguridad de Datos
- [x] response_model en todos los endpoints
- [x] Schemas de lectura separados de los de escritura
- [x] deleted_at no expuesto en respuestas

## Estructura
- [x] Código organizado por módulos
- [x] Cada módulo tiene: router, schema, service, model, repository, uow
- [x] database.py centraliza la conexión a PostgreSQL
- [x] .env para variables de entorno sensibles
- [x] .gitignore incluye .venv, __pycache__, .env

## Video de Presentación
- [ ] Duración: El video dura 15 minutos o menos.
- [ ] Audio/Video: La voz es clara y la resolución de pantalla permite leer el código.
- [ ] Demo: Se muestra el flujo completo desde la creación hasta la persistencia en la DB.