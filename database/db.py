"""Conexion y gestion de la base de datos SQLite.

Crea las tablas categories y products con la relacion FK
al iniciar la instancia. Proporciona el metodo _connect() 
que los DAOs usan para obtener una conexion.
"""

import sqlite3


class Database:
    """Maneja la conexion y esquema de la base de datos SQLite.

    Attributes:
        path: Ruta al archivo .db (por defecto 'products.db' en el cwd).
    """

    def __init__(self, path="products.db"):
        self.path = path
        # Crear tablas si no existen al inicializar
        self._create_tables()

    def _connect(self):
        """Retorna una nueva conexion SQLite al archivo de la BD."""
        return sqlite3.connect(self.path)

    def _create_tables(self):
        """Crea las tablas categories y products si no existen.

        Esquema:
            categories: id (PK), name (UNIQUE, NOT NULL)
            products:   id (PK), name (NOT NULL), category_id (FK→categories),
                        price (REAL, NOT NULL), units (INTEGER, DEFAULT 0)
        """
        with self._connect() as conn:
            cur = conn.cursor()
            # Tabla de categorias
            cur.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            """)
            # Tabla de productos con FK a categorias
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category_id INTEGER NOT NULL,
                    price REAL NOT NULL,
                    units INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """)
            conn.commit()
