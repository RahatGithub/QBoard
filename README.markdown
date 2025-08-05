# QBoard Dashboard Data Generator API

A RESTful API for generating and serving realistic dashboard data (employees, users, orders, products, leaderboards, etc.) for frontend projects, prototyping, and testing. It includes authentication, filtering, analytics, customizable data generation, and more.

## 🚀 Features

- **CRUD Operations**: Manage Users, Employees, Products, and Orders.
- **Random Data Generation**: Generate realistic data on-demand using Faker.
- **Filtering, Searching, Pagination**: Available on all list endpoints.
- **JWT Authentication**: Secure endpoints with `djangorestframework-simplejwt`.
- **Role-based Access Control**: Supports admin, manager, and user roles.
- **Dashboard Analytics Endpoints**: Provides summary, charts, and activity data.
- **Bulk Create**: Efficiently create multiple Products and Orders.
- **Stock Management**: Implements business rules for inventory.
- **Order with Multiple Products**: Supports `OrderItem` model.
- **Swagger/OpenAPI Docs**: Optional API documentation.
- **CORS Support**: Enables seamless frontend integration.
- **Docker & CI/CD Ready**: Optional setup for containerization and deployment.

## 🛠️ Tech Stack

- Python 3.10+
- Django 4+
- Django REST Framework
- `djangorestframework-simplejwt`
- `django-cors-headers`
- Faker
- PostgreSQL (recommended) or SQLite (for demo)
- Docker (optional)

## ⚡ Quick Start

### 1. Clone & Setup

Clone the repository and set up the virtual environment:

```bash
git clone https://github.com/yourusername/qboard-dashboard-api.git
cd qboard-dashboard-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Database

The project uses **SQLite** by default. To use **PostgreSQL**, update the `DATABASES` setting in `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Run Migrations

Apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

Create an admin user for the Django admin panel:

```bash
python manage.py createsuperuser
```

### 5. Run the Development Server

Start the local development server:

```bash
python manage.py runserver
```

Access the API at `http://localhost:8000`.

## 📦 Deployment on Render

1. **Procfile**: Ensure a `Procfile` exists in the root with:
   ```
   web: gunicorn qboard_dashboard_api.wsgi:application
   ```
2. **Requirements**: Include dependencies in `requirements.txt` (e.g., `django`, `djangorestframework`, `djangorestframework-simplejwt`, `django-cors-headers`, `faker`, `gunicorn`, `psycopg2-binary` for PostgreSQL).
3. **GitHub Integration**: Connect your repository to Render via GitHub.
4. **Create Web Service**:
   - Select your repository and branch (e.g., `main`).
   - Configure:
     - Environment: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn qboard_dashboard_api.wsgi:application`
   - Add environment variables (e.g., `DJANGO_SECRET_KEY`, `DATABASE_URL` for PostgreSQL).
5. **Static Files**: For production, configure static files:
   - Set `DEBUG=False` in `config/settings.py`.
   - Add `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')` in `settings.py`.
   - Run `python manage.py collectstatic` locally or include in the build command.
6. Deploy and monitor logs on Render.

## 🔧 Additional Configuration

- **CORS**: Ensure `django-cors-headers` is configured in `settings.py` for frontend access:
  ```python
  CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'https://your-frontend-domain.com']
  ```
- **JWT**: Configure `REST_FRAMEWORK` in `settings.py` for JWT authentication:
  ```python
  REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': [
          'rest_framework_simplejwt.authentication.JWTAuthentication',
      ]
  }
  ```
- **Swagger Docs**: If using `drf-yasg`, access API docs at `/swagger/` or `/redoc/`.