
# src\file_conversor\__main__.py

import subprocess
import sys

from rich import print

# user provided imports
from file_conversor.cli import app_cmd, STATE, CONFIG, LOG, logger, _
from file_conversor.system import reload_user_path


# Entry point of the app
def main():
    exitcode = 0
    try:
        # begin app
        reload_user_path()
        app_cmd(prog_name="file_conversor")
    except Exception as e:
        error_type = str(type(e)).split("'")[1]
        logger.error(f"{error_type} ({e})", exc_info=True if STATE["debug"] else None)
        if isinstance(e, subprocess.CalledProcessError):
            logger.error(f"CMD: {e.cmd} ({e.returncode})")
            logger.error(f"STDERR: {e.stderr}")
            logger.error(f"STDOUT: {e.stdout}")
        if STATE["debug"]:
            LOG.shutdown()
            raise
        exitcode = 1
    finally:
        LOG.shutdown()
        sys.exit(exitcode)


# Start the application
if __name__ == "__main__":
    main()
