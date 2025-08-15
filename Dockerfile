# ResumeRefiner Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    texlive-full \
    poppler-utils \
    ghostscript \
    imagemagick \
    curl \
    wget \
    git \
    build-essential \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    libssl-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
COPY backend/requirements.txt backend/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the application
COPY . .

# Install frontend dependencies
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Switch back to app directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/backend/uploads /app/backend/temp

# Set environment variables
ENV PYTHONPATH=/app/backend
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/resume/health || exit 1

# Run the application
CMD ["python", "backend/src/main.py"]

