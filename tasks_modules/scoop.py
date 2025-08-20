# tasks_modules\choco.py

import json
from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import base

SCOOP_PATH = str("bucket")
SCOOP_JSON = Path(f"{SCOOP_PATH}/{PROJECT_NAME}.json")

SCOOP_DEPS = {
    # "python": ""
}


@task
def mkdirs(c: InvokeContext):
    _config.mkdir([
        SCOOP_PATH,
    ])


@task(pre=[mkdirs])
def clean_scoop(c: InvokeContext):
    remove_path(f"{SCOOP_PATH}/*")


@task(pre=[clean_scoop, ])
def manifest(c: InvokeContext):
    """Update choco files, based on pyproject.toml"""

    print("[bold] Updating Scoop manifest files ... [/]", end="")

    INSTALL_APP_AUTOUPDATE = INSTALL_APP_URL.replace(PROJECT_VERSION, "$version")

    # bucket/file_conersor.json
    SCOOP_JSON.write_text(json.dumps({
        "version": PROJECT_VERSION,
        "description": PROJECT_DESCRIPTION,
        "homepage": PROJECT_HOMEPAGE,
        "license": "Apache-2.0",
        "depends": list(SCOOP_DEPS.keys()),
        "url": INSTALL_APP_URL,
        "hash": f"{_config.get_remote_hash(INSTALL_APP_URL)}",
        "bin": f"{PROJECT_NAME}.exe",
        "pre_install": [
            rf'$exePath = Get-ChildItem -Path "$dir" -Filter *-Installer.exe  | Select-Object -ExpandProperty FullName',
            rf'Start-Process -FilePath "$exePath" -ArgumentList "/DIR=$dir", "/SUPPRESSMSGBOXES", "/VERYSILENT", "/NORESTART", "/SP-" -Wait',
            rf'if (!(Test-Path "$dir\{PROJECT_NAME}.exe")) {{throw "Install failed: executable {PROJECT_NAME}.exe not found"}}',
            rf'Remove-Item -Path "$exePath"',
        ],
        "pre_uninstall": [
            rf'$exePath = Get-ChildItem -Path "$dir" -Filter {UNINSTALL_APP.name}  | Select-Object -ExpandProperty FullName',
            rf'Start-Process -FilePath "$exePath" -ArgumentList "/SUPPRESSMSGBOXES", "/VERYSILENT", "/NORESTART", "/SP-" -Wait',
            rf'if (Test-Path "$dir\{PROJECT_NAME}.exe") {{throw "Uninstall failed: executable still exists"}}',
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
    }, indent=4), encoding="utf-8")
    assert SCOOP_JSON.exists()

    print("[bold green] OK [/]",)


@task
def install(c: InvokeContext):
    if shutil.which("scoop"):
        return
    print("[bold] Installing Scoop ... [/]")
    assert INSTALL_SCOOP.exists()
    c.run(f'powershell.exe -ExecutionPolicy Bypass -File "{INSTALL_SCOOP}"')
    if not shutil.which("scoop"):
        raise RuntimeError("'scoop' not found in PATH")


@task(pre=[manifest, install,])
def build(c: InvokeContext):
    pass


@task(pre=[build,],)
def install_app(c: InvokeContext):
    print(f"[bold] Installing scoop package ... [/]")
    result = c.run(rf'scoop install "{SCOOP_JSON}"')
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Installing scoop package ... [/][bold green]OK[/]")


@task
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
    result = c.run(f'git status', hide=True)
    assert (result is not None) and (result.return_code == 0)
    if Path(SCOOP_PATH).name not in result.stdout:
        print(f"[bold] Skipping publish: no changes in bucket file. [/]")
        return
    result = c.run(f'git add "{SCOOP_PATH}"', hide=True)
    assert (result is not None) and (result.return_code == 0)

    result = c.run(f'git commit -m "ci: scoop bucket {GIT_RELEASE}"', hide=True)
    assert (result is not None) and (result.return_code == 0)

    result = c.run(f'git push')
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Publishing to Scoop (using GitHub) ... OK [/]")
