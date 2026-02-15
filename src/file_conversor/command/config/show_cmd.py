
# src\file_conversor\command\config\show_cmd.py

from enum import Enum

# user-provided modules
from file_conversor.config import Configuration, Log, State, get_translation


# get app config
CONFIG = Configuration.get()
STATE = State.get()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class ConfigShowCommand:
    EXTERNAL_DEPENDENCIES: set[str] = set()

    class SupportedInFormats(Enum):
        """empty enum since this command doesn't take input files."""

    class SupportedOutFormats(Enum):
        """empty enum since this command doesn't take input files."""

    @classmethod
    def show(cls):
        logger.info(f"{_('Configuration')}: {CONFIG.to_dict()}")


__all__ = [
    "ConfigShowCommand",
]
