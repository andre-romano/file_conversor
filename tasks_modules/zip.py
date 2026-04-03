# tasks_modules\zip.py

from invoke.tasks import task  # pyright: ignore[reportUnknownVariableType]

# user provided
from tasks_modules import _config, base, pyapp
from tasks_modules._config import *  # noqa: S2208


BUILD_DIR = pyapp.BUILD_DIR

APP_EXE = pyapp.PORTABLE_EXE
APP_GUI_EXE = pyapp.PORTABLE_GUI_EXE
build_app = pyapp.check

if base.WINDOWS:
    ZIPPED_APP_CURR = ZIPPED_APP_WIN
elif base.LINUX:
    ZIPPED_APP_CURR = ZIPPED_APP_LIN  # pyright: ignore[reportConstantRedefinition]
else:
    ZIPPED_APP_CURR = ZIPPED_APP_MAC  # pyright: ignore[reportConstantRedefinition]


@task
def mkdirs(_: InvokeContext):
    _config.mkdir([
        "dist",
        "build",
    ])


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean_zip(_: InvokeContext):
    _config.remove_path_pattern(f"{ZIPPED_APP_WIN}")
    _config.remove_path_pattern(f"{ZIPPED_APP_LIN}")
    _config.remove_path_pattern(f"{ZIPPED_APP_MAC}")


@task(pre=[clean_zip, build_app])  # pyright: ignore[reportUntypedFunctionDecorator]
def build(_: InvokeContext):
    print(f"[bold] Building archive '{ZIPPED_APP_CURR}' ... [/]")

    human_size, size_bytes_orig = get_dir_size(BUILD_DIR)
    print(f"Size BEFORE compression: {human_size} ({BUILD_DIR})")

    _config.compress(src=BUILD_DIR, dst=ZIPPED_APP_CURR)
    if not ZIPPED_APP_CURR.exists():
        raise RuntimeError(f"'{ZIPPED_APP_CURR}' not found")

    human_size, size_bytes_final = get_dir_size(ZIPPED_APP_CURR)
    print(f"Size AFTER compression: {human_size} (-{100 - (size_bytes_final / size_bytes_orig * 100):.2f}%)")
    print(f"[bold] Building archive '{ZIPPED_APP_CURR}' ... [/][bold green]OK[/]")


@task(pre=[build,],)  # pyright: ignore[reportUntypedFunctionDecorator]
def extract_app(_: InvokeContext):
    print(rf'[bold] Extracting {ZIPPED_APP_CURR} ... [/]')
    _config.remove_path_pattern(str(BUILD_DIR))
    assert not APP_EXE.exists(), f"'{APP_EXE}' found"
    assert not APP_GUI_EXE.exists(), f"'{APP_GUI_EXE}' found"

    _config.extract(src=ZIPPED_APP_CURR, dst=BUILD_DIR.parent)
    assert APP_EXE.exists(), f"'{APP_EXE}' not found"
    assert APP_GUI_EXE.exists(), f"'{APP_GUI_EXE}' not found"
    print(rf'[bold] Extracting {ZIPPED_APP_CURR} ... [/][bold green]OK[/]')


@task(pre=[extract_app,])  # pyright: ignore[reportUntypedFunctionDecorator]
def check(c: InvokeContext):
    print("[bold] Checking .ZIP ... [/]")
    if not base.WINDOWS:
        c.run(f"chmod +rx {APP_EXE.resolve()}")
    result = c.run(f"{APP_EXE.resolve()} --version")
    assert (result is not None) and (result.return_code == 0)
    print("[bold] Checking .ZIP ... [/][bold green]OK[/]")
