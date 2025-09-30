
import sys
import os

from pathlib import Path


def configure_site_packages():
    sites = [
        Path(__file__).parent / "_internal",
    ]
    for path in sites:
        if path.exists() and str(path) not in sys.path:
            sys.path.insert(0, str(path))


def configure_path():
    PATH = os.environ["PATH"].split(os.pathsep)
    paths = [
        Path(__file__).parent / "_internal" / "bin",
    ]
    for path in paths:
        if path.exists() and str(path) not in PATH:
            PATH.append(str(path))
    os.environ["PATH"] = os.pathsep.join(PATH)


def print_python_version():
    print(f"Python version: {sys.version} ({sys.executable}) ")
    print(f"Site-packages: {sys.path}")
    print(f"PATH: {os.environ['PATH'].split(os.pathsep)}")


def shim_main() -> None:
    configure_site_packages()
    configure_path()
    try:
        from file_conversor.__main__ import main
        main()
    except:
        print_python_version()
        raise


# Start the application
if __name__ == "__main__":
    shim_main()
