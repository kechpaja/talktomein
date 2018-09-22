#! /bin/bash

sitelogin=kechpaja_talktomein@ssh.phx.nearlyfreespeech.net

basedir="$(dirname $(readlink -f "$0"))"

scp -r $basedir/src/py/* $sitelogin:/home/protected/pyenv/app
scp $basedir/src/js/* $sitelogin:/home/public/js
scp $basedir/src/css/* $sitelogin:/home/public/css
