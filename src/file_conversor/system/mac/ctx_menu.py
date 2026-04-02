
# src/file_conversor/system/mac/ctx_menu.py

from typing import override

from file_conversor.system.context_menu import ContextMenu, ContextMenuItem


class MacContextMenu(ContextMenu):
    """Dummy MacOS context menu handler (OS does not support this feature)."""

    @override
    def add_extension(self, ext: str, commands: list[ContextMenuItem]) -> None:
        """Dummy method (not supported in mac)."""


__all__ = [
    "MacContextMenu",
]
