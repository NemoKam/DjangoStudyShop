from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kazan_express.settings')
 
app = Celery('kazan_express')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every': { 
        'task': 'repeat_order_make_task',
        'schedule': crontab(minute=0, hour='*/1'),# по умолчанию выполняет каждую минуту, очень гибко 
    },                                                              # настраивается

}