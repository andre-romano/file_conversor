
# src/file_conversor.py

import subprocess
import sys

from rich import print

# user provided imports
from cli.app_cmd import app_cmd, STATE, CONFIG, logger, _
from system import reload_user_path


# Entry point of the app
def main():
    try:
        # begin app
        reload_user_path()
        app_cmd()
    except Exception as e:
        error_type = str(type(e)).split("'")[1]
        logger.error(f"{error_type} ({e})", exc_info=True if STATE["debug"] else None)
        if isinstance(e, subprocess.CalledProcessError):
            logger.error(f"CMD: {e.cmd} ({e.returncode})")
            logger.error(f"STDERR: {e.stderr}")
            logger.error(f"STDOUT: {e.stdout}")
        if STATE["debug"]:
            raise
        sys.exit(1)


# Start the application
if __name__ == "__main__":
    main()
