# src/file_conversor/cli/_utils/abstract_typer_command.py

from pathlib import Path
from typing import Any, Callable

import typer

# user-provided modules
from file_conversor.system import (
    ContextMenu,
    LinuxContextMenu,
    LinuxSystem,
    MacContextMenu,
    MacSystem,
    System,
    WinContextMenu,
    WindowsSystem,
)


def _get_ctx_menu() -> ContextMenu:
    match System:
        case WindowsSystem():
            return WinContextMenu.get_instance()
        case LinuxSystem():
            return LinuxContextMenu.get_instance()
        case MacSystem():
            return MacContextMenu.get_instance()
        case _:
            raise ValueError(f"Unsupported system: {System}")


class AbstractTyperCommand:
    _CTX_MENU: ContextMenu = _get_ctx_menu()

    @property
    def COMMAND_NAME(self) -> str:  # noqa: S100
        return self._COMMAND_NAME

    @property
    def GROUP_NAME(self) -> str:  # noqa: S100
        return self._GROUP_NAME

    @property
    def RICH_HELP_PANEL(self) -> str:  # noqa: S100
        return self._typer_cmd.info.rich_help_panel or ""

    def register_ctx_menu(self, ctx_menu: ContextMenu, icons_folder: Path) -> None:
        """ Override this method to register context menu items for this command. By default, it does nothing. """

    def __init__(
        self,
        function: Callable[..., Any],
        command_name: str,
        group_name: str | None = None,
        short_help: str | None = None,
        help: str | None = None,
        epilog: str | None = None,
        rich_help_panel: str | None = None,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool = False,
    ) -> None:
        super().__init__()
        self._GROUP_NAME = group_name or ""
        self._COMMAND_NAME = command_name

        self._typer_cmd = typer.Typer()
        self._typer_cmd.command(
            name=command_name,
            help=help,
            epilog=epilog,
            short_help=short_help,
            rich_help_panel=rich_help_panel,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated,
        )(function)

        self._CTX_MENU.register_callback(self.register_ctx_menu)

    def get_typer(self) -> typer.Typer:
        return self._typer_cmd


__all__ = [
    "AbstractTyperCommand",
]
