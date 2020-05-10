#!/bin/sh
echo "-*-* Wait For DB *-*-"
python3 /app/manage.py wait_for_db
echo "-*-* Finish Waiting for db *-*-"
echo "-*-* Finish Waiting for db *-*-"
echo "-*-* Finish Waiting for db *-*-"
echo "-*-* Finish Waiting for db *-*-"
echo "-*-* Finish Waiting for db *-*-"
exec "$@"