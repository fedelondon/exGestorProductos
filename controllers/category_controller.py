"""Controlador de logica de negocio para categorias.

Valida los datos de entrada, verifica unicidad de nombres
y controla la eliminacion segura (no permite si tiene productos).
"""

from models.category import Category
from database.category_dao import CategoryDAO
from database.product_dao import ProductDAO


class CategoryController:
    """Gestiona la logica de negocio de categorias.

    Valida nombre (no vacio, no duplicado) antes de persistir.
    Verifica que no se elimine una categoria con productos asociados.

    Args:
        category_dao: DAO de categorias para operaciones de BD.
        product_dao: DAO de productos (para verificar dependencias al eliminar).
    """

    def __init__(self, category_dao: CategoryDAO, product_dao: ProductDAO):
        self.category_dao = category_dao
        self.product_dao = product_dao

    def add_category(self, name: str):
        """Valida y crea una nueva categoria.

        Args:
            name: Nombre de la categoria (no vacio, debe ser unico).

        Raises:
            ValueError: Si el nombre esta vacio o ya existe otra categoria igual.
        """
        if not name.strip():
            raise ValueError("El nombre de la categoria no puede estar vacio")
        # Verificar que no exista otra categoria con el mismo nombre (case-insensitive)
        existing = self.category_dao.get_all()
        for cat in existing:
            if cat.name.lower() == name.strip().lower():
                raise ValueError("Ya existe una categoria con ese nombre")
        # Crear y persistir
        category = Category(id=None, name=name.strip())
        self.category_dao.create(category)

    def list_categories(self):
        """Retorna todas las categorias ordenadas alfabeticamente.

        Returns:
            List[Category]: Lista de categorias.
        """
        return self.category_dao.get_all()

    def get_category(self, category_id: int):
        """Busca una categoria por su id.

        Args:
            category_id: Identificador de la categoria.

        Returns:
            Category si existe, None si no.
        """
        return self.category_dao.get_by_id(category_id)

    def update_category(self, category_id: int, name: str):
        """Valida y actualiza una categoria existente.

        Args:
            category_id: ID de la categoria a actualizar.
            name: Nuevo nombre (no vacio, unico entre categorias).

        Raises:
            ValueError: Si el nombre esta vacio o ya existe otra categoria igual.
        """
        if not name.strip():
            raise ValueError("El nombre de la categoria no puede estar vacio")
        # Verificar unicidad excluyendo la propia categoria
        existing = self.category_dao.get_all()
        for cat in existing:
            if cat.name.lower() == name.strip().lower() and cat.id != category_id:
                raise ValueError("Ya existe otra categoria con ese nombre")
        # Actualizar
        category = Category(id=category_id, name=name.strip())
        self.category_dao.update(category)

    def delete_category(self, category_id: int) -> bool:
        """Elimina una categoria si no tiene productos asociados.

        Args:
            category_id: ID de la categoria a eliminar.

        Returns:
            bool: True si se elimino correctamente.
                  False si no se pudo eliminar (tiene productos asociados).
        """
        # Verificar que no tenga productos antes de eliminar
        count = self.product_dao.count_by_category(category_id)
        if count > 0:
            return False
        self.category_dao.delete(category_id)
        return True
