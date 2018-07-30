#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=config.settings.production
python app/manage.py runserver
