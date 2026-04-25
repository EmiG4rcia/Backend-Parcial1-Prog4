
# Responsable únicamente de las operaciones de DB.
# Incluye funciones para navegación del árbol de categorías:
# - get_roots(): categorías sin padre
# - get_children(): hijos directos de una categoría
# - get_tree_path(): recorre hacia arriba hasta la raíz
# - get_all_flat_with_level(): árbol completo con niveles
#   para el dropdown indentado del frontend

#*
# 
# *#


from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from app.categoria.model import Categoria
from app.categoria.schema import CategoriaCreate, CategoriaUpdate


class CategoriaRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Categoria]:
        """Retorna todas las categorías no eliminadas."""
        statement = (
            select(Categoria)
            .where(Categoria.deleted_at == None)
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def get_by_id(self, id: int) -> Optional[Categoria]:
        """Retorna una categoría por ID si no está eliminada."""
        statement = (
            select(Categoria)
            .where(Categoria.id == id)
            .where(Categoria.deleted_at == None)
        )
        return self.session.exec(statement).first()

    def get_roots(self) -> List[Categoria]:
        """
        Retorna todas las categorías raíz (sin padre).
        Son el primer nivel del árbol.
        """
        statement = (
            select(Categoria)
            .where(Categoria.parent_id == None)
            .where(Categoria.deleted_at == None)
        )
        return self.session.exec(statement).all()

    def get_children(self, parent_id: int) -> List[Categoria]:
        """
        Retorna los hijos directos de una categoría.
        Se usa para construir el árbol nivel por nivel.
        """
        statement = (
            select(Categoria)
            .where(Categoria.parent_id == parent_id)
            .where(Categoria.deleted_at == None)
        )
        return self.session.exec(statement).all()

    def get_tree_path(self, id: int) -> List[Categoria]:
        """
        Recorre el árbol HACIA ARRIBA desde una categoría hasta la raíz.
        Retorna la lista ordenada desde la raíz hasta la categoría actual.
        Ejemplo: [Hamburguesas, De carne, Con Carne Sin Verdura]
        """
        path = []
        current = self.get_by_id(id)

        while current is not None:
            path.insert(0, current)  # Inserta al inicio para orden raíz→hoja
            if current.parent_id is None:
                break
            current = self.get_by_id(current.parent_id)

        return path

    def get_all_flat_with_level(self) -> List[dict]:
        """
        Retorna TODAS las categorías con su nivel de profundidad
        y ruta completa, ordenadas para mostrar el árbol como
        lista indentada en el frontend.
        Nivel 0 = raíz, 1 = hijo, 2 = nieto, etc.
        Algoritmo: DFS (depth-first search) iterativo.
        """
        result = []
        # Comenzamos con las raíces
        roots = self.get_roots()

        def traverse(categoria: Categoria, level: int, parent_path: str):
            """Recorre el árbol en profundidad construyendo la ruta."""
            current_path = f"{parent_path} > {categoria.nombre}" if parent_path else categoria.nombre
            result.append({
                "id": categoria.id,
                "nombre": categoria.nombre,
                "descripcion": categoria.descripcion,
                "imagen_url": categoria.imagen_url,
                "parent_id": categoria.parent_id,
                "level": level,
                "path": current_path,
            })
            # Recursión para los hijos
            children = self.get_children(categoria.id)
            for child in children:
                traverse(child, level + 1, current_path)

        for root in roots:
            traverse(root, 0, "")

        return result

    def get_by_nombre(self, nombre: str) -> Optional[Categoria]:
        """
        Verifica si ya existe una categoría con ese nombre.
        Se usa para validar unicidad antes de crear o actualizar.
        """
        statement = (
            select(Categoria)
            .where(Categoria.nombre == nombre)
            .where(Categoria.deleted_at == None)
        )
        return self.session.exec(statement).first()

    def create(self, data: CategoriaCreate) -> Categoria:
        """Crea una nueva categoría y la agrega a la sesión."""
        categoria = Categoria(
            nombre=data.nombre,
            descripcion=data.descripcion,
            imagen_url=data.imagen_url,
            parent_id=data.parent_id,
        )
        self.session.add(categoria)
        return categoria

    def update(self, categoria: Categoria, data: CategoriaUpdate) -> Categoria:
        """Actualiza los campos modificados de una categoría."""
        if data.nombre is not None:
            categoria.nombre = data.nombre
        if data.descripcion is not None:
            categoria.descripcion = data.descripcion
        if data.imagen_url is not None:
            categoria.imagen_url = data.imagen_url
        if data.parent_id is not None:
            categoria.parent_id = data.parent_id
        categoria.updated_at = datetime.utcnow()
        self.session.add(categoria)
        return categoria

    def soft_delete(self, categoria: Categoria) -> None:
        """Marca la categoría como eliminada (soft delete)."""
        categoria.deleted_at = datetime.utcnow()
        self.session.add(categoria)

    def soft_delete_children(self, parent_id: int) -> None:
        """
        Soft delete recursivo de todos los hijos.
        Se llama antes de eliminar el padre para mantener
        la integridad del árbol.
        """
        children = self.get_children(parent_id)
        for child in children:
            # Primero elimina los hijos del hijo (recursión)
            self.soft_delete_children(child.id)
            # Luego elimina el hijo
            self.soft_delete(child)