# Dockerfile (in the backend/ directory)
FROM python:3.10-slim

WORKDIR /app

# Copy the requirements file from the root of the build context
# (Assuming requirements.txt is in the root of the Space clone)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# --- FIX: Changed 'COPY backend/ .' to 'COPY . .' ---
# Copy the code and necessary files (Dockerfile, app_core.py, embeddings/) 
# from the root of the build context into the WORKDIR.
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app_core:app", "--host", "0.0.0.0", "--port", "8000"]