# tasks_modules\git.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules._config import *

from tasks_modules import pypi, scoop


@task
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
    print(f"[bold] Generating {changelog_path} ... OK [/]")


@task(pre=[changelog,])
def release_notes(c):
    print(f"[bold] Creating release notes ... [/]")
    release_notes_path = Path("RELEASE_NOTES.md")
    if release_notes_path.exists():
        release_notes_path.unlink()

    c.run(f"pdm run git-changelog --release-notes > {release_notes_path}")
    if not release_notes_path.exists():
        raise RuntimeError(f"{release_notes_path} does not exist")
    print(f"[bold] Creating release notes ... OK [/]")


@task(pre=[pypi.publish,], post=[scoop.publish,])
def publish(c):
    """"Publish Git"""
    print(f"[bold] Publishing to GitHub ... [/]")
    c.run(f"git tag {GIT_RELEASE}")
    c.run(f"git push")
    c.run(f"git push --tags")
    print(f"[bold] Publishing to GitHub ... [/][bold green]OK[/]")


@task
def unpublish(c):
    print(f"[bold] Removing tag {GIT_RELEASE} from GitHub ... [/]")
    c.run(f"git tag -d {GIT_RELEASE}")
    c.run(f"git push origin --delete {GIT_RELEASE}")
    print(f"[bold] Removing tag {GIT_RELEASE} from GitHub ... [/][bold green]OK[/]")
