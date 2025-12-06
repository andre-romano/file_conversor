# src\file_conversor\backend\gui\_webview_api.py

import re
import webview

from webview.dom import DOMEventHandler
from pathlib import Path
from typing import Any, Sequence
from natsort import natsorted, ns


# user-provided modules
from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import get_translation

from file_conversor.utils.formatters import format_file_types_webview, format_py_to_js

from file_conversor.system import set_window_icon

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class WebViewState:
    """State shared between the webview and the main application."""

    # Global last open directory
    _lastOpenDir: Path = Path(CONFIG['gui-output-dir']).resolve()
    _icon_configured: bool = False

    @classmethod
    def is_icon_configured(cls) -> bool:
        return cls._icon_configured

    @classmethod
    def set_icon_configured(cls, value: bool) -> None:
        cls._icon_configured = value

    @classmethod
    def get_last_open_dir(cls) -> Path:
        return cls._lastOpenDir

    @classmethod
    def set_last_open_dir(cls, path: str | Path) -> None:
        if isinstance(path, str):
            path = Path(path)
        cls._lastOpenDir = path.resolve()


class WebViewAPI:
    """API exposed to the webview JavaScript context."""

    def _get_window(self, index: int = 0) -> webview.Window:
        """Get the webview window."""
        if len(webview.windows) > index:
            window = webview.windows[index]
            # logger.debug(f"Found webview windows: {','.join([w.title for w in webview.windows])}")
            return window
        raise RuntimeError(_("No webview window found."))

    # ###### #
    # EVENTS #
    # ###### #

    def _on_load(self) -> None:
        logger.debug("WebViewAPI page loaded.")
        window = self._get_window()
        window.dom.document.events.dragover += DOMEventHandler(
            self._on_drag,
            prevent_default=True,
            stop_propagation=True,
            stop_immediate_propagation=True,
            debounce=100,
        )  # pyright: ignore[reportOperatorIssue]
        window.dom.document.events.drop += DOMEventHandler(
            self._on_drop,
            prevent_default=True,
            stop_propagation=True,
            stop_immediate_propagation=True,
        )  # pyright: ignore[reportOperatorIssue]

    def _on_drag(self, event) -> None:
        # empty handler to allow drop event
        pass

    def _on_drop(self, event) -> None:
        logger.debug("Drop event detected")
        data_transfer: dict[str, Any] = event.get('dataTransfer', {})
        files: list[dict[str, Any]] = data_transfer.get('files', [])

        filepaths: list[str] = [
            str(file.get('pywebviewFullPath'))
            for file in files
            if file.get('pywebviewFullPath')
        ]
        filepaths = natsorted(filepaths, alg=ns.PATH)  # natural sort for paths

        if filepaths:
            dir_name = Path(filepaths[0]).parent
            WebViewState.set_last_open_dir(dir_name)

        logger.debug(f"Dropped files: {filepaths}")
        self._get_window().evaluate_js("""
            window.dispatchEvent(new CustomEvent('filesDropped', {
                detail: { files: %s }
            }));
        """ % format_py_to_js(filepaths))

    # ######### #
    # COMMANDS #
    # ######### #

    def reset_config(self):
        """Reset the application configuration to factory defaults."""
        CONFIG.reset_factory_default()
        CONFIG.save()
        logger.info("Configuration reset to factory defaults.")

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

    def set_icon(self) -> None:
        """Set the window icon (Windows only)."""
        if WebViewState.is_icon_configured():
            return
        try:
            set_window_icon(
                self._get_window().title,
                icon_path=Environment.get_app_icon(),
                cx=128, cy=128,
            )
            WebViewState.set_icon_configured(True)
            logger.info("Window icon set.")
        except Exception as e:
            logger.warning(f"Failed to set window icon - {repr(e)}")

    def get_last_open_dir(self) -> str:
        """Get the last opened directory."""
        return str(WebViewState.get_last_open_dir())

    def open_folder_dialog(self, options: dict[str, Any]) -> list[str]:
        """
        Open a folder in the system file explorer.

        :param multiple: Whether to allow multiple folder selection.
        :param path: Optional initial directory path.
        """
        window = self._get_window()
        result = list(window.create_file_dialog(
            dialog_type=webview.FileDialog.FOLDER,
            directory=options.get("path") or self.get_last_open_dir(),
            allow_multiple=bool(options.get("multiple", False)),
        ) or [])
        result = natsorted(result, alg=ns.PATH)  # natural sort for paths
        if result:
            dir_path = Path(result[0])
            WebViewState.set_last_open_dir(dir_path)
        logger.debug(f"Selected save file: {result}")
        return result

    def open_file_dialog(self, options: dict[str, Any]) -> list[str]:
        """
        Open a file dialog and return the selected file paths.

        :param file_types: Optional file type filters (e.g., 'Image Files (*.png;*.jpg)')
        :param multiple: Whether to allow multiple file selection.
        :param path: Optional initial directory path.

        :return: List of selected file paths.
        """
        window = self._get_window()
        result = list(window.create_file_dialog(
            dialog_type=webview.FileDialog.OPEN,
            directory=options.get("path") or self.get_last_open_dir(),
            allow_multiple=bool(options.get("multiple", False)),                  # allow selecting multiple files
            file_types=options.get("file_types") or [
                format_file_types_webview(),  # filter for all files
            ],
        ) or [])
        result = natsorted(result, alg=ns.PATH)  # natural sort for paths
        if result:
            dir_path = Path(result[0]).parent
            WebViewState.set_last_open_dir(dir_path)
        logger.debug(f"Selected files: {result}")
        return result

    def save_file_dialog(self, options: dict[str, Any]) -> list[str]:
        """
        Open a save file dialog and return the selected file path.

        :param file_types: Optional file type filters (e.g., 'Text Files (*.txt)')
        :param filename: Optional default file name to use in the dialog.
        :param path: Optional initial directory path.

        :return: The selected file path.
        """
        window = self._get_window()
        result = list(window.create_file_dialog(
            dialog_type=webview.FileDialog.SAVE,
            directory=options.get("path") or self.get_last_open_dir(),
            save_filename=Path(options.get("filename", "")).name,
            file_types=options.get("file_types", [format_file_types_webview()]),
        ) or [])
        result.sort()

        logger.debug(f"Selected save file: {result}")
        if not result:
            return result

        dir_path = Path(result[0]).parent
        WebViewState.set_last_open_dir(dir_path)

        # adjust file suffix based on selected file type
        file_types: list[str] = options.get("file_types", [])
        if not file_types:
            return result

        match = re.search(r"\(\*(\.[^);]+)", file_types[0])
        if not match:
            return result

        suffix = match.group(1)
        res = f"{Path(result[0]).with_suffix(suffix).resolve()}"
        logger.debug(f"Adjusted saved file: '{res}'")
        return [res]


__all__ = ['WebViewAPI']
