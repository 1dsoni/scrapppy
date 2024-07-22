#!/usr/bin/env bash

gunicorn --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker \
         --backlog 0 \
         --timeout 120 \
         --graceful-timeout 30 \
         --workers 4 \
         --worker-connections 256 \
         --max-requests 100000 \
         --max-requests-jitter 100 \
         main:app