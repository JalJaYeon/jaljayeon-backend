python3 manage.py migrate;\
gunicorn jaljayeon_backend.wsgi:application --bind 0.0.0.0:8000