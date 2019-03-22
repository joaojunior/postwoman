while ! pg_isready -h ${DB_HOST} -p ${DB_PORT} > /dev/null 2> /dev/null; do
    echo "Connecting to ${DB_HOST} Failed"
    sleep 1
done
coverage run --source='.' manage.py test
radon cc . -a
coverage report --omit=*test*,*migrations*,*__init__*,*settings*,*wsgi.py*,*manage.py*,postwoman/apps.py
flake8 postwoman/*
