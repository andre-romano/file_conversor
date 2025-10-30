# src\file_conversor\backend\gui\_webview_api.py

import webview

from pathlib import Path
from typing import Any, Sequence

# user-provided modules
from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

from file_conversor.utils.formatters import format_file_types_webview

from file_conversor.system import set_window_icon

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WebViewAPI:
    """API exposed to the webview JavaScript context."""

    def _get_window(self, index: int = 0) -> webview.Window:
        """Get the webview window."""
        if len(webview.windows) > index:
            window = webview.windows[index]
            # logger.debug(f"Found webview windows: {','.join([w.title for w in webview.windows])}")
            return window
        raise RuntimeError(_("No webview window found."))

    def get_config(self) -> dict[str, Any]:
        """Get the current application configuration."""
        return CONFIG.to_dict()

    def touch_file(self, options: dict[str, Any]) -> bool:
        """Create an empty file at the specified path."""
        path = options.get("path")
        if not path:
            raise ValueError("Path must be provided.")

        Environment.touch(path)
        logger.debug(f"Touched file at '{path}'.")
        return True

    def move_file(self, options: dict[str, Any]) -> bool:
        """Move a file from src to dst."""
        src = options.get("src")
        dst = options.get("dst")
        overwrite = bool(options.get("overwrite", False))

        if not src or not dst:
            raise ValueError("Source and destination paths must be provided.")

        Environment.move(src, dst, overwrite=overwrite)
        logger.debug(f"Moved file from '{src}' to '{dst}' (overwrite={overwrite}).")
        return True

    def copy_file(self, options: dict[str, Any]) -> bool:
        """Copy a file from src to dst."""
        src = options.get("src")
        dst = options.get("dst")
        overwrite = bool(options.get("overwrite", False))

        if not src or not dst:
            raise ValueError("Source and destination paths must be provided.")

        Environment.copy(src, dst, overwrite=overwrite)
        logger.debug(f"Copied file from '{src}' to '{dst}' (overwrite={overwrite}).")
        return True

    def close(self) -> bool:
        self._get_window().destroy()
        logger.debug("Window closed.")
        return True

    def minimize(self) -> bool:
        self._get_window().minimize()
        logger.debug("Window minimized.")
        return True

    def maximize(self) -> bool:
        self._get_window().maximize()
        logger.debug("Window maximized.")
        return True

    def show(self) -> bool:
        self._get_window().show()
        logger.debug("Window shown.")
        return True

    def hide(self) -> bool:
        self._get_window().hide()
        logger.debug("Window hidden.")
        return True

    def resize(self, options: dict[str, int]) -> bool:
        width = options.get("width")
        height = options.get("height")

        if not width or not height:
            raise ValueError("Width and height must be provided.")

        self._get_window().resize(int(width), int(height))
        logger.debug(f"Window resized to {width}x{height}.")
        return True

    def fullscreen(self) -> bool:
        self._get_window().toggle_fullscreen()
        logger.debug("Window fullscreen toggled.")
        return True

    def move(self, options: dict[str, int]) -> bool:
        x = options.get("x")
        y = options.get("y")

        if not x or not y:
            raise ValueError("X and Y coordinates must be provided.")

        self._get_window().move(int(x), int(y))
        logger.debug(f"Window moved to ({x},{y}).")
        return True

    def set_title(self, options: dict[str, str]) -> bool:
        title = options.get("title")

        if not title:
            raise ValueError("Title must be provided.")

        self._get_window().set_title(title)
        logger.debug(f"Window title set to '{title}'.")
        return True

    def set_icon(self) -> bool:
        """Set the window icon (Windows only)."""
        res = set_window_icon(
            self._get_window().title,
            icon_path=Environment.get_app_icon(),
            cx=128, cy=128,
        )
        if not res:
            logger.warning("Failed to set window icon.")
            return False
        logger.debug("Window icon set.")
        return True

    def open_folder_dialog(self, options: dict[str, Any]) -> list[str]:
        """
        Open a folder in the system file explorer.

        :param multiple: Whether to allow multiple folder selection.
        :param path: Optional initial directory path.
        """
        window = self._get_window()
        result = window.create_file_dialog(
            dialog_type=webview.FileDialog.FOLDER,
            directory=options.get("path") or str(Path().resolve()),
            allow_multiple=bool(options.get("multiple", False)),
        )
        logger.debug(f"Selected save file: {result}")
        return list(result or [])

    def open_file_dialog(self, options: dict[str, Any]) -> list[str]:
        """
        Open a file dialog and return the selected file paths.

        :param file_types: Optional file type filters (e.g., 'Image Files (*.png;*.jpg)')
        :param multiple: Whether to allow multiple file selection.
        :param path: Optional initial directory path.

        :return: List of selected file paths.
        """
        window = self._get_window()
        result = window.create_file_dialog(
            dialog_type=webview.FileDialog.OPEN,
            directory=options.get("path") or str(Path().resolve()),
            allow_multiple=bool(options.get("multiple", False)),                  # allow selecting multiple files
            file_types=options.get("file_types") or [
                format_file_types_webview(),  # filter for all files
            ],
        )
        logger.debug(f"Selected files: {result}")
        return list(result or [])

    def save_file_dialog(self, options: dict[str, Any]) -> list[str]:
        """
        Open a save file dialog and return the selected file path.

        :param file_types: Optional file type filters (e.g., 'Text Files (*.txt)')
        :param filename: Optional default file name to use in the dialog.
        :param path: Optional initial directory path.

        :return: The selected file path.
        """
        window = self._get_window()
        result = window.create_file_dialog(
            dialog_type=webview.FileDialog.SAVE,
            directory=options.get("path") or str(Path().resolve()),
            save_filename=options.get("filename", ""),
            file_types=options.get("file_types", [format_file_types_webview()]),
        )
        logger.debug(f"Selected save file: {result}")
        if not result:
            return []

        # adjust file suffix based on selected file type
        file_types: list[str] = options.get("file_types", [])
        if not file_types:
            return list(result)

        suffix = file_types[0].split("*")[-1]
        res = f"{Path(result[0]).with_suffix(suffix).resolve()}"
        logger.debug(f"Adjusted saved file: {res}")
        return [res]


__all__ = ['WebViewAPI']
