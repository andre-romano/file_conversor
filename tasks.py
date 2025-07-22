# tasks.py (invoke)

import re
import shutil
import hashlib
import tomllib

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

from typing import Any

from pathlib import Path
import zipfile
from rich import print

from invoke.tasks import task

# Read version from pyproject.toml
PYPROJECT: dict[str, Any]
with open("pyproject.toml", "rb") as f:
    PYPROJECT = tomllib.load(f)

# CONSTANTS
PROJECT_AUTHORS: list[str] = list(str(a["name"]) if isinstance(a, dict) else str(a) for a in PYPROJECT["project"]["authors"])
PROJECT_KEYWORDS: list[str] = PYPROJECT["project"]["keywords"]

PROJECT_VERSION = str(PYPROJECT["project"]["version"])
PROJECT_NAME = str(PYPROJECT["project"]["name"])

PROJECT_TITLE = str(PYPROJECT["tool"]["myproject"]["title"])

ICON_FILE = str(PYPROJECT["tool"]["myproject"]["icon"])

I18N_PATH = str(PYPROJECT["tool"]["myproject"]["locales_path"])
I18N_TEMPLATE = f"{I18N_PATH}/messages.pot"

CHOCO_PATH = str(PYPROJECT["tool"]["myproject"]["choco_path"])
CHOCO_NUSPEC = f"{CHOCO_PATH}/{PROJECT_NAME}.nuspec"

CHOCO_DEPS = {}
for dependency in PYPROJECT["tool"]["myproject"]["choco_deps"]:
    re_pattern = re.compile(r"^(.+?)([@](.+))?$")
    match = re_pattern.search(dependency)
    if not match:
        raise RuntimeError(f"Invalid dependency '{dependency}' format. Valid format is 'package@version' or 'package'.")
    package, version = match.group(1), match.group(3)
    CHOCO_DEPS[package] = version

GIT_RELEASE_NAME = f"v{PROJECT_VERSION}"
GIT_RELEASE_COMMIT = f"Release {GIT_RELEASE_NAME}"


