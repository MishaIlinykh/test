#!/usr/bin/env bash
set -e

echo "Запуск приложения..."
export PYTHONPATH=/opt/app/src
python src/etl.py