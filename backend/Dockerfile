FROM python:3.10-slim

WORKDIR /app

# Copy root requirements.txt
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ .

# app_core.py contains: app = FastAPI()
CMD ["uvicorn", "app_core:app", "--host", "0.0.0.0", "--port", "7860"]
