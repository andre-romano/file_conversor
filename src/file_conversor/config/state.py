# src\file_conversor\config\state.py


from dataclasses import dataclass

# user provided imports
from file_conversor.config.log import LOG, Log


logger = LOG.getLogger(__name__)


class StateLogfile:
    def __init__(self, enabled: bool = True) -> None:
        super().__init__()
        self.__enabled = enabled

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self.__enabled = value
        logger.debug(f"File logging: [bold]{'[blue]ENABLED' if value else '[red]DISABLED'}[/]")


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
        logger.debug(f"Log Mode: [bold blue]{value.set().name}[/]")


class StateProgressBar:
    def __init__(self, enabled: bool = True) -> None:
        super().__init__()
        self.__enabled = enabled

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self.__enabled = value
        logger.debug(f"Progress bars: [bold]{'[blue]ENABLED' if self.enabled else '[red]DISABLED'}[/]")


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
        logger.debug(f"Output overwrite mode: [bold]{'[blue]ENABLED' if self.enabled else '[red]DISABLED'}[/]")


@dataclass
class StatesDataModel:
    """States data structure"""
    progress: StateProgressBar
    overwrite_output: StateOverwriteOutput
    loglevel: StateLogLevel
    logfile: StateLogfile


# STATE controller dict class
STATE = StatesDataModel(
    progress=StateProgressBar(),
    overwrite_output=StateOverwriteOutput(),
    loglevel=StateLogLevel(),
    logfile=StateLogfile(),
)

__all__ = [
    "STATE",
]
