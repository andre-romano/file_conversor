# src\file_conversor\gui\flask_app.py

import typer
import time
import webview
import threading

from flask import Flask
from typing import Any, Callable, Self

# user-provided modules
from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import AVAILABLE_LANGUAGES, get_system_locale, get_translation

from file_conversor.gui.flask_route import FlaskRoute

# Get app config
CONFIG = Configuration.get_instance()
STATE = State.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger()


# Create a Flask application
class FlaskApp:
    _instance: Self | None = None

    @classmethod
    def get_instance(cls, *params, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = cls(*params, **kwargs)
        return cls._instance

    def __init__(self, non_interactive: bool = False) -> None:
        super().__init__()
        self.non_interactive = non_interactive

        web_path = Environment.get_web_folder()

        self.flask_thread: threading.Thread | None = None
        self.app = Flask(
            __name__,
            static_folder=web_path / 'static',
            template_folder=web_path / 'templates',
        )
        self._register_routes()

    def _register_routes(self) -> None:
        for fr in FlaskRoute.get_routes():
            self.app.route(fr.route, **fr.options)(fr.handler)
            logger.debug(f"Registered: {fr}")

    def _run_flask(self):
        logger.info(f"[bold]{_('Starting Flask server...')}[/]")
        while True:
            try:
                self.app.run(
                    host=CONFIG["host"],
                    port=CONFIG["port"],
                    debug=STATE["debug"],
                    threaded=True,  # Allow handling multiple requests
                    use_reloader=False,   # Disable the reloader to avoid issues with threading
                )
            except (typer.Abort, typer.Exit, KeyboardInterrupt, SystemExit) as e:
                logger.info(f"[bold]{_('Attempting to shut down Flask server...')}[/]")
                break
            except Exception as e:
                logger.error(f"Error in Flask server: {repr(e)}")
                time.sleep(0.100)  # Wait before retrying
        logger.info(f"[bold]{_('Flask server stopped.')}[/]")

    def _run_webview(self):
        logger.info(f"[bold]{_('Starting the GUI window...')}[/]")
        webview.create_window(
            title="file_conversor",
            url=f"http://127.0.0.1:{CONFIG['port']}",
            width=CONFIG["window_width"],
            height=CONFIG["window_height"],
            x=0, y=0,
            easy_drag=False,
            min_size=(200, 100),
            localization={
                "ok_button": _("Accept"),
                "cancel_button": _("Cancel"),
            },
        )
        webview.start(
            debug=STATE["debug"],
            icon=str(Environment.get_icons_folder() / "icon.ico"),
        )
        logger.info(f"[bold]{_('Shutting down the GUI...')}[/]")

    def _run_non_interactive(self):
        try:
            logger.info(f"[bold]{_('Running in non-interactive mode. Press Ctrl+C to exit.')}[/]")
            logger.info(f"[bold]{_('Access the GUI at:')} http://127.0.0.1:{CONFIG['port']}[/]")
            while True:
                time.sleep(0.100)
        except (typer.Abort, typer.Exit, KeyboardInterrupt, SystemExit) as e:
            logger.info(f"[bold]{_('Shutting down main thread...')}[/]")

    def get(self) -> Flask:
        """"Get the Flask application instance."""
        return self.app

    def run(self) -> None:
        """Run the Flask server and the webview window."""
        flask_thread = threading.Thread(target=self._run_flask, daemon=True)
        flask_thread.start()

        if self.non_interactive:
            self._run_non_interactive()
        else:
            self._run_webview()
        logger.info(f"[bold]{_('Shutting down the application ...')}[/]")
        raise typer.Exit(0)
