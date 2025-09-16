# tasks_modules\git.py

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules._config import *
from tasks_modules import _config, base


@task
def checksum(c: InvokeContext):
    print(f"[bold] Generating SHA256 hash ... [/]")
    INSTALL_APP_HASH.parent.mkdir(parents=True, exist_ok=True)
    if INSTALL_APP_HASH.exists():
        INSTALL_APP_HASH.unlink()
    INSTALL_APP_HASH.write_text(rf"""
{"\n".join([f"{_config.get_hash(path)}  {path.name}" for path in Path("./dist").glob("*")])}
""", encoding="utf-8")
    if not INSTALL_APP_HASH.exists():
        raise RuntimeError("Failed to create sha256 file")

    print(f"{INSTALL_APP_HASH}:")
    print(INSTALL_APP_HASH.read_text())

    if shutil.which("sha256sum"):
        with c.cd(str(INSTALL_APP_HASH.parent)):
            c.run(f"sha256sum -c {INSTALL_APP_HASH.name}")
    else:
        _config.verify_with_sha256_file(INSTALL_APP_HASH)
    print(f"[bold] Generating SHA256 hash ... [/][bold green]OK[/]")


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
    if RELEASE_NOTES_PATH.exists():
        RELEASE_NOTES_PATH.unlink()

    result = c.run(f"pdm run git-changelog --release-notes > {RELEASE_NOTES_PATH}")
    assert (result is not None) and (result.return_code == 0)
    if not RELEASE_NOTES_PATH.exists():
        raise RuntimeError(f"{RELEASE_NOTES_PATH} does not exist")
    print(f"[bold] Creating release notes ... OK [/]")


@task(pre=[base.tests])
def tag(c: InvokeContext):
    print(f"[bold] Git tagging {GIT_RELEASE} ... [/]")
    result = c.run(f"git push")
    assert (result is not None) and (result.return_code == 0)

    result = c.run(f"git tag {GIT_RELEASE}")
    assert (result is not None) and (result.return_code == 0)

    result = c.run(f"git push --tags")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Git tagging {GIT_RELEASE} ... [bold green]OK[/][/]")


@task
def untag(c: InvokeContext):
    print(f"[bold] Removing tag {GIT_RELEASE} from GitHub ... [/]")
    result = c.run(f"git tag -d {GIT_RELEASE}")
    assert (result is not None) and (result.return_code == 0)

    result = c.run(f"git push origin --delete {GIT_RELEASE}")
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Removing tag {GIT_RELEASE} from GitHub ... [/][bold green]OK[/]")


@task(pre=[release_notes, checksum])
def publish(c: InvokeContext):
    print(f"[bold] Publishing to GitHub ... [/]")
    gh_cmd = [
        "gh", "release",
        "create", rf'"{GIT_RELEASE}"',
        "--title", rf'"{GIT_RELEASE}"',
        "--notes-file", rf'"{RELEASE_NOTES_PATH}"',
        'dist/*',
    ]
    result = c.run(" ".join(gh_cmd))
    assert (result is not None) and (result.return_code == 0)
    print(f"[bold] Publishing to GitHub ... [/][bold green]OK[/]")
