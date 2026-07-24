"""Acceso a datos de la tabla categorias.

Proporciona operaciones CRUD completas para gestionar
las categorias de productos.
"""

from models.category import Category
from database.db import Database


class CategoryDAO:
    """Data Access Object para la tabla categories.

    Args:
        db: Instancia de Database para obtener conexiones.
    """

    def __init__(self, db: Database):
        self.db = db

    def create(self, category: Category):
        """Inserta una nueva categoria en la BD.

        Args:
            category: Objeto Category con name. El id se genera automaticamente.
        """
        with self.db._connect() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO categories (name) VALUES (?)", (category.name,))
            conn.commit()

    def get_all(self):
        """Retorna todas las categorias ordenadas alfabeticamente.

        Returns:
            List[Category]: Lista de categorias existentes.
        """
        with self.db._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM categories ORDER BY name")
            rows = cur.fetchall()
        return [Category(id=r[0], name=r[1]) for r in rows]

    def get_by_id(self, category_id: int):
        """Busca una categoria por su id.

        Args:
            category_id: Identificador de la categoria.

        Returns:
            Category si existe, None si no se encuentra.
        """
        with self.db._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM categories WHERE id=?", (category_id,))
            r = cur.fetchone()
        if r:
            return Category(id=r[0], name=r[1])
        return None

    def update(self, category: Category):
        """Actualiza el nombre de una categoria existente.

        Args:
            category: Objeto Category con id existente y nuevo name.
        """
        with self.db._connect() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE categories SET name=? WHERE id=?", (category.name, category.id))
            conn.commit()

    def delete(self, category_id: int):
        """Elimina una categoria por su id.

        NOTA: La validacion de que no tenga productos asociados
        se realiza en el CategoryController, no aqui.

        Args:
            category_id: Identificador de la categoria a eliminar.
        """
        with self.db._connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM categories WHERE id=?", (category_id,))
            conn.commit()
