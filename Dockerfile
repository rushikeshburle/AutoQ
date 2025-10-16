# Multi-stage Docker build for AutoQ

# Backend Stage
FROM python:3.11-slim as backend

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy backend code
COPY backend/ .

# Expose port
EXPOSE 8000

# Run backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
