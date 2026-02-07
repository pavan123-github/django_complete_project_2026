import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_dev.settings")

app = Celery("django_dev")

app.config_from_object("django.conf:settings", namespace="CELERY")

# 🔴 THIS LINE IS MOST IMPORTANT
app.autodiscover_tasks()

