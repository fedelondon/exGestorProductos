"""Vista del formulario para editar una categoria existente.

Carga el nombre actual de la categoria por id y lo muestra
pre-llenado en un formulario identical al de creacion.
"""

import ttkbootstrap as tb
from ttkbootstrap.constants import SUCCESS, SECONDARY
from tkinter import messagebox


class CategoryEditView(tb.Frame):
    """Formulario para modificar una categoria existente.

    Carga el nombre actual al construirse. Al guardar,
    valida unicidad y actualiza en la BD.

    Args:
        parent: Widget padre (area de contenido de App).
        category_controller: Controlador de categorias.
        category_id: ID de la categoria a editar.
        on_back: Callback de navegacion para volver a la lista.
    """

    def __init__(self, parent, category_controller, category_id, on_back=None):
        super().__init__(parent)
        self.category_controller = category_controller
        self.category_id = category_id
        self.on_back = on_back
        self._build()
        # Cargar datos de la categoria existente
        self._load_data()

    def _build(self):
        """Construye el formulario con campo nombre y botones de accion."""
        tb.Label(self, text="Editar Categoria", font=("Arial", 20)).pack(pady=20)

        # Formulario simple: solo nombre
        form = tb.Frame(self)
        form.pack(pady=10)
        tb.Label(form, text="Nombre").grid(row=0, column=0, padx=5, pady=5)
        self.name = tb.Entry(form, width=30)
        self.name.grid(row=0, column=1, padx=5, pady=5)

        # Botones de accion
        btn_frame = tb.Frame(self)
        btn_frame.pack(pady=20)
        tb.Button(btn_frame, text="Guardar", bootstyle=SUCCESS,
                  command=self._save).pack(side="left", padx=5)
        tb.Button(btn_frame, text="Volver", bootstyle=SECONDARY,
                  command=self._go_back).pack(side="left", padx=5)

    def _load_data(self):
        """Carga el nombre actual de la categoria en el campo del formulario."""
        category = self.category_controller.get_category(self.category_id)
        if category:
            self.name.insert(0, category.name)

    def _save(self):
        """Valida y actualiza la categoria, mostrando mensajes de error o exito."""
        try:
            self.category_controller.update_category(self.category_id, self.name.get())
            messagebox.showinfo("OK", "Categoria actualizada correctamente")
            self._go_back()
        except ValueError as e:
            # Errores de validacion: nombre vacio o duplicado
            messagebox.showerror("Error de validacion", str(e))
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))

    def _go_back(self):
        """Navega de vuelta a la lista de categorias."""
        if self.on_back:
            self.on_back("category_list")
