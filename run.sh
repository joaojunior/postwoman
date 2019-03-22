while ! pg_isready -h ${DB_HOST} -p ${DB_PORT} > /dev/null 2> /dev/null; do
    echo "Connecting to ${DB_HOST} Failed"
    sleep 1
done
python manage.py migrate
python manage.py collectstatic -c
python manage.py loaddata -v 3 data.json
gunicorn --workers=2 --pythonpath code/ postwoman_project.wsgi --log-file - -b 0.0.0.0
