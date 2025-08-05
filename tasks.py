# tasks.py (invoke)

import re
import shutil
import hashlib
import tomllib

from typing import Any

from pathlib import Path

from rich import print

from invoke.tasks import task

# Read version from pyproject.toml
PYPROJECT: dict[str, Any]
with open("pyproject.toml", "rb") as f:
    PYPROJECT = tomllib.load(f)

# CONSTANTS
PROJECT_AUTHORS: list[str] = list(str(a["name"]) if isinstance(a, dict) else str(a) for a in PYPROJECT["project"]["authors"])
PROJECT_KEYWORDS: list[str] = PYPROJECT["project"]["keywords"]

PROJECT_NAME = str(PYPROJECT["project"]["name"])
PROJECT_VERSION = str(PYPROJECT["project"]["version"])
PROJECT_DESCRIPTION = str(PYPROJECT["project"]["description"])

PROJECT_TITLE = str(PYPROJECT["tool"]["myproject"]["title"])
ICON_FILE = str(PYPROJECT["tool"]["myproject"]["icon"])

I18N_PATH = str(PYPROJECT["tool"]["myproject"]["locales_path"])
I18N_TEMPLATE = f"{I18N_PATH}/messages.pot"

GIT_RELEASE = f"v{PROJECT_VERSION}"

CHOCO_ZIP_FILENAME = f"{PROJECT_NAME}-windows-latest.zip"

CHOCO_PATH = str(PYPROJECT["tool"]["myproject"]["choco_path"])
CHOCO_NUSPEC = Path(f"{CHOCO_PATH}/{PROJECT_NAME}.nuspec")

CHOCO_DEPS = {}
for dependency in PYPROJECT["tool"]["myproject"]["choco_deps"]:
    re_pattern = re.compile(r"^(.+?)([@](.+))?$")
    match = re_pattern.search(dependency)
    if not match:
        raise RuntimeError(f"Invalid dependency '{dependency}' format. Valid format is 'package@version' or 'package'.")
    package, version = match.group(1), match.group(3)
    CHOCO_DEPS[package] = version


