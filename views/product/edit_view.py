"""Vista del formulario para editar un producto existente.

Carga los datos del producto por id y los muestra pre-llenados
en un formulario identical al de creacion, con Combobox de categoria.
"""

import ttkbootstrap as tb
from ttkbootstrap.constants import SUCCESS, SECONDARY
from tkinter import messagebox


class ProductEditView(tb.Frame):
    """Formulario para modificar un producto existente.

    Carga los datos actuales del producto al construirse.
    Al guardar, valida y actualiza en la BD.

    Args:
        parent: Widget padre (area de contenido de App).
        product_controller: Controlador de productos.
        category_controller: Controlador de categorias (para el Combobox).
        product_id: ID del producto a editar.
        on_back: Callback de navegacion para volver a la lista.
    """

    def __init__(self, parent, product_controller, category_controller, product_id, on_back=None):
        super().__init__(parent)
        self.product_controller = product_controller
        self.category_controller = category_controller
        self.product_id = product_id
        self.on_back = on_back
        self._build()
        # Cargar datos del producto existente en los campos
        self._load_data()

    def _build(self):
        """Construye el formulario con labels, entries y Combobox de categoria."""
        tb.Label(self, text="Editar Producto", font=("Arial", 20)).pack(pady=20)

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

        # Combobox de categorias
        categories = self.category_controller.list_categories()
        cat_names = [c.name for c in categories]
        self._categories = categories
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

    def _load_data(self):
        """Carga los datos del producto existente en los campos del formulario.

        Si el producto no existe, muestra error y vuelve a la lista.
        """
        product = self.product_controller.get_product(self.product_id)
        if not product:
            messagebox.showerror("Error", "Producto no encontrado")
            self._go_back()
            return
        # Pre-llenar campos con los valores actuales
        self.name.insert(0, product.name)
        self.price.insert(0, str(product.price))
        self.units.insert(0, str(product.units))
        # Seleccionar la categoria actual en el Combobox
        for i, cat in enumerate(self._categories):
            if cat.id == product.category_id:
                self.cat.current(i)
                break

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
        """Valida y actualiza el producto, mostrando mensajes de error o exito."""
        try:
            category_id = self._get_selected_category_id()
            self.product_controller.update_product(
                self.product_id, self.name.get(), category_id,
                self.price.get(), self.units.get()
            )
            messagebox.showinfo("OK", "Producto actualizado correctamente")
            self._go_back()
        except ValueError as e:
            messagebox.showerror("Error de validacion", str(e))
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))

    def _go_back(self):
        """Navega de vuelta a la lista de productos."""
        if self.on_back:
            self.on_back("product_list")
