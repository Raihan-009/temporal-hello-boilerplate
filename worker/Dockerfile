# === Stage 1: Build worker image ===
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary project parts
COPY worker/worker.py ./worker.py

COPY activities ./activities
COPY workflows ./workflows

# Optional: install dotenv if you load .env in Python
# RUN pip install python-dotenv

# Run the worker
CMD ["python", "-u", "worker.py"]
