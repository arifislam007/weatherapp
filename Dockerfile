# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECURE_WEATHER_API_KEY weather-883d37bb24536f00b4r

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only the dependencies definition file to the working directory
COPY pyproject.toml poetry.lock /app/

# Install project dependencies
RUN poetry install --no-dev

# Copy the rest of the application code to the working directory
COPY . /app

# Expose port 80 to the outside world
EXPOSE 80

# Define the command to run your Flask application
CMD ["poetry", "run", "python", "app.py"]
