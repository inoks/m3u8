#!/usr/bin/env bash

set -e

export DJANGO_SETTINGS_MODULE=project.production
NAME="Playlist"
SOCKFILE=/tmp/playlist.sock
NUM_WORKERS=2
# Set this to 0 for unlimited requests. During development, you might want to
# set this to 1 to automatically restart the process on each request (i.e. your
# code will be reloaded on every request).
MAX_REQUESTS=0

echo "Starting $NAME as `whoami`"

source ENV/bin/activate

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec gunicorn \
     --workers $NUM_WORKERS \
     --max-requests $MAX_REQUESTS \
     --timeout=600 \
     --log-level=info \
     --bind unix:$SOCKFILE \
     project.wsgi:application
