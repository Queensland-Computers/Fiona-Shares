#!/bin/bash
PKGS=/home/site/wwwroot/.python_packages/lib/site-packages
if [ ! -d "$PKGS/yfinance" ]; then
    echo "Installing Python packages..."
    pip install -r /home/site/wwwroot/requirements.txt --target "$PKGS" --quiet
fi
export PYTHONPATH="$PKGS:$PYTHONPATH"
exec gunicorn --bind=0.0.0.0 --timeout 600 app:app
