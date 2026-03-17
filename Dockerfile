FROM python:3.12-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

WORKDIR /app

# Dependencias del sistema (mínimas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente (sin data/ — viene del volumen)
COPY app/ ./app/
COPY run.py .
COPY manage_users.py .

# Crear directorio de datos (el volumen se monta aquí)
RUN mkdir -p /app/data

# Usuario no-root por seguridad
RUN useradd -m -u 1000 pizarra && chown -R pizarra:pizarra /app
USER pizarra

EXPOSE 8001

# Gunicorn: 2 workers, timeout generoso para SQLite
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "--workers", "2", "--timeout", "60", "--access-logfile", "-", "run:app"]
