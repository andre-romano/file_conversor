# src\file_conversor\system\win\context_menu.py

from dataclasses import dataclass
from typing import Iterable, Self, Callable
from pathlib import Path

# user-provided modules
from file_conversor.system.win.reg import WinRegFile, WinRegKey
from file_conversor.system.win.utils import is_admin


@dataclass
class WinContextCommand:
    name: str
    """ Name used to create command keys """
    description: str
    """ Description of the command (as the user sees it) """
    command: str
    """ Command to execute (accepts "%1" for single path input, %* for many inputs - no DOUBLE QUOTES) """
    icon: str | None = None
    """ Icon to display with command. """


class WinContextMenu:
    _instance = None

    @classmethod
    def get_instance(cls, icons_folder: Path) -> 'WinContextMenu':
        if cls._instance is None:
            cls._instance = WinContextMenu(icons_folder)
        return cls._instance

    def __init__(self, icons_folder: Path) -> None:
        """Set context menu for all users, or for current user ONLY"""
        super().__init__()

        self.MENU_NAME = "File Conversor"
        self.ICON_FILE_PATH = Path(f"{icons_folder}/icon.ico").resolve()

        self.ROOT_KEY_USER = rf"HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\{{ext}}\shell\FileConversor"
        self.ROOT_KEY_MACHINE = rf"HKEY_LOCAL_MACHINE\Software\Classes\SystemFileAssociations\{{ext}}\shell\FileConversor"

        self._root_key_template = self.ROOT_KEY_MACHINE if is_admin() else self.ROOT_KEY_USER
        self._reg_file = WinRegFile()
        self._register_callbacks: list[Callable[[Self], None]] = []

    def get_reg_file(self) -> WinRegFile:
        # run callback prior to getting reg_file
        while self._register_callbacks:
            callback = self._register_callbacks.pop()
            callback(self)
        return self._reg_file

    def register_callback(self, function: Callable[[Self], None]) -> None:
        self._register_callbacks.append(function)

    def add_extension(self, ext: str, commands: Iterable[WinContextCommand]):
        """
        Add extension and context menu for commands

        :param ext: Extension. Format .EXT
        :param commands: Format {name: command}
        """
        root_key_name = self._root_key_template.replace(f"{{ext}}", f"{ext}")
        root_key = WinRegKey(root_key_name).update({
            "MUIVerb": self.MENU_NAME,
            "Icon": str(self.ICON_FILE_PATH),
            "SubCommands": "",
        })
        self._reg_file.add_key(root_key)
        for cmd in commands:
            self._reg_file.update([
                WinRegKey(rf"{root_key}\shell\{cmd.name}").update({
                    "MUIVerb": cmd.description,
                    "Icon": cmd.icon if cmd.icon else "",
                }),
                WinRegKey(rf"{root_key}\shell\{cmd.name}\command").update({
                    "@": cmd.command,
                }),
            ])


__all__ = [
    "WinContextMenu",
    "WinContextCommand",
]
