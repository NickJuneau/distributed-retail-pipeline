FROM python:3.12-slim

# Prevent Python from buffering stdout/stderr and writing .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set container working directory
WORKDIR /app

# Create a dedicated non-root user for security
RUN adduser --disabled-password --gecos "" appuser

# Copy requirments and install dependencies
COPY services/worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy worker application source code
COPY services/worker ./services/worker/

# Grant ownership to non-root user and switch user
RUN chown -R appuser:appuser /app
USER appuser

# Set entrypoint to run the worker module
ENTRYPOINT [ "python", "-m", "services.worker.main" ]