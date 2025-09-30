# tasks_modules\pyinstaller.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config, base
from tasks_modules._config import *

from tasks_modules import locales

APP_FOLDER = Path(f"dist/{PROJECT_NAME}")
APP_EXE = APP_FOLDER / (f"{PROJECT_NAME}" if not base.WINDOWS else f"{PROJECT_NAME}.exe")


@task
def mkdirs(c: InvokeContext):
    _config.mkdir([
        "build",
        "dist",
        f"{APP_FOLDER}",
    ])


@task(pre=[mkdirs])
def clean_app_folder(c: InvokeContext):
    _config.remove_path(str(APP_FOLDER))


@task(pre=[mkdirs, locales.build])
def copy_dependencies(c: InvokeContext):
    print("[bold]Copying dependencies into pyinstaller ...[/]")
    SITE_PACKAGES = APP_FOLDER / "_internal"

    # cmd_list = [
    #     "pip",
    #     "install",
    #     "-t", f"{SITE_PACKAGES}",
    #     "--compile",
    #     "--no-warn-script-location",
    #     "--exists-action=w",
    #     "--upgrade",
    #     ".",
    # ]
    # print(rf"$ {cmd_list}")
    # result = c.run(" ".join(cmd_list))
    # assert (result is not None) and (result.return_code == 0)

    print("[bold]Copying dependencies into pyinstaller ... [/][bold green]OK[/]")


@task(pre=[clean_app_folder,], post=[copy_dependencies,])
def build(c: InvokeContext):
    SHIM_PATH = Path(rf"src/{PROJECT_NAME}/__shim__.py")

    print(f"[bold] Building Pyinstaller (EXE) ... [/]")
    cmd_list = [
        "pdm", "run", "pyinstaller", f'"{SHIM_PATH}"',
        "--name", f'"{PROJECT_NAME}"',
        "--icon", f'"{ICON_APP}"',
        "--additional-hooks-dir=hooks",
        "--clean",
        "--onedir",
    ]
    print(rf"$ {cmd_list}")
    # sys.exit(0)
    result = c.run(" ".join(cmd_list))
    assert (result is not None) and (result.return_code == 0)

    if not APP_FOLDER.exists():
        raise RuntimeError(f"Not found '{APP_FOLDER}'")
    print(f"[bold] Building Pyinstaller (EXE) ... [/][bold green]OK[/]")


@task(pre=[build,],)
def check(c: InvokeContext):
    base.check(c, exe=APP_FOLDER / f"{PROJECT_NAME}")
