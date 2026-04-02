# src/file_conversor/system/context_menu.py

from abc import abstractmethod
from pathlib import Path
from typing import Annotated, Callable, Self

from pydantic import BaseModel, Field, model_validator


class ContextMenuItem(BaseModel):
    name: Annotated[str, Field(min_length=1)]
    description: Annotated[str, Field(min_length=1)]
    args: Annotated[list[str], Field(min_length=1)]
    icon: Path | None = None
    keep_terminal_open: bool = False

    @model_validator(mode='after')
    def _model_validator(self):
        if self.icon and (not self.icon.exists() or not self.icon.is_file()):
            raise ValueError(f"Icon file does not exist: {self.icon}")
        return self


class ContextMenu:
    _instance: Self | None = None

    CallbackSignature = Callable[[Self, Path], None]

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()  # type: ignore
        return cls._instance  # type: ignore

    def __init__(self) -> None:
        super().__init__()

        from file_conversor.config.environment import Environment
        self._icons_folder = Environment.get_icons_folder()
        self._exe_path = Environment.get_executable()
        self._register_callbacks: list[ContextMenu.CallbackSignature] = []

    def _execute_callbacks(self) -> None:
        while self._register_callbacks:
            callback = self._register_callbacks.pop()
            callback(self, self._icons_folder)

    def register_callback(self, function: 'ContextMenu.CallbackSignature') -> None:
        self._register_callbacks.append(function)

    @abstractmethod
    def add_extension(self, ext: str, commands: list[ContextMenuItem]) -> None:
        ...


__all__ = [
    "ContextMenuItem",
    "ContextMenu",
]
