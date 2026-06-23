
ShopEase - Minimal Django E-Commerce

Setup and run (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Notes:
- Media uploads require Pillow (included in `requirements.txt`).
- In development, media files are served by Django when `DEBUG=True`.
- Create products in the admin or via Django shell. Product images can be uploaded via admin.

# ShopEase
 
