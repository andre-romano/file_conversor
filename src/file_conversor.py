
# src/file_conversor.py

import sys
from pathlib import Path

from rich import print

# user provided imports
from cli.app_cmd import app_cmd, STATE, CONFIG, _
from system import reload_user_path


def get_script_path() -> Path:
    """Get the absolute path of the currently running script."""
    # 1. Check for frozen executables (PyInstaller)
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve()

    # 2. Try __file__ attribute (works for normal scripts/modules)
    try:
        return Path(__file__).resolve()
    except NameError:
        pass

    # 3. Check sys.argv[0] (works when run directly)
    if len(sys.argv) > 0 and sys.argv[0]:
        script_path = Path(sys.argv[0]).resolve()
        if script_path.exists():
            return script_path

    # fallback
    return Path(__file__).resolve()


def get_executable() -> tuple[str, str]:
    path = get_script_path()
    if path.suffix == ".py":
        return f"pdm run python '{path}'", str(path.parent.parent)
    return str(path), str(path.parent)


# Entry point of the app
def main():
    try:
        # set script executable
        STATE['script_executable'], STATE['script_workdir'] = get_executable()
        # begin app
        reload_user_path()
        app_cmd()
    except Exception as e:
        if STATE["debug"]:
            raise
        else:
            error_type = str(type(e)).split("'")[1]
            print(f"[red bold]{_('ERROR')}[/]: {error_type}")
            print(f"{str(e)}")
        sys.exit(1)


# Start the application
if __name__ == "__main__":
    main()
