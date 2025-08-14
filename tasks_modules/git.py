# tasks_modules\git.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules._config import *

from tasks_modules import pypi, scoop


@task
def changelog(c: InvokeContext):
    """
    Generate CHANGELOG.md file
    """
    print(f"[bold] Generating CHANGELOG.md ... [/]")
    changelog_path = Path("CHANGELOG.md")
    if changelog_path.exists():
        changelog_path.unlink()

    result = c.run(f"pdm run git-changelog")
    assert (result is not None) and (result.return_code == 0)
    if not changelog_path.exists():
        raise RuntimeError(f"{changelog_path} does not exist")
    print(f"[bold] Generating {changelog_path} ... OK [/]")


@task(pre=[changelog,])
def release_notes(c: InvokeContext):
    print(f"[bold] Creating release notes ... [/]")
    release_notes_path = Path("RELEASE_NOTES.md")
    if release_notes_path.exists():
        release_notes_path.unlink()

    result = c.run(f"pdm run git-changelog --release-notes > {release_notes_path}")
    assert (result is not None) and (result.return_code == 0)
    if not release_notes_path.exists():
        raise RuntimeError(f"{release_notes_path} does not exist")
    print(f"[bold] Creating release notes ... OK [/]")


@task(pre=[pypi.publish,], post=[scoop.publish,])
def publish(c: InvokeContext):
    """"Publish Git"""
    print(f"[bold] Publishing to GitHub ... [/]")
    result = c.run(f"git tag {GIT_RELEASE}")
    assert (result is not None) and (result.return_code == 0)

    result = c.run(f"git push")
    assert (result is not None) and (result.return_code == 0)

    result = c.run(f"git push --tags")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Publishing to GitHub ... [/][bold green]OK[/]")


@task
def unpublish(c: InvokeContext):
    print(f"[bold] Removing tag {GIT_RELEASE} from GitHub ... [/]")
    result = c.run(f"git tag -d {GIT_RELEASE}")
    assert (result is not None) and (result.return_code == 0)

    result = c.run(f"git push origin --delete {GIT_RELEASE}")
    assert (result is not None) and (result.return_code == 0)

    print(f"[bold] Removing tag {GIT_RELEASE} from GitHub ... [/][bold green]OK[/]")
