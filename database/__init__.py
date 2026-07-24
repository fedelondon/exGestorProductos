"""Paquete de acceso a datos de la aplicacion.

Expone la conexion Database y los DAOs (Data Access Objects)
para persistir y recuperar datos de SQLite.
"""

from database.db import Database
from database.product_dao import ProductDAO
from database.category_dao import CategoryDAO
