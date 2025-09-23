# Use an official lightweight Python image
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (better cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy your whole project
COPY . .

# Expose port (Azure sets $PORT, but nice for local dev)
EXPOSE 8000

# Default startup command (Azure overrides PORT)
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "--bind", "0.0.0.0:${PORT:-8000}", "website.application.main:app"]