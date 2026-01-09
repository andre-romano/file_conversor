# src\file_conversor\config\state.py

from pathlib import Path

from dataclasses import dataclass

# user provided imports
from file_conversor.config.log import Log

# Get app config
LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class StateLogfile:
    def __init__(self, enabled: bool = True) -> None:
        super().__init__()
        self.enabled = enabled

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self.__enabled = value
        logger.debug(f"'File logging': [blue bold]{'ENABLED' if value else 'DISABLED'}[/]")


class StateLogLevel:
    """State action to set log level."""

    def __init__(self, level: Log.Level = Log.Level.INFO) -> None:
        super().__init__()
        self.level = level

    def get(self) -> Log.Level:
        return Log.Level.get()

    @property
    def level(self) -> Log.Level:
        return self.get()

    @level.setter
    def level(self, value: Log.Level) -> None:
        logger.debug(f"Log Mode: [blue bold]{value.set().name}[/]")


class StateProgressBar:
    def __init__(self, enabled: bool = True) -> None:
        super().__init__()
        self.enabled = enabled

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self.__enabled = value
        logger.debug(f"'Progress bars': [blue red]'{'ENABLED' if self.enabled else 'DISABLED'}'[/]")


class StateOverwriteOutput:
    def __init__(self, enabled: bool = False) -> None:
        super().__init__()
        self.__enabled = enabled

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self.__enabled = value
        logger.debug(f"Output overwrite mode: [blue bold]{'ENABLED' if self.enabled else 'DISABLED'}[/]")


@dataclass
class StatesDataModel:
    """States data structure"""
    progress: StateProgressBar
    overwrite_output: StateOverwriteOutput
    loglevel: StateLogLevel
    logfile: StateLogfile


# STATE controller dict class
class State:
    """Application state manager."""
    __states: StatesDataModel = StatesDataModel(
        progress=StateProgressBar(),
        overwrite_output=StateOverwriteOutput(),
        loglevel=StateLogLevel(),
        logfile=StateLogfile(),
    )

    @classmethod
    def get(cls) -> StatesDataModel:
        """Get application states data."""
        return cls.__states


__all__ = [
    "State",
    "StatesDataModel",
]
