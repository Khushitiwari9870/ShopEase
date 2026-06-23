

# ShopEase — E-Commerce Demo (Django)

A minimal, modern e-commerce reference app built with Django (backend), SQLite (data), and Bootstrap 5 (frontend). This README explains setup, development workflow, and project features so you can run and extend the app locally.

## Features

- Product catalog (name, slug, description, price, stock, image)
- Product detail pages
- Session-backed shopping cart (add/update/remove)
- Checkout that persists `Order` and `OrderItem`
- User auth: register, login, logout
- Admin interface for managing products and orders
- Sample product fixtures and media images

## Tech stack

- Python 3.11+ (project worked with 3.13 in this environment)
- Django >= 4.2
- SQLite (default development DB)
- Bootstrap 5 (CDN)

## Prerequisites

- Python 3.11+ installed
- Git (optional)

## Setup (development)

Open a terminal and run:

```bash
git clone <your-repo-url> "ShopEase - E-Commerce Application"
cd "ShopEase - E-Commerce Application"
python -m venv .venv
# Windows PowerShell
.\\.venv\\Scripts\\Activate.ps1
# or on cmd.exe
.\\.venv\\Scripts\\activate
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install Django manually:

```bash
pip install django
```

Run migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Load sample data (fixtures):

```bash
python manage.py loaddata store/fixtures/initial_products.json
```

Assign the shipped media images to products (the project includes `media/products/*.svg`):

```bash
python manage.py assign_images
```

Start the dev server:

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ to view the app.

## Media & Static files

- Development: `MEDIA_URL = '/media/'` and `MEDIA_ROOT` are set in `shopease/settings.py`. Django serves media files in DEBUG mode.
- Uploaded images are stored under `media/products/`.
- The management command `assign_images` (see `store/management/commands/assign_images.py`) attaches `media/products/<slug>.svg` to each `Product.image`.

## Admin

Visit `/admin/` and log in with the superuser created earlier to manage `Product`, `Order`, and `OrderItem` entries.

## Useful commands

- Run server: `python manage.py runserver`
- Make migrations: `python manage.py makemigrations` then `python manage.py migrate`
- Load fixtures: `python manage.py loaddata store/fixtures/initial_products.json`
- Assign product images: `python manage.py assign_images`
- Open Django shell: `python manage.py shell`

## Deployment notes

- For production: set `DEBUG=False`, configure `ALLOWED_HOSTS`, set a secure `SECRET_KEY` via env var, and serve static files via `collectstatic` and a CDN or web server.
- Configure a WSGI/ASGI server (e.g., Gunicorn + Nginx) and persist media on an object store (S3) or shared filesystem.

## Troubleshooting

- Images not showing: confirm `Product.image` has a value (in admin or via shell) and that files exist under `media/products/`.
- If using Windows and `Activate.ps1` errors, use `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` temporarily.

## Contributing / Extending

- Add new product images under `media/products/` and either update DB records or re-run `assign_images` if slugs match image names.
- To allow image uploading from the admin, the current `Product` model uses an `ImageField` — install `Pillow` if needed: `pip install Pillow`.

## Files of interest

- Project settings: `shopease/settings.py`
- Main app: `store/` (models, views, templates)
- Assign images command: `store/management/commands/assign_images.py`


---

If you'd like, I can:
- Add photographic PNG/JPEG samples and update fixtures to reference them, or
- Add a small `README` section showing how to run the app with Docker.

