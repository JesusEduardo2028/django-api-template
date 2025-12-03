#!/bin/sh
set -e

DEFAULT_WORKERS=3
DEFAULT_TIMEOUT=290
DEFAULT_PORT=8000

NUMBER_OF_WORKERS="${NUMBER_OF_WORKERS:-$DEFAULT_WORKERS}"
WORKERS_TIMEOUT="${WORKERS_TIMEOUT:-$DEFAULT_TIMEOUT}"

print_worker_config() {
    echo "========================================="
    echo "Worker Configuration:"
    echo "  Number of workers: $NUMBER_OF_WORKERS"
    echo "  Workers timeout: $WORKERS_TIMEOUT"
    echo "========================================="
}

print_server_config() {
    echo "========================================="
    echo "Server Configuration:"
    echo "  Admin interface: ${ADMIN_ENABLED:-true}"
    echo "  API interface: ${API_ENABLED:-true}"
    echo "========================================="
}

wait_for_databases() {
    echo "-*-* Waiting for databases to be ready *-*-"
    wait-for-it db:5432 --timeout=30
    echo "-*-* Databases are ready *-*-"
}

run_migrations() {
    echo "========================================="
    echo "Running database migrations..."
    echo "========================================="

    echo "--> Migrating main database..."
    python manage.py migrate

    echo "========================================="
    echo "Migrations completed successfully!"
    echo "========================================="
}

start_gunicorn() {
    local use_ddtrace=$1

    echo "Starting gunicorn server..."
    print_worker_config
    print_server_config

    local gunicorn_cmd="gunicorn backend.wsgi \
        --bind 0.0.0.0:$DEFAULT_PORT \
        --chdir=/backend \
        --timeout $WORKERS_TIMEOUT \
        --workers $NUMBER_OF_WORKERS \
        -c /backend/utils/logging/gconfig.py"

    if [ "$use_ddtrace" = "true" ]; then
        echo "DataDog tracing: enabled"
        exec ddtrace-run $gunicorn_cmd
    else
        exec $gunicorn_cmd
    fi
}

start_dev_server() {
    wait_for_databases
    run_migrations

    echo "Starting Django development server..."
    print_server_config

    exec python manage.py runserver 0.0.0.0:$DEFAULT_PORT
}

case "${1:-}" in
    "") start_gunicorn false ;;
    "ddtrace-gunicorn") start_gunicorn true ;;
    "django") start_dev_server ;;
    *) exec "$@" ;;
esac