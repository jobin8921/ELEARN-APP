<<<<<<< HEAD
web: gunicorn elearning.wsgi
release: python manage.py migrate
=======
web: bash -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn elearning.wsgi"

>>>>>>> afe7b5f8921fb0ee8a3d1fb75ecc438819a504c5
