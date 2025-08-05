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
def install_choco(c):
    INSTALL_CHOCO = Path('scripts/install_choco.ps1')
    c.run(f'powershell.exe -ExecutionPolicy Bypass -File "{INSTALL_CHOCO}"')
    if not shutil.which("choco"):
        raise RuntimeError("'choco' not found in PATH")


@task
def mkdirs(c):
    dirs = [
        "build",
        "dist",
        "choco",
        "docs",
        "htmlcov",
        "uml",
    ]
    for dir in dirs:
        Path(dir).mkdir(parents=True, exist_ok=True)
        if not Path(dir).exists():
            raise RuntimeError(f"Cannot create dir '{dir}'")


@task(pre=[mkdirs])
def clean_choco(c):
    remove_path(f"choco/*")


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
def clean_dist_binary(c):
    remove_path(f"dist/{PROJECT_NAME}")


@task(pre=[mkdirs])
def clean_htmlcov(c):
    remove_path(f"htmlcov/*")


@task(pre=[mkdirs])
def clean_docs(c):
    remove_path(f"docs/*")


@task(pre=[mkdirs])
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
    print("[bold] Generating uml/ ... [/]")
    c.run("pdm run pyreverse -A --filter-mode=ALL --colorized -d uml/ -o jpg src/")
    if not Path("uml/classes.jpg").exists():
        raise RuntimeError("UML PyReverse - Empty dist/classes.jpg")
    c.run("pdm run pydeps src/ --noshow --reverse -Tpng -o uml/dependencies.png")
    if not Path("uml/dependencies.png").exists():
        raise RuntimeError("UML PyDeps - Empty dist/dependencies.png")
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
$toolsDir = "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)"

# Install deps
& python -m pip install --upgrade pip
& pip install pipx

# Install app
& python -m pipx ensurepath
& pipx install "$packageName"@{PROJECT_VERSION}

# Run post-install configuration
& $packageName config set --install-context-menu-all-users
& $packageName win install-menu
""", encoding="utf-8")

    # chocolateyUninstall.ps1
    uninstall_ps1_path = Path(f"{CHOCO_TOOLS_PATH}/chocolateyUninstall.ps1")
    uninstall_ps1_path.write_text(f"""
$ErrorActionPreference = 'Stop'
$packageName = "{PROJECT_NAME}"
$toolsDir = "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)"

# Run pre-uninstall configuration
& $packageName win uninstall-menu

# Uninstall app
& pipx uninstall $packageName
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
def changelog(c):
    """
    Generate CHANGELOG.md file
    """
    print(f"[bold] Generating CHANGELOG.md ... [/]", end="")
    c.run(f"pdm run git-changelog")
    if not Path("CHANGELOG.md").exists():
        raise RuntimeError("CHANGELOG.md does not exist")
    c.run(f"git add CHANGELOG.md")
    c.run(f"git commit -m \"CHANGELOG.md for {PROJECT_VERSION}\"")
    print(f"[bold green]OK[/]")


@task(pre=[clean_dist_choco, create_choco_files,])
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
