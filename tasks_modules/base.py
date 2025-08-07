# tasks_modules\base.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *


@task
def mkdirs(c):
    dirs = [
        "build",
        "dist",
        "docs",
        "htmlcov",
        "uml",
    ]
    for dir in dirs:
        Path(dir).mkdir(parents=True, exist_ok=True)
        if not Path(dir).exists():
            raise RuntimeError(f"Cannot create dir '{dir}'")


@task
def clean_logs(c):
    remove_path(f"*.log")
    remove_path(f"*.log.*")


@task(pre=[mkdirs])
def clean_build(c):
    remove_path(f"build/*")


@task(pre=[mkdirs])
def clean_dist(c):
    remove_path(f"dist/*")


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
           clean_htmlcov,
           clean_docs,
           clean_uml, ])
def clean(c):
    pass


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
    print(f"[bold] Building locales .mo files ... [/]")
    c.run(f"pdm run pybabel compile -d {I18N_PATH}")
    print(f"[bold] Building locales .mo files ... [/][bold green]OK[/]")


@task
def publish_install_script(c):
    print(f"[bold] Publishing install script ... [/]")
    result = c.run(f"git status", hide=True)
    if INSTALL_APP_PY.name not in result.stdout:
        print(f"[bold] Skipping publish: no changes in install script.  [/]")
        return
    c.run(f"git add {INSTALL_APP_PY}", hide=True)
    c.run(f"git commit -m \"ci: install script update\"", hide=True)
    c.run(f"git push")
    print(f"[bold] Publishing install script ... OK [/]")
