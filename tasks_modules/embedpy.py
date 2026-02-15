# tasks_modules\embedpy.py

from pathlib import Path

from invoke.tasks import task  # type: ignore

# user provided
from tasks_modules import _config, base, pypi
from tasks_modules._config import *


BUILD_DIR = Path("build") / PROJECT_NAME
PORTABLE_PYTHON_DIR = BUILD_DIR / "python"

PORTABLE_PYTHON_EXE = PORTABLE_PYTHON_DIR / "python.exe"
PORTABLE_PIP_EXE = PORTABLE_PYTHON_DIR / "Scripts" / "pip.exe"
PORTABLE_APP_EXE = PORTABLE_PYTHON_DIR / "Scripts" / f"{PROJECT_NAME}.exe"

PORTABLE_SHIM_CLI_BAT = BUILD_DIR / f"{PROJECT_NAME}.bat"

PORTABLE_SHIM_GUI_BAT = BUILD_DIR / f"{PROJECT_NAME}_gui.bat"
PORTABLE_SHIM_GUI_VBS = BUILD_DIR / f"{PROJECT_NAME}_gui.vbs"


def get_pip_install_cmd(*modules: str):
    return " ".join([
        f'"{PORTABLE_PYTHON_EXE.resolve()}"', "-m",
        "pip",
        "install",
        "--ignore-installed",
        "--no-user",
        "--prefix", f"{PORTABLE_PYTHON_DIR.resolve()}",
        *modules,
    ])


@task
def mkdirs(_: InvokeContext):
    _config.mkdir([
        "build",
    ])


@task(pre=[mkdirs])  # pyright: ignore[reportUntypedFunctionDecorator]
def clean_build(_: InvokeContext):
    remove_path_pattern(f"build/*")


@task(pre=[clean_build])  # pyright: ignore[reportUntypedFunctionDecorator]
def get_portable_python(c: InvokeContext):
    if not base.WINDOWS:
        raise RuntimeError("Portable Python is only available on Windows")

    print(f"[bold] Getting portable Python ... [/]")
    PORTABLE_PYTHON_DIR.parent.mkdir(parents=True, exist_ok=True)

    _, cached_python_zip = _config.get_url(EMBEDPY_URL)
    if not cached_python_zip or not cached_python_zip.exists():
        raise RuntimeError(f"'{cached_python_zip}' not found")

    print(f"Extracting '{cached_python_zip}' ... ", end="")
    _config.extract(src=cached_python_zip, dst=PORTABLE_PYTHON_DIR)
    assert PORTABLE_PYTHON_DIR.exists()
    print(f"[bold green]OK[/]")

    if not PORTABLE_PYTHON_EXE:
        raise RuntimeError(f"'{PORTABLE_PYTHON_EXE}' not found")

    result = c.run(f'"{PORTABLE_PYTHON_EXE.resolve()}" --version')
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Cannot run portable Python: {result}")
    print(f"[bold] Getting portable Python ... [/][bold green]OK[/]")


@task(pre=[get_portable_python],)  # pyright: ignore[reportUntypedFunctionDecorator]
def config_import(_: InvokeContext):
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

        content_list: list[str] = []
        for line in content.splitlines():
            line_parsed = line.strip()
            if line_parsed and line_parsed not in content_list:
                content_list.append(line_parsed)
                print(line_parsed)
        path.write_text("\n".join(content_list).strip() + "\n", encoding="utf-8")
        print(f"Updated '{path}'")


