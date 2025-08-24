FROM python:3.10-slim

# Install system dependencies including MySQL client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create templates directory and add HTML files
RUN mkdir -p templates
COPY templates/ ./templates/

EXPOSE 5000

CMD ["python", "app.py"]
