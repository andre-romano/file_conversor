#!/bin/bash
# _env.sh - A script to set environment variables for build and package scripts.

echo "Setting environment variables ..."
echo

export REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -z "${CGO_ENABLED:-}" ]]; then
    export CGO_ENABLED=1
fi

export GOOS=$(go env GOOS)
export GOARCH=$(go env GOARCH)
export EXT=""
if [ "$GOOS" = "windows" ]; then
    export EXT=".exe"
fi
export BUILD_DIR="build/${GOOS}-${GOARCH}"

export TAG="$(git describe --tags --always 2>/dev/null || echo dev)"
export VERSION="${TAG#v}"
export COMMIT=$(git rev-parse --short HEAD)
export DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
export BUILT_BY="git_actions_bot"

echo "Environment variables:"
echo "    PACKAGES_REPOS: $PACKAGES_REPOS"
echo "    CGO_ENABLED: $CGO_ENABLED"
echo "    GOOS: $GOOS"
echo "    GOARCH: $GOARCH"
echo "    BUILD_DIR: $BUILD_DIR"
echo "    EXE: $EXT"
echo "    TAG: $TAG"
echo "    VERSION: $VERSION"
echo "    COMMIT: $COMMIT"
echo "    DATE: $DATE"
echo "    BUILT_BY: $BUILT_BY"
echo 