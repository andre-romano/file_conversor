#!/bin/bash

# scripts\docker_build.sh
# --- Script to build and test the Docker image for file_conversor ---

# Exit immediately if a command exits with a non-zero status
set -e
SCRIPT_DIR=$(dirname "$(realpath "$0")")
cd "${SCRIPT_DIR}/.."
echo "Building Docker image in '${PWD}' ..."

# get version from pyproject.toml
VERSION=$(grep -Po '(?<=^version = ")[^"]*' "pyproject.toml")

docker build -t "andreromano/file_conversor:latest" \
    -t "andreromano/file_conversor:${VERSION}" \
    .
echo "Building Docker image in '${PWD}' ... OK"

echo "Testing Docker image ..."
docker run --rm andreromano/file_conversor:latest --help
docker run --rm -v ./:/data andreromano/file_conversor:latest text check /data/tests/.data/test.json
echo "Testing Docker image ... OK"

echo "All done."