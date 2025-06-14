#!/bin/bash

# Path: ./run.sh

echo "Waiting for postgres..."

ENV_PATH=${ENV_PATH:-/app/env.sh}
echo "Checking for script in $ENV_PATH"
if [ -f $ENV_PATH ] ; then
    echo "Running script $ENV_PATH"
    . "$ENV_PATH"
else
    echo "There is no script $ENV_PATH"
fi

# If there's a prestart.sh script in the /app directory or other path specified, run it before starting
PRE_START_PATH=${PRE_START_PATH:-/app/prestart.sh}
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi

export APP_MODULE=${APP_MODULE-app.main:app}
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8000}
export BACKEND_CORS_ORIGINS=${BACKEND_CORS_ORIGINS:-["*"]}

exec uvicorn "$APP_MODULE" --host $HOST --port $PORT --reload
