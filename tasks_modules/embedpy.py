# tasks_modules\embedpy.py

import tempfile

from pathlib import Path
from invoke.tasks import task

# user provided
from tasks_modules import _config
from tasks_modules._config import *

from tasks_modules import base, pypi

BUILD_DIR = Path("build") / PROJECT_NAME
PORTABLE_PYTHON_DIR = BUILD_DIR / "python"

PORTABLE_PYTHON_EXE = PORTABLE_PYTHON_DIR / "python.exe"
PORTABLE_PIP_EXE = PORTABLE_PYTHON_DIR / "Scripts" / "pip.exe"
PORTABLE_APP_EXE = PORTABLE_PYTHON_DIR / "Scripts" / f"{PROJECT_NAME}.exe"

PORTABLE_SHIM_BAT = BUILD_DIR / f"{PROJECT_NAME}.bat"


def get_pip_install_cmd(*modules: str):
    cmd = " ".join([
        f'"{PORTABLE_PYTHON_EXE.resolve()}"', "-m",
        "pip",
        "install",
        "--ignore-installed",
        "--prefix", f"{PORTABLE_PYTHON_DIR.resolve()}",
        *modules,
    ])
    return cmd


@task
def mkdirs(c: InvokeContext):
    _config.mkdir([
        "build",
    ])


@task(pre=[mkdirs])
def clean_build(c: InvokeContext):
    remove_path(f"build/*")


@task(pre=[clean_build])
def get_portable_python(c: InvokeContext):
    if not base.WINDOWS:
        raise RuntimeError("Portable Python is only available on Windows")

    print(f"[bold] Getting portable Python ... [/]")
    PORTABLE_PYTHON_DIR.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_zip = Path(temp_dir) / "embedpy.zip"

        print(f"Downloading '{EMBEDPY_URL}' ... ", end="")
        temp_zip.write_bytes(_config.get_url(EMBEDPY_URL))
        print(f"[bold green]OK[/]")

        print(f"Extracting '{temp_zip}' ... ", end="")
        _config.extract(src=temp_zip, dst=PORTABLE_PYTHON_DIR)
        assert PORTABLE_PYTHON_DIR.exists()
        print(f"[bold green]OK[/]")

    if not PORTABLE_PYTHON_EXE:
        raise RuntimeError(f"'{PORTABLE_PYTHON_EXE}' not found")

    result = c.run(f'"{PORTABLE_PYTHON_EXE.resolve()}" --version')
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Cannot run portable Python: {result}")
    print(f"[bold] Getting portable Python ... [/][bold green]OK[/]")


@task(pre=[get_portable_python],)
def config_pip(c: InvokeContext):
    print(f"[bold] Configuring pip ... [/]")
    for path in PORTABLE_PYTHON_DIR.glob("*._pth"):
        content = path.read_text()
        content = re.sub(rf"#.*", "", content)  # remove comments
        if "Lib" not in content:
            content += "\nLib\n"
        if "Lib\\site-packages" not in content:
            content += "\nLib\\site-packages\n"
        if "import site" not in content:
            content += "\nimport site\n"

        content_list = []
        for line in content.splitlines():
            line = line.strip()
            if line and line not in content_list:
                content_list.append(line)
                print(line)
        path.write_text("\n".join(content_list).strip() + "\n", encoding="utf-8")
        print(f"Updated '{path}'")


@task(pre=[config_pip],)
def install_pip(c: InvokeContext):
    print(f"[bold] Installing pip ... [/]")
    get_pip_script = PORTABLE_PYTHON_DIR / "get-pip.py"
    get_pip_script.write_bytes(
        _config.get_url("https://bootstrap.pypa.io/get-pip.py")
    )

    cmd = " ".join([
        f'"{PORTABLE_PYTHON_EXE.resolve()}"',
        f'"{get_pip_script.resolve()}"',
    ])
    print(f"$ {cmd}")
    result = c.run(cmd, out_stream=sys.stdout, err_stream=sys.stderr)
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Cannot install pip: {result}")

    result = c.run(f'"{PORTABLE_PYTHON_EXE.resolve()}" -m pip --version')
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Cannot verify pip installation: {result}")

    if not PORTABLE_PIP_EXE.exists():
        raise RuntimeError(f"pip.exe not found after installation")

    _config.remove_path(get_pip_script.name, base_path=PORTABLE_PYTHON_DIR)
    print(f"[bold] Installing pip ... [/][bold green]OK[/]")


@task(pre=[install_pip],)
def install_setuptools(c: InvokeContext):
    print(f"[bold] Installing setuptools ... [/]")
    cmd = get_pip_install_cmd("setuptools", "wheel")
    print(f"$ {cmd}")
    result = c.run(cmd, out_stream=sys.stdout, err_stream=sys.stderr)
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Cannot install setuptools: {result}")
    print(f"[bold] Installing setuptools ... [/][bold green]OK[/]")


