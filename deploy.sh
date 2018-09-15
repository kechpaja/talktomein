#! /bin/bash

sitelogin="" # TODO

basedir="$(dirname $(readlink -f "$0"))"

scp $basedir/src/py/* $sitelogin:/home/protected/env/src
scp $basedir/src/js/* $sitelogin:/home/public/js
scp $basedir/src/css/* $sitelogin:/home/public/css
