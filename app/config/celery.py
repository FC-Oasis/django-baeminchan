from celery import Celery

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    # Calls repr() on the argument first
    print('Request: {0!r}'.format(self.request))
