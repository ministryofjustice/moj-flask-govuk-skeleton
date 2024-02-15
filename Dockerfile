FROM python:3.11-slim

# Set environment variables
ENV FLASK_APP=govuk-frontend-flask.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /usr/src/app

# Create a non-root user
RUN adduser --disabled-password --gecos '' containeruser
# Change ownership of the working directory to the non-root user
RUN chown -R containeruser:containeruser /usr/src/app

# Copy the dependencies file to the working directory
COPY govuk-frontend-flask.py config.py requirements.in build.sh ./

# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.in

# Make the shell script executable
RUN chmod +x build.sh

# Run build shell to create assets for project
RUN ./build.sh

# Copy the project code into the working directory
COPY . .

# Give user permission to the following:
RUN chown -R containeruser:containeruser /usr/src/app/app/static/.webassets-cache/

# Switch to the non-root user
USER containeruser

# Expose the Flask port
EXPOSE 8000

# Run the Flask application for development
CMD ["flask", "run", "--cert=adhoc"]