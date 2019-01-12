#! /bin/bash

sitelogin=gunicorn@talktomein.com

basedir="$(dirname $(readlink -f "$0"))"

scp -r $basedir/src/py/* $sitelogin:/home/gunicorn/pyenv/app
scp $basedir/src/js/* $sitelogin:/home/gunicorn/www/js
scp $basedir/src/css/* $sitelogin:/home/gunicorn/www/css
