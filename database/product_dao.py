"""Acceso a datos de la tabla productos.

Proporciona operaciones CRUD completas: crear, consultar, 
actualizar, eliminar y contar productos por categoria.
"""

from models.product import Product
from database.db import Database


class ProductDAO:
    """Data Access Object para la tabla products.

    Args:
        db: Instancia de Database para obtener conexiones.
    """

    def __init__(self, db: Database):
        self.db = db

    def create(self, product: Product):
        """Inserta un nuevo producto en la BD.

        Args:
            product: Objeto Product con category_id, price y units.
                     El id se genera automaticamente (AUTOINCREMENT).
        """
        with self.db._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO products (name, category_id, price, units) VALUES (?, ?, ?, ?)",
                (product.name, product.category_id, product.price, product.units)
            )
            conn.commit()

    def get_all(self):
        """Retorna una lista con todos los productos de la BD.

        Returns:
            List[Product]: Lista de productos ordenados por id.
        """
        with self.db._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, category_id, price, units FROM products")
            rows = cur.fetchall()
        return [Product(id=r[0], name=r[1], category_id=r[2], price=r[3], units=r[4]) for r in rows]

    def get_by_id(self, product_id: int):
        """Busca un producto por su id.

        Args:
            product_id: Identificador del producto a buscar.

        Returns:
            Product si existe, None si no se encuentra.
        """
        with self.db._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, category_id, price, units FROM products WHERE id=?", (product_id,))
            r = cur.fetchone()
        if r:
            return Product(id=r[0], name=r[1], category_id=r[2], price=r[3], units=r[4])
        return None

    def get_by_category(self, category_id: int):
        """Retorna todos los productos de una categoria especifica.

        Args:
            category_id: ID de la categoria a filtrar.

        Returns:
            List[Product]: Productos que pertenecen a esa categoria.
        """
        with self.db._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, category_id, price, units FROM products WHERE category_id=?", (category_id,))
            rows = cur.fetchall()
        return [Product(id=r[0], name=r[1], category_id=r[2], price=r[3], units=r[4]) for r in rows]

    def update(self, product: Product):
        """Actualiza los datos de un producto existente.

        Args:
            product: Objeto Product con id existente y campos actualizados.
        """
        with self.db._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE products SET name=?, category_id=?, price=?, units=? WHERE id=?",
                (product.name, product.category_id, product.price, product.units, product.id)
            )
            conn.commit()

    def delete(self, product_id: int):
        """Elimina un producto por su id.

        Args:
            product_id: Identificador del producto a eliminar.
        """
        with self.db._connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE id=?", (product_id,))
            conn.commit()

    def count_by_category(self, category_id: int) -> int:
        """Cuenta cuantos productos pertenecen a una categoria.

        Se usa para validar si se puede eliminar una categoria
        (no se permite si tiene productos asociados).

        Args:
            category_id: ID de la categoria a verificar.

        Returns:
            int: Cantidad de productos en esa categoria.
        """
        with self.db._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM products WHERE category_id=?", (category_id,))
            return cur.fetchone()[0]
