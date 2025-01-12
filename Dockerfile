# Use a slim Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY etf_recommendation.py ./ 

# Expose the application port
EXPOSE 6001

# Update Gunicorn command to point to etf_recommendation.py
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT:-6001} etf_recommendation:app"]