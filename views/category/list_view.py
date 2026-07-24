"""Vista del listado de categorias en tabla.

Muestra todas las categorias registradas y permite
editar o eliminar las seleccionadas. Tiene boton para ir a crear.
"""

import ttkbootstrap as tb
from ttkbootstrap.constants import SUCCESS, WARNING, INFO, DANGER
from tkinter import messagebox


class CategoryListView(tb.Frame):
    """Tabla con todas las categorias registradas en el sistema.

    Args:
        parent: Widget padre (area de contenido de App).
        category_controller: Controlador de categorias.
        on_edit: Callback de navegacion para ir a crear/editar.
    """

    def __init__(self, parent, category_controller, on_edit=None):
        super().__init__(parent)
        self.category_controller = category_controller
        self.on_edit = on_edit
        self._build()

    def _build(self):
        """Construye la interfaz: header, tabla y botones de accion."""
        # Header con titulo y boton de crear
        header = tb.Frame(self)
        header.pack(fill="x", padx=20, pady=(20, 0))
        tb.Label(header, text="Listado de Categorias", font=("Arial", 20)).pack(side="left")
        tb.Button(header, text="+ Nueva", bootstyle=SUCCESS,
                  command=self._go_create).pack(side="right")

        # Tabla Treeview con columnas
        columns = ("id", "name")
        self.tree = tb.Treeview(self, columns=columns, show="headings", bootstyle=INFO)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Nombre")
        self.tree.column("id", width=80)
        self.tree.column("name", width=300)
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

    def refresh(self):
        """Recarga los datos de la tabla desde la BD.

        Se llama al inicio y despues de cada eliminacion.
        """
        # Limpiar tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Insertar categorias
        categories = self.category_controller.list_categories()
        for c in categories:
            self.tree.insert("", "end", values=(c.id, c.name))

    def _go_create(self):
        """Navega a la vista de crear categoria."""
        if self.on_edit:
            self.on_edit("category_create")

    def _edit_selected(self):
        """Navega a la vista de editar con la categoria seleccionada.

        Muestra advertencia si no hay ninguna seleccionada.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona una categoria para editar")
            return
        cat_id = self.tree.item(selected[0])["values"][0]
        if self.on_edit:
            self.on_edit("category_edit", cat_id)

    def _delete_selected(self):
        """Elimina la categoria seleccionada previa confirmacion.

        Si la categoria tiene productos asociados, el controller
        retorna False y se muestra un error al usuario.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona una categoria para eliminar")
            return
        cat_id = self.tree.item(selected[0])["values"][0]
        cat_name = self.tree.item(selected[0])["values"][1]
        # Pedir confirmacion antes de eliminar
        confirm = messagebox.askyesno("Confirmar", f"Eliminar la categoria '{cat_name}'?")
        if not confirm:
            return
        try:
            deleted = self.category_controller.delete_category(cat_id)
            if not deleted:
                # No se pudo eliminar: tiene productos asociados
                messagebox.showerror("Error", "No se puede eliminar: hay productos asociados a esta categoria")
                return
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))
