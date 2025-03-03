# Use Python 3.13 as the base image
FROM python:3.13

# Set working directory
WORKDIR /bot

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files (including .env)
COPY . .

# Explicitly set environment variables
ENV PYTHONUNBUFFERED=1
CMD ["bash", "-c", "source .env && python bot.py"]
