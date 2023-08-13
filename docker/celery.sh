#!/bin/sh

celery -A admin.tasks:app worker --loglevel=INFO