def generate_sha256(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read file in chunks to handle large files
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def remove_path(path_pattern):
    """Remove dir or file, using globs / wildcards"""
    for path in Path('.').glob(path_pattern):
        if not path.exists():
            pass
        print(f"Cleaning '{path}' ... ", end="")
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()  # Remove single file
        print("[bold green]OK[/]")


@task
def clean_choco(c):
    remove_path(f"choco/*")


@task
def clean_build(c):
    remove_path(f"build/*")


@task
def clean_dist(c):
    remove_path(f"dist/*")


@task
def clean_dist_choco(c):
    remove_path("dist/*.nupkg")


@task
def clean_dist_binary(c):
    remove_path(f"dist/{PROJECT_NAME}")


@task
def clean_htmlcov(c):
    remove_path(f"htmlcov/*")


@task
def clean_docs(c):
    remove_path(f"docs/*")


@task
def clean_uml(c):
    remove_path(f"uml/*")


@task(pre=[clean_build, clean_dist, clean_choco, clean_htmlcov, clean_docs, clean_uml, ])
def clean(c):
    pass


@task
def locales_template(c):
    """ Update locales template (.pot)"""
    print(f"[bold] Creating locales template (.pot) ... [/]", end="")
    c.run(f"pdm run pybabel extract -F babel.cfg -o {I18N_TEMPLATE} .")
    print(f"[bold] Creating locales template (.pot) ... [/][bold green]OK[/]")


@task(pre=[locales_template])
def locales_create(c, locale: str):
    """
    Create a locale (e.g., en_US, pt_BR, etc) translation using Babel.

    :param locale: Locale code (e.g., en_US, pt_BR, etc)
    """
    print(f"[bold] Creating new locale '{locale}' ... [/]")
    c.run(f"pdm run pybabel init -i {I18N_TEMPLATE} -d {I18N_PATH} -l {locale}")
    print(f"[bold] Creating new locale '{locale}' ... [/][bold green]OK[/]")


@task(pre=[locales_template])
def locales_update(c):
    """ Update locales' .PO files based on current template (.pot)"""
    print(f"[bold] Updating locales based on template .pot file ... [/]")
    c.run(f"pdm run pybabel update -i {I18N_TEMPLATE} -d {I18N_PATH}")
    print(f"[bold] Updating locales based on template .pot file ... [/][bold green]OK[/]")


@task
def locales_build(c):
    """ Build locales' .MO files based on .PO files ..."""
    print(f"[bold] Building locales .mo files ... [/]", end="")
    c.run(f"pdm run pybabel compile -d {I18N_PATH}")
    print(f"[bold] Building locales .mo files ... [/][bold green]OK[/]")


@task(pre=[clean_htmlcov, ])
def tests(c, args: str = ""):
    print("[bold] Running tests ... [/]")
    c.run(f"pdm run pytest {args.split()}")


@task(pre=[clean_uml,])
def uml(c):
    UML_PATH = Path(f"uml")
    UML_PATH.mkdir(parents=True, exist_ok=True)

    print("[bold] Generating uml/ ... [/]")
    c.run("pdm run pyreverse -A --filter-mode=ALL --colorized -d uml/ -o jpg src/")
    c.run("pdm run pydeps src/ --noshow --reverse -Tpng -o uml/dependencies.png")
    print("[bold] Generating uml/ ... [/][bold green]OK[/]")


@task(pre=[clean_choco,])
def create_choco_files(c):
    """Update choco files, based on pyproject.toml"""

    print("[bold] Updating Chocolatey manifest files ... [/]", end="")
    CHOCO_TOOLS_PATH = Path(f"{CHOCO_PATH}/tools")
    CHOCO_TOOLS_PATH.mkdir(parents=True, exist_ok=True)

    # chocolateyInstall.ps1
    install_ps1_path = Path(f"{CHOCO_TOOLS_PATH}/chocolateyInstall.ps1")
    install_ps1_path.write_text(f"""
$ErrorActionPreference = 'Stop'
$packageName = "{PROJECT_NAME}"
$exeName = "$packageName.exe"
$toolsDir = "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)"
$url = "https://github.com/andre-romano/file_conversor/releases/download/{GIT_RELEASE}/{CHOCO_ZIP_FILENAME}"
$zipFile = Join-Path $toolsDir '{CHOCO_ZIP_FILENAME}'
$exePath = Join-Path $toolsDir "$packageName" "$exeName"

# Download the zip file
Get-ChocolateyWebFile -PackageName $packageName -FileFullPath $zipFile -Url $url

# Unzip to tools directory
Get-ChocolateyUnzip -FileFullPath $zipFile -Destination $toolsDir

# Remove the zip
Remove-Item -Force $zipFile

# Register executable manually
Install-BinFile -Name $packageName -Path $exePath

# Run post-install configuration
& $exePath config set --install-context-menu-all-users --install-deps True
& $exePath win install-menu
""", encoding="utf-8")

    # chocolateyUninstall.ps1
    uninstall_ps1_path = Path(f"{CHOCO_TOOLS_PATH}/chocolateyUninstall.ps1")
    uninstall_ps1_path.write_text(f"""
$ErrorActionPreference = 'Stop'
$packageName = "{PROJECT_NAME}"
$toolsDir = "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)"
$exeName = "$packageName.exe"
$exePath = Join-Path $toolsDir "$packageName" "$exeName"

# Run pre-uninstall configuration
& $exePath win uninstall-menu

# Remove the executable shim
Uninstall-BinFile -Name $packageName

# Remove the installation directory
Remove-Item -Recurse -Force (Join-Path $toolsDir $packageName)
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
    <iconUrl>http://rawcdn.githack.com/andre-romano/{PROJECT_NAME}/master/icons/icon.png</iconUrl>
    <projectUrl>https://github.com/andre-romano/{PROJECT_NAME}</projectUrl>
    <projectSourceUrl>https://github.com/andre-romano/{PROJECT_NAME}</projectSourceUrl>
    <licenseUrl>https://github.com/andre-romano/{PROJECT_NAME}/blob/master/LICENSE</licenseUrl>
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
def copy_include_folders(c):
    # create package folder
    print(f"[bold] Copying [tool.pdm] includes into dist/ ... [/]")
    dest_base = Path("dist") / PROJECT_NAME
    dest_base.mkdir(parents=True, exist_ok=True)

    pdm: dict = PYPROJECT["tool"]["pdm"]
    for path_glob_str in pdm.get("includes", []):
        for src_path in Path(".").glob(path_glob_str):
            dest_path = dest_base / src_path
            print(f"Copying '{src_path}' to '{dest_path}' ...")
            if src_path.is_dir():
                dest_path.mkdir(parents=True, exist_ok=True)
            else:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dest_path)
    print(f"[bold] Copying [tool.pdm] includes into dist/ ... [/][bold green]OK[/]")


@task(pre=[clean_dist_choco, create_choco_files, locales_build])
def build_choco(c):
    dest_base = Path("dist")
    dest_base.mkdir(parents=True, exist_ok=True)

    if not CHOCO_NUSPEC.exists():
        raise RuntimeError(f"Nuspec file '{CHOCO_NUSPEC}' not found!")

    print(f"[bold] Building choco package ... [/]")
    c.run(f"choco pack -y --outdir dist/ {CHOCO_NUSPEC}")
    print(f"[bold] Building choco package ... [/][bold green]OK[/]")


@task(pre=[clean_build, clean_dist_binary, locales_build], post=[copy_include_folders,])
def build_binary(c):
    print(f"[bold] Building EXE (pyinstaller) ... [/]")
    c.run(f"pdm run pyinstaller src/file_conversor.py --name {PROJECT_NAME} -i {ICON_FILE} --onedir")
    print(f"[bold] Building EXE (pyinstaller) ... [/][bold green]OK[/]")


@task
def gen_changelog(c):
    """
    Generate CHANGELOG.md file
    """
    print(f"[bold] Generating CHANGELOG.md ... [/]", end="")
    c.run(f"pdm run git-changelog")
    c.run(f"git add CHANGELOG.md")
    c.run(f"git commit -m \"CHANGELOG.md for {PROJECT_VERSION}\"")
    print(f"[bold green]OK[/]")


@task
def gen_checksum_file(c):
    """
    Generate checksum.sha256 file
    """
    dest_base = Path("dist")
    dest_base.mkdir(parents=True, exist_ok=True)

    checksum_path = Path("dist/checksums.sha256")
    print("[bold] Generating SHA256 checksums ... [/]", end="")
    files = Path("dist").glob("*")  # Change to your target directory
    with open(checksum_path, "w") as f:
        for file in files:
            if file.is_file() and not file.name == checksum_path.name:
                checksum = generate_sha256(str(file))
                f.write(f"{checksum}  {file.name}\n")
    print("[bold green]OK[/]")


@task(pre=[build_choco])
def install_choco(c):
    """
    Install program (using choco)
    """
    print(f"[bold] Installing program using `choco` ... [/]")
    c.run(f"choco install {PROJECT_NAME} -y -s dist/")
    print(f"[bold] Installing program using `choco` ... [/][bold green]OK[/]")


@task(pre=[gen_changelog])
def publish(c):
    """"Publish Git"""
    print(f"[bold] Publishing program to GitHub ... [/]")
    c.run(f"git tag {GIT_RELEASE}")
    c.run(f"git push --tags")
    print(f"[bold] Publishing program to GitHub ... [/][bold green]OK[/]")
