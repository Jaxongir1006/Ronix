# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc tzdata netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
COPY .env .env
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Default command (boshqariladi docker-compose ichida)
CMD ["gunicorn", "Ronix.wsgi:application", "--bind", "0.0.0.0:8010"]
