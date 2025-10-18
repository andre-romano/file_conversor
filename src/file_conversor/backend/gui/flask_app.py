# src\file_conversor\gui\flask_app.py

import os
import signal
import webbrowser
import typer
import time
import threading

from flask import Flask, request
from typing import Any, Callable, Iterable, Self

# user-provided modules
from file_conversor.backend.gui.flask_route import FlaskRoute
from file_conversor.backend.gui.flask_status import FlaskStatus

from file_conversor.config import Configuration, Environment, Log, State
from file_conversor.config.locale import AVAILABLE_LANGUAGES, get_system_locale, get_translation

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
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def get_form_data(cls) -> dict[str, Any]:
        data: dict[str, Any] = request.form.to_dict()
        logger.debug(f"Received data: {data}")
        # Update the configuration with the provided data
        for key, value in data.items():
            # Attempt to convert to appropriate type
            if value.lower() in ('true', 'on'):
                value = True
            elif value.lower() in ('false', 'off'):
                value = False
            elif value.lower() == 'none':
                value = None
            else:
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass  # Keep as string if conversion fails
            data[key] = value
        return data

    def __init__(self) -> None:
        super().__init__()
        web_path = Environment.get_web_folder()

        self.app = Flask(
            __name__,
            static_folder=web_path / 'static',
            template_folder=web_path / 'templates',
        )
        self.routes: set[FlaskRoute] = set()
        self.status: dict[str, FlaskStatus] = {}

    def _run_flask(self):
        logger.info(f"[bold]{_('Registering routes ...')}[/]")
        for route in self.routes:
            route.register(self.app)
            logger.debug(f"Route registered: {route.rule} -> {route.options}")
        logger.info(f"[bold]{_('Starting Flask server ...')}[/]")
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
                logger.info(f"[bold]{_('Attempting to shut down Flask server ...')}[/]")
                break
            except Exception as e:
                logger.error(f"Error in Flask server: {repr(e)}")
                time.sleep(0.100)  # Wait before retrying
        logger.info(f"[bold]{_('Flask server stopped.')}[/]")

    def add_status(self, status_id: str, status: FlaskStatus) -> None:
        """Add or update the status of a specific operation by its ID."""
        self.status[status_id] = status

    def get_status(self, status_id: str) -> FlaskStatus | None:
        """Get the status of a specific operation by its ID."""
        return self.status.get(status_id)

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

    def run(self, open_browser: bool) -> None:
        """Run the Flask server and the webview window."""
        flask_thread = threading.Thread(target=self._run_flask, daemon=True)
        flask_thread.start()

        # new=0 → same window (if possible)
        # new=1 → new window
        # new=2 → new tab (recommended)
        url = f"http://127.0.0.1:{CONFIG['port']}"
        if open_browser:
            webbrowser.open(url, new=2)
        try:
            logger.info(f"[bold]{_('Access the app at')} {url}[/]")
            logger.info(f"[bold]{_('Press Ctrl+C to exit.')}[/]")
            while True:
                time.sleep(0.100)
        except (typer.Abort, typer.Exit, KeyboardInterrupt, SystemExit) as e:
            logger.info(f"[bold]{_('Shutting down main thread...')}[/]")

        logger.info(f"[bold]{_('Shutting down the application ...')}[/]")
        raise typer.Exit(0)

    def stop(self) -> None:
        """Stop the Flask server."""
        logger.info(f"[bold]{_('Flask server is shutting down...')}[/]")
        os.kill(os.getpid(), signal.SIGINT)
        logger.info(f"[bold]{_('Flask server has shut down.')}[/]")


__all__ = ["FlaskApp"]
