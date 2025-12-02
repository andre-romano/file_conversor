# src\file_conversor\system\win\context_menu.py

from typing import Self, Callable
from pathlib import Path

from rich import print

# user-provided modules
from file_conversor.system.win.reg import WinRegFile, WinRegKey
from file_conversor.system.win.utils import is_admin

from file_conversor.config import Environment, Log, AbstractSingletonThreadSafe
from file_conversor.config.locale import get_translation

# get app config
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WinContextCommand:
    def __init__(self, name: str, description: str, command: str, icon: str | None = None) -> None:
        """
        Creates a windows context menu

        multi_select =
        ```python
        True  # command accepts multi file selection
        False # command available for single files (only)
        ```

        :param name: Name used to create command keys
        :param description: Description of the command (as the user sees it)
        :param command: Command to execute (accepts "%1" for single path input, %* for many inputs - no DOUBLE QUOTES)
        :param multi_select_model: If command valid for multiple files.
        :param icon: Icon to display with command.
        """
        super().__init__()
        self.name = name
        self.description = description
        self.command = command
        self.icon = icon


class WinContextMenu(AbstractSingletonThreadSafe):

    def __init__(self) -> None:
        """Set context menu for all users, or for current user ONLY"""
        super().__init__()

        self.MENU_NAME = "File Conversor"
        self.ICON_FILE_PATH = Path(f"{Environment.get_icons_folder()}/icon.ico").resolve()

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

    def add_extension(self, ext: str, commands: list[WinContextCommand]):
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
        logger.debug(f"Added commands for '{root_key}'")


__all__ = [
    "WinContextMenu",
    "WinContextCommand",
]
