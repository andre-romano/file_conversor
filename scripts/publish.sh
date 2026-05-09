#!/bin/bash
# scripts/publish.sh 
# - A script to publish the app to package repos.

# Exit immediately if a command exits with a non-zero status, treat unset variables as an error, and prevent errors in a pipeline from being masked.
set -Eeuo pipefail

# Trap errors and print the command that failed, its exit code, and the line number before exiting with the same code.
trap 'rc=$?;
echo "ERROR: command \"${BASH_COMMAND}\" failed with exit code $rc at line ${LINENO}";
exit $rc' ERR

. "$(dirname "$0")/_env.sh"

echo "Publishing ..."

echo "    1. Cloning packaging repositories ..."
mkdir -p build/packaging
pushd build/packaging
for repo in $SUPPORTED_REPOS; do
    mkdir -p "$repo"
    rm -rf "${repo}/*"
    git clone git@github.com:${OWNER_REPO}/${repo}.git
done
popd > /dev/null # move back to project dir root (defined in _env.sh script)

echo "    2. Generating package manifest files ..."
go run tools/gen_packages/main.go

if [ "$GOOS" = "linux" ]; then
    echo "    3. Generating Linux repositories (DEB, RPM) ..."
    . "$(dirname "$0")/_gen_lin_repos.sh"
else
    echo "    3. Generating Linux repositories (DEB, RPM) ... [SKIPPED] (GOOS='$GOOS')"
fi

echo "    4. Publishing repos for '$GOOS' (git push) ..."
for repo in $SUPPORTED_REPOS ; do        
    echo "        - Publishing $repo ..."
    pushd "build/packaging/${repo}"
    git add .
    git commit -m "Update package files to $TAG"
    git push
    git tag -f "$TAG"
    git push --tags --force    
    popd > /dev/null # move back to project dir root (defined in _env.sh script)
done

echo "Publishing ... Done!"
echo
