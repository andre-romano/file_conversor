# syntax=docker/dockerfile:1.7

ARG APP_NAME="file_conversor"
ARG BUILD_BASE_IMAGE="golang:latest"
ARG RELEASE_BASE_IMAGE="debian:stable-slim"

# --------------------
# STAGE 0 - binaries
# --------------------
FROM andreromano/gifsicle:latest AS gifsicle
FROM andreromano/mozjpeg:latest AS mozjpeg
FROM andreromano/oxipng:latest AS oxipng

# --------------------
# STAGE 1 - build
# --------------------
FROM ${BUILD_BASE_IMAGE} AS build

WORKDIR /app

COPY . .
COPY --from=gifsicle /usr/local/bin /root/.local/bin
COPY --from=mozjpeg /usr/local/bin /root/.local/bin
COPY --from=oxipng /usr/local/bin /root/.local/bin

RUN go build -o /root/.local/bin -trimpath -ldflags="-s -w" ./cmd/...

# --------------------
# STAGE 2 - release
# --------------------

FROM ${RELEASE_BASE_IMAGE} AS release

WORKDIR /app

COPY --from=build /root/.local/bin /root/.local/bin

ENV PATH="/root/.local/bin:${PATH}"
RUN echo "Installing system dependencies ..." \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        ca-certificates \
    && echo "Installing system dependencies ... OK" \    
    && echo "Cleaning up ..." \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf \
        /usr/share/doc-base/* \
        /usr/share/doc/* \
        /usr/share/man/* \
        /usr/share/info/* \
        /usr/share/lintian/* \
        /usr/share/linda/* \
        /var/lib/apt/lists/* \
        /var/cache/* \
        /var/log/* \
        /var/tmp/* \
        /tmp/* \
        /root/.cache/* \
        /app/* \
    && echo "Cleaning up ... OK" \
    && echo "Testing installation ..." \
    && ${APP_NAME} --version \
    && echo "Testing installation ... OK" \
    && echo "All done."

# final settings
# EXPOSE 5000 
ENTRYPOINT [ "${APP_NAME}" ]
