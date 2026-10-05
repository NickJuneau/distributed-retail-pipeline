FROM python:3.12-slim

# Prevent python from buffering stdout/stderr and writing .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set container working directory
WORKDIR /app

# Create a dedicated non-root user for security
RUN adduser --disabled-password --gecos "" appuser

# Copy requirments and install dependencies
COPY services/replay/requirments.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and data
COPY services/replay ./services/replay/
COPY data/ ./data/

# Grant ownership to non-root user and switch user
RUN chown -R appuser:appuser /app
USER appuser

# Set entrypoint to run the module
ENTRYPOINT [ "python", "-m", "services.replay.main" ]
CMD [ "--limit", "10", "--delay", "0.5" ]