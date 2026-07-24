"""Define el modelo de datos para los productos del sistema.

Un producto pertenece a una categoria y tiene precio y unidades en stock.
Se almacena en la tabla 'products' de SQLite con FK a categories.
"""

from dataclasses import dataclass

@dataclass
class Product:
    """Representa un producto del inventario.

    Attributes:
        id: Identificador unico en la BD. None si es nuevo (aun no persistido).
        name: Nombre descriptivo del producto.
        category_id: FK al id de la tabla categories.
        price: Precio unitario del producto.
        units: Cantidad de unidades en stock.
    """
    id: int | None
    name: str
    category_id: int
    price: float
    units: int
