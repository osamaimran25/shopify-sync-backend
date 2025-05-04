# Shopify-Integrated Django Backend

A friendly, end-to-end starter project using Django + DRF, Celery, Redis, and PostgreSQL—built to manage products, process Shopify webhooks, and run nightly import/report tasks.

---

## 🚀 Features

- CRUD API for products: name, SKU, price, quantity, last_updated  
- Filtering & search by name, SKU, price, quantity  
- BasicAuth + group-based permissions  
- Shopify webhook endpoint (HMAC verification + inventory updates)  
- Celery task chain (CSV import → validate/update → email report)  
- Admin customizations: list filters, search, bulk-price actions  
- Docker-first for easy local setup  

---

## 🛠️ Tech Stack

- Python 3.12  
- Django & Django REST Framework  
- Celery & Redis  
- PostgreSQL  
- Docker & Docker Compose  
- pytest for testing  

---

## 📁 Project Structure

```
.
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── prod.py
│   └── wsgi.py
├── products/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── services/
│       └── product_service.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🔧 Prerequisites

- Docker ≥ 20.10  
- Docker Compose ≥ 1.29  
- A UNIX-style shell (macOS/Linux) or WSL/PowerShell on Windows  

---

## 🛠️ Getting Started

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-org/shopify-backend.git
   cd shopify-backend
   ```

2. **Copy & configure environment**  
   ```bash
   cp .env.example .env
   # - Set DJANGO_SECRET_KEY: openssl rand -hex 32
   # - Choose a strong POSTGRES_PASSWORD
   # - For dev, keep DJANGO_DEBUG=True
   ```

3. **Build & launch**  
   ```bash
   docker-compose up --build -d
   ```
   Services started:
   - db (PostgreSQL)  
   - redis (Broker & result backend)  
   - web (Django + Gunicorn)  
   - celery (Worker)  
   - celery-beat (Scheduler)  

4. **Initialize database & create superuser**  
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Browse the app**  
   - API root: http://localhost:8000/api/  
   - Admin panel: http://localhost:8000/admin/  

---

## ⚙️ Development Workflow

- **Code changes** auto-reload via volume mounts.  
- **Migrations**  
  ```bash
  docker-compose exec web python manage.py makemigrations
  docker-compose exec web python manage.py migrate
  ```
- **Run tests**  
  ```bash
  docker-compose exec web pytest
  ```
- **Shell**  
  ```bash
  docker-compose exec web python manage.py shell
  ```
- **Logs**  
  ```bash
  docker-compose logs -f web
  ```

---

## 🔑 Environment Variables

Copy `.env.example` to `.env`:

```dotenv
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=shopify_db
POSTGRES_USER=shopify_user
POSTGRES_PASSWORD=changeme
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=${REDIS_URL}
CELERY_RESULT_BACKEND=${REDIS_URL}
```

> The Postgres image auto-creates the database & user on first start, storing data in the `postgres_data` volume.

---

## 🐳 Docker Services

- **db**: postgres:15  
- **redis**: redis:7  
- **web**: Django + Gunicorn  
- **celery**: Celery worker  
- **celery-beat**: Scheduler  

Volume:

- `postgres_data` persists database between restarts.

---

## 🌐 API & Admin

- Endpoints under `/api/`  
- Shopify webhook at `/webhook/`  
- Admin filters on SKU, name, last_updated  
- Bulk-price update action

---

## ✅ Testing

Run tests:

```bash
docker-compose exec web pytest
```

---

## 🤝 Contributing

1. Fork & branch:
   ```bash
   git checkout -b feature/your-feature
   ```
2. Implement:
   - Extend serializers for validation only  
   - Update `ProductService`  
   - Wire views & URLs  
   - Write tests
3. Commit & PR:
   ```bash
   git add .
   git commit -m "Add X"
   git push origin feature/your-feature
   ```
4. Open PR & request review.

---

## 📄 License

MIT License. See LICENSE for details.

---

🎉 **Welcome!** Dive in, ask questions, and happy coding!
