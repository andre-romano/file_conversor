# tasks_modules\pyapp.py
from typing import Annotated, Literal

from invoke.tasks import task  # pyright: ignore[reportUnknownVariableType]
from pydantic import BaseModel, Field  # pyright: ignore[reportUnknownVariableType]

# user provided
from tasks_modules import _config, base, pypi
from tasks_modules._config import *  # noqa: S2208


_binary_suffix = ".exe" if base.WINDOWS else ""

BUILD_PYAPP_DIR = Path("build") / "pyapp"
BUILD_DIR = Path("build") / f"{PROJECT_NAME}-{GIT_RELEASE}"

PORTABLE_EXE = BUILD_DIR / f"{PROJECT_NAME}{_binary_suffix}"
PORTABLE_GUI_EXE = BUILD_DIR / f"{PROJECT_NAME}_gui{_binary_suffix}"

PYAPP_URL = f"https://github.com/ofek/pyapp/releases/latest/download/source.zip"

EMBEDPY_TIMESTAMP = "20260325"
EMBEDPY_WINDOWS_URL = f"https://github.com/astral-sh/python-build-standalone/releases/download/{EMBEDPY_TIMESTAMP}/cpython-{PYTHON_VERSION}+{EMBEDPY_TIMESTAMP}-x86_64-pc-windows-msvc-install_only_stripped.tar.gz"
EMBEDPY_LINUX_URL = f"https://github.com/astral-sh/python-build-standalone/releases/download/{EMBEDPY_TIMESTAMP}/cpython-{PYTHON_VERSION}+{EMBEDPY_TIMESTAMP}-x86_64_v4-unknown-linux-gnu-install_only_stripped.tar.gz"
EMBEDPY_MAC_URL = f"https://github.com/astral-sh/python-build-standalone/releases/download/{EMBEDPY_TIMESTAMP}/cpython-{PYTHON_VERSION}+{EMBEDPY_TIMESTAMP}-aarch64-apple-darwin-install_only_stripped.tar.gz"

EMBEDPY_URL = EMBEDPY_WINDOWS_URL if base.WINDOWS else (EMBEDPY_LINUX_URL if base.LINUX else EMBEDPY_MAC_URL)


@task
def mkdirs(_: InvokeContext):
    _config.mkdir([
        BUILD_DIR,
    ])


@task
def clean_pyapp(_: InvokeContext):
    _config.remove_path_pattern(f"{BUILD_PYAPP_DIR}")


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean_exe(_: InvokeContext):
    remove_path_pattern(f"{BUILD_DIR}/*")


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def install(c: InvokeContext):
    result = c.run(f"cargo -h", hide=True)
    assert (result is not None) and (result.return_code == 0), "Cargo is not installed or not found in PATH."

    if BUILD_PYAPP_DIR.exists() and (BUILD_PYAPP_DIR / "Cargo.toml").exists():
        print(f"[bold yellow]WARN[/]: PyApp source already found in '{BUILD_PYAPP_DIR}'. Skipping installation.")
        return

    _, cached_pyapp_zip = _config.get_url(PYAPP_URL)
    assert cached_pyapp_zip and cached_pyapp_zip.exists(), f"'{cached_pyapp_zip}' not found"

    remove_path_pattern(str(BUILD_PYAPP_DIR))
    print(f"Extracting to '{BUILD_PYAPP_DIR}' ... ", end="")
    _config.extract(src=cached_pyapp_zip, dst=BUILD_PYAPP_DIR.parent)
    for path in BUILD_PYAPP_DIR.parent.glob("pyapp-v*"):
        if not path.is_dir():
            continue
        _config.move(path, BUILD_PYAPP_DIR)
    assert BUILD_PYAPP_DIR.exists() and (BUILD_PYAPP_DIR / "Cargo.toml").exists(), f"Failed to extract PyApp"
    print(f"[bold green]OK[/]")


