# === Stage 1: Build layer with dependencies ===
FROM python:3.12-slim

WORKDIR /app

COPY worker/requirements.txt .

# Install Python deps into a virtual environment-like folder
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY worker/worker.py ./worker.py
COPY app ./app
COPY worker/.env /app/.env

CMD ["python", "-u", "worker.py"]
