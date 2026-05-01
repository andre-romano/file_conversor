#!/bin/bash
# build.sh - A script to build the app using Go.

# Exit immediately if a command exits with a non-zero status, treat unset variables as an error, and prevent errors in a pipeline from being masked.
set -euo pipefail


# Trap errors and print the command that failed, its exit code, and the line number before exiting with the same code.
trap 'rc=$?;
echo "ERROR: command \"${BASH_COMMAND}\" failed with exit code $rc at line ${LINENO}";
exit $rc' ERR

if [[ -z "${CGO_ENABLED:-}" ]]; then
    export CGO_ENABLED=1
fi

GOOS=$(go env GOOS)
GOARCH=$(go env GOARCH)
EXT=""
if [ "$GOOS" = "windows" ]; then
    EXT=".exe"
fi

VERSION="$(git describe --tags --always 2>/dev/null || echo dev)"
COMMIT=$(git rev-parse --short HEAD)
DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
BUILT_BY="git_actions_bot"

echo "Environment variables:"
echo "    CGO_ENABLED: $CGO_ENABLED"
echo "    GOOS: $GOOS"
echo "    GOARCH: $GOARCH"
echo "    EXE: $EXT"
echo "    VERSION: $VERSION"
echo "    COMMIT: $COMMIT"
echo "    DATE: $DATE"
echo "    BUILT_BY: $BUILT_BY"
echo 

echo "Building ..."

echo "    1. Running go mod tidy ..."
go mod tidy

echo "    2. Running go generate ..."
go generate ./...

echo "    3. Running go test ..."
go test -v ./...

echo "    4. Building go build ..."
for cmd in ./cmd/* ; do
    if ! [ -d "$cmd" ]; then
        continue
    fi

    FILENAME="$(basename $cmd)_${VERSION}_${GOOS}_${GOARCH}${EXT}"
    OUTPUT="build/$FILENAME"
    
    rm -f "$OUTPUT"
    go build \
        -trimpath \
        -ldflags="\
            -s \
            -w \
            -X main.version=$VERSION \
            -X main.commit=$COMMIT \
            -X main.date=$DATE \
            -X main.builtBy=$BUILT_BY \
        " \
        -o "$OUTPUT" "$cmd"
    chmod +rx "$OUTPUT"
    "./$OUTPUT" --version > /dev/null 2>&1
done

echo "Building ... Done!"
echo 