@task
def clean_unused_files(c: InvokeContext, dry_run: bool = False):
    print(f"[bold] Cleaning unused files ... [/]")
    human_size, size_bytes_orig = _config.get_dir_size(BUILD_DIR)
    print(f"Size BEFORE cleaning: {human_size} ({BUILD_DIR})")

    remove_path("**/test", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/tests", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/testing", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/docs", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/examples", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/samples", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/Demos", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/demos", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/benchmarks", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/benchmark", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/.git", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/.github", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/__pycache__", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/*.pyc", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/*.pyo", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path("**/*.chm", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)

    human_size, size_bytes_final = _config.get_dir_size(BUILD_DIR)
    print(f"Size AFTER cleaning: {human_size} ({100 - (size_bytes_final / size_bytes_orig * 100):.2f}%)")
    print(f"[bold] Cleaning unused files ... [/][bold green]OK[/]")


@task(pre=[clean_unused_files],)
def compile_all(c: InvokeContext):
    print(f"[bold] Compile all .py files ... [/]")
    human_size, size_bytes_orig = _config.get_dir_size(BUILD_DIR)
    print(f"Size BEFORE compiling: {human_size} ({BUILD_DIR})")

    cmd = " ".join([
        f'"{PORTABLE_PYTHON_EXE.resolve()}"', "-m",
        'compileall',
        '-b', '-f', '-q',
        '--invalidation-mode=unchecked-hash',
        f'"{PORTABLE_PYTHON_DIR.resolve()}"',
    ])
    print(f"$ {cmd}")
    result = c.run(cmd, out_stream=sys.stdout, err_stream=sys.stderr)
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Cannot compile all .py files: {result}")

    # remove all .py files
    remove_path("**/*.py", base_path=PORTABLE_PYTHON_DIR, verbose=False)

    result = c.run(f'"{PORTABLE_PYTHON_EXE.resolve()}" -m {PROJECT_NAME} --version')
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Failed to run package '{PROJECT_NAME}': {result}")

    human_size, size_bytes_final = _config.get_dir_size(BUILD_DIR)
    print(f"Size AFTER compiling: {human_size} ({100 - (size_bytes_final / size_bytes_orig * 100):.2f}%)")
    print(f"[bold] Compiling all .py files ... [/][bold green]OK[/]")


@task(pre=[install_setuptools, pypi.build], post=[compile_all],)
def install_app(c: InvokeContext):
    print(f"[bold] Installing app {PROJECT_NAME} ... [/]")

    cmd = get_pip_install_cmd(str(_config.get_whl_file()))
    print(f"$ {cmd}")
    result = c.run(cmd, out_stream=sys.stdout, err_stream=sys.stderr)
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Cannot install package '{PROJECT_NAME}': {result}")

    result = c.run(f'"{PORTABLE_PYTHON_EXE.resolve()}" -m {PROJECT_NAME} --version')
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Failed to run package '{PROJECT_NAME}': {result}")

    if not PORTABLE_APP_EXE.exists():
        raise RuntimeError(f"{PROJECT_NAME}.exe not found after installation")
    print(f"[bold] Installing app {PROJECT_NAME} ... [/][bold green]OK[/]")


@task(pre=[install_app],)
def create_shim(c: InvokeContext):
    print(f"[bold] Creating shim ... [/]")
    PORTABLE_SHIM_BAT.write_text(rf"""@echo off
    setlocal
    set SCRIPT_DIR=%~dp0
    set PYTHONHOME=%SCRIPT_DIR%\\{PORTABLE_PYTHON_DIR.relative_to(BUILD_DIR)}    
    set PATH=%PYTHONHOME%\\Scripts;%PYTHONHOME%;%PATH%
    set PYTHON_EXE=%PYTHONHOME%\\{PORTABLE_PYTHON_EXE.relative_to(PORTABLE_PYTHON_DIR)}
    "%PYTHON_EXE%" -m {PROJECT_NAME} %*
    endlocal
""", encoding="utf-8")

    result = c.run(f'"{PORTABLE_SHIM_BAT.resolve()}" --version')
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Failed to run shim for '{PROJECT_NAME}': {result}")
    print(f"[bold] Creating shim ... [/][bold green]OK[/]")


@task(pre=[create_shim])
def build(c: InvokeContext):
    pass


@task(pre=[build,])
def check(c: InvokeContext):
    print("[bold] Checking shim ... [/]")
    result = c.run(f'"{PORTABLE_SHIM_BAT.resolve()}" --version')
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Failed to run shim for '{PROJECT_NAME}': {result}")
    print("[bold] Checking shim ... [/][bold green]OK[/]")
