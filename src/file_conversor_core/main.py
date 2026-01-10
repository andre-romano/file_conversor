
# src\file_conversor_core\main.py

import subprocess
import sys

from typing import Callable

# user provided imports
from file_conversor.config import State, Log, get_translation, add_cleanup_task
from file_conversor.system import reload_user_path

# Get app config
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


def _cleanup():
    """Cleanup function to be called on exit."""
    logger.debug(f"{_('Shutting down log system')} ...")
    LOG.shutdown()


# Entry point of the app
def start_app(start_app_callback: Callable[[], None]) -> None:
    try:
        # Register cleanup for normal exits
        add_cleanup_task(_cleanup)

        # config env variables
        reload_user_path()

        # begin app
        start_app_callback()

        # terminate app
        sys.exit(0)
    except Exception as e:
        debug_mode = STATE.loglevel.level.is_debug()
        error_type = str(type(e))
        error_type = error_type.split("'")[1]
        logger.error(f"{error_type} ({e})", exc_info=True if debug_mode else None)
        if isinstance(e, subprocess.CalledProcessError):
            logger.error(f"CMD: {e.cmd} ({e.returncode})")
            logger.error(f"STDERR: {e.stderr}")
            logger.error(f"STDOUT: {e.stdout}")
        if debug_mode:
            raise
        sys.exit(1)


__all__ = [
    "start_app",
]
