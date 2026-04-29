
# src/file_conversor/system/lin/ctx_menu.py

import mimetypes
import re
import sys

from pathlib import Path
from typing import override

from file_conversor.config import Environment
from file_conversor.system.context_menu import ContextMenu, ContextMenuItem


class LinuxContextMenu(ContextMenu):
    """Linux context menu handler (KDE Dolphin service menus)."""

    APP_NAME = "file_conversor"
    MENU_NAME = "File Conversor"

    def __init__(self) -> None:
        super().__init__()
        # mime_type -> {dedupe_key: ContextMenuItem}
        self._entries: dict[str, dict[str, ContextMenuItem]] = {}

    def _ext_to_mime(self, ext: str) -> str:
        """Convert a file extension (e.g. '.jpg') to its MIME type."""
        mime, _ = mimetypes.guess_type(f"file{ext}")
        return mime or f"application/x-{ext.lstrip('.').lower()}"

    def _action_id(self, mime: str, index: int, cmd: ContextMenuItem) -> str:
        """Build a stable, KDE-safe action identifier."""
        mime_clean = re.sub(r"[^A-Za-z0-9-]", "-", mime).strip("-")
        name_slug = re.sub(r"[^A-Za-z0-9-]", "-", cmd.description.casefold()).strip("-")
        name_slug = re.sub(r"-+", "-", name_slug) or "action"
        return f"fileconversor-{mime_clean}-{index:02d}-{name_slug}"

    def _cmd_dedupe_key(self, cmd: ContextMenuItem) -> str:
        icon = str(cmd.icon) if cmd.icon else ""
        args = "\x1f".join(cmd.args)
        return f"{cmd.name}\x1e{cmd.description}\x1e{args}\x1e{icon}\x1e{int(cmd.keep_terminal_open)}"

    def _build_exec(self, cmd: ContextMenuItem) -> str:
        launcher = [sys.executable, "-m", Environment.get_app_name(), *cmd.args, "%F"]

        def _quote(arg: str) -> str:
            escaped = arg.replace("\\", "\\\\").replace('"', '\\"')
            if any(ch.isspace() for ch in escaped) or any(ch in escaped for ch in ('"', "'", "\\")):
                return f'"{escaped}"'
            return escaped

        exec_str = " ".join(_quote(arg) for arg in launcher)
        if cmd.keep_terminal_open:
            # TODO: Allow users to configure their preferred terminal emulator in the future.
            # TODO: Add a GUI for this instead of a CLI prompt?
            return f"konsole --hold -e {exec_str}"
        return exec_str

    @override
    def add_extension(self, ext: str, commands: list[ContextMenuItem]) -> None:
        """Register Dolphin context-menu actions for files with the given extension."""
        mime = self._ext_to_mime(ext)
        if mime not in self._entries:
            self._entries[mime] = {}
        actions = self._entries[mime]
        for cmd in commands:
            dedupe_key = self._cmd_dedupe_key(cmd)
            actions[dedupe_key] = cmd

    def _build_desktop_content(self, mime: str) -> str:
        """Render the .desktop file content for a single MIME type."""
        actions = self._entries[mime]
        ordered_actions = sorted(
            actions.items(),
            key=lambda item: (
                item[1].description.casefold(),
                item[1].name.casefold(),
                item[0],
            ),
        )
        action_ids = [
            self._action_id(mime, index, cmd)
            for index, (_, cmd) in enumerate(ordered_actions, start=1)
        ]

        app_icon = self._icons_folder / "icon.png"
        if not app_icon.exists():
            app_icon = self._icons_folder / "icon.ico"  # fallback just in case

        lines: list[str] = [
            "[Desktop Entry]",
            "Type=Service",
            "ServiceTypes=KonqPopupMenu/Plugin",
            "X-KDE-ServiceTypes=KonqPopupMenu/Plugin",
            "X-KDE-Priority=TopLevel",
            f"Icon={app_icon}",
            f"X-KDE-SubMenuIcon={app_icon}",  # fallback
            f"X-KDE-Submenu={self.MENU_NAME}",
            f"MimeType={mime};",
            f"Actions={';'.join(action_ids)};",
            "",
        ]

        for index, (_, cmd) in enumerate(ordered_actions, start=1):
            action_id = self._action_id(mime, index, cmd)
            exec_str = self._build_exec(cmd)
            lines += [
                f"[Desktop Action {action_id}]",
                f"Name={cmd.description}",
                f"Icon={cmd.icon}" if cmd.icon else "Icon=",
                f"Exec={exec_str}",
                "",
            ]

        return "\n".join(lines)

    def get_desktop_install_dir(self) -> Path:
        """Return the KDE service-menus directory appropriate for the current privilege level."""
        from file_conversor.system.lin.linux_system import LinuxSystem

        if LinuxSystem.is_admin():
            if Path("/usr/share/kio/servicemenus").exists():
                return Path("/usr/share/kio/servicemenus")
            return Path("/usr/share/kservices5/ServiceMenus")
        if (Path.home() / ".local" / "share" / "kio" / "servicemenus").exists():
            return Path.home() / ".local" / "share" / "kio" / "servicemenus"
        return Path.home() / ".local" / "share" / "kservices5" / "ServiceMenus"

    def get_desktop_files(self) -> dict[Path, str]:
        """Execute registered callbacks and return ``{install_path: content}`` for every extension."""
        self._execute_callbacks()
        install_dir = self.get_desktop_install_dir()
        result: dict[Path, str] = {}
        for mime in self._entries:
            clean = mime.replace("/", "_").replace("-", "_").replace("+", "_").lower()
            filename = f"{self.APP_NAME}_{clean}.desktop"
            result[install_dir / filename] = self._build_desktop_content(mime)
        return result

    def get_desktop_uninstall_paths(self) -> list[Path]:
        """Return paths of all currently installed desktop files belonging to this app."""
        dirs = [
            Path.home() / ".local" / "share" / "kio" / "servicemenus",
            Path("/usr/share/kio/servicemenus"),
            Path.home() / ".local" / "share" / "kservices5" / "ServiceMenus",
            Path("/usr/share/kservices5/ServiceMenus"),
        ]
        result: list[Path] = []
        for directory in dirs:
            if not directory.exists():
                continue
            result.extend(sorted(directory.glob(f"{self.APP_NAME}_*.desktop")))
        # Remove duplicate paths while preserving order.
        return list(dict.fromkeys(result))


__all__ = [
    "LinuxContextMenu",
]
