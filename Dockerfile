# Dockerfile
FROM python:3.12-slim

# 1. Set working directory
WORKDIR /app

# 2. Avoid Python buffering and bytecode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Install system dependencies (including libpq-dev for psycopg2)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Install Python dependencies
COPY requirements/ requirements/
RUN pip install --upgrade pip \
    && pip install -r requirements/local.txt

# 5. Copy project files
COPY . .

# 6. Collect static files
RUN python manage.py collectstatic --noinput

# 7. Default command
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
