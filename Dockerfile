FROM python:3.12-slim

# Set environment variables
ENV FLASK_APP=govuk-frontend-flask.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nodejs \
        npm \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python dependencies file to the working directory
COPY requirements_dev.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_dev.txt

# Copy the project code into the working directory
COPY . .

# Install Node.js dependencies
#RUN npm install

# Build static assets
#RUN npm run build

# Expose the Flask port
EXPOSE 8000

# Run the Flask application
CMD ["flask", "run"]