FROM python:3.11-slim

WORKDIR /app

# System dependencies for reportlab (fonts, etc) and pandas (if needed)
RUN apt-get update && apt-get install -y \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Command to run
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
