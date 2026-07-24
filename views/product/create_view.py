"""Vista del formulario para crear un nuevo producto.

Presenta un formulario con campos: nombre, categoria (Combobox),
precio y unidades. La categoria se carga desde la BD.
"""

import ttkbootstrap as tb
from ttkbootstrap.constants import SUCCESS, SECONDARY
from tkinter import messagebox


class ProductCreateView(tb.Frame):
    """Formulario para agregar un producto nuevo al sistema.

    Args:
        parent: Widget padre (area de contenido de App).
        product_controller: Controlador de productos.
        category_controller: Controlador de categorias (para el Combobox).
        on_back: Callback de navegacion para volver a la lista.
    """

    def __init__(self, parent, product_controller, category_controller, on_back=None):
        super().__init__(parent)
        self.product_controller = product_controller
        self.category_controller = category_controller
        self.on_back = on_back
        self._build()

    def _build(self):
        """Construye el formulario con labels, entries y Combobox de categoria."""
        tb.Label(self, text="Crear Producto", font=("Arial", 20)).pack(pady=20)

        # Formulario con grid
        form = tb.Frame(self)
        form.pack(pady=10)
        tb.Label(form, text="Nombre").grid(row=0, column=0, padx=5, pady=5)
        tb.Label(form, text="Categoria").grid(row=1, column=0, padx=5, pady=5)
        tb.Label(form, text="Precio").grid(row=2, column=0, padx=5, pady=5)
        tb.Label(form, text="Unidades").grid(row=3, column=0, padx=5, pady=5)

        # Campo nombre
        self.name = tb.Entry(form, width=30)
        self.name.grid(row=0, column=1, padx=5, pady=5)

        # Combobox de categorias: carga nombres desde la BD
        categories = self.category_controller.list_categories()
        cat_names = [c.name for c in categories]
        self._categories = categories  # Guardar lista de objetos Category para obtener el id
        self.cat = tb.Combobox(form, values=cat_names, state="readonly", width=28)
        self.cat.grid(row=1, column=1, padx=5, pady=5)

        # Campo precio
        self.price = tb.Entry(form, width=30)
        self.price.grid(row=2, column=1, padx=5, pady=5)

        # Campo unidades
        self.units = tb.Entry(form, width=30)
        self.units.grid(row=3, column=1, padx=5, pady=5)

        # Botones de accion
        btn_frame = tb.Frame(self)
        btn_frame.pack(pady=20)
        tb.Button(btn_frame, text="Guardar", bootstyle=SUCCESS,
                  command=self._save).pack(side="left", padx=5)
        tb.Button(btn_frame, text="Volver", bootstyle=SECONDARY,
                  command=self._go_back).pack(side="left", padx=5)

    def _get_selected_category_id(self):
        """Obtiene el id de la categoria seleccionada en el Combobox.

        Returns:
            int si hay seleccion, None si no se selecciono nada.
        """
        idx = self.cat.current()
        if idx < 0:
            return None
        return self._categories[idx].id

    def _save(self):
        """Valida y guarda el producto, mostrando mensajes de error o exito."""
        try:
            category_id = self._get_selected_category_id()
            self.product_controller.add_product(
                self.name.get(), category_id, self.price.get(), self.units.get()
            )
            messagebox.showinfo("OK", "Producto guardado correctamente")
            self._go_back()
        except ValueError as e:
            # Errores de validacion del controller
            messagebox.showerror("Error de validacion", str(e))
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))

    def _go_back(self):
        """Navega de vuelta a la lista de productos."""
        if self.on_back:
            self.on_back("product_list")
