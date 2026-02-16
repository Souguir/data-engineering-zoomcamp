FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir google-cloud-storage==2.10.0

# Copy the script
COPY load_yellow_taxi_data.py .

# Credentials are mounted at runtime via docker-compose (do not copy at build)

# Run the script
CMD ["python", "load_yellow_taxi_data.py"]
