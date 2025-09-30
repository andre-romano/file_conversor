
# tasks_modules\choco.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config, base, zip
from tasks_modules._config import *
from tasks_modules._deps import *

VAGRANT_PATH = Path(f"vagrant")

CHOCO_PATH = str("choco")
CHOCO_NUSPEC = Path(f"{CHOCO_PATH}/{PROJECT_NAME}.nuspec")

CHOCO_APP_EXE = Path(zip.APP_EXE.name)  # e.g. PROJECT_NAME.bat

CHOCO_DESCRIPTION = rf"""
A powerful Python-based CLI tool for converting, compressing, and manipulating audio, video, text, document, and image files.

**Summary**:
  - [Usage](#usage)
    - [CLI - Command line interface](#cli---command-line-interface)
    - [Windows Context Menu (Windows OS only)](#windows-context-menu-windows-os-only)
  - [Why use File Conversor?](#why-use-file-conversor)
  - [Features](#features)
  - [External dependencies](#external-dependencies)
  - [Installing](#installing)
    - [For Windows](#for-windows)
    - [For Linux / MacOS](#for-linux--macos)
  - [Contributing \& Support](#contributing--support)
  - [License and Copyright](#license-and-copyright)

## Usage

### CLI - Command line interface

![cli_terminal_demo](https://cdn.jsdelivr.net/gh/andre-romano/file_conversor@master/assets/cli_demo.gif)

Run ``file_conversor -h`` to explore all available commands and options.

### Windows Context Menu (Windows OS only)

1. Right click a file in Windows Explorer
2. Choose an action from "File Conversor" menu

![windows_context_menu](https://cdn.jsdelivr.net/gh/andre-romano/file_conversor@master/assets/ctx_menu.jpg)

## Why use File Conversor?

- Automate repetitive file conversion or compression tasks
- Manipulate various media formats with a single tool
- Integrate seamlessly with scripting workflows
- Configure advanced file processing pipelines

## Features

- **Format Conversion**
  - **Documents**: `docx ⇄ odt`, `docx → pdf`, etc
  - **Spreadsheets**: `xlsx ⇄ ods`, `xlsx → pdf`, etc
  - **Video**: `mkv ⇄ mp4`, `avi ⇄ mp4`, etc.
  - **Images**: `jpg ⇄ png`, `gif ⇄ webp`, `bmp ⇄ tiff`, etc.
  - **Audio**: `mp3 ⇄ m4a`, etc.
  - **Text**: `json ⇄ yaml`, `xml ⇄ json`, etc
  - And more ...

- **Compression**  
  - Optimizes size for formats like MP4, MP3, PDF, JPG, and others.

- **Metadata Inspection**  
  - Retrieves EXIF data from images, stream details from audio/video.

- **File Manipulation**  
  - **PDFs**: split, rotate, encrypt, etc  
  - **Images**: rotate, enhance, and apply other transformations  

- **Batch Processing**  
  - Use pipelines and config files for automation and advanced tasks.

- **Multiple Interfaces**  
  - **Windows Explorer integration**: right-click files for quick actions
  - CLI for scripting and automation  

*For full feature set, check* [`FEATURE_SET.md`](https://github.com/andre-romano/file_conversor/blob/master/FEATURE_SET.md)
"""

if len(CHOCO_DESCRIPTION) >= 4000:
    raise RuntimeError("CHOCO_DESCRIPTION must be < 4000 characters")


