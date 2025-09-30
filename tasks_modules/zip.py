# tasks_modules\zip.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import base, pyinstaller

BUILD_DIR = Path("build") / PROJECT_NAME
APP_EXE = BUILD_DIR / pyinstaller.APP_EXE.name

if base.WINDOWS:
    INSTALL_APP_CURR = INSTALL_APP_WIN
elif base.LINUX:
    INSTALL_APP_CURR = INSTALL_APP_LIN
else:
    INSTALL_APP_CURR = INSTALL_APP_MAC


@task
def mkdirs(c: InvokeContext):
    _config.mkdir([
        "dist",
        "build",
    ])


@task(pre=[mkdirs])
def clean_build(c: InvokeContext):
    remove_path(f"build/*")


@task(pre=[mkdirs])
def clean_zip(c: InvokeContext):
    _config.remove_path(f"{INSTALL_APP_WIN}")
    _config.remove_path(f"{INSTALL_APP_LIN}")
    _config.remove_path(f"{INSTALL_APP_MAC}")


@task(pre=[pyinstaller.check],)
def move_pyinstaller_to_build(c: InvokeContext):
    clean_build(c)
    _config.move(src=pyinstaller.APP_FOLDER, dst=BUILD_DIR)


@task(pre=[clean_zip, move_pyinstaller_to_build],)
def build(c: InvokeContext):
    print(f"[bold] Building archive '{INSTALL_APP_CURR}' ... [/]")
    _config.compress(src=BUILD_DIR, dst=INSTALL_APP_CURR)
    if not INSTALL_APP_CURR.exists():
        raise RuntimeError(f"'{INSTALL_APP_CURR}' not found")
    print(f"[bold] Building archive '{INSTALL_APP_CURR}' ... [/][bold green]OK[/]")


@task(pre=[build,],)
def extract_app(c: InvokeContext):
    print(rf'[bold] Extracting {INSTALL_APP_CURR} ... [/]')
    _config.remove_path(str(BUILD_DIR))
    _config.extract(src=INSTALL_APP_CURR, dst=BUILD_DIR.parent)
    if not BUILD_DIR.exists():
        raise RuntimeError(f"'{BUILD_DIR}' not found")
    print(rf'[bold] Extracting {INSTALL_APP_CURR} ... [/][bold green]OK[/]')


@task(pre=[extract_app,])
def check(c: InvokeContext):
    print("[bold] Checking .ZIP ... [/]")
    if not base.WINDOWS:
        c.run(f"chmod +rx {APP_EXE.resolve()}")
    result = c.run(f"{APP_EXE.resolve()} --version")
    assert (result is not None) and (result.return_code == 0)
    print("[bold] Checking .ZIP ... [/][bold green]OK[/]")
