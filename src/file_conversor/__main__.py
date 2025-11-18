
# src\file_conversor\__main__.py

import subprocess
import sys

# user provided imports
from file_conversor.cli import Environment, app_cmd, STATE, CONFIG, LOG, logger, _
from file_conversor.config import add_cleanup_task
from file_conversor.system import reload_user_path


def cleanup():
    """Cleanup function to be called on exit."""
    logger.debug(f"{_('Shutting down log system')} ...")
    LOG.shutdown()


# Entry point of the app
def main() -> None:
    try:
        # Register cleanup for normal exits
        add_cleanup_task(cleanup)

        # begin app
        reload_user_path()
        app_cmd(prog_name=Environment.get_app_name())
        sys.exit(0)
    except Exception as e:
        error_type = str(type(e))
        error_type = error_type.split("'")[1]
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
