#!/bin/sh

celery -A admin.tasks:app beat
