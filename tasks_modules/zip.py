# tasks_modules\zip.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import base, embedpy

BUILD_DIR = embedpy.BUILD_DIR

APP_EXE = embedpy.PORTABLE_SHIM_BAT
APP_GUI_EXE = embedpy.PORTABLE_SHIM_VBS

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


@task(pre=[clean_zip, embedpy.check],)
def build(c: InvokeContext):
    print(f"[bold] Building archive '{INSTALL_APP_CURR}' ... [/]")

    human_size, size_bytes_orig = get_dir_size(BUILD_DIR)
    print(f"Size BEFORE compression: {human_size} ({BUILD_DIR})")

    _config.compress(src=BUILD_DIR, dst=INSTALL_APP_CURR)
    if not INSTALL_APP_CURR.exists():
        raise RuntimeError(f"'{INSTALL_APP_CURR}' not found")

    human_size, size_bytes_final = get_dir_size(INSTALL_APP_CURR)
    print(f"Size AFTER compression: {human_size} (-{100 - (size_bytes_final / size_bytes_orig * 100):.2f}%)")
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
