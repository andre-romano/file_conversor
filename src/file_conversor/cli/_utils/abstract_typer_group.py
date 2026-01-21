# src/file_conversor/cli/_utils/abstract_typer_group.py

import typer

from typing import Any, Callable, Protocol, Self

# user-provided modules


class GetTyperProtocol(Protocol):
    def get_typer(self) -> "typer.Typer":
        ...


class AbstractTyperGroup(GetTyperProtocol):
    @property
    def GROUP_NAME(self) -> str:
        return self._typer_cmd.info.name or ""

    @property
    def RICH_HELP_PANEL(self) -> str:
        return self._typer_cmd.info.rich_help_panel or ""

    def __init__(
        self,
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
        self._typer_cmd = typer.Typer(
            name=group_name,
            help=help,
            epilog=epilog,
            short_help=short_help,
            rich_help_panel=rich_help_panel,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated,
        )
        # fix attributes in TyperInfo object
        self._typer_cmd.info.rich_help_panel = rich_help_panel

    def add(self, *objs: GetTyperProtocol):
        for obj in objs:
            self._typer_cmd.add_typer(obj.get_typer())

    def get_typer(self) -> typer.Typer:
        return self._typer_cmd


__all__ = [
    "AbstractTyperGroup",
]
