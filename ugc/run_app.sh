#!/usr/bin/env bash
set -e

echo "Запуск приложения..."
export PYTHONPATH=/opt/app/src
gunicorn src.main:app --bind 0.0.0.0:9001 --workers 4
