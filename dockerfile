# Use a slim, stable Python image to reduce size
FROM python:3.11-slim

# Install Tesseract OCR and its dependencies
# Use a multi-stage command to ensure the package list is up to date and clean
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libleptonica-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port for the FastAPI app
EXPOSE 8000

# Set the command to run your app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]