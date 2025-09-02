
# tasks_modules\choco.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *
from tasks_modules._deps import *

from tasks_modules import base

CHOCO_PATH = str("choco")
CHOCO_NUSPEC = Path(f"{CHOCO_PATH}/{PROJECT_NAME}.nuspec")


@task
def mkdirs(c: InvokeContext):
    _config.mkdir([
        CHOCO_PATH,
        "dist",
    ])


@task(pre=[mkdirs])
def clean_choco(c: InvokeContext):
    remove_path(f"{CHOCO_PATH}/*")


@task(pre=[mkdirs])
def clean_nupkg(c: InvokeContext):
    remove_path("dist/*.nupkg")


@task(pre=[clean_choco, ])
def create_manifest(c: InvokeContext):
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
$dir         = Join-Path ${{env:ProgramFiles(x86)}} "$packageName"
$url         = "{INSTALL_APP_WIN_EXE_URL}"
$checksum    = "{_config.get_remote_hash(INSTALL_APP_WIN_EXE_URL)}"  # SHA256

Write-Output "Installing app ..."
Install-ChocolateyPackage -PackageName $packageName `
    -FileType "exe" `
    -SilentArgs "/DIR=`"$dir`" /SUPPRESSMSGBOXES /VERYSILENT /NORESTART /SP-" `
    -Url $url `
    -Checksum $checksum `
    -ChecksumType "sha256"

Write-Output "Installing shim ..."
$exePath = Join-Path $dir "{PROJECT_NAME}.exe"
Install-BinFile -Name "{PROJECT_NAME}" -Path $exePath
''', encoding="utf-8")
    assert install_ps1_path.exists()

    # chocolateyUninstall.ps1
    uninstall_ps1_path = Path(f"{CHOCO_TOOLS_PATH}/chocolateyUninstall.ps1")
    uninstall_ps1_path.write_text(rf"""
$ErrorActionPreference = 'Stop'

$packageName = "{PROJECT_NAME}"
$version     = "{PROJECT_VERSION}" 
$toolsDir    = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
$dir         = Join-Path ${{env:ProgramFiles(x86)}} "$packageName"
$uninstaller = Join-Path "$dir" "{UNINSTALL_APP_WIN.name}"

Write-Output "Removing shim ..."
Uninstall-BinFile -Name "{PROJECT_NAME}"

Write-Output "Uninstalling app ..."
Start-Process -FilePath "$uninstaller" -ArgumentList "/SUPPRESSMSGBOXES", "/VERYSILENT", "/NORESTART", "/SP-" -Wait
""", encoding="utf-8")
    assert uninstall_ps1_path.exists()

    # PACKAGE.nuspec
    CHOCO_NUSPEC.write_text(f"""<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://schemas.microsoft.com/packaging/2015/06/nuspec.xsd">
  <metadata>
    <id>{PROJECT_NAME}</id>
    <version>{PROJECT_VERSION}</version>
    <title>{PROJECT_TITLE}</title>
    <authors>{", ".join(PROJECT_AUTHORS)}</authors>
    <description>{_config.get_url(README_URL).decode("utf-8")}</description>
    <summary>{PROJECT_DESCRIPTION}</summary>
    <tags>{" ".join(PROJECT_KEYWORDS)}</tags>
    <iconUrl>http://rawcdn.githack.com/andre-romano/{PROJECT_NAME}/master/{ICONS_PATH}/icon.png</iconUrl>
    <projectSourceUrl>{PROJECT_HOMEPAGE}</projectSourceUrl>
    <packageSourceUrl>{SOURCE_URL}</packageSourceUrl>
    <licenseUrl>{LICENSE_URL}</licenseUrl>
    <releaseNotes>{RELEASE_NOTES_URL}</releaseNotes>
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
    assert CHOCO_NUSPEC.exists()

    print("[bold green]OK[/]")

    print(f"{install_ps1_path}:")
    print(install_ps1_path.read_text())

    print(f"{uninstall_ps1_path}:")
    print(uninstall_ps1_path.read_text())

    print(f"{CHOCO_NUSPEC}:")
    print(CHOCO_NUSPEC.read_text())


@task
def install(c: InvokeContext):
    if shutil.which("choco"):
        return
    print("[bold] Installing Chocolatey ... [/]")
    if not INSTALL_CHOCO.exists():
        raise RuntimeError(f"Install Choco - Script {INSTALL_CHOCO} does not exist")
    c.run(f'powershell.exe -ExecutionPolicy Bypass -File "{INSTALL_CHOCO}"')
    if not shutil.which("choco"):
        raise RuntimeError("'choco' not found in PATH")


@task(pre=[clean_nupkg, create_manifest, install,])
def build(c: InvokeContext):
    if not CHOCO_NUSPEC.exists():
        raise RuntimeError(f"Nuspec file '{CHOCO_NUSPEC}' not found!")

    print(f"[bold] Building choco package ... [/]")
    result = c.run(f"choco pack -y --outdir dist/ {CHOCO_NUSPEC}")
    assert (result is not None) and (result.return_code == 0)
    if not list(Path("dist").glob("*.nupkg")):
        raise RuntimeError("Build CHOCO - Empty dist/*.nupkg")
    print(f"[bold] Building choco package ... [/][bold green]OK[/]")


@task(pre=[build, base.is_admin,],)
def install_app(c: InvokeContext):
    print(rf'[bold] Installing choco package ... [/]')
    dist_path = Path(rf".\dist")
    result = c.run(rf'choco install -y --acceptlicense "{PROJECT_NAME}" --version="{PROJECT_VERSION}" --source="{dist_path}"')
    assert (result is not None) and (result.return_code == 0)
    print(rf'[bold] Installing choco package ... [/][bold green]OK[/]')


@task(pre=[base.is_admin,])
def uninstall_app(c: InvokeContext):
    print(rf'[bold] Uninstalling choco package ... [/]')
    result = c.run(rf'choco uninstall -y "{PROJECT_NAME}"')
    assert (result is not None) and (result.return_code == 0)
    print(rf'[bold] Uninstalling choco package ... [/][bold green]OK[/]')


@task(pre=[install_app,], post=[uninstall_app,])
def check(c: InvokeContext):
    base.check(c)


@task(pre=[build,])
def publish(c: InvokeContext):
    print(rf'[bold] Publihsing choco package ... [/]')
    nupkg_path = list(Path("dist").glob("*.nupkg"))[0]
    result = c.run(rf'choco push {nupkg_path} --source https://push.chocolatey.org/')
    assert (result is not None) and (result.return_code == 0)
    print(rf'[bold] Publihsing choco package ... [/][bold green]OK[/]')
