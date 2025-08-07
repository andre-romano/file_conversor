# tasks_modules\git.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import pypi, scoop


@task
def changelog(c):
    """
    Generate CHANGELOG.md file
    """
    print(f"[bold] Generating CHANGELOG.md ... [/]")
    c.run(f"pdm run git-changelog")
    if not Path("CHANGELOG.md").exists():
        raise RuntimeError("CHANGELOG.md does not exist")

    result = c.run(f"git status", hide=True)
    if all(f not in result.stdout for f in ["CHANGELOG.md", "pyproject.toml"]):
        print(f"[bold] Skipping commit: no changes in CHANGELOG.md  [/]")
        return

    c.run(f"git add CHANGELOG.md pyproject.toml", hide=True)
    c.run(f"git commit -m \"=> CHANGELOG.md for {PROJECT_VERSION}\"", hide=True)
    c.run(f"git push")
    print(f"[bold] Generating CHANGELOG.md ... OK [/]")


@task(pre=[changelog, pypi.publish, scoop.publish,])
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
