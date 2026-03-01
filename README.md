# E-Commerce API

This repository contains a **Django-based e‑commerce backend** built as a RESTful API. It implements user authentication, shopping cart, inventory management, order processing, wallet operations, notifications, and an admin dashboard. The project is configured for containerized development and uses Celery for asynchronous tasks.

---

## 🔧 Key Technologies

- **Python 3.12** / Django 6.0
- Django REST Framework with JWT authentication
- Celery workers + Redis broker for background tasks
- PostgreSQL as the primary database
- Stripe integration for payment processing
- `drf-spectacular` for OpenAPI docs
- Docker & docker-compose for reproducible environments
- Jazzmin theme for the Django admin

---

## ⚙️ Project Structure

```
config/          # Django settings, urls, ASGI/WSGI
users/           # Custom user models, auth, tasks
inventory/       # Products, categories, images, ratings
cart/            # Shopping cart and related services
order/           # Order models, views, serializers
wallet/          # Customer wallet & Stripe webhook handling
notifications/   # In-app notifications and cleanup tasks
dashboard/       # Admin dashboard components
services/        # Shared services (email, stripe, etc.)

templates/       # HTML templates used by emails & admin
manage.py        # Django management utility
requirements.txt # Python dependencies
Dockerfile, docker-compose.yml # Container setup
```

Each app follows Django conventions with models, serializers, views, urls, and tests.

---

## 🚀 Development Setup

1. **Clone repo**

   ```bash
   git clone <URL> e-commerce-api
   cd e-commerce-api
   ```

2. **Create environment** (optional when using Docker)

   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. **Copy `.env.example` to `.env`** and populate:

   ```env
   SECRET_KEY=your-secret
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=db
   DB_PORT=5432
   REDIS=redis://redis:6379/0
   FRONTEND_DOMAIN=http://localhost:3000
   STRIPE_SECRET_KEY=...
   STRIPE_PUBLISHABLE_KEY=...
   STRIPE_WEBHOOK_SECRET=...
   ```

4. **Run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

   Services launched:
   - `web` Django/Gunicorn app
   - `celery` worker
   - `redis` broker/cache
   - `db` PostgreSQL
   - `nginx` reverse proxy (ports 80)
   - `stripe` CLI forwarding webhooks

5. **Run migrations & collectstatic** (handled by entrypoint script)

6. **Access the API** at `http://localhost/` and admin at `/admin/`.

7. **Create a superuser**:

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

8. **API documentation** available at `/api/schema/` (OpenAPI JSON) and `/api/schema/swagger-ui/`.


---

## 🧪 Running Tests

Inside the container or virtualenv:

```bash
python manage.py test
```

Tests are located under each app’s `tests/` package.

---

## 📦 Deployment

This project is configured for production using the `config.settings.prod` settings module.
You should run migrations, collectstatic, and use a production WSGI/ASGI server (Gunicorn is used by default).
Ensure environment variables are set appropriately and static/media volumes are persisted.

Use `docker-compose -f docker-compose.prod.yml` (not included) or your own orchestration.

---



