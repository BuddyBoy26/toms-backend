# 1. Base Python image
FROM python:3.11-slim

# 2. Set work dir
WORKDIR /app

# 3. Install system deps for psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# 4. Copy & install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy app code & Alembic config
COPY app ./app
COPY alembic.ini .
COPY alembic ./alembic

# 6. Expose port & start Uvicorn
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
