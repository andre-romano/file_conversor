# tasks_modules\base.py

import os
import platform

from invoke.tasks import task

from pathlib import Path

# user provided
from tasks_modules import _config
from tasks_modules._config import *

WINDOWS = (platform.system() == "Windows")


@task
def mkdirs(c: InvokeContext):
    dirs = [
        "build",
        "dist",
        "docs",
        "htmlcov",
    ]
    for dir in dirs:
        Path(dir).mkdir(parents=True, exist_ok=True)
        if not Path(dir).exists():
            raise RuntimeError(f"Cannot create dir '{dir}'")


@task
def clean_logs(c: InvokeContext):
    remove_path(f"**/*.log")
    remove_path(f"**/*.log.*")


@task(pre=[mkdirs])
def clean_build(c: InvokeContext):
    remove_path(f"build/*")


@task(pre=[mkdirs])
def clean_dist(c: InvokeContext):
    remove_path(f"dist/*")


@task(pre=[mkdirs])
def clean_htmlcov(c: InvokeContext):
    remove_path(f"htmlcov/*")


@task(pre=[mkdirs])
def clean_docs(c: InvokeContext):
    remove_path(f"docs/*")


@task(pre=[mkdirs])
def clean_changelog(c: InvokeContext):
    remove_path(f"CHANGELOG.md")
    remove_path(f"RELEASE_NOTES.md")


@task(pre=[clean_logs,
           clean_build,
           clean_dist,
           clean_htmlcov,
           clean_docs,
           clean_changelog,
           ])
def clean(c: InvokeContext):
    pass


@task(pre=[clean_htmlcov, ])
def tests(c, args: str = ""):
    print("[bold] Running tests ... [/]")
    result = c.run(f"pdm run pytest {args.split()}")
    assert (result is not None) and (result.return_code == 0)
    print("[bold] Running tests ... [bold green]OK[/][/]")


# @task(pre=[clean_uml,])
# def uml(c:InvokeContext):
#     print("[bold] Generating uml/ ... [/]")
#     c.run("pdm run pyreverse -A --filter-mode=ALL --colorized -d uml/ -o jpg src/")
#     if not Path("uml/classes.jpg").exists():
#         raise RuntimeError("UML PyReverse - Empty dist/classes.jpg")
#     c.run("pdm run pydeps src/ --noshow --reverse -Tpng -o uml/dependencies.png")
#     if not Path("uml/dependencies.png").exists():
#         raise RuntimeError("UML PyDeps - Empty dist/dependencies.png")
#     print("[bold] Generating uml/ ... [/][bold green]OK[/]")

@task
def check(c: InvokeContext):
    print(f"[bold] Checking app '{PROJECT_NAME}' ... [/]")
    app_exe = shutil.which(PROJECT_NAME)
    if not app_exe:
        raise RuntimeError(f"'{PROJECT_NAME}' not found in PATH")
    print(f"[bold] '{PROJECT_NAME}' found:[/] '{app_exe}'")
    result = c.run(f'"{app_exe}" -V')
    assert result is not None
    if PROJECT_VERSION not in result.stdout:
        raise RuntimeError(f"'{PROJECT_NAME}' version mismatch. Expected: '{PROJECT_VERSION}'.")
    assert result.return_code == 0
    print(f"[bold] Checking app '{PROJECT_NAME}' ... [/][bold green]OK[/]")


@task
def is_admin(c: InvokeContext):
    print(f"[bold] Checking for admin rights ... [/]")
    if WINDOWS:
        try:
            import ctypes
            if ctypes.windll.shell32.IsUserAnAdmin():
                return
        except:
            pass
    else:
        if os.geteuid() == 0:  # type: ignore
            return
    raise RuntimeError("User is not admin")
