#!/usr/bin/env bash
set -e
echo " ожидание"
sleep 20
echo "Запуск приложения..."
export PYTHONPATH=/opt/app/src
python src/main.py