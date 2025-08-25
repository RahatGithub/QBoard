# QBoard Dashboard Data Generator API

A RESTful API for generating and serving realistic dashboard data (employees, users, orders, products, leaderboards, etc.) for frontend projects, prototyping, and testing.

![QBoard Cover](static/img/Qboard.png)

## 🚀 Features

- CRUD Operations: Manage Users, Employees, Products, and Orders.
- Random Data Generation: Generate realistic data using Faker.
- Filtering, Searching, Pagination: Available on all list endpoints.
- JWT Authentication: Secure endpoints with `djangorestframework-simplejwt`.
- Role-based Access Control: Supports admin, manager, and user roles.
- Dashboard Analytics Endpoints: Provides summary, charts, and activity data.
- Bulk Create: Efficiently create multiple Products and Orders.
- Stock Management: Implements business rules for inventory.
- Order with Multiple Products: Supports `OrderItem` model.
- Swagger/OpenAPI Docs: Optional API documentation.
- CORS Support: Enables seamless frontend integration.
- Docker & CI/CD Ready: Optional setup for containerization and deployment.

## 🛠️ Tech Stack

- Python 3.10+
- Django 4+
- Django REST Framework
- `djangorestframework-simplejwt`
- `django-cors-headers`
- Faker
- PostgreSQL (recommended) or SQLite (for demo)
- Docker (optional)

## 🚦 How to Use This API in Your Frontend

### 1. Base URL

All endpoints are available at:

```
https://qboard.onrender.com/api/v1/
```

### 2. Authentication

- **Register**:
  - `POST /api/v1/auth/register/`
  - Send: `{ "username": "...", "email": "...", "password": "...", "role": "user" }`

- **Login**:
  - `POST /api/v1/auth/login/`
  - Send: `{ "username": "...", "password": "..." }`
  - Returns: `access` and `refresh` tokens.

- **Use Access Token**:
  - Add header to API calls: `Authorization: Bearer <access_token>`

- **Refresh Tokens**:
  - When access token expires, use: `POST /api/v1/auth/refresh/`
  - Send: `{ "refresh": "<refresh_token>" }`
  - Returns: New access token.

### 3. Making Requests

Example with `fetch` in JavaScript:

```javascript
fetch('https://qboard.onrender.com/api/v1/products/', {
  headers: {
    'Authorization': 'Bearer <access_token>',
    'Content-Type': 'application/json'
  }
})
.then(res => res.json())
.then(data => console.log(data));
```

For `POST`/`PUT` requests:
- Set `Content-Type: application/json` and send data as JSON.

### 4. CORS

CORS is enabled, allowing API calls from any frontend domain.

### 5. API Endpoints

Refer to API documentation (e.g., `/swagger/`) for all available endpoints.

### 6. Error Handling

- **401 Error**: Token expired; refresh it or log in again.
- **403 Error**: Insufficient permissions for the action.

## 🔧 Additional Configuration

- **CORS**: Configured in `settings.py`:
  ```python
  CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'https://your-frontend-domain.com']
  ```
- **JWT**: Configured in `settings.py`:
  ```python
  REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': [
          'rest_framework_simplejwt.authentication.JWTAuthentication',
      ]
  }
  ```
- **Swagger Docs**: Access at `/swagger/` or `/redoc/` if using `drf-yasg`.