@task(pre=[config_import],)  # pyright: ignore[reportUntypedFunctionDecorator]
def install_pip(c: InvokeContext):
    print(f"[bold] Installing pip ... [/]")

    PIP_SCRIPT_URL = "https://bootstrap.pypa.io/get-pip.py"

    _, CACHED_PIP_PY = _config.get_url(PIP_SCRIPT_URL)
    if not CACHED_PIP_PY or not CACHED_PIP_PY.exists():
        raise RuntimeError(f"'{CACHED_PIP_PY}' not found")

    cmd = " ".join([
        f'"{PORTABLE_PYTHON_EXE.resolve()}"',
        f'"{CACHED_PIP_PY.resolve()}"',
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

    print(f"[bold] Installing pip ... [/][bold green]OK[/]")


@task(pre=[install_pip],)  # pyright: ignore[reportUntypedFunctionDecorator]
def install_setuptools(c: InvokeContext):
    print(f"[bold] Installing setuptools ... [/]")
    cmd = get_pip_install_cmd("setuptools", "wheel")
    print(f"$ {cmd}")
    result = c.run(cmd, out_stream=sys.stdout, err_stream=sys.stderr)
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Cannot install setuptools: {result}")
    print(f"[bold] Installing setuptools ... [/][bold green]OK[/]")


@task
def clean_unused_files(_: InvokeContext, dry_run: bool = False):
    print(f"[bold] Cleaning unused files ... [/]")
    human_size, size_bytes_orig = _config.get_dir_size(BUILD_DIR)
    print(f"Size BEFORE cleaning: {human_size} ({BUILD_DIR})")

    # remove_path_pattern("**/test", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    # remove_path_pattern("**/tests", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    # remove_path_pattern("**/testing", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path_pattern("**/docs", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path_pattern("**/examples", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path_pattern("**/samples", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path_pattern("**/Demos", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path_pattern("**/demos", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path_pattern("**/benchmarks", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path_pattern("**/benchmark", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path_pattern("**/.git", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path_pattern("**/.github", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path_pattern("**/__pycache__", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path_pattern("**/*.pyc", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path_pattern("**/*.pyo", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)
    remove_path_pattern("**/*.chm", base_path=PORTABLE_PYTHON_DIR, dry_run=dry_run)

    human_size, size_bytes_final = _config.get_dir_size(BUILD_DIR)
    print(f"Size AFTER cleaning: {human_size} ({100 - (size_bytes_final / size_bytes_orig * 100):.2f}%)")
    print(f"[bold] Cleaning unused files ... [/][bold green]OK[/]")


@task(pre=[install_setuptools, pypi.build])  # pyright: ignore[reportUntypedFunctionDecorator]
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


@task(pre=[install_app],)  # pyright: ignore[reportUntypedFunctionDecorator]
def create_shim(c: InvokeContext):
    print(f"[bold] Creating shim ... [/]")

    def get_shim_bat_contents(py_module_name: str, *args: str):
        return rf"""@echo off
    setlocal
    set SCRIPT_DIR=%~dp0
    set PYTHONHOME=%SCRIPT_DIR%\\{PORTABLE_PYTHON_DIR.relative_to(BUILD_DIR)}    
    set PATH=%PYTHONHOME%\\Scripts;%PYTHONHOME%;%PATH%
    set PYTHON_EXE=%PYTHONHOME%\\{PORTABLE_PYTHON_EXE.relative_to(PORTABLE_PYTHON_DIR)}
    "%PYTHON_EXE%" -m {py_module_name} {' '.join(args)} %*
    endlocal
"""
    PORTABLE_SHIM_CLI_BAT.write_text(
        get_shim_bat_contents(PROJECT_NAME),
        encoding="utf-8",
    )
    result = c.run(f'"{PORTABLE_SHIM_CLI_BAT.resolve()}" --version')
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Failed to run CLI shim for '{PROJECT_NAME}': {result}")

    PORTABLE_SHIM_GUI_BAT.write_text(
        get_shim_bat_contents(f"{PROJECT_NAME}_gui"),
        encoding="utf-8",
    )
    if not PORTABLE_SHIM_GUI_BAT.exists():
        raise RuntimeError(f"Failed to create GUI shim for '{PROJECT_NAME}'")

    PORTABLE_SHIM_GUI_VBS.write_text(rf'''
    Set WshShell = CreateObject("WScript.Shell")

    ' Folder where the VBS script is located
    scriptFolder = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

    ' Full path to the .bat file
    batPath = scriptFolder & "\{PORTABLE_SHIM_GUI_BAT.name}"

    ' Run hidden (0), don't wait (False)
    WshShell.Run """" & batPath & """ gui start", 0, False
    ''', encoding="utf-8")
    if not PORTABLE_SHIM_GUI_VBS.exists():
        raise RuntimeError(f"Failed to create VBS shim for '{PROJECT_NAME}'")

    print(f"[bold] Creating shim ... [/][bold green]OK[/]")


@task(pre=[create_shim])  # pyright: ignore[reportUntypedFunctionDecorator]
def build(c: InvokeContext):
    pass


@task(pre=[build,])  # pyright: ignore[reportUntypedFunctionDecorator]
def check(c: InvokeContext):
    print("[bold] Checking shim ... [/]")
    result = c.run(f'"{PORTABLE_SHIM_CLI_BAT.resolve()}" --version')
    if (result is None) or (result.return_code != 0):
        raise RuntimeError(f"Failed to run shim for '{PROJECT_NAME}': {result}")
    print("[bold] Checking shim ... [/][bold green]OK[/]")
