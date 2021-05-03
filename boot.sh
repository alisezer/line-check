#!/bin/bash

while true; do
    flask deploy
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done

cron
exec gunicorn -c gunicorn.py line_check:app