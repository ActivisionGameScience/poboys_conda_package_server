#!/bin/bash

echo "activate conda env.."
source "$(which activate)" dev

echo "launch..."
python poboys_conda_package_server.py
