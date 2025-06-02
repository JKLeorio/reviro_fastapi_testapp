#!/usr/bin/env bash


set -e

echo "Running database migrations..."
uv run alembic upgrade head

echo "Running tests..."

uv run pytest tests/

echo "Starting application..."
uv run main.py