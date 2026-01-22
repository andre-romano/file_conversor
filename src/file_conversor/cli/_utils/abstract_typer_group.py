# src/file_conversor/cli/_utils/abstract_typer_group.py

import typer
import typer.core

from enum import Enum
from typing import Any, Callable, Protocol, Self
from dataclasses import dataclass

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

    class MarkupMode(Enum):
        NONE = None
        MARKDOWN = "markdown"
        RICH = "rich"

    @dataclass
    class CallbackDataModel:
        function: Callable[..., Any]
        help: str | None = None
        epilog: str | None = None
        short_help: str | None = None
        hidden: bool = False
        deprecated: bool = False

        def attach(self, typer_cmd: typer.Typer) -> None:
            typer_cmd.callback(
                help=self.help,
                epilog=self.epilog,
                short_help=self.short_help,
                hidden=self.hidden,
                deprecated=self.deprecated,
            )(self.function)

    def __init__(
        self,
        group_name: str | None = None,
        short_help: str | None = None,
        help: str | None = None,
        epilog: str | None = None,
        rich_help_panel: str | None = None,
        rich_markup_mode: MarkupMode = MarkupMode(typer.core.DEFAULT_MARKUP_MODE),
        no_args_is_help: bool = True,
        hidden: bool = False,
        deprecated: bool = False,
        context_settings: dict[Any, Any] | None = None,
        callback: CallbackDataModel | None = None,
    ) -> None:
        super().__init__()
        self._typer_cmd = typer.Typer(
            name=group_name,
            help=help,
            epilog=epilog,
            short_help=short_help,
            rich_help_panel=rich_help_panel,
            rich_markup_mode=rich_markup_mode.value,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated,
            context_settings=context_settings
        )
        # fix attributes in TyperInfo object
        self._typer_cmd.info.rich_help_panel = rich_help_panel

        if callback is not None:
            callback.attach(self._typer_cmd)

    def add(self, *objs: GetTyperProtocol):
        for obj in objs:
            self._typer_cmd.add_typer(obj.get_typer())

    def get_typer(self) -> typer.Typer:
        return self._typer_cmd


__all__ = [
    "AbstractTyperGroup",
]
