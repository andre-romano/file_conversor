#!/bin/bash
# publish.sh - A script to publish the app to package repos.

# Exit immediately if a command exits with a non-zero status, treat unset variables as an error, and prevent errors in a pipeline from being masked.
set -Eeuo pipefail

# Trap errors and print the command that failed, its exit code, and the line number before exiting with the same code.
trap 'rc=$?;
echo "ERROR: command \"${BASH_COMMAND}\" failed with exit code $rc at line ${LINENO}";
exit $rc' ERR

. "$(dirname "$0")/_env.sh"

echo "Publishing ..."

SUPPORTED_REPOS=""
if [[ "$GOOS" == "windows" ]]; then
    SUPPORTED_REPOS="scoop choco"
elif [[ "$GOOS" == "linux" ]]; then
    SUPPORTED_REPOS=""
elif [[ "$GOOS" == "darwin" ]]; then
    SUPPORTED_REPOS="homebrew-tap"
else
    echo "Unsupported OS: $GOOS"
    exit 1
fi

echo "    1. Cloning packaging repositories ..."
mkdir -p build/packaging
cd build/packaging
for package in $SUPPORTED_REPOS; do
    mkdir -p "$package"
    rm -rf "$package/*"
    git clone git@github.com:file-conversor/$package.git
done

echo "    2. Generating package manifest files ..."
cd "$REPO_DIR"
go run tools/gen_packages/main.go

echo "    3. Publishing repos for '$GOOS' (git push) ..."
for repo in $SUPPORTED_REPOS ; do        
    echo "        - Publishing $repo ..."
    cd "build/packaging/${repo}"
    git add .
    git commit -m "Update package files to $TAG"
    git push
    git tag -f "$TAG"
    git push --tags --force    
    cd "$REPO_DIR"
done

echo "Publishing ... Done!"
echo
