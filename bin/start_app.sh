#!/usr/bin/env bash

set -e

flask db upgrade

WORKER_CLASS="${WORKER_CLASS:-'gthread'}"
WORKERS="${WORKERS:-1}"
CONNECTIONS="${CONNECTIONS:-1}"

echo "worker-class: $WORKER_CLASS, workers: $WORKERS, connections: $CONNECTIONS"
gunicorn --bind 0.0.0.0:5000 \
        --workers $WORKERS \
        --threads $CONNECTIONS \
        app:app