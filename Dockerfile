# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source tree
COPY . .

# Expose the default Flask port
EXPOSE 8000

# Environment variable defaults (can be overridden at run‑time)
ENV VERTX_DEBUG=False
ENV VERTX_COOKIE_SECURE=False

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]