def escape_xml(text: str | None) -> str:
    """
    Escape invalid characters for XML.
    """
    if text is None:
        return ""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
    )


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
$exePath = Join-Path $dir "{CHOCO_APP_EXE}"
Install-BinFile -Name "{PROJECT_NAME}" -Path $exePath
''', encoding="utf-8")
    assert install_ps1_path.exists()

    # chocolateyUninstall.ps1
    uninstall_ps1_path = Path(f"{CHOCO_TOOLS_PATH}/chocolateyUninstall.ps1")
    uninstall_ps1_path.write_text(rf"""
$ErrorActionPreference = 'Stop'

$packageName = '{PROJECT_NAME}'

[array]$key = Get-UninstallRegistryKey -SoftwareName '{PROJECT_TITLE}*'

if ($key.Count -eq 1) {{
    $key | ForEach-Object {{
        $packageArgs = @{{
            packageName    = $packageName
            fileType       = 'EXE'
            silentArgs     = '/SUPPRESSMSGBOXES /VERYSILENT /NORESTART /SP-'
            validExitCodes = @(0)
            file           = "$($_.UninstallString)"
        }}

        Uninstall-ChocolateyPackage @packageArgs
        Uninstall-BinFile -Name "$packageName"
    }}
}}
elseif ($key.Count -eq 0) {{
    Write-Warning "$packageName has already been uninstalled by other means."
}}
elseif ($key.Count -gt 1) {{
    Write-Warning "$($key.Count) matches found!"
    Write-Warning "To prevent accidental data loss, no programs will be uninstalled."
    Write-Warning "Please alert package maintainer the following keys were matched:"
    $key | ForEach-Object {{ Write-Warning "- $($_.DisplayName)" }}
}}
""", encoding="utf-8")
    assert uninstall_ps1_path.exists()

    # PACKAGE.nuspec
    CHOCO_NUSPEC.write_text(f"""<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://schemas.microsoft.com/packaging/2015/06/nuspec.xsd">
  <metadata>
    <id>{escape_xml(PROJECT_NAME)}</id>
    <version>{escape_xml(PROJECT_VERSION)}</version>
    <title>{escape_xml(PROJECT_TITLE)}</title>
    <authors>{escape_xml(", ".join(PROJECT_AUTHORS))}</authors>
    <description>
        {escape_xml(CHOCO_DESCRIPTION)}
    </description>
    <summary>{escape_xml(PROJECT_DESCRIPTION)}</summary>
    <tags>{escape_xml(" ".join(PROJECT_KEYWORDS))}</tags>
    <iconUrl>{ICON_URL}</iconUrl>
    <projectUrl>{PROJECT_HOMEPAGE}</projectUrl>
    <projectSourceUrl>{PROJECT_HOMEPAGE}</projectSourceUrl>
    <packageSourceUrl>{CHOCO_PKG_REPO_URL}</packageSourceUrl>
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


@task(pre=[install])
def install_vagrant(c: InvokeContext):
    if shutil.which("vagrant"):
        return
    print("[bold] Installing Vagrant ... [/]")
    c.run(rf'choco install -y vagrant')
    if not shutil.which("vagrant"):
        raise RuntimeError("'vagrant' not found in PATH")


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
    result = c.run(rf'choco install -y --acceptlicense "{PROJECT_NAME}" --version="{PROJECT_VERSION}" --source="{dist_path};https://community.chocolatey.org/api/v2/"')
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


@task(pre=[build, install_vagrant])
def check_vm(c: InvokeContext):
    print(rf'[bold] Checking choco package in Vagrant VM ... [/]')
    with c.cd(VAGRANT_PATH):
        result = c.run(rf'vagrant snapshot restore good --no-provision')
        assert (result is not None) and (result.return_code == 0)

        result = c.run(rf'vagrant up --provision')
        assert (result is not None) and (result.return_code == 0)

        result = c.run(rf'vagrant halt')
        assert (result is not None) and (result.return_code == 0)
    print(rf'[bold] Checking choco package in Vagrant VM ... [/][bold green]OK[/]')


@task(pre=[build,])
def publish(c: InvokeContext, api_key: str = ""):
    print(rf'[bold] Publishing choco package ... [/]')
    for nupkg_path in Path("dist").glob("*.nupkg"):
        if api_key:
            result = c.run(rf'choco push {nupkg_path} --source https://push.chocolatey.org/ --apikey {api_key}')
        else:
            result = c.run(rf'choco push {nupkg_path} --source https://push.chocolatey.org/')
        assert (result is not None) and (result.return_code == 0)
    print(rf'[bold] Publishing choco package ... [/][bold green]OK[/]')
