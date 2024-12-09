# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required dependencies (if any)
RUN pip install --no-cache-dir --upgrade pip

# Define the command to run your script
CMD ["python", "/app/fixed_width_parser.py"]
