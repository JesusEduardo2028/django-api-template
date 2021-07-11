#!/bin/sh
echo "-*-* Wait For DB .. *-*-"
python3 manage.py wait_for_db
echo "-*-* Finish Waiting for db *-*-"

echo "-*-* Running migrations.. *-*-"
python manage.py migrate
echo "-*-* Finish applying migrations *-*-"

python manage.py runserver 0.0.0.0:8000
exec "$@"