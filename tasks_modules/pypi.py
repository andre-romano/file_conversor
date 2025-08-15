# tasks_modules\pypi.py

from pathlib import Path
from invoke.tasks import task
from requests import post

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import base


@task
def mkdirs(c: InvokeContext):
    _config.mkdir([
        "build",
        "dist",
    ])


@task(pre=[mkdirs])
def clean_whl(c: InvokeContext):
    remove_path("dist/*.whl")
    remove_path("dist/*.tar.gz")


@task(pre=[clean_whl, base.locales_build, ])
def build(c: InvokeContext):
    print(f"[bold] Building PyPi package ... [/]")
    result = c.run(f"pdm build")
    assert (result is not None) and (result.return_code == 0)
    if not list(Path("dist").glob("*.whl")):
        raise RuntimeError("Build WHL - Empty dist/*.whl")
    print(f"[bold] Building PyPi package ... [/][bold green]OK[/]")
    print(f"[bold] Checking .WHL build ... [/]")
    result = c.run(f"pdm run twine check dist/*.whl dist/*.tar.gz")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Checking .WHL build ... [/][bold green]OK[/]")


@task(pre=[build,],)
def install_app(c: InvokeContext):
    print(f"[bold] Installing PyPi package ... [/]")
    whl_path: Path | None = None
    for whl in list(Path("dist").glob("*.whl")):
        if PROJECT_VERSION in str(whl):
            whl_path = whl
    assert whl_path is not None
    print(f"Installing '{whl_path}' ...")
    result = c.run(rf'pip install "{whl_path}"')
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Installing PyPi package ... [/][bold green]OK[/]")


@task
def uninstall_app(c: InvokeContext):
    print(f"[bold] Uninstalling PyPi package ... [/]")
    result = c.run(rf'pip uninstall -y "{PROJECT_NAME}"')
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Uninstalling PyPi package ... [/][bold green]OK[/]")


@task(pre=[install_app,], post=[uninstall_app,])
def check(c: InvokeContext):
    base.check(c)


@task(pre=[build, ])
def test(c: InvokeContext):
    print(f"[bold] Testing PyPi ... [/]")
    result = c.run(f"pdm run twine upload --repository testpypi dist/*.whl dist/*.tar.gz")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Testing PyPi ... [/][bold green]OK[/]")


@task(pre=[build,],)
def publish(c: InvokeContext):
    print(f"[bold] Publishing to PyPi ... [/]")
    result = c.run(f"pdm run twine upload dist/*.whl dist/*.tar.gz")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Publishing to PyPi ... [/][bold green]OK[/]")
