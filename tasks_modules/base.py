# tasks_modules\base.py

import os
import platform

from invoke.tasks import task

from pathlib import Path

# user provided
from tasks_modules import _config, locales
from tasks_modules._config import *

WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MACOS = (platform.system() == "Darwin")


@task
def mkdirs(c: InvokeContext):
    dirs = [
        "build",
        "dist",
        f"{CACHE_DIR}",
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
def clean_cache(c: InvokeContext):
    remove_path(f"{CACHE_DIR}/*")


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


@task(pre=[mkdirs])
def clean_requirements(c: InvokeContext):
    remove_path(f"requirements.txt")


@task(pre=[clean_logs,
           clean_build,
           clean_dist,
           clean_cache,
           clean_htmlcov,
           clean_docs,
           clean_changelog,
           ])
def clean(c: InvokeContext):
    pass


@task(pre=[clean_requirements,])
def requirements(c: InvokeContext, prod: bool = True):
    print("[bold]Generating requirements.txt ... [/]")
    result = c.run(f"pdm export -f requirements --without-hashes {'--prod' if prod else ''} > requirements.txt")
    assert (result is not None) and (result.return_code == 0)
    print("[bold]Generating requirements.txt ... [/][bold green]OK[/]")


@task(pre=[clean_htmlcov, locales.build,])
def tests(c: InvokeContext, args: str = ""):
    print("[bold] Running tests ... [/]")
    result = c.run(f"pdm run pytest {args.strip()}")
    assert (result is not None) and (result.return_code == 0)
    print("[bold] Running tests ... [/][bold green]OK[/]")


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
def check(c: InvokeContext, exe: str | Path = ""):
    exe = exe if exe else PROJECT_NAME
    print(f"[bold] Checking app '{exe}' ... [/]")
    app_exe = shutil.which(exe)
    if not app_exe:
        raise RuntimeError(f"'{exe}' not found in PATH")
    print(f"[bold] Found:[/] '{app_exe}'")
    result = c.run(f'"{app_exe}" -V')
    assert result is not None
    if PROJECT_VERSION not in result.stdout:
        raise RuntimeError(f"'{exe}' version mismatch. Expected: '{PROJECT_VERSION}'.")
    assert result.return_code == 0
    print(f"[bold] Checking app '{exe}' ... [/][bold green]OK[/]")


@task
def is_admin(c: InvokeContext):
    print(f"[bold] Checking for admin rights ... [/]")
    if WINDOWS:
        try:
            import ctypes
            if ctypes.windll.shell32.IsUserAnAdmin():  # pyright: ignore[reportAttributeAccessIssue]
                return
        except:
            pass
    else:
        if os.geteuid() == 0:  # type: ignore
            return
    raise RuntimeError("User is not admin")
