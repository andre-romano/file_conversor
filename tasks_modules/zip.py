# tasks_modules\zip.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import pyinstaller, base

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
    ])


@task(pre=[mkdirs])
def clean_zip(c: InvokeContext):
    _config.remove_path(f"{INSTALL_APP_WIN}")
    _config.remove_path(f"{INSTALL_APP_LIN}")
    _config.remove_path(f"{INSTALL_APP_MAC}")


@task(pre=[clean_zip, pyinstaller.check,], post=[pyinstaller.clean_app_folder,])
def build(c: InvokeContext):
    print(f"[bold] Building archive '{INSTALL_APP_CURR}' ... [/]")
    _config.compress(src=pyinstaller.APP_FOLDER, dst=INSTALL_APP_CURR)
    if not INSTALL_APP_CURR.exists():
        raise RuntimeError(f"'{INSTALL_APP_CURR}' not found")
    print(f"[bold] Building archive '{INSTALL_APP_CURR}' ... [/][bold green]OK[/]")


@task(pre=[build,],)
def extract_app(c: InvokeContext):
    print(rf'[bold] Extracting {INSTALL_APP_CURR} ... [/]')
    _config.extract(src=INSTALL_APP_CURR, dst=pyinstaller.APP_FOLDER.parent)
    if not pyinstaller.APP_FOLDER.exists():
        raise RuntimeError(f"'{pyinstaller.APP_FOLDER}' not found")
    print(rf'[bold] Extracting {INSTALL_APP_CURR} ... [/][bold green]OK[/]')


@task
def unextract_app(c: InvokeContext):
    print(rf'[bold] Removing extracted path {INSTALL_APP_CURR} ... [/]')
    _config.remove_path(str(pyinstaller.APP_FOLDER))
    print(rf'[bold] Removing extracted path {INSTALL_APP_CURR} ... [/][bold green]OK[/]')


@task(pre=[extract_app,], post=[unextract_app,])
def check(c: InvokeContext):
    pyinstaller.check(c)
