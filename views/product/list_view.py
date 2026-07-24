"""Vista del listado de productos en tabla.

Muestra todos los productos con sus datos (nombre, categoria, precio, unidades)
y permite editar o eliminar los seleccionados. Tiene boton para ir a crear.
"""

import ttkbootstrap as tb
from ttkbootstrap.constants import PRIMARY, SUCCESS, SECONDARY, WARNING, INFO, DANGER
from tkinter import messagebox


class ProductListView(tb.Frame):
    """Tabla con todos los productos registrados en el sistema.

    Args:
        parent: Widget padre (area de contenido de App).
        product_controller: Controlador de productos.
        category_controller: Controlador de categorias (para resolver nombres).
        on_edit: Callback de navegacion para ir a crear/editar.
    """

    def __init__(self, parent, product_controller, category_controller, on_edit=None):
        super().__init__(parent)
        self.product_controller = product_controller
        self.category_controller = category_controller
        self.on_edit = on_edit
        # Mapa id_categoria -> nombre para mostrar nombre en vez de id
        self._categories_map = {}
        self._build()

    def _build(self):
        """Construye la interfaz: header, barra de filtro, tabla y botones de accion."""
        # Header con titulo y boton de crear
        header = tb.Frame(self)
        header.pack(fill="x", padx=20, pady=(20, 0))
        tb.Label(header, text="Listado de Productos", font=("Arial", 20)).pack(side="left")
        tb.Button(header, text="+ Nuevo", bootstyle=SUCCESS,
                  command=self._go_create).pack(side="right")

        # Barra de filtro por categoria
        filter_frame = tb.Frame(self)
        filter_frame.pack(fill="x", padx=20, pady=(10, 0))
        tb.Label(filter_frame, text="Filtrar por Categoria:").pack(side="left", padx=(0, 5))

        # Cargar categorias para el Combobox
        self._categories = self.category_controller.list_categories()
        cat_names = ["Todas"] + [c.name for c in self._categories]
        self.filter_cat = tb.Combobox(filter_frame, values=cat_names, state="readonly", width=20)
        self.filter_cat.current(0)  # Seleccionar "Todas" por defecto
        self.filter_cat.pack(side="left", padx=(0, 5))
        tb.Button(filter_frame, text="Filtrar", bootstyle=PRIMARY,
                  command=self._apply_filter).pack(side="left", padx=(0, 5))
        tb.Button(filter_frame, text="Mostrar todos", bootstyle=SECONDARY,
                  command=self._clear_filter).pack(side="left")

        # Tabla Treeview con columnas
        columns = ("id", "name", "category", "price", "units")
        self.tree = tb.Treeview(self, columns=columns, show="headings", bootstyle=INFO)
        # Configurar encabezados y ancho de columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("category", text="Categoria")
        self.tree.heading("price", text="Precio")
        self.tree.heading("units", text="Unidades")
        self.tree.column("id", width=60)
        self.tree.column("name", width=200)
        self.tree.column("category", width=150)
        self.tree.column("price", width=100)
        self.tree.column("units", width=80)
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        # Botones de accion (editar / eliminar)
        btn_frame = tb.Frame(self)
        btn_frame.pack(pady=(0, 20))
        tb.Button(btn_frame, text="Editar", bootstyle=WARNING,
                  command=self._edit_selected).pack(side="left", padx=5)
        tb.Button(btn_frame, text="Eliminar", bootstyle=DANGER,
                  command=self._delete_selected).pack(side="left", padx=5)

        # Cargar datos iniciales
        self.refresh()

    def refresh(self, category_id=None):
        """Recarga los datos de la tabla desde la BD.

        Actualiza el mapa de categorias y vuelve a insertar los productos.
        Se llama al inicio, despues de cada eliminacion, y al filtrar.

        Args:
            category_id: Si se provee, solo muestra productos de esa categoria.
                         Si es None, muestra todos.
        """
        # Reconstruir mapa id_categoria -> nombre
        self._categories_map = {c.id: c.name for c in self.category_controller.list_categories()}
        # Limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Obtener productos (filtrados o todos)
        products = self.product_controller.list_products(category_id)
        for p in products:
            cat_name = self._categories_map.get(p.category_id, "Sin categoria")
            self.tree.insert("", "end", values=(p.id, p.name, cat_name, f"{p.price:.2f}", p.units))

    def _go_create(self):
        """Navega a la vista de crear producto."""
        if self.on_edit:
            self.on_edit("product_create")

    def _edit_selected(self):
        """Navega a la vista de editar con el producto seleccionado.

        Muestra advertencia si no hay ninguno seleccionado.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un producto para editar")
            return
        # Obtener el id del primer elemento seleccionado
        prod_id = self.tree.item(selected[0])["values"][0]
        if self.on_edit:
            self.on_edit("product_edit", prod_id)

    def _delete_selected(self):
        """Elimina el producto seleccionado previa confirmacion del usuario.

        Muestra dialogo de confirmacion antes de eliminar.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un producto para eliminar")
            return
        prod_id = self.tree.item(selected[0])["values"][0]
        prod_name = self.tree.item(selected[0])["values"][1]
        # Pedir confirmacion antes de eliminar
        confirm = messagebox.askyesno("Confirmar", f"Eliminar el producto '{prod_name}'?")
        if not confirm:
            return
        try:
            self.product_controller.delete_product(prod_id)
            # Recargar tabla manteniendo el filtro activo
            self._apply_filter()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _apply_filter(self):
        """Filtra la tabla mostrando solo los productos de la categoria seleccionada.

        Si se selecciona "Todas", muestra todos los productos.
        """
        idx = self.filter_cat.current()
        if idx == 0:
            # Opcion "Todas": mostrar todo sin filtro
            self.refresh()
        else:
            # Obtener el id de la categoria seleccionada (idx-1 porque "Todas" ocupa posicion 0)
            category_id = self._categories[idx - 1].id
            self.refresh(category_id)

    def _clear_filter(self):
        """Limpia el filtro: selecciona 'Todas' en el Combobox y recarga la tabla completa."""
        self.filter_cat.current(0)
        self.refresh()
