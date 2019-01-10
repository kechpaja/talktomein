#! /bin/bash

source bin/activate
exec gunicorn --bind unix:gunicorn.sock app:app --reload --pid gunicorn.pid &
