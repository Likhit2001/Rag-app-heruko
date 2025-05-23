FROM python:3.10-slim

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY backend/ backend/
COPY frontend/ frontend/

COPY final_model_partial_frezzing/ final_model_partial_frezzing/
COPY chunk_store/ chunk_store/

COPY backend/requirements.txt backend/
COPY frontend/requirements.txt frontend/

RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir -r frontend/requirements.txt

WORKDIR /app

EXPOSE 8000
EXPOSE 8501

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port $PORT & streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0"]