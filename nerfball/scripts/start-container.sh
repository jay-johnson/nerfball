#!/bin/bash

echo ""
date

cd /opt/nerfball
source /opt/nerfball/venv/bin/activate

touch /tmp/keeprunning
tail -f /tmp/keeprunning
