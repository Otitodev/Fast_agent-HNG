# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY ./app /app/app

# Expose the port (FastAPI/Uvicorn default)
EXPOSE 8000

# Command to run the application using Uvicorn (FastAPI's recommended ASGI server)
# Use a high-performance, production-ready command (Gunicorn + Uvicorn workers)
CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker", "--workers", "4"]