# tasks.py (invoke)

import re
import shutil
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
ICONS_PATH = str(PYPROJECT["tool"]["myproject"]["icons_path"])

I18N_PATH = str(PYPROJECT["tool"]["myproject"]["locales_path"])
I18N_TEMPLATE = f"{I18N_PATH}/messages.pot"

GIT_RELEASE = f"v{PROJECT_VERSION}"

INNO_PATH = str(PYPROJECT["tool"]["myproject"]["inno_path"])
INNO_ISS = Path(f"{INNO_PATH}/setup.iss")

CHOCO_PATH = str(PYPROJECT["tool"]["myproject"]["choco_path"])
CHOCO_NUSPEC = Path(f"{CHOCO_PATH}/{PROJECT_NAME}.nuspec")

INSTALL_CHOCO = Path(f'scripts/install_choco.ps1')

CHOCO_DEPS = {}
for dependency in PYPROJECT["tool"]["myproject"]["choco_deps"]:
    re_pattern = re.compile(r"^(.+?)([@](.+))?$")
    match = re_pattern.search(dependency)
    if not match:
        raise RuntimeError(f"Invalid dependency '{dependency}' format. Valid format is 'package@version' or 'package'.")
    package, version = match.group(1), match.group(3)
    CHOCO_DEPS[package] = version


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
        if path.exists():
            raise RuntimeError(f"Cannot remove dir / file '{path}'")
        print("[bold green]OK[/]")


@task
def mkdirs(c):
    dirs = [
        "build",
        "dist",
        CHOCO_PATH,
        INNO_PATH,
        "docs",
        "htmlcov",
        "uml",
    ]
    for dir in dirs:
        Path(dir).mkdir(parents=True, exist_ok=True)
        if not Path(dir).exists():
            raise RuntimeError(f"Cannot create dir '{dir}'")


def clean_logs(c):
    remove_path(f"*.log")
    remove_path(f"*.log.*")


@task(pre=[mkdirs])
def clean_choco(c):
    remove_path(f"{CHOCO_PATH}/*")


@task(pre=[mkdirs])
def clean_inno(c):
    remove_path(f"{INNO_PATH}/*")


@task(pre=[mkdirs])
def clean_build(c):
    remove_path(f"build/*")


@task(pre=[mkdirs])
def clean_dist(c):
    remove_path(f"dist/*")


@task(pre=[mkdirs])
def clean_dist_choco(c):
    remove_path("dist/*.nupkg")


@task(pre=[mkdirs])
def clean_dist_whl(c):
    remove_path("dist/*.whl")
    remove_path("dist/*.tar.gz")


@task(pre=[mkdirs])
def clean_dist_exe(c):
    remove_path(f"dist/*.exe")


@task(pre=[mkdirs])
def clean_htmlcov(c):
    remove_path(f"htmlcov/*")


@task(pre=[mkdirs])
def clean_docs(c):
    remove_path(f"docs/*")


@task(pre=[mkdirs])
def clean_uml(c):
    remove_path(f"uml/*")


@task(pre=[clean_logs,
           clean_build,
           clean_dist,
           clean_choco,
           clean_inno,
           clean_htmlcov,
           clean_docs,
           clean_uml, ])
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
    print("[bold] Generating uml/ ... [/]")
    c.run("pdm run pyreverse -A --filter-mode=ALL --colorized -d uml/ -o jpg src/")
    if not Path("uml/classes.jpg").exists():
        raise RuntimeError("UML PyReverse - Empty dist/classes.jpg")
    c.run("pdm run pydeps src/ --noshow --reverse -Tpng -o uml/dependencies.png")
    if not Path("uml/dependencies.png").exists():
        raise RuntimeError("UML PyDeps - Empty dist/dependencies.png")
    print("[bold] Generating uml/ ... [/][bold green]OK[/]")


