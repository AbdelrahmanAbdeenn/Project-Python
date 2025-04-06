#!/usr/bin/env bash

set -e

BIN_ROOT=$(dirname $0)

echo "Waiting for PostgreSQL to be ready..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done

echo "PostgreSQL is up - running Alembic and starting server..."


alembic upgrade head

uvicorn --reload --workers 1 --host 0.0.0.0 --port 8000 main:app