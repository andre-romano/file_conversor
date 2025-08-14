# tasks_modules\pypi.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import base


@task
def mkdirs(c):
    _config.mkdir([
        "build",
        "dist",
    ])


@task(pre=[mkdirs])
def clean_whl(c):
    remove_path("dist/*.whl")
    remove_path("dist/*.tar.gz")


@task(pre=[clean_whl, base.locales_build, ])
def build(c):
    print(f"[bold] Building PyPi package ... [/]")
    c.run(f"pdm build")
    if not list(Path("dist").glob("*.whl")):
        raise RuntimeError("Build WHL - Empty dist/*.whl")
    print(f"[bold] Building PyPi package ... [/][bold green]OK[/]")


@task(pre=[build, ])
def check(c):
    if not list(Path("dist").glob("*.whl")):
        raise RuntimeError("Test PyPi - Empty dist/*.whl")
    print(f"[bold] Checking .WHL build ... [/]")
    c.run(f"pdm run twine check dist/*.whl dist/*.tar.gz")
    print(f"[bold] Checking .WHL build ... [/][bold green]OK[/]")


@task(pre=[check, ])
def test(c):
    print(f"[bold] Testing PyPi ... [/]")
    c.run(f"pdm run twine upload --repository testpypi dist/*.whl dist/*.tar.gz")
    print(f"[bold] Testing PyPi ... [/][bold green]OK[/]")


@task(pre=[check,], post=[base.publish_install_script,])
def publish(c):
    print(f"[bold] Publishing to PyPi ... [/]")
    c.run(f"pdm run twine upload dist/*.whl dist/*.tar.gz")
    print(f"[bold] Publishing to PyPi ... [/][bold green]OK[/]")
