FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production \
    PORT=5000

# Create non-root user
RUN adduser --disabled-password --gecos '' ctf-user && \
    chown -R ctf-user:ctf-user /app

USER ctf-user

# Run migrations and start the application
CMD flask db upgrade && \
    gunicorn --bind 0.0.0.0:$PORT run:app