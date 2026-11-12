# Librería Online

> *Django e-commerce web app for a bookstore: catalog, cart, reviews, offers, chatbot and admin panel.*

Tienda web para una librería: catálogo de libros por categoría, búsqueda, carrito de compras, reseñas de clientes, ofertas y un panel de administración para gestionar el inventario.

## Funcionalidades

- **Catálogo** con portadas, categorías, paginación y búsqueda.
- **Carrito de compras**: agregar, actualizar y eliminar libros.
- **Reseñas** con calificación de 1 a 5 estrellas.
- **Ofertas**: precio de oferta por libro, gestionado desde el panel.
- **Chatbot** de atención que responde preguntas frecuentes y recomienda libros.
- **Registro e inicio de sesión** de usuarios y **panel de administración** propio (crear, editar y eliminar libros).
- Formulario de **contacto**.

## Tecnologías

Python · Django · SQLite · Pillow · HTML/CSS/JavaScript

## Cómo ejecutarlo

```bash
git clone https://github.com/JuarezRoger/Libreria.git
cd Libreria
python -m venv venv
venv\Scripts\activate            # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Luego abre http://127.0.0.1:8000/.

En producción, define la variable de entorno `DJANGO_SECRET_KEY`.

## Autor

**Roger de Jesús Juárez Mejía**: [LinkedIn](https://www.linkedin.com/in/roger-juárez-8a3370236)
