############################################################
# Dockerfile to build Flask App
############################################################

FROM python:3.12

# Install system build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Fix Python packaging issues before installing anything
RUN pip install --upgrade pip && \
    pip install watchdog && \
    pip install setuptools>=69.5.1 setuptools_scm wheel

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user with UID 1000 (optional but helpful on shared volumes)
RUN adduser --uid 1000 --disabled-password --gecos "" flaskuser

# Set working directory
WORKDIR /app

# Copy dependencies separately for better cache
COPY requirements.txt /tmp/requirements.txt
COPY wsgi.py /app/wsgi.py

RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy app code and set correct ownership
COPY --chown=flaskuser:flaskuser . /app

# Switch to non-root user
USER flaskuser

# Expose port for Gunicorn
EXPOSE 5000

# Start the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
