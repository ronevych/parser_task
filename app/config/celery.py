import os
from celery import Celery

# Встановлюємо змінну оточення для налаштувань Django за замовчуванням
# Це те саме, що ми робимо в manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Створюємо екземпляр додатку
app = Celery("config")

# Завантажуємо налаштування з файлу settings.py
# namespace='CELERY' означає, що в settings.py всі змінні для Celery 
# повинні починатися з префіксу CELERY_ (напр. CELERY_BROKER_URL)
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматично знаходимо таски в папках додатків (tasks.py)
app.autodiscover_tasks()