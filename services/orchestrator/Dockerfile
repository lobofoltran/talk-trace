FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create runtime directory
RUN mkdir -p /app/runtime/sessions

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
