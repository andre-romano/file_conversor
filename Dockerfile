# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.13

ARG DEPENDENCIES_APT_GET="ghostscript ffmpeg libreoffice-nogui"
ARG DEPENDENCIES_HOMEBREW="gifsicle oxipng mozjpeg"

# STAGE 1 - BUILD .WHL
FROM python:${PYTHON_VERSION}-slim AS build
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

# copy data
WORKDIR /app
COPY . .

# Leverage BuildKit cache:
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update &&\
    apt-get install -y --no-install-recommends curl &&\
    rm -rf /var/lib/apt/lists/*

# Leverage BuildKit cache:
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -U pip &&\
    pip install pdm invoke &&\
    pdm install &&\
    pdm run invoke pypi.build

# STAGE 2 - RELEASE
FROM python:${PYTHON_VERSION}-slim AS release
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    LANG=en_US.UTF-8 LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    HOMEBREW_NO_INSTALL_CLEANUP=1 \
    PATH="/home/linuxbrew/.linuxbrew/opt/mozjpeg/bin:/home/linuxbrew/.linuxbrew/bin:$PATH"

# Leverage BuildKit cache:
WORKDIR /app
COPY . .
COPY --from=build /app/dist /app/dist
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update &&\
    apt-get install -y --no-install-recommends locales curl ${DEPENDENCIES_APT_GET} &&\
    rm -rf /var/lib/apt/lists/* &&\    
    sed -i '/en_US.UTF-8/s/^# //' /etc/locale.gen && \
    locale-gen en_US.UTF-8 &&\
    bash -c "curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash" && \
    brew install ${DEPENDENCIES_HOMEBREW} &&\
    useradd -m app &&\
    chown -R app:app /app &&\
    pip install dist/*.whl
USER app
ENTRYPOINT ["file_conversor"]
