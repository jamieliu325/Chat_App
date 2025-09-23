# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port (Azure will map it)
EXPOSE 8000

# Default startup command
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "--bind", "0.0.0.0:8000", "website.application.main:app"]