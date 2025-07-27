
# src/file_conversor.py

import sys

from rich import print
from cli.app_cmd import app_cmd, STATE

from system import reload_user_path


# Entry point of the app
def main():
    try:
        reload_user_path()
        app_cmd()
    except Exception as e:
        if STATE["debug"]:
            raise
        else:
            error_type = str(type(e)).split("'")[1]
            print(f"[red bold]ERROR[/]: {error_type}")
            print(f"{str(e)}")
        sys.exit(1)


# Start the application
if __name__ == "__main__":
    main()
