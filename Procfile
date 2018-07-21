web: gunicorn assessment.wsgi --log-file -
worker: celery -A assessment worker --loglevel=info