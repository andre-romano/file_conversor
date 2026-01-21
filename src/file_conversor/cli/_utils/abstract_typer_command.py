# src/file_conversor/cli/_utils/abstract_typer_command.py

import typer

from typing import Any, Callable, Iterable, Protocol, Self

# user-provided modules
from file_conversor.config.environment import Environment
from file_conversor.system.win.ctx_menu import WinContextMenu


class RegisterCtxMenuProtocol(Protocol):
    def register_ctx_menu(self, ctx_menu: WinContextMenu) -> None:
        ...


class AbstractTyperCommand(RegisterCtxMenuProtocol):
    @property
    def COMMAND_NAME(self) -> str:
        return self._COMMAND_NAME

    @property
    def GROUP_NAME(self) -> str:
        return self._GROUP_NAME

    @property
    def RICH_HELP_PANEL(self) -> str:
        return self._typer_cmd.info.rich_help_panel or ""

    def __init__(
        self,
        function: Callable[..., Any],
        command_name: str,
        group_name: str | None = None,
        short_help: str | None = None,
        help: str | None = None,
        epilog: str | None = None,
        rich_help_panel: str | None = None,
        no_args_is_help: bool = True,
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

        ctx_menu = WinContextMenu.get_instance(icons_folder=Environment.get_icons_folder())
        ctx_menu.register_callback(self.register_ctx_menu)

    def get_typer(self) -> typer.Typer:
        return self._typer_cmd


__all__ = [
    "RegisterCtxMenuProtocol",
    "AbstractTyperCommand",
]
