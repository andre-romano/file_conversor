
# src/file_conversor/system/lin/ctx_menu.py

from typing import override

from file_conversor.system.context_menu import ContextMenu, ContextMenuItem


class LinuxContextMenu(ContextMenu):
    """Linux context menu handler."""

    @override
    def add_extension(self, ext: str, commands: list[ContextMenuItem]) -> None:
        """TODO: implement context menu for linux (not trivial, since it depends on the desktop environment)."""


__all__ = [
    "LinuxContextMenu",
]
