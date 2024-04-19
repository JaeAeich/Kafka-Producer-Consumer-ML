FROM python:3.11.8-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "app.py"]
