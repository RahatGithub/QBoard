# QBoard Dashboard Data Generator API

A RESTful API for generating and serving realistic dashboard data (employees, users, orders, products, leaderboards, etc.) for frontend projects, prototyping, and testing.

Includes authentication, filtering, analytics, customizable data generation, and more.

---

## 🚀 Features

- **CRUD Operations** for Users, Employees, Products, Orders  
- **Random Data Generation** (on-demand, with Faker)  
- **Filtering, Searching, Pagination** on all list endpoints  
- **JWT Authentication** (`djangorestframework-simplejwt`)  
- **Role-based Access Control** (admin, manager, user)  
- **Dashboard Analytics Endpoints** (summary, charts, activity)  
- **Bulk Create** for Products and Orders  
- **Stock Management** with business rules  
- **Order with Multiple Products** (`OrderItem` model)  
- **Swagger/OpenAPI Docs** (optional)  
- **CORS Support** for frontend integration  
- **Ready for Docker & CI/CD** (optional)  

---

## 🛠️ Tech Stack

- Python 3.10+  
- Django 4+  
- Django REST Framework  
- `djangorestframework-simplejwt`  
- `django-cors-headers`  
- Faker  
- PostgreSQL or SQLite (for demo)  
- Docker (optional)  

---

## ⚡ Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/qboard-dashboard-api.git
cd qboard-dashboard-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

### 2. Configure Database

By default, the project uses **SQLite**.  
To use **PostgreSQL**, update the `DATABASES` setting in `config/settings.py`.

---

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate

### 4. Create Superuser

```bash
python manage.py createsuperuser

### 5. Create Superuser

```bash
python manage.py runserver
