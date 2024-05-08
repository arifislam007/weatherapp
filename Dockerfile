# Use the official Python image as base
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY . /app/

# Install Poetry
RUN pip install poetry

# Export dependencies to requirements.txt
RUN poetry export --format requirements.txt --output requirements.txt --without-hashes

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
#COPY app.py /app/

# Expose the port Flask is running on
EXPOSE 5000

# Command to run the application
CMD ["python", "run_app.py"]
