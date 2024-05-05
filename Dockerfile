FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY main.py /app/

# Create a directory to persist data
RUN mkdir /data

# Command to run the script
CMD ["python", "main.py"]
