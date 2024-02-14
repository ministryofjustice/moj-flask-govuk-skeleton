FROM python:3.11-slim

RUN useradd containeruser

WORKDIR /home/containeruser

COPY app app
COPY govuk-frontend-flask.py config.py requirements.in ./
RUN pip install -r requirements.in \
    && chown -R containeruser:containeruser ./

# Set environment variables
ENV FLASK_APP=govuk-frontend-flask.py \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER containeruser

EXPOSE 8000

CMD ["flask", "--app", "app", "run", "--debug"]