@task(pre=[clean_inno,])
def create_inno_files(c):
    """Update inno files, based on pyproject.toml"""

    print("[bold] Updating InnoSetup .ISS files ... [/]", end="")

    if not INSTALL_CHOCO.exists():
        raise RuntimeError(f"Create Inno Files - Script {INSTALL_CHOCO} does not exist")

    # chocolateyInstall.ps1
    setup_path = Path(f"{INNO_ISS}")
    setup_path.write_text(rf'''
; Copywright(c) -- Andre Luiz Romano Madureira

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName={PROJECT_NAME}
AppVersion={PROJECT_VERSION}
DefaultDirName={{tmp}}  
DisableWelcomePage=yes  
DisableDirPage=yes
DisableReadyPage=yes  
DisableFinishedPage=yes 
DisableProgramGroupPage=yes 
DisableReadyMemo=yes 
DisableStartupPrompt=yes
Compression=LZMA2
ShowLanguageDialog=yes
PrivilegesRequired=admin
SourceDir={Path(".").resolve()}
OutputDir={Path("./dist").resolve()}
OutputBaseFilename={PROJECT_NAME}-{GIT_RELEASE}-Win_x64-Installer

[Files]
Source: "{INSTALL_CHOCO.resolve()}"; DestDir: "{{tmp}}"; Flags: ignoreversion createallsubdirs recursesubdirs allowunsafefiles 

[Run]
; Install chocolatey
StatusMsg: "Installing Chocolatey ..."; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{{tmp}}\{INSTALL_CHOCO.name}"""; Flags: runascurrentuser waituntilterminated
StatusMsg: "Installing App ..." ; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -Command ""choco install {PROJECT_NAME} --version {PROJECT_VERSION} -y"""; Flags: runascurrentuser waituntilterminated
''', encoding="utf-8")
    print("[bold green]OK[/]")


