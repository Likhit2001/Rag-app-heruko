# Use official slim Python image
FROM python:3.10-slim

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy backend and frontend code
COPY backend/ backend/
COPY frontend/ frontend/
COPY final_model_partial_frezzing/ final_model_partial_frezzing/
COPY chunk_store/ chunk_store/

# Copy requirement files
COPY backend/requirements.txt backend/
COPY frontend/requirements.txt frontend/

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir -r frontend/requirements.txt

# Expose Streamlit default port (optional for local Docker)
EXPOSE 8501

# Run Streamlit only, binding to Heroku's dynamic $PORT
CMD ["streamlit", "run", "frontend/app.py", "--server.port=$PORT", "--server.address=0.0.0.0"]