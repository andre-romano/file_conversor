
# src\file_conversor\main_helper.py

import sys

from typing import Any, Callable

# user provided imports
from file_conversor.config import Log, State, get_translation
from file_conversor.system import System


# Get app config
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class MainHelper:
    __cleanup_tasks: list[Callable[[], None]] = []

    @classmethod
    def _on_exit(cls):
        """Cleanup function to be called on exit."""
        logger.debug(f"{_('Shutting down log system')} ...")
        LOG.shutdown()

    @classmethod
    def _register_cleanup_tasks(cls):
        """Register cleanup tasks to be executed on exit."""
        import atexit

        def _atextit_callback():
            logger.debug("Running cleanup tasks ...")
            for task in cls.__cleanup_tasks:
                try:
                    task()
                except Exception as e:
                    logger.error(f"Error in cleanup task {task}: {repr(e)}", exc_info=True)
        atexit.register(_atextit_callback)

    @classmethod
    def add_cleanup_task(cls, func: Callable[[], Any]) -> None:
        """Add a cleanup task to be executed on exit."""
        cls.__cleanup_tasks.append(func)

    @classmethod
    def run(cls, app_callback: Callable[[], int]) -> None:
        """ Run the main helper with the provided callback. """
        try:
            System.reload_user_path()

            # register cleanup tasks
            cls._register_cleanup_tasks()

            # begin app
            sys.exit(app_callback())
        except Exception as e:
            import subprocess

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
    "MainHelper",
]