@task(pre=[clean_choco, ])
def create_choco_files(c):
    """Update choco files, based on pyproject.toml"""

    print("[bold] Updating Chocolatey manifest files ... [/]", end="")
    CHOCO_TOOLS_PATH = Path(f"{CHOCO_PATH}/tools")
    CHOCO_TOOLS_PATH.mkdir(parents=True, exist_ok=True)

    # chocolateyInstall.ps1
    install_ps1_path = Path(f"{CHOCO_TOOLS_PATH}/chocolateyInstall.ps1")
    install_ps1_path.write_text(rf'''
$ErrorActionPreference = 'Stop'

# Ensure Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {{
    Write-Error "Python is not installed or not in PATH."
    exit 1
}}                                
                                
Write-Output "Updating Python pip ..."
& python -m pip install --upgrade pip

Write-Output "Installing app "{PROJECT_NAME}=={PROJECT_VERSION}" ..."
& python -m pip install "{PROJECT_NAME}=={PROJECT_VERSION}"

Write-Output "Finding binPath for python scripts ..."
$binPath = & python -c "import sys; from pathlib import Path ; print(Path(sys.executable).parent / 'Scripts')"
Write-Output $binPath

Write-Output "Checking system PATH ..."
$existingPath = [Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
if (-not ($existingPath.Split(';') -contains $binPath)) {{
    Write-Output "Modifying system PATH ..."
    [Environment]::SetEnvironmentVariable("Path", "$existingPath;$binPath", [System.EnvironmentVariableTarget]::Machine)
}}

# Update current PATH env
Write-Output "Modifying current PS env PATH ..."
$env:PATH += ";$binPath"

# Run post-install configuration
if (-not (Get-Command {PROJECT_NAME} -ErrorAction SilentlyContinue)) {{
    Write-Error "{PROJECT_NAME} is not installed or not in PATH."
    exit 1
}}              
Write-Output "Configuring windows context menu ..."
& {PROJECT_NAME} config set --install-context-menu-all-users
& {PROJECT_NAME} win install-menu
''', encoding="utf-8")

    # chocolateyBeforeModify.ps1
    before_modify_ps1_path = Path(f"{CHOCO_TOOLS_PATH}/chocolateyBeforeModify.ps1")
    before_modify_ps1_path.write_text(rf"""
$ErrorActionPreference = 'Stop'
                           
if (Get-Command {PROJECT_NAME} -ErrorAction SilentlyContinue) {{
    # Run pre-uninstall configuration
    Write-Output "Uninstalling windows context menu ..."
    & {PROJECT_NAME} win uninstall-menu       
}}                                      
""", encoding="utf-8")

    # chocolateyUninstall.ps1
    uninstall_ps1_path = Path(f"{CHOCO_TOOLS_PATH}/chocolateyUninstall.ps1")
    uninstall_ps1_path.write_text(rf"""
$ErrorActionPreference = 'Stop'

# Uninstall app
if (Get-Command {PROJECT_NAME} -ErrorAction SilentlyContinue) {{
    Write-Output "Uninstalling app using PIP ..."
    & python -m pip uninstall -y {PROJECT_NAME}
}}
Write-Output "App uninstalled"
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
    <projectUrl>https://github.com/andre-romano/{PROJECT_NAME}</projectUrl>
    <projectSourceUrl>https://github.com/andre-romano/{PROJECT_NAME}</projectSourceUrl>
    <licenseUrl>https://github.com/andre-romano/{PROJECT_NAME}/blob/master/LICENSE</licenseUrl>
    <releaseNotes>https://github.com/andre-romano/{PROJECT_NAME}/blob/master/CHANGELOG.md</releaseNotes>
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
def changelog(c):
    """
    Generate CHANGELOG.md file
    """
    print(f"[bold] Generating CHANGELOG.md ... [/]", end="")
    c.run(f"pdm run git-changelog")
    if not Path("CHANGELOG.md").exists():
        raise RuntimeError("CHANGELOG.md does not exist")
    c.run(f"git add CHANGELOG.md pyproject.toml")
    c.run(f"git commit -m \"=> CHANGELOG.md for {PROJECT_VERSION}\"")
    print(f"[bold green]OK[/]")


@task(pre=[clean_choco,])
def install_choco(c):
    print("[bold] Installing Chocolatey ... [/]")
    if shutil.which("choco"):
        return
    if not INSTALL_CHOCO.exists():
        raise RuntimeError(f"Install Choco - Script {INSTALL_CHOCO} does not exist")
    c.run(f'powershell.exe -ExecutionPolicy Bypass -File "{INSTALL_CHOCO}"')
    if not shutil.which("choco"):
        raise RuntimeError("'choco' not found in PATH")


@task(pre=[install_choco,])
def install_inno(c):
    print("[bold] Installing InnoSetup ... [/]")
    if shutil.which("iscc"):
        return
    c.run(f'powershell.exe -ExecutionPolicy Bypass -Command "choco install -y innosetup"')
    if not shutil.which("iscc"):
        raise RuntimeError("'iscc' not found in PATH")


@task(pre=[clean_dist_choco, create_choco_files, install_choco,])
def build_choco(c):
    if not CHOCO_NUSPEC.exists():
        raise RuntimeError(f"Nuspec file '{CHOCO_NUSPEC}' not found!")

    print(f"[bold] Building choco package ... [/]")
    c.run(f"choco pack -y --outdir dist/ {CHOCO_NUSPEC}")
    if not list(Path("dist").glob("*.nupkg")):
        raise RuntimeError("Build CHOCO - Empty dist/*.nupkg")
    print(f"[bold] Building choco package ... [/][bold green]OK[/]")


@task(pre=[clean_dist_whl, locales_build, ])
def build_whl(c):
    print(f"[bold] Building PyPi package ... [/]")
    c.run(f"pdm build")
    if not list(Path("dist").glob("*.whl")):
        raise RuntimeError("Build WHL - Empty dist/*.whl")
    print(f"[bold] Building PyPi package ... [/][bold green]OK[/]")


@task(pre=[clean_dist_exe, create_inno_files, install_inno,])
def build_exe(c):
    print(f"[bold] Building Installer (EXE) ... [/]")
    c.run(f"iscc /Qp \"{INNO_ISS}\"")
    if not list(Path("dist").glob("*.exe")):
        raise RuntimeError("Build EXE - Empty dist/*.exe")
    print(f"[bold] Building Installer (EXE) ... [/][bold green]OK[/]")


@task(pre=[build_whl, ])
def test_pypi(c):
    if not list(Path("dist").glob("*.whl")):
        raise RuntimeError("Test PyPi - Empty dist/*.whl")
    print(f"[bold] Testing PyPi ... [/]")
    c.run(f"pdm run twine check dist/*.whl dist/*.tar.gz")
    c.run(f"pdm run twine upload --repository testpypi dist/*.whl dist/*.tar.gz")
    print(f"[bold] Testing PyPi ... [/][bold green]OK[/]")


@task(pre=[build_whl, ])
def publish_pypi(c):
    if not list(Path("dist").glob("*.whl")):
        raise RuntimeError("Publish PyPi - Empty dist/*.whl")
    print(f"[bold] Publishing to PyPi ... [/]")
    c.run(f"pdm run twine check dist/*.whl dist/*.tar.gz")
    c.run(f"pdm run twine upload dist/*.whl dist/*.tar.gz")
    print(f"[bold] Publishing to PyPi ... [/][bold green]OK[/]")


@task(pre=[changelog, publish_pypi])
def publish(c):
    """"Publish Git"""
    print(f"[bold] Publishing to GitHub ... [/]")
    c.run(f"git tag {GIT_RELEASE}")
    c.run(f"git push --tags")
    print(f"[bold] Publishing to GitHub ... [/][bold green]OK[/]")


@task
def unpublish(c):
    print(f"[bold] Removing tag {GIT_RELEASE} from GitHub ... [/]")
    c.run(f"git tag -d {GIT_RELEASE}")
    c.run(f"git push origin --delete {GIT_RELEASE}")
    print(f"[bold] Removing tag {GIT_RELEASE} from GitHub ... [/][bold green]OK[/]")
