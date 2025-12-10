# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION="3.13.7-slim-bookworm"
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
FROM python:${PYTHON_VERSION} AS build

COPY --from=gifsicle /usr/local/bin /root/.local/bin
COPY --from=mozjpeg /usr/local/bin /root/.local/bin
COPY --from=oxipng /usr/local/bin /root/.local/bin

COPY . /app
WORKDIR /app

# INSTALL BUILD DEPENDENCIES AND BUILD APP:
RUN echo "Installing Python dependencies ..." \
    && python -m pip install --upgrade pip \
    && python -m pip install --upgrade setuptools wheel pdm \
    && python -m pdm install --dev --no-lock \
    && echo "Installing Python dependencies ... OK" \
    && echo "Building .whl ..." \
    && python -m pdm run invoke pypi.build \
    && echo "Building .whl ... OK" 

# --------------------
# STAGE 2 - release
# --------------------
FROM python:${PYTHON_VERSION} AS release

COPY --from=build /root/.local/bin /root/.local/bin
COPY --from=build /app/dist /app/dist

WORKDIR /app

ENV PATH="/root/.local/bin:${PATH}"
RUN apt-get update \
    && echo "Installing system dependencies ..." \
    && apt-get install -y --no-install-recommends ${APT_DEPENDENCIES} \
    && echo "Installing system dependencies ... OK" \
    && echo "Installing Python app from wheel ..." \
    && python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir --upgrade setuptools wheel \
    && python -m pip install --no-cache-dir /app/dist/*.whl \
    && echo "Installing Python app from wheel ... OK" \    
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
        /app/dist/* \
    && echo "Cleaning up ... OK" \
    && echo "Testing installation ..." \
    && python -m file_conversor --help \
    && python -m file_conversor --version \
    && echo "Testing installation ... OK" \
    && echo "All done."

# final settings
EXPOSE 5000 
ENTRYPOINT [ "python", "-m", "file_conversor" ]
