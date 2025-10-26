# src\file_conversor\gui\web_app.py

import webview
import tempfile
import webbrowser
import typer
import time
import threading

from flask import Flask, request
from pathlib import Path
from typing import Any, Callable, Iterable, Self

# user-provided modules
from file_conversor.backend.gui._webview_api import WebViewAPI

from file_conversor.backend.gui.flask_route import FlaskRoute
from file_conversor.backend.gui.flask_status import FlaskStatus, FlaskStatusCompleted, FlaskStatusError, FlaskStatusProcessing, FlaskStatusReady, FlaskStatusUnknown

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import AVAILABLE_LANGUAGES, get_system_locale, get_translation
from file_conversor.utils.formatters import parse_js_to_py

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


# Create a web application
class WebApp:
    LOCALIZATION = {
        'global.quitConfirmation': _('Do you really want to quit?'),
        'global.ok': _('OK'),
        'global.quit': _('Quit'),
        'global.cancel': _('Cancel'),
        'global.saveFile': _('Save file'),
        'cocoa.menu.about': _('About'),
        'cocoa.menu.services': _('Services'),
        'cocoa.menu.view': _('View'),
        'cocoa.menu.edit': _('Edit'),
        'cocoa.menu.hide': _('Hide'),
        'cocoa.menu.hideOthers': _('Hide Others'),
        'cocoa.menu.showAll': _('Show All'),
        'cocoa.menu.quit': _('Quit'),
        'cocoa.menu.fullscreen': _('Enter Fullscreen'),
        'cocoa.menu.cut': _('Cut'),
        'cocoa.menu.copy': _('Copy'),
        'cocoa.menu.paste': _('Paste'),
        'cocoa.menu.selectAll': _('Select All'),
        'windows.fileFilter.allFiles': _('All files'),
        'windows.fileFilter.otherFiles': _('Other file types'),
        'linux.openFile': _('Open file'),
        'linux.openFiles': _('Open files'),
        'linux.openFolder': _('Open folder'),
    }

    _instance: Self | None = None

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def get_args(cls):
        return request.args.to_dict()

    @classmethod
    def get_form_data(cls) -> dict[str, Any]:
        data: dict[str, Any] = request.form.to_dict()
        logger.debug(f"Received data: {data}")
        # Update the configuration with the provided data
        for key, value in data.items():
            data[key] = parse_js_to_py(value)
        return data

    @classmethod
    def get_files_list(cls, key: str) -> tuple[list[Path], Path]:
        """
        Save the uploaded files from the request into temporary dir, for processing.

        :return: tuple[list[Path], Path]: A tuple containing the list of saved file paths and the temporary directory path.
        """
        res: list[Path] = []
        files = request.files.getlist(key)
        temp_dir = Path(tempfile.mkdtemp())
        for file in files:
            if not file.filename:
                continue
            file_path = temp_dir / file.filename
            file.save(file_path)
            res.append(file_path)
        return res, temp_dir

    def __init__(self) -> None:
        super().__init__()
        web_path = Environment.get_web_folder()

        window = webview.create_window(
            title="File Conversor",
            url=f"http://127.0.0.1:{CONFIG['port']}",
            localization=self.LOCALIZATION,
            maximized=True,
            js_api=WebViewAPI(),
        )
        if window is None:
            raise RuntimeError("Failed to create webview window.")
        self.window: webview.Window = window
        self.app = Flask(
            __name__,
            static_folder=web_path / 'static',
            template_folder=web_path / 'templates',
        )
        self._flask_ready = threading.Event()
        self.routes: set[FlaskRoute] = set()
        self.status: dict[str, FlaskStatus] = {}

    def _open_browser(self, url: str) -> None:
        # new=0 → same window (if possible)
        # new=1 → new window
        # new=2 → new tab (recommended)
        webbrowser.open(url, new=2)

    def _run_flask(self):
        logger.info(f"{_('Registering routes ...')}")
        for route in self.routes:
            route.register(self.app)
            # logger.debug(f"Route registered: {route.rule} -> {route.options}")
        logger.info(f"{_('[bold] Starting Flask server ... [/]')}")
        while True:
            try:
                self._flask_ready.set()
                self.app.run(
                    host="127.0.0.1",
                    port=CONFIG["port"],
                    debug=STATE["debug"],
                    threaded=True,  # Allow handling multiple requests
                    use_reloader=False,   # Disable the reloader to avoid issues with threading
                )
            except (typer.Abort, typer.Exit, KeyboardInterrupt, SystemExit) as e:
                logger.info(f"{_('Attempting to shut down Flask server ...')}")
                break
            except Exception as e:
                logger.error(f"Error in Flask server: {repr(e)}")
                time.sleep(0.100)  # Wait before retrying
        logger.info(f"[bold]{_('Flask server stopped.')}[/]")

    def _run_webview(self) -> None:
        logger.info(f"[bold]{_('Starting webview window ...')}[/]")
        webview.start(
            debug=STATE['debug'],
            icon=str(Environment.get_icons_folder() / "icon.ico"),
        )
        logger.info(f"[bold]{_('Webview window closed.')}[/]")

    def expose(self, *func: Callable[..., Any]) -> Self:
        """Expose a new function to the webview JS API."""
        self.window.expose(*func)
        return self

    def evaluate_js(
            self,
            script: str,
            callback: Callable[..., Any] | None = None,
    ) -> Any:
        """Evaluate a JavaScript script in the webview window."""
        return self.window.evaluate_js(script, callback)

    def add_status(self) -> FlaskStatus:
        """Add or update the status of a specific operation by its ID."""
        status_id = len(self.status) + 1
        status = FlaskStatusProcessing(id=status_id)
        self.status[status._id] = status
        return status

    def get_status(self, status_id: str | None) -> FlaskStatus:
        """Get the status of a specific operation by its ID."""
        if status_id is None or status_id.lower() in ('', 'none', 'null', '0'):
            return FlaskStatusReady()
        status = self.status.get(status_id)
        # remove completed or error statuses
        if status is not None and isinstance(status, (FlaskStatusCompleted, FlaskStatusError)):
            del self.status[status_id]
        return status or FlaskStatusUnknown(status_id)

    def add_route(self, routes: FlaskRoute | Iterable[FlaskRoute]) -> Self:
        """Add a new route to the Flask application."""
        for route in (routes if isinstance(routes, Iterable) else [routes]):
            if route in self.routes:
                raise RuntimeError(f"Route already exists: {route}")
            self.routes.add(route)
        return self

    def add_context_processor(self, func: Callable[..., dict[str, Any]]) -> Self:
        """Add a new context processor to the Flask application."""
        self.app.context_processor(func)
        return self

    def run(self) -> None:
        """Run the Flask server and the webview window."""
        flask_thread = threading.Thread(target=self._run_flask, daemon=True)
        flask_thread.start()

        logger.debug(f"{_('Waiting for Flask to be ready ...')}")
        self._flask_ready.wait()

        url = f"http://127.0.0.1:{CONFIG['port']}"
        try:
            logger.info(f"[bold]{_('Access the app at')} {url}[/]")
            logger.info(f"[bold]{_('Press Ctrl+C to exit.')}[/]")
            self._run_webview()
        except (typer.Abort, typer.Exit, KeyboardInterrupt, SystemExit) as e:
            logger.info(f"{_('Shutting down main thread...')}")

        logger.info(f"{_('[bold] Shutting down the application ... [/]')}")
        raise typer.Exit(0)


__all__ = ["WebApp"]
