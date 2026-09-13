FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Enable unbuffered logging and suppress pip root warning
ENV PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the bot
CMD ["python", "main.py"]
