"""Controlador de logica de negocio para productos.

Valida los datos de entrada antes de pasarlos al DAO.
Orquesta las operaciones CRUD de productos.
"""

from models.product import Product
from database.product_dao import ProductDAO
from database.category_dao import CategoryDAO


class ProductController:
    """Gestiona la logica de negocio de productos.

    Valida nombre, categoria, precio y unidades antes de persistir.
    Coordina entre ProductDAO (productos) y CategoryDAO (para validaciones).

    Args:
        product_dao: DAO de productos para operaciones de BD.
        category_dao: DAO de categorias (para validaciones futuras).
    """

    def __init__(self, product_dao: ProductDAO, category_dao: CategoryDAO):
        self.product_dao = product_dao
        self.category_dao = category_dao

    def add_product(self, name: str, category_id: int, price: str, units: str):
        """Valida y crea un nuevo producto.

        Args:
            name: Nombre del producto (no puede estar vacio).
            category_id: ID de la categoria (debe existir).
            price: Precio como string (se convierte a float, debe ser >= 0).
            units: Unidades como string (se convierte a int, debe ser >= 0).

        Raises:
            ValueError: Si algun campo no cumple las validaciones.
        """
        # Validar nombre no vacio
        if not name.strip():
            raise ValueError("El nombre no puede estar vacio")
        # Validar que se haya seleccionado una categoria
        if category_id is None:
            raise ValueError("Debe seleccionar una categoria")
        # Validar y convertir precio
        try:
            price_float = float(price)
        except ValueError:
            raise ValueError("El precio debe ser numerico")
        if price_float < 0:
            raise ValueError("El precio no puede ser negativo")
        # Validar y convertir unidades
        try:
            units_int = int(units)
        except ValueError:
            raise ValueError("Las unidades deben ser un numero entero")
        if units_int < 0:
            raise ValueError("Las unidades no pueden ser negativas")
        # Crear el objeto Product y persistirlo
        product = Product(id=None, name=name.strip(), category_id=category_id, price=price_float, units=units_int)
        self.product_dao.create(product)

    def list_products(self, category_id=None):
        """Retorna la lista de productos, opcionalmente filtrados por categoria.

        Args:
            category_id: Si se provee, filtra solo productos de esa categoria.
                         Si es None, retorna todos.

        Returns:
            List[Product]: Lista de productos.
        """
        if category_id:
            return self.product_dao.get_by_category(category_id)
        return self.product_dao.get_all()

    def get_product(self, product_id: int):
        """Busca un producto por su id.

        Args:
            product_id: Identificador del producto.

        Returns:
            Product si existe, None si no.
        """
        return self.product_dao.get_by_id(product_id)

    def update_product(self, product_id: int, name: str, category_id: int, price: str, units: str):
        """Valida y actualiza un producto existente.

        Args:
            product_id: ID del producto a actualizar (debe existir).
            name: Nuevo nombre (no puede estar vacio).
            category_id: Nuevo id de categoria (debe existir).
            price: Nuevo precio como string (se convierte a float, >= 0).
            units: Nuevas unidades como string (se convierte a int, >= 0).

        Raises:
            ValueError: Si algun campo no cumple las validaciones.
        """
        # Mismas validaciones que add_product
        if not name.strip():
            raise ValueError("El nombre no puede estar vacio")
        if category_id is None:
            raise ValueError("Debe seleccionar una categoria")
        try:
            price_float = float(price)
        except ValueError:
            raise ValueError("El precio debe ser numerico")
        if price_float < 0:
            raise ValueError("El precio no puede ser negativo")
        try:
            units_int = int(units)
        except ValueError:
            raise ValueError("Las unidades deben ser un numero entero")
        if units_int < 0:
            raise ValueError("Las unidades no pueden ser negativas")
        # Crear objeto con el id existente y actualizar
        product = Product(id=product_id, name=name.strip(), category_id=category_id, price=price_float, units=units_int)
        self.product_dao.update(product)

    def delete_product(self, product_id: int):
        """Elimina un producto por su id.

        Args:
            product_id: Identificador del producto a eliminar.
        """
        self.product_dao.delete(product_id)
