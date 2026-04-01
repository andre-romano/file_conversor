# src/file_conversor/command/abstract_cmd.py

from abc import abstractmethod
from enum import StrEnum
from typing import Annotated, Any, Callable, Iterable

from pydantic import BaseModel, Field


class AbstractCommand[InFormatStrEnum: StrEnum, OutFormatStrEnum: StrEnum](BaseModel):
    """
    Abstract base class for all commands in the file conversor application.
    This class defines the interface that all concrete command classes must implement.
    """
    progress_callback: Annotated[Callable[[float], Any], Field(exclude=True)] = lambda p: p  # default to a no-op callback

    @classmethod
    @abstractmethod
    def _external_dependencies(cls) -> Iterable[str]:  # noqa: S100
        """
        List of external dependencies required by the command.
        This should be overridden by concrete command classes to specify their dependencies.
        """

    @classmethod
    @abstractmethod
    def _supported_in_formats(cls) -> type[InFormatStrEnum]:  # noqa: S100
        """ 
        Get the supported input formats for the command. 
        This should be overridden by concrete command classes to specify their supported input formats. 
        """

    @classmethod
    @abstractmethod
    def _supported_out_formats(cls) -> type[OutFormatStrEnum]:  # noqa: S100
        """ 
        Get the supported output formats for the command. 
        This should be overridden by concrete command classes to specify their supported output formats. 
        """

    @classmethod
    def get_in_formats(cls) -> list[str]:
        """
        Get the supported input formats for the command.
        """
        return [format.value.lower() for format in cls._supported_in_formats()]  # noqa: S5864

    @classmethod
    def get_out_formats(cls) -> list[str]:
        """
        Get the supported output formats for the command.
        """
        return [format.value.lower() for format in cls._supported_out_formats()]  # noqa: S5864

    @classmethod
    def check_dependencies(cls) -> bool:
        """
        Check if all external dependencies required by the command are available.
        This method can be overridden by concrete command classes to implement specific checks.
        """
        import shutil
        return all(shutil.which(dep) is not None for dep in cls._external_dependencies())  # noqa: S5864

    def set_progress_callback(self, callback: Callable[[float], Any]) -> None:
        """
        Set the progress callback function that will be called to update the progress of the command execution.
        """
        self.progress_callback = callback

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the command. This method must be implemented by all concrete command classes to perform the actual work of the command.
        """


__all__ = [
    "AbstractCommand",
]
