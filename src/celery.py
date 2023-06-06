from celery import Celery
from celery.schedules import crontab
from datetime import timedelta


celery_app = Celery('tasks')

celery_app.config_from_object('src.config')

celery_app.conf.beat_schedule = {
   'update-location-cars': {
       'task': 'src.transportation.tasks.start_func',
       'schedule': timedelta(minutes=3),
   },
}
