"""Punto de entrada de la aplicacion: ventana principal con navegacion por sidebar.

Configura la ventana raiz, instancia los controladores y orquesta la navegacion
entre vistas usando un metodo centralizado navigate().
"""

import ttkbootstrap as tb
import tkinter as tk

# Capa de datos
from database.db import Database
from database.product_dao import ProductDAO
from database.category_dao import CategoryDAO

# Capa de logica de negocio
from controllers.product_controller import ProductController
from controllers.category_controller import CategoryController

# Vistas
from views.sidebar import Sidebar
from views.product.list_view import ProductListView
from views.product.create_view import ProductCreateView
from views.product.edit_view import ProductEditView
from views.category.list_view import CategoryListView
from views.category.create_view import CategoryCreateView
from views.category.edit_view import CategoryEditView


class App(tb.Window):
    """Ventana principal de la aplicacion Gestion de Productos.

    Patrón de diseño: sidebar de navegacion que cambia el contenido del area principal.
    Layout: grid con sidebar (columna 0) y area de contenido (columna 1).
    """

    def __init__(self):
        super().__init__(title="Gestion de Productos", themename="flatly")

        # Inicializar capa de datos y controladores (compartidos por todas las vistas)
        db = Database()                                         # Conexion SQLite
        product_dao = ProductDAO(db)                            # Acceso a tabla productos
        category_dao = CategoryDAO(db)                          # Acceso a tabla categorias
        self.product_controller = ProductController(product_dao, category_dao)
        self.category_controller = CategoryController(category_dao, product_dao)

        self.geometry("900x600")
        self._build_layout()
        # Mostrar la vista de listado de productos al iniciar
        self.navigate("product_list")

    def _build_layout(self):
        """Construye el layout principal: sidebar fijo a la izquierda + area de contenido."""
        # Configurar grid responsive: columna 1 (contenido) se expande
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Sidebar de navegacion con botones para cada vista
        self.sidebar = Sidebar(self, on_navigate=self.navigate)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Area de contenido principal (se reemplaza al navegar)
        self.content = tk.Frame(self, bg="#ECF0F1")
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)

    def _clear_content(self):
        """Elimina todos los widgets del area de contenido antes de cargar una nueva vista."""
        for widget in self.content.winfo_children():
            widget.destroy()

    def navigate(self, view_name, *args):
        """Metodo central de navegacion: destruye la vista actual y carga la solicitada.

        Args:
            view_name: Identificador de la vista (ej: 'product_list', 'category_create').
            *args: Argumentos adicionales (ej: product_id para vistas de edicion).
        """
        self._clear_content()

        # Mapeo de nombre de vista -> instancia de vista
        if view_name == "product_list":
            view = ProductListView(self.content, self.product_controller,
                                   self.category_controller, on_edit=self.navigate)
        elif view_name == "product_create":
            view = ProductCreateView(self.content, self.product_controller,
                                     self.category_controller, on_back=self.navigate)
        elif view_name == "product_edit":
            # args[0] contiene el product_id a editar
            view = ProductEditView(self.content, self.product_controller,
                                   self.category_controller, args[0], on_back=self.navigate)
        elif view_name == "category_list":
            view = CategoryListView(self.content, self.category_controller,
                                    on_edit=self.navigate)
        elif view_name == "category_create":
            view = CategoryCreateView(self.content, self.category_controller,
                                      on_back=self.navigate)
        elif view_name == "category_edit":
            # args[0] contiene el category_id a editar
            view = CategoryEditView(self.content, self.category_controller,
                                    args[0], on_back=self.navigate)
        else:
            return
        view.grid(row=0, column=0, sticky="nsew")


# Punto de entrada: crea la ventana y ejecuta el loop principal
if __name__ == "__main__":
    App().mainloop()
