# Gestion de Productos

Aplicacion de escritorio para gestionar productos y categorias, construida con Python y ttkbootstrap siguiendo el patron MVC (Modelo-Vista-Controlador).

## Caracteristicas

- **CRUD de Productos**: crear, listar, editar y eliminar productos.
- **CRUD de Categorias**: crear, listar, editar y eliminar categorias.
- **Filtrado**: filtrar productos por categoria desde el listado.
- **Combobox de categorias**: seleccionar categoria desde base de datos (no texto libre).
- **Proteccion de eliminacion**: no se puede eliminar una categoria que tenga productos asociados.
- **Validaciones**: nombre obligatorio, precio numerico, unidades enteras, unicidad de categorias.

## Requisitos

- Python 3.14 o superior
- ttkbootstrap >= 2.0.0

## Instalacion

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd exGestorProductos

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecucion

```bash
python app.py
```

La base de datos `products.db` se crea automaticamente al ejecutar por primera vez.

## Estructura del proyecto

```
exGestorProductos/
├── app.py                          # Punto de entrada y ventana principal
├── models/
│   ├── product.py                  # Modelo Product (id, name, category_id, price, units)
│   └── category.py                 # Modelo Category (id, name)
├── controllers/
│   ├── product_controller.py       # Logica de negocio y validaciones de productos
│   └── category_controller.py      # Logica de negocio y validaciones de categorias
├── database/
│   ├── db.py                       # Conexion SQLite y creacion de tablas
│   ├── product_dao.py              # Acceso a datos de productos (CRUD)
│   └── category_dao.py             # Acceso a datos de categorias (CRUD)
├── views/
│   ├── sidebar.py                  # Barra lateral de navegacion
│   ├── product/
│   │   ├── list_view.py            # Listado de productos con filtro
│   │   ├── create_view.py          # Formulario de creacion
│   │   └── edit_view.py            # Formulario de edicion
│   └── category/
│       ├── list_view.py            # Listado de categorias
│       ├── create_view.py          # Formulario de creacion
│       └── edit_view.py            # Formulario de edicion
├── requirements.txt
└── .gitignore
```

## Arquitectura MVC

```
┌─────────────────────────────────────┐
│            VISTAS (views/)          │
│  Formularios y tablas ttkbootstrap  │
└──────────────┬──────────────────────┘
               │ llama a
               ▼
┌─────────────────────────────────────┐
│        CONTROLADORES (controllers/) │
│  Validacion de datos y orquestacion │
└──────────────┬──────────────────────┘
               │ delega en
               ▼
┌─────────────────────────────────────┐
│     ACCESO A DATOS (database/)      │
│  Queries SQL via sqlite3            │
└──────────────┬──────────────────────┘
               │ mapea a
               ▼
┌─────────────────────────────────────┐
│          MODELOS (models/)          │
│  Dataclasses: Product, Category     │
└─────────────────────────────────────┘
```

## Base de datos

Se utiliza SQLite con el archivo `products.db` (generado automaticamente). Esquema:

```sql
CREATE TABLE categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    price       REAL NOT NULL,
    units       INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```
