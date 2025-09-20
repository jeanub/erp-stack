FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Paquetes nativos para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Instala dependencias primero para cache eficiente
COPY backend/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copia TODO el backend (manage.py, config/, apps/, etc.)
# En dev, /app/apps será sobrescrito por el volumen
COPY backend/ /app/

# Por defecto no exponemos ni corremos nada; lo setea compose (dev/prod)
