#!/bin/bash
# scripts/_env.sh 
# - A script to set environment variables for build and package scripts.

echo "Setting environment variables ..."
echo

export PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

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

export OWNER_REPO="file-conversor"

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
export SUPPORTED_REPOS

echo "Environment variables:"
echo "    SUPPORTED_REPOS: $SUPPORTED_REPOS"
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