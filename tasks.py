# tasks.py (invoke)

import re
import shutil
import hashlib
import tomllib

from invoke.tasks import task

from pathlib import Path
from rich import print

# CONSTANTS
PROJECT_NAME = f"file_conversor"
ICON_FILE = f"data/icon.ico"

I18N_PATH = f"locales"
I18N_TEMPLATE = f"{I18N_PATH}/messages.pot"

CHOCO_PATH = f"choco"

ISS_FILE = f"setup/setup.iss"


def get_pyproject_version() -> str:
    # Read version from pyproject.toml
    with open("pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
    return str(pyproject["project"]["version"])


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
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()  # Remove single file


@task
def clean_build(c):
    remove_path("build/*")
    remove_path("dist/*")


@task
def clean_tests(c):
    remove_path("htmlcov/*")


@task
def clean_docs(c):
    remove_path("docs/*")


@task
def clean_uml(c):
    remove_path("uml/classes.*")
    remove_path("uml/packages.*")


@task
def clean_deps_graph(c):
    remove_path("uml/dependencies.*")


@task(pre=[clean_build, clean_tests, clean_docs, clean_uml, clean_deps_graph, ])
def clean(c):
    print("Cleaning... [bold green]OK[/]")


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


@task(pre=[locales_update])
def locales_build(c):
    """ Build locales' .MO files based on .PO files ..."""
    print(f"[bold] Building locales .mo files ... [/]", end="")
    c.run(f"pdm run pybabel compile -d {I18N_PATH}")
    print(f"[bold] Building locales .mo files ... [/][bold green]OK[/]")


@task(pre=[clean_tests, locales_build])
def tests(c, args: str = ""):
    print("[bold] Running tests ... [/]")
    c.run(f"pdm run pytest {args.split()}")


@task(pre=[clean_docs])
def docs(c):
    print(f"[bold] Generating docs/ ... [/]", end="")
    c.run(f"pdm run pdoc src -o docs --math --mermaid -d restructuredtext --logo ../{ICON_FILE} --favicon ../{ICON_FILE}")
    print(f"[bold green]OK[/]")


@task(pre=[clean_uml])
def uml(c):
    print("[bold] Generating uml/ ... [/]")
    c.run("pdm run pyreverse -A --filter-mode=ALL --colorized -d uml/ -o jpg src/")
    print("[bold] Generating uml/ ... [/][bold green]OK[/]")


@task(pre=[clean_deps_graph])
def deps_graph(c):
    print("[bold] Generating dependencies graph ... [/]", end="")
    c.run("pdm run pydeps src/ --noshow --reverse -Tpng -o uml/dependencies.png")
    print("[bold green]OK[/]")


@task
def version_choco(c):
    """Update version for choco .nuspec, based on pyproject.toml"""

    print("[bold] Updating Chocolatey project version ... [/]", end="")
    version = get_pyproject_version()

    nuspec_path = Path(f"{CHOCO_PATH}/file_conversor.nuspec")
    content = nuspec_path.read_text()
    content = re.sub(
        r'(<version>)[^<]+(</version>)',
        lambda m: f"{m.group(1)}{version}{m.group(2)}",
        content
    )
    nuspec_path.write_text(content)
    print("[bold green]OK[/]")


@task
def version_innosetup(c):
    """Update version for setup.iss, based on pyproject.toml"""

    print("[bold] Updating InnoSetup project version ... [/]", end="")
    version = get_pyproject_version()

    iss_path = Path("setup/setup.iss")
    content = iss_path.read_text()
    content = re.sub(
        r'(AppVersion\s*=\s*)[^\n]+',
        lambda m: f"{m.group(1)}{version}",
        content
    )
    iss_path.write_text(content)
    print("[bold green]OK[/]")


@task(pre=[version_choco, version_innosetup,])
def version_update(c):
    """Version number set in other project files, based on pyproject.toml"""
    # empty on purpose
    pass


@task(pre=[locales_build, version_update, docs,])
def update(c):
    """
    Update program dependencies (list)
    """
    # empty on purpose
    pass


@task(pre=[clean_build, update])
def build_whl(c):
    print("[bold] Building WHL (build tools) ... [/]")
    c.run("pdm build")
    print("[bold] Building WHL ... [/][bold green]OK[/]")


@task(pre=[clean_build, update])
def build_exe(c):
    print(f"[bold] Building EXE (pyinstaller) ... [/]")
    c.run(f"pdm run pyinstaller src/file_conversor.py --name {PROJECT_NAME} -i {ICON_FILE} --onefile")
    print(f"[bold] Building EXE (pyinstaller) ... [/][bold green]OK[/]")


@task(pre=[build_exe])
def build_setup(c):
    print(f"[bold] Building setup.exe (InnoSetup) ... [/]")
    c.run(f'ISCC {ISS_FILE}')
    print(f"[bold] Building setup.exe (InnoSetup) ...  [/][bold green]OK[/]")


@task(pre=[build_whl, build_exe, build_setup])
def gen_checksum_file(c):
    """
    Generate checksum.sha256 file
    """
    checksum_path = Path("dist/checksums.sha256")
    print("[bold] Generating SHA256 checksums ... [/]", end="")
    files = Path("dist").glob("*")  # Change to your target directory
    with open(checksum_path, "w") as f:
        for file in files:
            if file.is_file() and not file.name == checksum_path.name:
                checksum = generate_sha256(str(file))
                f.write(f"{checksum}  {file.name}\n")
    print("[bold green]OK[/]")


@task(pre=[build_setup])
def gen_verification_file(c):
    """
    Generate VERIFICATION.txt for choco package
    """
    verification_path = Path(f"{CHOCO_PATH}/tools/VERIFICATION.txt")
    print(f"[bold] Generating '{str(verification_path)}' file ... [/]", end="")

    setup_path = Path("dist/file_conversor_setup.exe")
    setup_checksum = generate_sha256(str(setup_path))

    content = f"""VERIFICATION
============
1. File: {Path(setup_path).name}
2. SHA-256: {setup_checksum}
3. Generated by Python hashlib (SHA-256)
"""
    with open(verification_path, "w") as f:
        f.write(content)
    print("[bold green]OK[/]")


@task(pre=[build_setup, gen_verification_file])
def build_choco(c):
    print(f"[bold] Building choco package ... [/]")
    c.run(f"choco pack -y --outdir dist/ {CHOCO_PATH}")
    print(f"[bold] Building choco package ... [/][bold green]OK[/]")


@task
def install_deps(c):
    print("[bold] Installing project dependencies ... [/]")
    c.run("pip install pdm")
    c.run("pdm install")
    print("[bold] Installing project dependencies ... [/][bold green]OK[/]")


@task(pre=[build_whl])
def install_whl(c):
    """
    Install program (using pip - .WHL)
    """
    print("[bold] Installing program using .WHL ... [/]")
    c.run("pip install dist/*.whl")
    print("[bold] Installing program using .WHL ... [/][bold green]OK[/]")


@task(pre=[build_choco])
def install_choco(c):
    """
    Install program (using choco)
    """
    print(f"[bold] Installing program using `choco` ... [/]")
    c.run(f"choco install {PROJECT_NAME} -y -s dist/")
    print(f"[bold] Installing program using `choco` ... [/][bold green]OK[/]")


@task(pre=[build_whl])
def publish_whl(c):
    """"Publish dist/*.whl"""
    print(f"[bold] Publishing program to PyPi ... [/]")
    c.run("twine upload dist/*.whl dist/*.tar.gz")
    print(f"[bold] Publishing program to PyPi ... [/][bold green]OK[/]")


@task(pre=[build_choco])
def publish_choco(c):
    """"Publish Chocolatey package"""
    print(f"[bold] Publishing program to Chocolatey ... [/]")
    c.run("choco push dist/*.nupkg -y -s https://push.chocolatey.org/")
    print(f"[bold] Publishing program to Chocolatey ... [/][bold green]OK[/]")


@task(pre=[gen_checksum_file, build_setup])
def publish_github(c):
    """"Publish GitHub Release (using CI/CD Git Actions with ``git tag``)"""
    release_name = f"v{get_pyproject_version()}"
    changelog = f"Release {release_name}"

    print(f"[bold] Creating Git Tag '{release_name}' ... [/]")
    c.run(f"git tag {release_name}")
    c.run(f"git push --tags")
    print(f"[bold] Creating Git Tag '{release_name}' ... [/][bold green]OK[/]")

    print(f"[bold] Publishing Git Release '{release_name}' ... [/]")
    c.run(f"gh release create '{release_name}' dist/*_setup.exe dist/*.whl --title '{release_name}' --notes '{changelog}'")
    print(f"[bold] Publishing Git Release '{release_name}' ... [/][bold green]OK[/]")


@task(pre=[publish_choco, publish_github, publish_whl,])
def publish(c):
    """Publish packages (choco, Github Release, PyPi)"""
    pass
