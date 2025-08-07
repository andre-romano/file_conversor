
# tasks_modules\choco.py

import re
from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

CHOCO_PATH = str("choco")
CHOCO_NUSPEC = Path(f"{CHOCO_PATH}/{PROJECT_NAME}.nuspec")

CHOCO_DEPS = {
    "python": ""
}


@task
def mkdirs(c):
    _config.mkdir([
        CHOCO_PATH,
        "dist",
    ])


@task(pre=[mkdirs])
def clean_choco(c):
    remove_path(f"{CHOCO_PATH}/*")


@task(pre=[mkdirs])
def clean_nupkg(c):
    remove_path("dist/*.nupkg")


@task(pre=[clean_choco, ])
def create_manifest(c):
    """Update choco files, based on pyproject.toml"""

    print("[bold] Updating Chocolatey manifest files ... [/]", end="")
    CHOCO_TOOLS_PATH = Path(f"{CHOCO_PATH}/tools")
    CHOCO_TOOLS_PATH.mkdir(parents=True, exist_ok=True)

    # chocolateyInstall.ps1
    install_ps1_path = Path(f"{CHOCO_TOOLS_PATH}/chocolateyInstall.ps1")
    install_ps1_path.write_text(rf'''
$ErrorActionPreference = 'Stop'

$packageName = "{PROJECT_NAME}"
$version     = "{PROJECT_VERSION}" 
$toolsDir    = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
$installer   = "$toolsDir\{INSTALL_APP_PY.name}"
$url         = "{INSTALL_APP_URL}"
$checksum    = "{_config.gen_sha256(INSTALL_APP_PY)}"  # SHA256

Get-ChocolateyWebFile -PackageName "$packageName" `
                      -FileFullPath "$installer" `
                      -Url "$url" `
                      -Checksum "$checksum" `
                      -ChecksumType "sha256"

Write-Output "Installing app ..."
& python "$installer" -i --version "$version"                                     
''', encoding="utf-8")

    # chocolateyUninstall.ps1
    uninstall_ps1_path = Path(f"{CHOCO_TOOLS_PATH}/chocolateyUninstall.ps1")
    uninstall_ps1_path.write_text(rf"""
$ErrorActionPreference = 'Stop'

$packageName = "{PROJECT_NAME}"
$version     = "{PROJECT_VERSION}" 
$toolsDir    = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
$installer   = "$toolsDir\{INSTALL_APP_PY.name}"
$url         = "{INSTALL_APP_URL}"
$checksum    = "{_config.gen_sha256(INSTALL_APP_PY)}"  # SHA256

Get-ChocolateyWebFile -PackageName "$packageName" `
                      -FileFullPath "$installer" `
                      -Url "$url" `
                      -Checksum "$checksum" `
                      -ChecksumType "sha256"

Write-Output "Uninstalling app ..."
& python "$installer" -u --version "$version"
""", encoding="utf-8")

    # PACKAGE.nuspec
    CHOCO_NUSPEC.write_text(f"""<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://schemas.microsoft.com/packaging/2015/06/nuspec.xsd">
  <metadata>
    <id>{PROJECT_NAME}</id>
    <version>{PROJECT_VERSION}</version>
    <title>{PROJECT_TITLE}</title>
    <authors>{", ".join(PROJECT_AUTHORS)}</authors>
    <description>{PROJECT_DESCRIPTION}</description>
    <tags>{" ".join(PROJECT_KEYWORDS)}</tags>
    <iconUrl>http://rawcdn.githack.com/andre-romano/{PROJECT_NAME}/master/{ICONS_PATH}/icon.png</iconUrl>
    <projectUrl>{PROJECT_HOMEPAGE}</projectUrl>
    <projectSourceUrl>{PROJECT_HOMEPAGE}</projectSourceUrl>
    <licenseUrl>{PROJECT_HOMEPAGE}/blob/master/LICENSE</licenseUrl>
    <releaseNotes>{PROJECT_HOMEPAGE}/blob/master/CHANGELOG.md</releaseNotes>
    <requireLicenseAcceptance>false</requireLicenseAcceptance>
    <dependencies>
        {"\n        ".join(f'<dependency id="{dep}" ' + (f'version="{version}" ' if version else '') + "/>" for dep, version in CHOCO_DEPS.items())}
    </dependencies>
  </metadata>
  <files>
    <file src="tools\\**" target="tools" />
  </files>  
</package>
""", encoding="utf-8")
    print("[bold green]OK[/]")


@task
def install(c):
    if shutil.which("choco"):
        return
    print("[bold] Installing Chocolatey ... [/]")
    if not INSTALL_CHOCO.exists():
        raise RuntimeError(f"Install Choco - Script {INSTALL_CHOCO} does not exist")
    c.run(f'powershell.exe -ExecutionPolicy Bypass -File "{INSTALL_CHOCO}"')
    if not shutil.which("choco"):
        raise RuntimeError("'choco' not found in PATH")


@task(pre=[clean_nupkg, create_manifest, install,])
def build(c):
    if not CHOCO_NUSPEC.exists():
        raise RuntimeError(f"Nuspec file '{CHOCO_NUSPEC}' not found!")

    print(f"[bold] Building choco package ... [/]")
    c.run(f"choco pack -y --outdir dist/ {CHOCO_NUSPEC}")
    if not list(Path("dist").glob("*.nupkg")):
        raise RuntimeError("Build CHOCO - Empty dist/*.nupkg")
    print(f"[bold] Building choco package ... [/][bold green]OK[/]")


@task(pre=[build,])
def check(c):
    print(f"[bold] Test choco package ... [/]")
    c.run(f"choco install -y {PROJECT_NAME} --source-dir=./dist")
    print(f"[bold] Test choco package ... [/][bold green]OK[/]")

    print(f"[bold] Cleaning choco tests ... [/]")
    c.run(f"choco uninstall -y {PROJECT_NAME} --source-dir=./dist")
    print(f"[bold] Cleaning choco tests ... [/][bold green]OK[/]")
