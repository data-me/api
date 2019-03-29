release: sh -c 'cd mysite && python manage.py migrate'
web: sh -c 'cd mysite && gunicorn decide.wsgi --log-file -'