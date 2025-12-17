# Dockerfile (in the backend/ directory)
FROM python:3.10-slim

WORKDIR /app

# --- FIX: Changed path to . to copy from the build context root ---
# Since deploy-backend-debug.yml copies backend/ contents to the Space root,
# requirements.txt is now also at the Space root.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------------

COPY . .

EXPOSE 8000
# FIX: Removed the invalid '--timeout 120' flag. 
# The lifespan manager in app_core.py handles the startup time.
CMD ["uvicorn", "app_core:app", "--host", "0.0.0.0", "--port", "8000"]
