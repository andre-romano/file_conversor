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
    "python": ""
}


@task
def mkdirs(c):
    _config.mkdir([
        SCOOP_PATH,
    ])


@task(pre=[mkdirs])
def clean_scoop(c):
    remove_path(f"{SCOOP_PATH}/*")


@task(pre=[clean_scoop, base.publish_install_script, ])
def create_manifest(c):
    """Update choco files, based on pyproject.toml"""

    print("[bold] Updating Scoop manifest files ... [/]", end="")

    if not INSTALL_APP_PY.exists():
        raise RuntimeError(f"File '{INSTALL_APP_PY}' not found!")

    # bucket/file_conersor.json
    SCOOP_JSON.write_text(json.dumps({
        "version": PROJECT_VERSION,
        "description": PROJECT_DESCRIPTION,
        "homepage": PROJECT_HOMEPAGE,
        "license": "Apache-2.0",
        "depends": list(SCOOP_DEPS.keys()),
        "url": INSTALL_APP_URL,
        "hash": f"{_config.get_remote_hash(INSTALL_APP_URL)}",
        "bin": [
            f"{INSTALL_APP_PY.name}.cmd",
        ],
        "installer": {
            "script": [
                f"python3 \"$dir\\{INSTALL_APP_PY.name}\" -i --version $version",
            ]
        },
        "uninstaller": {
            "script": [
                f"python3 \"$dir\\{INSTALL_APP_PY.name}\" -u --version $version"
            ]
        },
        "checkver": {
            "github": PROJECT_HOMEPAGE,
        },
        "autoupdate": {
            "url": INSTALL_APP_URL,
        }
    }, indent=4), encoding="utf-8")
    if not SCOOP_JSON.exists():
        raise FileNotFoundError(f"File '{SCOOP_JSON}' not found!")

    print("[bold green] OK [/]",)


@task
def install(c):
    if shutil.which("scoop"):
        return
    print("[bold] Installing Scoop ... [/]")
    if not INSTALL_SCOOP.exists():
        raise RuntimeError(f"Install Scoop - Script {INSTALL_SCOOP} does not exist")
    c.run(f'powershell.exe -ExecutionPolicy Bypass -File "{INSTALL_SCOOP}"')
    if not shutil.which("scoop"):
        raise RuntimeError("'scoop' not found in PATH")


@task(pre=[create_manifest, install,])
def build(c):
    pass


@task(pre=[build,])
def publish(c):
    print(f"[bold] Publishing to Scoop (using GitHub) ... [/]")
    result = c.run(f'git status', hide=True)
    if Path(SCOOP_PATH).name not in result.stdout:
        print(f"[bold] Skipping publish: no changes in bucket file. [/]")
        return
    c.run(f'git add "{SCOOP_PATH}"', hide=True)
    c.run(f'git commit -m "ci: scoop bucket {GIT_RELEASE}"', hide=True)
    c.run(f'git push')
    print(f"[bold] Publishing to Scoop (using GitHub) ... OK [/]")


@task(pre=[install,])
def add_bucket(c):
    result = c.run(f'scoop bucket list "{SCOOP_PATH}"', hide=True)
    if PROJECT_HOMEPAGE in result.stdout:
        print(f"[bold] {PROJECT_NAME} bucket already in Scoop [/]")
        return
    print(f"[bold] Adding bucket '{PROJECT_NAME}' to Scoop ... [/]")
    c.run(f'scoop bucket add "{PROJECT_NAME}" "{PROJECT_HOMEPAGE}"')
    print(f"[bold] Adding bucket '{PROJECT_NAME}' to Scoop ... OK [/]")


@task(pre=[install,])
def rm_bucket(c):
    result = c.run(f'scoop bucket list "{SCOOP_PATH}"', hide=True)
    if not PROJECT_HOMEPAGE in result.stdout:
        print(f"[bold] {PROJECT_NAME} bucket NOT in Scoop [/]")
        return
    print(f"[bold] Removing bucket from Scoop ... [/]")
    c.run(f'scoop bucket rm "{PROJECT_NAME}"')
    print(f"[bold] Removing bucket from Scoop ... OK [/]")


@task(pre=[add_bucket,],)
def install_app(c):
    print(f"[bold] Installing scoop package ... [/]")
    c.run(f"scoop install {PROJECT_NAME}")
    print(f"[bold] Installing scoop package ... [/][bold green]OK[/]")


@task(post=[rm_bucket,],)
def uninstall_app(c):
    print(f"[bold] Uninstalling scoop package ... [/]")
    c.run(f"scoop uninstall {PROJECT_NAME}")
    print(f"[bold] Uninstalling scoop package ... [/][bold green]OK[/]")


@task(pre=[install_app,], post=[uninstall_app,])
def check(c):
    if not shutil.which(PROJECT_NAME):
        raise RuntimeError(f"'{PROJECT_NAME}' not found in PATH")
