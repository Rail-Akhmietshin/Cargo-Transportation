#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery --app=src.celery:celery_app worker --beat -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery --app=src.celery:celery_app flower
fi