#!/bin/bash
set -e

DEFAULT_UID=1000
DEFAULT_GID=1000
DEFAULT_ZIP=build.zip

BUILD_UID=${BUILD_UID:-${DEFAULT_UID}}
BUILD_GID=${BUILD_GID:-${DEFAULT_GID}}
BUILD_ZIP=$(readlink -m $(pwd))/${BUILD_ZIP:-${DEFAULT_ZIP}}

# Create virtualenv
virtualenv /tmp/venv

# Install package and all dependencies
/tmp/venv/bin/pip install -e .

# Build the zip
cd /tmp/venv/lib/python3.6/site-packages/
zip -r ${BUILD_ZIP} *
chown ${BUILD_UID}:${BUILD_GID} ${BUILD_ZIP}
