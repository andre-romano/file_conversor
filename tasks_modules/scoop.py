# tasks_modules\scoop.py

import json
from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config, base, zip
from tasks_modules._config import *
from tasks_modules._deps import *

SCOOP_PATH = Path("bucket")
SCOOP_JSON = SCOOP_PATH / f"{PROJECT_NAME}.json"

SCOOP_APP_EXE = zip.APP_EXE


@task
def mkdirs(c: InvokeContext):
    _config.mkdir([
        f"{SCOOP_PATH}",
    ])


@task(pre=[mkdirs])
def clean_scoop(c: InvokeContext):
    remove_path(f"{SCOOP_PATH}/*")


@task(pre=[clean_scoop, ])
def manifest(c: InvokeContext):
    """Update choco files, based on pyproject.toml"""

    print("[bold] Updating Scoop manifest files ... [/]", end="")

    INSTALL_APP_AUTOUPDATE = INSTALL_APP_WIN_EXE_URL.replace(PROJECT_VERSION, "$version")

    # bucket/file_conersor.json
    json_obj = {
        "version": PROJECT_VERSION,
        "description": PROJECT_DESCRIPTION,
        "homepage": PROJECT_HOMEPAGE,
        "license": "Apache-2.0",
        "url": INSTALL_APP_WIN_EXE_URL,
        "hash": f"{_config.get_remote_hash(INSTALL_APP_WIN_EXE_URL)}",
        "bin": f"{SCOOP_APP_EXE}",
        "pre_install": [
            rf'$exePath = Get-ChildItem -Path "$dir" -Filter *-Installer.exe  | Select-Object -ExpandProperty FullName',
            rf'Start-Process -FilePath "$exePath" -ArgumentList "/DIR=$dir", "/CURRENTUSER", "/SUPPRESSMSGBOXES", "/VERYSILENT", "/NORESTART", "/SP-" -Wait',
            rf'if (!(Test-Path "$dir\{SCOOP_APP_EXE}")) {{throw "Install failed: executable {SCOOP_APP_EXE} not found"}}',
            rf'Remove-Item -Path "$exePath"',
        ],
        "pre_uninstall": [
            rf'$exePath = Get-ChildItem -Path "$dir" -Filter {UNINSTALL_APP_WIN.name}  | Select-Object -ExpandProperty FullName',
            rf'Start-Process -FilePath "$exePath" -ArgumentList "/SUPPRESSMSGBOXES", "/VERYSILENT", "/NORESTART", "/SP-" -Wait',
            rf'if (Test-Path "$dir\{SCOOP_APP_EXE}") {{throw "Uninstall failed: executable still exists"}}',
        ],
        "checkver": {
            "github": PROJECT_HOMEPAGE,
        },
        "autoupdate": {
            "url": f"{INSTALL_APP_AUTOUPDATE}",
            "hash": {
                "url": f"{INSTALL_APP_AUTOUPDATE.replace(".exe", INSTALL_APP_HASH.suffix)}"
            }
        }
    }
    if SCOOP_DEPS:
        json_obj["depends"] = list(SCOOP_DEPS.keys())
    SCOOP_JSON.write_text(json.dumps(json_obj, indent=4) + "\n", encoding="utf-8")
    assert SCOOP_JSON.exists()

    print("[bold green] OK [/]",)

    print(f"{SCOOP_JSON}:")
    print(SCOOP_JSON.read_text())


@task
def install(c: InvokeContext):
    if shutil.which("scoop"):
        return
    print("[bold] Installing Scoop ... [/]")
    assert INSTALL_SCOOP.exists()
    c.run(f'powershell.exe -ExecutionPolicy Bypass -File "{INSTALL_SCOOP}"')
    if not shutil.which("scoop"):
        raise RuntimeError("'scoop' not found in PATH")


@task(pre=[manifest,])
def build(c: InvokeContext):
    pass


@task(pre=[build, install],)
def install_app(c: InvokeContext):
    print(f"[bold] Installing scoop package ... [/]")
    result = c.run(rf'scoop install "{SCOOP_JSON}"')
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Installing scoop package ... [/][bold green]OK[/]")


@task(pre=[install])
def uninstall_app(c: InvokeContext):
    print(f"[bold] Uninstalling scoop package ... [/]")
    result = c.run(rf'scoop uninstall "{PROJECT_NAME}"')
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Uninstalling scoop package ... [/][bold green]OK[/]")


@task(pre=[install_app,], post=[uninstall_app,])
def check(c: InvokeContext):
    base.check(c)


@task(pre=[build,])
def publish(c: InvokeContext):
    print(f"[bold] Publishing to Scoop (using GitHub) ... [/]")

    git_commit_push(c, SCOOP_PATH, message=f"ci: scoop bucket {GIT_RELEASE}")

    print(f"[bold] Publishing to Scoop (using GitHub) ... OK [/]")
