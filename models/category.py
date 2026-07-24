"""Define el modelo de datos para las categorias del sistema.

Una categoria agrupa productos (ej: Fotografia, Computo).
Se almacena en la tabla 'categories' de SQLite.
"""

from dataclasses import dataclass

@dataclass
class Category:
    """Representa una categoria de productos.

    Attributes:
        id: Identificador unico en la BD. None si es nueva (aun no persistida).
        name: Nombre descriptivo de la categoria (debe ser unico).
    """
    id: int | None
    name: str