@task(pre=[clean_exe, install, pypi.build], post=[clean_pyapp])  # pyright: ignore[reportUntypedFunctionDecorator]
def build(c: InvokeContext):
    _, cached_python_tar_gz = _config.get_url(EMBEDPY_URL)
    assert cached_python_tar_gz and cached_python_tar_gz.exists(), f"'{cached_python_tar_gz}' not found"
    cached_python_tar_gz = cached_python_tar_gz.resolve()

    class PyAppEnv(BaseModel):
        TARGET_EXE: Annotated[str, Field(exclude=True)]                  # target executable filename
        PYAPP_PROJECT_PATH: str = str(_config.get_whl_file().resolve())  # .whl file of the current project
        PYAPP_PROJECT_FEATURES: Annotated[
            str,
            Field(exclude_if=lambda v: not v)
        ] = "gui"                                           # additional dependency groups
        PYAPP_EXEC_SPEC: str                                # entrypoint spec, e.g. "my_package.__main__:main"
        PYAPP_IS_GUI: Literal["true", "false"] = "false"    # run with pythonw to avoid console window
        PYAPP_UV_ENABLED: Literal["true", "false"] = "true"  # use UV as the backend for PyApp (instead of pip)

        # DISTRIBUTION
        PYAPP_DISTRIBUTION_PATH: Annotated[
            str,
            Field(exclude_if=lambda v: not v)
        ] = str(cached_python_tar_gz)                 # source URL for the python distribution to embed
        PYAPP_DISTRIBUTION_FORMAT: Literal[
            "zip", "tar|gzip", "tar|bzip2", "tar|zstd",
        ] = "tar|gzip"                                    # format of the python distribution (zip or tar.gz)
        PYAPP_DISTRIBUTION_PYTHON_PATH: str = (           # relative path to the python executable inside the embedded distribution
            "python/python.exe"
            if base.WINDOWS else
            "python/bin/python3"
        )
        PYAPP_DISTRIBUTION_EMBED: Literal["true", "false"] = "true"   # embed python distribution in the executable
        # PYAPP_PYTHON_VERSION: str = f"{sys.version_info.major}.{sys.version_info.minor}"  # Python version to use for PyApp

    print(f"[bold] Building PyApp package ... [/]")
    env_list = [
        PyAppEnv(
            TARGET_EXE=str(PORTABLE_EXE.resolve()),
            PYAPP_EXEC_SPEC=f"{PROJECT_NAME}.__main__:main",
        ),
        PyAppEnv(
            TARGET_EXE=str(PORTABLE_GUI_EXE.resolve()),
            PYAPP_IS_GUI="true",
            PYAPP_EXEC_SPEC=f"{PROJECT_NAME}.gui.__main__:main",
        )
    ]
    for env in env_list:
        print(f"\tBuilding {env.TARGET_EXE} ... ", end="")
        with c.cd(str(BUILD_PYAPP_DIR)):  # pyright: ignore[reportUnknownMemberType]
            result = c.run("cargo build --release", env=env.model_dump())
            assert (result is not None) and (result.return_code == 0), f"Failed to build PyApp package '{env.TARGET_EXE}'"
            _config.move(BUILD_PYAPP_DIR / "target" / "release" / f"pyapp{_binary_suffix}", Path(env.TARGET_EXE))
            assert Path(env.TARGET_EXE).exists(), f"Failed to rename PyApp executable to '{env.TARGET_EXE}'"
        print(f"[bold green]OK[/]")
    print(f"[bold] Building PyApp package ... [/][bold green]OK[/]")


@task(pre=[build,])  # pyright: ignore[reportUntypedFunctionDecorator]
def check(c: InvokeContext):
    print("[bold] Checking PyApp binary ... [/]")
    if not base.WINDOWS:
        c.run(f"chmod +rx {PORTABLE_EXE.resolve()}")
        c.run(f"chmod +rx {PORTABLE_GUI_EXE.resolve()}")

    result = c.run(f"{PORTABLE_EXE.resolve()} --version")
    assert (result is not None) and (result.return_code == 0)

    result = c.run(f"{PORTABLE_GUI_EXE.resolve()} --version")
    assert (result is not None) and (result.return_code == 0)
    print("[bold] Checking PyApp binary ... [/][bold green]OK[/]")
