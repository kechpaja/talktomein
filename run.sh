#! /bin/bash

source bin/activate
exec gunicorn -b 0.0.0.0:5000 site:app --reload
