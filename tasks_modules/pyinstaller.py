# tasks_modules\pyinstaller.py

import re

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import locales

APP_FOLDER = Path(f"dist/{PROJECT_NAME}")


def parse_manifest_includes() -> list[str]:
    add_data_list = []
    if not MANIFEST_IN_PATH.exists():
        raise RuntimeError(f"Manifest file '{MANIFEST_IN_PATH}' not exists")
    for line in MANIFEST_IN_PATH.read_text().splitlines():
        match = re.match(r"^[\s]*include[\s]+(.+)", line)
        if match:
            add_data_list.extend([filepath.strip() for filepath in match.group(1).split()])
            continue

        match = re.match(r"^[\s]*recursive-include[\s]+([^\s]+)", line)
        if match:
            add_data_list.append(match.group(1).strip())
            continue
    return add_data_list


@task
def mkdirs(c: InvokeContext):
    _config.mkdir([
        "dist",
        APP_FOLDER,
    ])


@task(pre=[mkdirs])
def clean_exe(c: InvokeContext):
    _config.remove_path(str(APP_FOLDER))


@task(pre=[mkdirs, locales.build])
def copy_includes(c: InvokeContext):
    print("[bold]Copying MANIFEST.in includes ...[/]")
    for include in parse_manifest_includes():
        include_path = Path(include)
        dest_path = APP_FOLDER / "_internal" / PROJECT_NAME / include_path.name
        _config.copy(src=include_path, dst=dest_path)
    print("[bold]Copying MANIFEST.in includes ... [/][bold green]OK[/]")


@task(pre=[clean_exe,], post=[copy_includes,])
def build(c: InvokeContext):
    MAIN_PATH = Path(rf"src/{PROJECT_NAME}/__main__.py")

    print(f"[bold] Building Pyinstaller (EXE) ... [/]")
    cmd_list = [
        "pdm", "run", "pyinstaller", f'"{MAIN_PATH}"',
        "--name", f'"{PROJECT_NAME}"',
        "--icon", f'"{ICON_APP}"',
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
    APP_EXE = APP_FOLDER / f"{PROJECT_NAME}.exe"
    result = c.run(f'"{APP_EXE}" -V')
    assert (result is not None) and (result.return_code == 0)
    assert PROJECT_VERSION in result.stdout
