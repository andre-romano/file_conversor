# src\file_conversor\config\cleanup.py

import atexit
import sys

from typing import Callable

# user provided imports
from file_conversor.config.log import Log

# Get app config
logger = Log.get_instance().getLogger(__name__)


__cleanup_tasks: list[Callable[[], None]] = []


def add_cleanup_task(func: Callable[[], None]) -> None:
    """Add a cleanup task to be executed on exit."""
    __cleanup_tasks.append(func)


def __cleanup():
    """Run all registered cleanup tasks."""
    logger.info("Running cleanup tasks ...")
    for task in __cleanup_tasks:
        try:
            task()
        except Exception as e:
            logger.error(f"Error in cleanup task {task}: {repr(e)}", exc_info=True)


atexit.register(__cleanup)


__all__ = [
    "add_cleanup_task",
]
