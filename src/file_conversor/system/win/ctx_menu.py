# src\file_conversor\system\win\context_menu.py

from typing import Iterable, override

from file_conversor.system.context_menu import ContextMenu, ContextMenuItem
from file_conversor.system.win.reg import WinRegFile, WinRegKey


class WinContextMenu(ContextMenu):
    def __init__(self) -> None:
        """Set context menu for all users, or for current user ONLY"""
        super().__init__()
        from file_conversor.system.win.windows_system import WindowsSystem

        self.MENU_NAME = "File Conversor"
        self.ICON_FILE_PATH = (self._icons_folder / "icon.ico").resolve()

        root_key_stem = self.MENU_NAME.replace(" ", "").strip()
        self.ROOT_KEY_USER = rf"HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\{{ext}}\shell\{root_key_stem}"
        self.ROOT_KEY_MACHINE = rf"HKEY_LOCAL_MACHINE\Software\Classes\SystemFileAssociations\{{ext}}\shell\{root_key_stem}"

        self._root_key_template = self.ROOT_KEY_MACHINE if WindowsSystem.is_admin() else self.ROOT_KEY_USER
        self._reg_file = WinRegFile()

    def _get_command(self, cmd: ContextMenuItem) -> str:
        args = ' '.join(f'"{arg}"' for arg in cmd.args)
        command = f'{self._exe_path} {args} "%1"'
        if cmd.keep_terminal_open:
            return f'cmd.exe /k "{command}"'
        return f'cmd.exe /c "{command}"'

    def get_reg_file(self) -> WinRegFile:
        self._execute_callbacks()
        return self._reg_file

    @override
    def add_extension(self, ext: str, commands: Iterable[ContextMenuItem]):
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
                    "Icon": str(cmd.icon) if cmd.icon else "",
                }),
                WinRegKey(rf"{root_key}\shell\{cmd.name}\command").update({
                    "@": self._get_command(cmd),
                }),
            ])


__all__ = [
    "WinContextMenu",
]
