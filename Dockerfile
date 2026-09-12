FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file first to leverage Docker caching
COPY requirements.txt .

# Install all python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app files into the container
COPY . .

# Expose the port that FastAPI runs on
EXPOSE 8000

# Command to start the FastAPI application via uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
