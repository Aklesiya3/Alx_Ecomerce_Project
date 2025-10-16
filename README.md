# Alx E-commerce Project (local setup)

This repo contains a Django REST API for an e-commerce app. It includes authentication using Djoser + Simple JWT.

Quick start (Windows PowerShell)

1. Create and activate a virtual environment (if not already created):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Copy environment example and set secrets:
```powershell
copy .env.example .env
# Edit .env to fill DJANGO_SECRET_KEY (for local dev, you can keep DEBUG=True)
```

4. Make migrations and migrate:
```powershell
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (optional):
```powershell
python manage.py createsuperuser
```

6. Run the development server:
```powershell
python manage.py runserver
```

Common API endpoints (base: /api/user/)
- POST /api/user/register/  - Register (body: {"email":"...","password":"..."})
- POST /api/user/token/     - Obtain JWT pair (body: {"email":"...","password":"..."})
- POST /api/user/token/refresh/ - Refresh access token (body: {"refresh":"..."})
- POST /api/user/logout/    - Logout (blacklist refresh) (body: {"refresh":"..."})
- GET /api/user/profile/    - Get current user profile (Authorization: Bearer <access>)

Notes
- Password reset emails are printed to console in development (EMAIL_BACKEND=configured to console).
- Static files are served by WhiteNoise in simple deployments; run `python manage.py collectstatic` prior to deployment.

If you want me to add Dockerfiles or a sample Gunicorn + Nginx config, tell me and I will add them.
