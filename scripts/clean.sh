#!/bin/bash
# clean.sh - A script to clean build artifacts.

# Exit immediately if a command exits with a non-zero status, treat unset variables as an error, and prevent errors in a pipeline from being masked.
set -euo pipefail

# Trap errors and print the command that failed, its exit code, and the line number before exiting with the same code.
trap 'rc=$?;
echo "ERROR: command \"${BASH_COMMAND}\" failed with exit code $rc at line ${LINENO}";
exit $rc' ERR

echo "Cleaning build artifacts ..."

mkdir -p build dist
rm -rf build/* dist/*

echo "Cleaning build artifacts ... Done."
echo