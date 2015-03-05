#!/bin/bash
# madsack epaper grabber v2
# Download the E-Paper for HAZ (Hannoversche Allgemeine Zeitung) with an account
#
# "THE BEER-WARE LICENSE" (Revision 42):
# <hazepaper -at- robertweidlich -dot- de> wrote this file. As long as you
# retain this notice you can do whatever you want with this stuff. If we meet 
# some day, and you think this stuff is worth it, you can buy me a beer in return.

BASEDIR=$(dirname $0)

if [ ! -e $BASEDIR/venv ]; then
    echo "First run, setting up virtualenv and installing mechanize"
    virtualenv $BASEDIR/venv
    source $BASEDIR/venv/bin/activate
    pip install mechanize
    deactivate
fi

source $BASEDIR/venv/bin/activate
python $BASEDIR/madsack_epaper_grabber.py $@
