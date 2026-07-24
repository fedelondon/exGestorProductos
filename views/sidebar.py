"""Barra lateral de navegacion de la aplicacion.

Widget fijo a la izquierda de la ventana principal con botones
que permiten navegar entre las vistas de productos y categorias.
"""

import ttkbootstrap as tb
from ttkbootstrap.constants import PRIMARY, INFO, SUCCESS, WARNING
import tkinter as tk


class Sidebar(tk.Frame):
    """Barra lateral con botones de navegacion agrupados por modulo.

    Args:
        parent: Widget padre (la ventana App).
        on_navigate: Callback que recibe el nombre de la vista a cargar.
    """

    def __init__(self, parent, on_navigate):
        super().__init__(parent, bg="#2C3E50", width=200)
        self.on_navigate = on_navigate
        # Fijar ancho fijo: el frame no se contrae ni expande
        self.grid_propagate(False)
        self._build()

    def _build(self):
        """Construye los botones de navegacion agrupados por seccion."""
        # Titulo de la aplicacion
        tk.Label(self, text="Gestor de\nProductos", bg="#2C3E50",
                 fg="white", font=("Arial", 14, "bold")).pack(pady=(20, 10))

        # Seccion de Productos
        tk.Label(self, text="PRODUCTOS", bg="#2C3E50", fg="#95A5A6",
                 font=("Arial", 9, "bold")).pack(pady=(10, 5), anchor="w", padx=15)
        tb.Button(self, text="Crear Producto", bootstyle=PRIMARY,
                  command=lambda: self.on_navigate("product_create")).pack(fill="x", pady=3, padx=10)
        tb.Button(self, text="Listar Productos", bootstyle=INFO,
                  command=lambda: self.on_navigate("product_list")).pack(fill="x", pady=3, padx=10)

        # Seccion de Categorias
        tk.Label(self, text="CATEGORIAS", bg="#2C3E50", fg="#95A5A6",
                 font=("Arial", 9, "bold")).pack(pady=(20, 5), anchor="w", padx=15)
        tb.Button(self, text="Crear Categoria", bootstyle=SUCCESS,
                  command=lambda: self.on_navigate("category_create")).pack(fill="x", pady=3, padx=10)
        tb.Button(self, text="Listar Categorias", bootstyle=WARNING,
                  command=lambda: self.on_navigate("category_list")).pack(fill="x", pady=3, padx=10)
