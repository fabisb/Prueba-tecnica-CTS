import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cts_turismo_backend.settings')

app = Celery('cts_turismo_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
