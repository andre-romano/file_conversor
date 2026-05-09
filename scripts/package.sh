#!/bin/bash
# scripts/package.sh 
# - A script to package the app using Chocolatey, FPM, etc.

# Exit immediately if a command exits with a non-zero status, treat unset variables as an error, and prevent errors in a pipeline from being masked.
set -Eeuo pipefail

# Trap errors and print the command that failed, its exit code, and the line number before exiting with the same code.
trap 'rc=$?;
echo "ERROR: command \"${BASH_COMMAND}\" failed with exit code $rc at line ${LINENO}";
exit $rc' ERR

. "$(dirname "$0")/_env.sh"

echo "Packaging ..."

mkdir -p build/packaging
rm -rf build/packaging/*

echo "    1. Generating package manifest files ..."
go run tools/gen_packages/main.go

echo "    2. Compiling packages ..."
go run tools/build_packages/main.go

echo "Packaging ... Done!"
echo