# tasks_modules\docker.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules._config import *

DOCKER_IMAGE = f"andre-romano/{PROJECT_NAME}:{PROJECT_VERSION}"

docker_bin = shutil.which("docker")
if not docker_bin:
    docker_bin = shutil.which("podman")


@task
def build(c: InvokeContext):
    print(f"[bold] Building docker image v{PROJECT_VERSION} ... [/]")
    if not docker_bin:
        raise RuntimeError("'docker' not found in PATH")
    build_cmd = [
        f"{docker_bin}", "build",
        "--no-cache",
        "-t", f"{DOCKER_IMAGE}",
        ".",
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
        f"{docker_bin}", "run",
        "--rm", "--it", f"{DOCKER_IMAGE}",
        f"{PROJECT_NAME}", "--help",
    ]
    result = c.run(" ".join(run_cmd))
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Checking docker image ... [/][bold green]OK[/]")


@task
def login(c: InvokeContext):
    print(f"[bold] Login to Docker Hub ... [/]")
    if not docker_bin:
        raise RuntimeError("'docker' not found in PATH")
    result = c.run(f"{docker_bin} login")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Login to Docker Hub ... [/][bold green]OK[/]")


@task(pre=[check, login,])
def publish(c: InvokeContext):
    print(f"[bold] Publishing to Docker Hub ... [/]")
    result = c.run(f"{docker_bin} push {DOCKER_IMAGE}")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Publishing to Docker Hub ... [/][bold green]OK[/]")
