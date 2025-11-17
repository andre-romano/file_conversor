# tasks_modules\pypi.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import base, locales

to_remove: set[Path] = set()


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


@task
def check_requirements(c: InvokeContext):
    print("[bold]Checking requirements ... [/]")
    result = c.run(f"pdm run pip check")
    assert (result is not None) and (result.return_code == 0)
    print("[bold]Checking requirements ... [/][bold green]OK[/]")


@task(pre=[locales.build])
def copy_includes(c: InvokeContext):
    print("[bold]Copying MANIFEST.in includes ...[/]")
    for include in _config.parse_manifest_includes():
        include_path = Path(include)
        dest_path = Path("./src") / PROJECT_NAME / include_path.name
        if include_path.resolve() == dest_path.resolve():
            continue
        to_remove.add(dest_path)
        _config.copy(src=include_path, dst=dest_path)
    print("[bold]Copying MANIFEST.in includes ... [/][bold green]OK[/]")


@task(pre=[locales.build])
def remove_includes(c: InvokeContext):
    print("[bold]Removing MANIFEST.in includes ...[/]")
    for path in to_remove:
        if path.exists():
            _config.remove_path(str(path))
    print("[bold]Removing MANIFEST.in includes ... [/][bold green]OK[/]")


@task(pre=[check_requirements, clean_whl, copy_includes,], post=[remove_includes,])
def build(c: InvokeContext):
    print(f"[bold] Building PyPi package ... [/]")
    result = c.run(f"pdm build")
    assert (result is not None) and (result.return_code == 0)
    whl_path = _config.get_whl_file()
    assert whl_path is not None
    print(f"[bold] Building PyPi package ... [/][bold green]OK[/]")
    print(f"[bold] Checking .WHL build ... [/]")
    result = c.run(f"pdm run twine check dist/*.whl dist/*.tar.gz")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Checking .WHL build ... [/][bold green]OK[/]")


@task(pre=[build,],)
def install_app(c: InvokeContext):
    print(f"[bold] Installing PyPi package ... [/]")
    whl_path = _config.get_whl_file()
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
