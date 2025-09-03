# tasks_modules\docker.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules._config import *
from tasks_modules._deps import *


docker_bin = shutil.which("docker")
if not docker_bin:
    docker_bin = shutil.which("podman")


@task
def create_dockerfile(c: InvokeContext):
    DOCKERFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DOCKERFILE_PATH.exists():
        DOCKERFILE_PATH.unlink()
    DOCKERFILE_PATH.write_text(rf"""# syntax=docker/dockerfile:1.7
# STAGE 1,2,3 - DEPENDENCIES
{"\n".join([rf"FROM {dep}:{version} AS {dep.split("/")[1]}" for dep, version in DOCKER_IMAGE_DEPS.items()])}

# STAGE 4 - RELEASE
FROM python:{DOCKER_PY_VERSION}-slim AS release
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8   

# copy binaries
{"\n".join([rf"COPY --from={dep.split("/")[1]} /usr/local/bin/* /usr/local/bin" for dep, version in DOCKER_IMAGE_DEPS.items()])}    

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt/lists \
    --mount=type=cache,target=/root/.cache/pip \
    apt-get update \
    && echo "Building app {PROJECT_NAME} ..." \
    && apt-get install -y --no-install-recommends git ca-certificates locales curl {" ".join(DOCKER_APT_DEPS)} \
    && sed -i '/en_US.UTF-8/s/^# //' /etc/locale.gen  \
    && locale-gen en_US.UTF-8 \
    && git clone {PROJECT_HOMEPAGE} /app \
    && cd /app \
    && git checkout {GIT_RELEASE} \
    && pip install -U pip \
    && pip install pdm invoke \
    && pdm install \
    && pdm run invoke base.tests \
    && pdm run invoke pypi.build \
    && echo "Building app {PROJECT_NAME} ... OK" \
    && echo "Installing app {PROJECT_NAME} ..." \
    && pip install dist/*.whl \
    && pdm run invoke base.check \    
    && rm -rf /app \
    && echo "Installing app {PROJECT_NAME} ... OK"

# define app userspace
WORKDIR /app
ENTRYPOINT [ "{PROJECT_NAME}" ]
CMD [ "--help" ]
""", encoding="utf-8")
    if not DOCKERFILE_PATH.exists():
        raise FileNotFoundError(f"'{DOCKERFILE_PATH}' not found")

    print(f"{DOCKERFILE_PATH}:")
    print(DOCKERFILE_PATH.read_text())


@task(pre=[create_dockerfile,])
def build(c: InvokeContext):
    print(f"[bold] Building docker image v{PROJECT_VERSION} ... [/]")
    if not docker_bin:
        raise RuntimeError("'docker' not found in PATH")
    build_cmd = [
        f"{docker_bin}", "build", "--no-cache",
        "-t", f"{DOCKER_REPOSITORY}/{PROJECT_NAME}:{PROJECT_VERSION}",
        "-t", f"{DOCKER_REPOSITORY}/{PROJECT_NAME}:latest",
        f"{DOCKERFILE_PATH.parent}",
    ]
    result = c.run(" ".join(build_cmd))
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Building docker image v{PROJECT_VERSION} ... [/][bold green]OK[/]")


@task(pre=[build,])
def check(c: InvokeContext):
    print(f"[bold] Checking docker image ... [/]")
    if not docker_bin:
        raise RuntimeError("'docker' not found in PATH")
    run_cmd = [
        f"{docker_bin}", "run", "--rm",
        f"-v", "./tests:/app/tests",
        f"{DOCKER_REPOSITORY}/{PROJECT_NAME}:latest",
    ]
    result = c.run(" ".join(run_cmd))
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Checking docker image ... [/][bold green]OK[/]")


@task(pre=[check,])
def publish(c: InvokeContext):
    print(f"[bold] Publishing to Docker Hub ... [/]")
    result = c.run(f"{docker_bin} push --all-tags {DOCKER_REPOSITORY}/{PROJECT_NAME}")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Publishing to Docker Hub ... [/][bold green]OK[/]")


@task(pre=[publish,])
def push(c: InvokeContext):
    pass
