# tasks.py (invoke)

import shutil

from pathlib import Path
from invoke.tasks import task
from rich import print


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
    print("Cleaning... [bold][green]OK[/green][/bold]")


@task
def locales_template(c):
    """ Update locales template (.pot)"""
    print("Creating locales/ template (.pot) ... ")
    c.run(f"pdm run pybabel extract -F babel.cfg -o locales/messages.pot .")


@task(pre=[locales_template])
def locales_create(c, locale: str):
    """
    Create a locale (e.g., en_US, pt_BR, etc) translation using Babel.
    """
    print(f"Creating new locale '{locale}' ... ")
    c.run(
        f"pdm run pybabel init -i locales/messages.pot -d locales -l {locale}")


@task(pre=[locales_template])
def locales_update(c):
    """ Update locales' .PO files based on current template (.pot)"""
    print(f"Updating locales based on template .pot file ... ")
    c.run(f"pdm run pybabel update -i locales/messages.pot -d locales")


@task(pre=[locales_update])
def locales_build(c):
    """ Build locales' .MO files based on .PO files ..."""
    c.run(f"pdm run pybabel compile -d locales")


@task(pre=[clean_tests, locales_build])
def tests(c, args: str = ""):
    print("Running tests ... ")
    c.run(f"pdm run pytest {args.split()}")


@task(pre=[clean_docs])
def docs(c):
    print("Generating docs/ ... ", end="")
    c.run("pdm run pdoc src -o docs --math --mermaid -d restructuredtext --logo ../data/icon.ico --favicon ../data/icon.ico")
    print("[bold][green]OK[/green][/bold]")


@task(pre=[clean_uml])
def uml(c):
    print("Generating uml/ ... ")
    c.run("pdm run pyreverse -A --filter-mode=ALL --colorized -d uml/ -o jpg src/")
    print("UML files: [bold][green]OK[/green][/bold]")


@task(pre=[clean_deps_graph])
def deps_graph(c):
    print("Generating dependencies graph ... ", end="")
    c.run("pdm run pydeps src/ --noshow --reverse -Tpng -o uml/dependencies.png")
    print("[bold][green]OK[/green][/bold]")


@task(pre=[clean_build, locales_build, docs, uml, deps_graph])
def build(c, exe: bool = True, whl: bool = True, setup: bool = False):
    """
    Build program

    :param exe: Build .EXE. Defaults to True.
    :param whl: Build .whl. Defaults to True.
    :param setup: Build setup.exe file (Inno Setup). Defaults to False.
    """
    if bool(exe):
        print("Building EXE (pyinstaller) ... ")
        c.run("pdm run pyinstaller src/file_conversor.py --name file_conversor --icon data/icon.ico --onefile")
        print("Building EXE (pyinstaller) ... [bold][green]OK[/green][/bold]")
    if bool(whl):
        print("Building WHL (build tools) ... ")
        c.run("pdm build")
        print("Building WHL ... [bold][green]OK[/green][/bold]")
    # TODO
    if bool(setup):
        pass


@task
def install_deps(c):
    print("Installing project dependencies ... ")
    c.run("pip install pdm")
    c.run("pdm install")
    print("Installing project dependencies ... [bold][green]OK[/green][/bold]")


@task(pre=[build])
def install(c, whl: bool = False, setup: bool = True):
    """
    Install program

    :param whl: Install .whl using `pip`. Defaults to False.
    :param setup: Install setup.exe (quiet flag). Defaults to True.
    """
    if bool(whl):
        print("Installing program using .WHL ... ")
        c.run("pip install dist/*.whl")
        print(
            "Installing program using .WHL ... [bold][green]OK[/green][/bold]")
    if bool(setup):
        print("Installing program using .EXE ... ")
        # TODO
        print(
            "Installing program using .EXE ... [bold][green]OK[/green][/bold]")


@task(pre=[build])
def publish(c):
    """"Git commit"""
    c.run("twine upload dist/*.whl dist/*.tar.gz")
