#!/bin/bash

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Waiting for postgres..."
  sleep 1;
done

echo "PostgreSQL started"


alembic upgrade head
echo "Database created"

echo "Uploading data to the database..."
python loading_default_data/upload_data.py
echo "The data has been successfully uploaded to the database"

gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
