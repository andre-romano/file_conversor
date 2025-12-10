#!/bin/bash
# docker_push.sh - Script to push the Docker image for file_conversor to a Docker registry

# Exit immediately if a command exits with a non-zero status
set -e
SCRIPT_DIR=$(dirname "$(realpath "$0")")
cd "${SCRIPT_DIR}/.."

# get version from pyproject.toml
VERSION=$(grep -Po '(?<=^version = ")[^"]*' "pyproject.toml")

echo "Pushing Docker image 'file_conversor:${VERSION}' to registry ..."
docker push "andreromano/file_conversor:${VERSION}" $@
docker push "andreromano/file_conversor:latest" $@
echo "Pushing Docker image 'file_conversor:${VERSION}' to registry ... OK"

echo "All done."