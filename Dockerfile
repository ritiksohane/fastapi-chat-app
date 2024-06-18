# Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app
COPY ./static /app/static
COPY ./templates /app/templates
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
