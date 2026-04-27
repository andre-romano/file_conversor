# syntax=docker/dockerfile:1.7

ARG TARGETPLATFORM
ARG APP_NAME="file_conversor"
ARG DOCKER_BASE_IMAGE="stable-slim"
ARG APT_DEPENDENCIES=" \
git \
ca-certificates \
ffmpeg \
ghostscript \
tesseract-ocr \
libreoffice-nogui \
"

# --------------------
# STAGE 0 - binaries
# --------------------
FROM andreromano/gifsicle:latest AS gifsicle
FROM andreromano/mozjpeg:latest AS mozjpeg
FROM andreromano/oxipng:latest AS oxipng

# --------------------
# STAGE 1 - build
# --------------------
FROM ${DOCKER_BASE_IMAGE} AS build

COPY --from=gifsicle /usr/local/bin /root/.local/bin
COPY --from=mozjpeg /usr/local/bin /root/.local/bin
COPY --from=oxipng /usr/local/bin /root/.local/bin

# --------------------
# STAGE 2 - release
# --------------------

FROM ${DOCKER_BASE_IMAGE} AS release

WORKDIR /app

COPY ${TARGETPLATFORM}/${APP_NAME}.deb /app
COPY --from=build /root/.local/bin /root/.local/bin

ENV PATH="/root/.local/bin:${PATH}"
RUN echo "Installing system dependencies ..." \
    && apt-get update \
    && apt-get install -y --no-install-recommends ${APT_DEPENDENCIES} \
    && echo "Installing system dependencies ... OK" \
    && echo "Installing app ..." \
    && dpkg -i ${APP_NAME}.deb \
    && chmod +rx /root/.local/bin/* \
    && chmod +rx /usr/bin/${APP_NAME} \
    && echo "Installing app ... OK" \
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
