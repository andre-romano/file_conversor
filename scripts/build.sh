#!/bin/bash
# build.sh - A script to build the app using Go.

# Exit immediately if a command exits with a non-zero status, treat unset variables as an error, and prevent errors in a pipeline from being masked.
set -Eeuo pipefail

# Trap errors and print the command that failed, its exit code, and the line number before exiting with the same code.
trap 'rc=$?;
echo "ERROR: command \"${BASH_COMMAND}\" failed with exit code $rc at line ${LINENO}";
exit $rc' ERR

. "$(dirname "$0")/_env.sh"

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

    FILENAME="$(basename $cmd)${EXT}"
    OUTPUT="${BUILD_DIR}/$FILENAME"
    
    mkdir -p "$(dirname "$OUTPUT")"
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
    
    echo "Testing ${OUTPUT} ..."
    chmod +rx "$OUTPUT"
    ./${OUTPUT} --version > /dev/null 2>&1
done

echo "Building ... Done!"
echo 
