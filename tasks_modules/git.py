# tasks_modules\git.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import pypi, scoop


@task(pre=[pypi.publish, scoop.publish,])
def tag(c):
    print(f"[bold] Creating tag {GIT_RELEASE} locally ... [/]")
    c.run(f"git tag {GIT_RELEASE}")
    print(f"[bold] Creating tag {GIT_RELEASE} locally ... OK [/]")


@task(pre=[tag,])
def changelog(c):
    """
    Generate CHANGELOG.md file
    """
    print(f"[bold] Generating CHANGELOG.md ... [/]")
    changelog_path = Path("CHANGELOG.md")
    if changelog_path.exists():
        changelog_path.unlink()

    c.run(f"pdm run git-changelog")
    if not changelog_path.exists():
        raise RuntimeError(f"{changelog_path} does not exist")

    result = c.run(f"git status", hide=True)
    if all(f not in result.stdout for f in [str(changelog_path), "pyproject.toml"]):
        print(f"[bold] Skipping commit: no changes in {changelog_path}  [/]")
        return

    c.run(f"git add {changelog_path} pyproject.toml", hide=True)
    c.run(f"git commit -m \"=> {changelog_path} for {PROJECT_VERSION}\"", hide=True)
    print(f"[bold] Generating {changelog_path} ... OK [/]")


@task(pre=[changelog,])
def publish(c):
    """"Publish Git"""
    print(f"[bold] Publishing to GitHub ... [/]")
    c.run(f"git push")
    c.run(f"git push --tags")
    print(f"[bold] Publishing to GitHub ... [/][bold green]OK[/]")


@task
def unpublish(c):
    print(f"[bold] Removing tag {GIT_RELEASE} from GitHub ... [/]")
    c.run(f"git tag -d {GIT_RELEASE}")
    c.run(f"git push origin --delete {GIT_RELEASE}")
    print(f"[bold] Removing tag {GIT_RELEASE} from GitHub ... [/][bold green]OK[/]")
