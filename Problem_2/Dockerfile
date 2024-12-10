# Base image with Python
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code and requirements
COPY generate_sample_data.py /app/
COPY anonymization_script.py /app/
COPY requirements.txt /app/

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Default entrypoint for running scripts
ENTRYPOINT ["python"]