class NuSpecParser:
    def __init__(self, nuspec_path: Path) -> None:
        super().__init__()

        self.nuspec_path = nuspec_path
        self.load()

    def load(self):
        self.tree = ET.parse(self.nuspec_path)
        self.root = self.tree.getroot()
        self.ns = {"ns": "http://schemas.microsoft.com/packaging/2015/06/nuspec.xsd"}

    def save(self):
        self.indent(self.root)
        self.tree.write(self.nuspec_path, encoding="utf-8", xml_declaration=True)
        self.fix_xml_format()

    def indent(self, elem: ET.Element, level: int = 0):
        """Indent XML elements for pretty printing."""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            for child in elem:
                self.indent(child, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def fix_xml_format(self):
        content = self.nuspec_path.read_text(encoding="utf-8")
        content = content.replace("ns0:", "")
        content = content.replace(":ns0", "")
        self.nuspec_path.write_text(content, encoding="utf-8")

    def get_element(self, tag: str, root: Element | None = None):
        if root is None:
            root = self.root
        elem = root.find(f"ns:{tag}", self.ns)
        if elem is None:
            raise RuntimeError(f"Tag <{tag}> not found.")
        return elem

    def set_tag_text(self, tag: str, value: str, root: Element | None = None):
        elem = self.get_element(tag, root=root)
        elem.text = value


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


@task(pre=[clean_tests, ])
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
def update_choco_nuspec(c):
    """Update choco .nuspec, based on pyproject.toml"""

    print("[bold] Updating Chocolatey .nuspec file ... [/]", end="")

    # rename .nuspec to new filename
    nuspec_path_old = next(Path(CHOCO_PATH).glob("*.nuspec"), None)
    if nuspec_path_old is None:
        raise RuntimeError("No .nuspec file found in CHOCO_PATH")
    nuspec_path_new = Path(CHOCO_NUSPEC)
    if nuspec_path_old != nuspec_path_new:
        nuspec_path_old.rename(nuspec_path_new)

    # create nuspec parser
    nuspec_parser = NuSpecParser(nuspec_path_new)

    # update <metadata> in .nuspec file
    metadata_elem = nuspec_parser.get_element("metadata")
    nuspec_parser.set_tag_text("id", str(PYPROJECT["project"]["name"]), root=metadata_elem)
    nuspec_parser.set_tag_text("version", str(PYPROJECT["project"]["version"]), root=metadata_elem)
    nuspec_parser.set_tag_text("description", str(PYPROJECT["project"]["description"]), root=metadata_elem)
    nuspec_parser.set_tag_text("title", PROJECT_TITLE, root=metadata_elem)
    nuspec_parser.set_tag_text("authors", ", ".join(PROJECT_AUTHORS), root=metadata_elem)
    nuspec_parser.set_tag_text("tags", " ".join(PROJECT_KEYWORDS), root=metadata_elem)

    # update <dependencies> in .nuspec file
    deps_elem = nuspec_parser.get_element("dependencies")
    deps_elem.clear()  # Remove existing dependencies
    for dep_name, dep_version in CHOCO_DEPS.items():
        attribs = {"id": dep_name}
        if dep_version:
            attribs["version"] = dep_version
        ET.SubElement(deps_elem, "dependency", attrib=attribs)

    # save changes
    nuspec_parser.save()
    print("[bold green]OK[/]")


@task
def update_choco_install(c):
    """Update choco Install.ps1 file, based on pyproject.toml"""

    print("[bold] Updating Chocolatey Install.ps1 file ... [/]", end="")

    # Read the content
    install_ps1_path = Path(f"{CHOCO_PATH}/tools/chocolateyInstall.ps1")
    content = install_ps1_path.read_text(encoding="utf-8")

    # Replace $packageName and $url values
    content = re.sub(r'(?m)^\s*\$packageName\s*=.*$', f'$packageName = "{PROJECT_NAME}"', content)
    content = re.sub(r'(?m)^\s*\$url\s*=.*$', f'$url = "https://github.com/andre-romano/{PROJECT_NAME}/releases/download/{GIT_RELEASE_NAME}/{PROJECT_NAME}_win.zip"', content)

    # Save updated content
    install_ps1_path.write_text(content, encoding="utf-8")

    print("[bold green]OK[/]")


@task(pre=[docs, uml, deps_graph,])
def update_files(c):
    """
    Update program documentation (docs, uml, etc)
    """
    # empty on purpose
    pass


@task(pre=[clean_build, ])
def copy_include_folders(c):
    # create package folder
    print(f"[bold] Copying [tool.pdm] includes into dist/ ... [/]")
    dest_base = Path("dist") / PROJECT_NAME
    dest_base.mkdir(parents=True, exist_ok=True)

    copied_paths = set([])
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


@task(pre=[clean_build, update_choco_nuspec, update_choco_install,])
def build_choco(c):
    print(f"[bold] Building choco package ... [/]")
    c.run(f"choco pack -y --outdir dist/ {CHOCO_PATH}")
    print(f"[bold] Building choco package ... [/][bold green]OK[/]")


@task(pre=[clean_build, ])
def build_whl(c):
    print("[bold] Building WHL (build tools) ... [/]")
    c.run("pdm build")
    print("[bold] Building WHL ... [/][bold green]OK[/]")


@task(pre=[clean_build, ], post=[copy_include_folders,])
def build_exe(c):
    print(f"[bold] Building EXE (pyinstaller) ... [/]")
    c.run(f"pdm run pyinstaller src/file_conversor.py --name {PROJECT_NAME} -i {ICON_FILE} --onedir")
    print(f"[bold] Building EXE (pyinstaller) ... [/][bold green]OK[/]")


@task(pre=[clean_build, build_exe, ])
def build_zip(c):
    print(f"[bold] Building ZIP portable ... [/]")

    dist_folder = Path("dist") / PROJECT_NAME
    zip_path = Path("dist") / f"{PROJECT_NAME}_win.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in dist_folder.rglob("*"):
            # Make path relative to dist_folder for zip structure
            print(f"Adding '{file_path}' to zip file ...")
            relative_path = file_path.relative_to(dist_folder.parent)
            zipf.write(file_path, arcname=relative_path)

    print(f"[bold] Building ZIP portable ... [/][bold green]OK[/]")


@task(pre=[build_zip, build_exe, build_whl, build_choco,])
def build(c):
    # empty on purpose
    pass


@task(pre=[build_zip, build_exe, build_whl,])
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


@task(pre=[build_zip, update_files, gen_checksum_file,])
def publish_github(c):
    """"Publish GitHub Release (using CI/CD Git Actions with ``git tag``)"""
    print(f"[bold] Commiting pending changes in Git ... [/]")
    c.run(f"git add .")
    c.run(f"git commit -m '{GIT_RELEASE_COMMIT}'")
    print(f"[bold] Commiting pending changes in Git ... [/][bold green]OK[/]")

    print(f"[bold] Creating Git Tag '{GIT_RELEASE_NAME}' ... [/]")
    c.run(f"git tag {GIT_RELEASE_NAME}")
    c.run(f"git push --all")
    print(f"[bold] Creating Git Tag '{GIT_RELEASE_NAME}' ... [/][bold green]OK[/]")

    print(f"[bold] Publishing Git Release '{GIT_RELEASE_NAME}' ... [/]")
    c.run(f"gh release create '{GIT_RELEASE_NAME}' dist/*.zip --title '{GIT_RELEASE_NAME}' --notes '{GIT_RELEASE_COMMIT}'")
    print(f"[bold] Publishing Git Release '{GIT_RELEASE_NAME}' ... [/][bold green]OK[/]")


@task(pre=[build_whl, publish_github,])
def publish_whl(c):
    """"Publish dist/*.whl"""
    print(f"[bold] Publishing program to PyPi ... [/]")
    c.run("twine upload dist/*.whl dist/*.tar.gz")
    print(f"[bold] Publishing program to PyPi ... [/][bold green]OK[/]")


@task(pre=[build_choco, publish_github,])
def publish_choco(c):
    """"Publish Chocolatey package"""
    print(f"[bold] Publishing program to Chocolatey ... [/]")
    c.run("choco push dist/*.nupkg -y -s https://push.chocolatey.org/")
    print(f"[bold] Publishing program to Chocolatey ... [/][bold green]OK[/]")


@task(pre=[publish_whl, publish_choco, publish_github,])
def publish(c):
    """Publish packages (choco, Github Release, PyPi)"""
    pass
