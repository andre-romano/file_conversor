#!/bin/bash
# get_python_version.sh
# This script reads the pyproject.toml file to extract the minimum and maximum
# supported Python versions specified in the requires-python field.

LINE=$(grep -E '^requires-python' pyproject.toml | sed 's/.*= "\(.*\)".*/\1/')

# Extract >=X.Y
MIN=$(echo "$LINE" | sed -n 's/.*>=\([0-9.]*\).*/\1/p')

# Extract <X.Y
MAX=$(echo "$LINE" | sed -n 's/.*<\([0-9.]*\).*/\1/p')

# Compute max allowed major.minor (subtract 1 from minor)
U_MAJOR=$(echo "$MAX" | cut -d. -f1)
U_MINOR=$(echo "$MAX" | cut -d. -f2)

MAX_MINOR=$((U_MINOR - 1))
MAX="${U_MAJOR}.${MAX_MINOR}"

echo "min=$MIN" 
echo "max=$MAX" 
