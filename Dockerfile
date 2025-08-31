# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.13

# STAGE 2 - RELEASE
FROM python:${PYTHON_VERSION}-slim AS release

ARG DEPENDENCIES_APT_GET="ghostscript ffmpeg libreoffice-nogui"
ARG DEPENDENCIES_HOMEBREW="gifsicle oxipng mozjpeg"

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    LANG=en_US.UTF-8 LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    HOMEBREW_NO_INSTALL_CLEANUP=1 \
    PATH="/home/linuxbrew/.linuxbrew/opt/mozjpeg/bin:/home/linuxbrew/.linuxbrew/bin:$PATH"

# Leverage BuildKit cache:
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update &&\
    apt-get install -y --no-install-recommends locales curl git ${DEPENDENCIES_APT_GET} &&\
    rm -rf /var/lib/apt/lists/* &&\    
    sed -i '/en_US.UTF-8/s/^# //' /etc/locale.gen && \
    locale-gen en_US.UTF-8 &&\    
    bash -c "curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash" && \
    brew install ${DEPENDENCIES_HOMEBREW} ;\
    brew cleanup -s ;\
    echo ok

RUN --mount=type=cache,target=/root/.cache/pip \    
    git clone https://github.com/andre-romano/file_conversor /app &&\    
    cd /app &&\    
    pip install -U pip &&\
    pip install pdm invoke &&\
    pdm install &&\
    pdm run invoke locales.build &&\
    pdm run invoke base.tests &&\
    pdm run invoke pypi.build &&\
    useradd -m app &&\    
    pip install /app/dist/*.whl &&\
    rm -rf /app &&\
    file_conversor -V

# define app userspace
WORKDIR /app
USER app
ENTRYPOINT ["file_conversor"]
