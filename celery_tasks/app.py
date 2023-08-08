import sys
from pathlib import Path

from celery import Celery
from woniu.libs.yuntongxun.sms import CCP
# BASE_DIR = Path(__file__).resolve().parent.parent
# sys.path.append(BASE_DIR)
# celery -A  celery_tasks.app worker -l info

app = Celery('woniu')

app.config_from_object('celery_tasks.celery_config')

app.autodiscover_tasks(['celery_tasks.sms'])