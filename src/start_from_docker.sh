#!/bin/bash

# bail on error
set -e 

echo "Activating conda env..."
source "$(which activate)" poboys_env

# copy everything from staging
mkdir /opt/poboys_conda_package_server
cp -ax /opt/poboys_staging/* /opt/poboys_conda_package_server
cd /opt/poboys_conda_package_server

if [ -n "$POBOYS_PORT" ]; then
    ARGS="--port $POBOYS_PORT"
fi

# if we are storing in S3 then sync from there (just in case we are missing anything locally)
if [ -n "$POBOYS_S3_BUCKET" ]; then
    ARGS="$ARGS"" --s3_bucket $POBOYS_S3_BUCKET"
    mkdir -p pkgs
    aws s3 sync s3://"$POBOYS_S3_BUCKET" pkgs
fi

echo "Serving..."
python poboys_conda_package_server.py $ARGS
