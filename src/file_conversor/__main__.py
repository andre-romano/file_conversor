
# src\file_conversor\__main__.py

import subprocess
import sys

from rich import print

# user provided imports
from file_conversor.cli import app_cmd, STATE, CONFIG, LOG, logger, _
from file_conversor.system import reload_user_path


# Entry point of the app
def main() -> None:
    try:
        # begin app
        reload_user_path()
        app_cmd(prog_name="file_conversor")
        LOG.shutdown()
        sys.exit(0)
    except Exception as e:
        error_type = str(type(e))
        error_type = error_type.split("'")[1]
        logger.error(f"{error_type} ({e})", exc_info=True if STATE["debug"] else None)
        if isinstance(e, subprocess.CalledProcessError):
            logger.error(f"CMD: {e.cmd} ({e.returncode})")
            logger.error(f"STDERR: {e.stderr}")
            logger.error(f"STDOUT: {e.stdout}")
        LOG.shutdown()
        if STATE["debug"]:
            raise
        sys.exit(1)


# Start the application
if __name__ == "__main__":
    main()
