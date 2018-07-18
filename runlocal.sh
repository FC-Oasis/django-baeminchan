#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=config.settings.local
python app/manage.py runserver
