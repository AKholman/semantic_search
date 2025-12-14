
# Dockerfile (in the backend/ directory)
FROM python:3.10-slim

WORKDIR /app

# Copy the requirements file from the root of the build context
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code from the backend subdirectory of the build context
COPY backend/ .

EXPOSE 8000
CMD ["uvicorn", "app_core:app", "--host", "0.0.0.0", "--port", "8000"]