FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for PyAV and librosa
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libavfilter-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create runtime directory
RUN mkdir -p /app/runtime/sessions

# Create models directory
RUN mkdir -p /app/models

# Expose port
EXPOSE 8001

# Run the application
CMD ["gunicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "1"]
