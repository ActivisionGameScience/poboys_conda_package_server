#!/bin/bash

mkdir /opt/poboys_conda_package_server
cp -ax /opt/poboys_staging/* /opt/poboys_conda_package_server
cd /opt/poboys_conda_package_server

echo "activate conda env.."
source "$(which activate)" dev

echo "launch..."
python poboys_conda_package_server.py
